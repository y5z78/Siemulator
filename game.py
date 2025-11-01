# I acknowledge the use of Gemini(https://gemini.google.com/app) to generate the initial lines 
# of code in this game.py file and the README.md after which I modified some sections to my 
# discretion.

import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

# --- GAME CONFIGURATION ---

# Scoring constants
POINTS_CORRECT_ALERT = 10
POINTS_CORRECT_SKIP = 5
PENALTY_FALSE_POSITIVE = -5
PENALTY_MISSED_ANOMALY = -10
PENALTY_TOO_SLOW = -1

# Time limit in milliseconds
TIME_LIMIT_MS = 10000 

# Log entries format: (Log string, Is Anomaly)
LOG_ENTRIES = [
    ("[08:00:01] IP: 192.168.1.10, User: Guest, Event: File Read (index.html)", False),
    ("[08:00:15] IP: 203.0.113.5, User: Admin, Event: Successful Login", True),  # Anomaly: External IP or privileged access
    ("[08:01:03] IP: 192.168.1.5, User: IT-Helpdesk, Event: Network Scan", False),
    ("[08:01:30] IP: 10.1.1.2, User: Finance, Event: File Write (data.csv)", True), # Anomaly: Potential data exfiltration
    ("[08:02:10] IP: 10.1.1.8, User: Guest, Event: 5x Failed Login Attempt", True), # Anomaly: Brute force attempt
    ("[08:03:05] IP: 192.168.1.20, User: HR, Event: Successful Login", False),
    ("[08:04:20] IP: 192.168.1.15, User: Marketing, Event: File Read (promo.pdf)", False),
    ("[08:05:00] IP: 10.1.1.25, User: Admin, Event: File Delete (audit_log.bak)", True), # Critical Anomaly: Deleting audit logs
    ("[08:06:10] IP: 10.1.1.1, User: CEO, Event: Successful Login", False),
    ("[08:07:00] IP: 203.0.113.10, User: IT-Helpdesk, Event: File Read (temp.log)", True), # Anomaly: External IP for IT-Helpdesk
]

class LogAnalystGame:
    def __init__(self, master):
        self.master = master
        master.title("Log Analyst: Anomaly Hunter")
        
        # Game state variables
        self.score = 0
        self.log_index = 0
        self.log_sequence = []
        self.start_time = 0
        self.timer_id = None
        self.is_game_running = False

        # --- STYLE CONFIGURATION (Dark Theme) ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Customize the frame/window background
        master.configure(bg="#2c3e50") # Dark Blue/Gray
        
        # Configure custom styles for labels and buttons
        style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=('Monospace', 12))
        style.configure("Title.TLabel", font=('Monospace', 16, 'bold'), foreground="#3498db")
        style.configure("Score.TLabel", font=('Monospace', 14, 'bold'), foreground="#f1c40f")
        style.configure("TButton", font=('Monospace', 12, 'bold'), borderwidth=1, relief="raised")
        style.map("Alert.TButton", foreground=[('active', 'white')], background=[('active', '#e74c3c')]) # Red on active
        style.map("Skip.TButton", foreground=[('active', 'white')], background=[('active', '#2ecc71')]) # Green on active
        style.configure("Alert.TButton", background="#c0392b", foreground="white") # Dark Red
        style.configure("Skip.TButton", background="#27ae60", foreground="white") # Dark Green
        
        # --- LAYOUT FRAMES ---
        
        # Main Info Frame (Score and Timer)
        self.info_frame = ttk.Frame(master, padding="10 10 10 10", style="TFrame")
        self.info_frame.pack(fill='x')
        self.info_frame.configure(style='TFrame', relief=tk.FLAT, borderwidth=0)
        
        # Log Display Frame
        self.log_frame = ttk.Frame(master, padding="10 10 10 10")
        self.log_frame.pack(fill='both', expand=True)

        # Feedback/Action Frame
        self.action_frame = ttk.Frame(master, padding="10 10 10 10")
        self.action_frame.pack(fill='x')

        # --- WIDGETS ---
        
        # Title
        ttk.Label(self.info_frame, text="LOG ANALYST: ANOMALY STREAM", style="Title.TLabel").pack(pady=5)
        
        # Score and Timer Display
        self.score_label = ttk.Label(self.info_frame, text="Score: 0", style="Score.TLabel")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.timer_label = ttk.Label(self.info_frame, text="Time: 10.0s", style="Score.TLabel")
        self.timer_label.pack(side=tk.RIGHT, padx=10)
        
        # Progress Bar for Time Limit
        self.progress_bar = ttk.Progressbar(self.info_frame, orient='horizontal', length=300, mode='determinate', maximum=TIME_LIMIT_MS)
        self.progress_bar.pack(expand=True, padx=20)
        
        # Log Console (Text Widget)
        self.log_console = tk.Text(self.log_frame, height=15, bg="#34495e", fg="#ecf0f1", font=('Monospace', 11), wrap='word', borderwidth=0, relief="flat", padx=5, pady=5)
        self.log_console.pack(fill='both', expand=True)
        
        # Configure Text Tags for Syntax Highlighting
        self.log_console.tag_config('anomaly', foreground='#e74c3c') # Red for Anomaly Keywords
        self.log_console.tag_config('user', foreground='#f1c40f') # Yellow for User names
        self.log_console.tag_config('success', foreground='#2ecc71') # Green for Success
        self.log_console.tag_config('feedback_correct', background='#27ae60', foreground='white')
        self.log_console.tag_config('feedback_incorrect', background='#c0392b', foreground='white')
        self.log_console.tag_config('normal', foreground='#ecf0f1')

        # Feedback/Status Label
        self.status_label = ttk.Label(self.action_frame, text="Click 'Start Monitoring' to begin.", font=('Monospace', 12, 'italic'))
        self.status_label.pack(pady=10)

        # Action Buttons
        self.alert_button = ttk.Button(self.action_frame, text="🚨 ALERT (A)", style="Alert.TButton", command=lambda: self.check_response(True), state=tk.DISABLED)
        self.alert_button.pack(side=tk.LEFT, expand=True, padx=5, pady=10)
        
        self.skip_button = ttk.Button(self.action_frame, text="✅ SKIP (S)", style="Skip.TButton", command=lambda: self.check_response(False), state=tk.DISABLED)
        self.skip_button.pack(side=tk.RIGHT, expand=True, padx=5, pady=10)

        # Start Button (Initial state)
        self.start_button = ttk.Button(self.master, text="Start Monitoring", command=self.start_game, style="TButton")
        self.start_button.pack(pady=10)


    # --- GAME LOGIC METHODS ---

    def start_game(self):
        """Initializes game state and starts the first log stream."""
        if self.is_game_running:
            return
            
        self.score = 0
        self.log_index = 0
        self.log_sequence = list(LOG_ENTRIES)
        random.shuffle(self.log_sequence)
        
        self.is_game_running = True
        self.start_button.pack_forget() # Hide start button
        self.alert_button.config(state=tk.NORMAL)
        self.skip_button.config(state=tk.NORMAL)
        self.update_score()
        self.status_label.config(text="Log stream active. Analyze incoming traffic.")
        self.log_console.delete(1.0, tk.END) # Clear console
        self.show_next_log()

    def end_game(self):
        """Cleans up game state and displays final score."""
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        
        self.is_game_running = False
        self.alert_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        self.timer_label.config(text="Time: 0.0s")

        messagebox.showinfo("End of Shift", f"Shift Complete! Your FINAL SCORE is: {self.score}")
        self.start_button.pack(pady=10) # Show start button again

    def highlight_log(self, log_entry):
        """Applies coloring to log keywords for visual aid."""
        
        # Keywords that often suggest high privilege or malicious intent
        anomaly_keywords = ["Admin", "Delete", "Write", "Failed", "External IP", "5x"]
        
        # User/Role keywords
        user_keywords = ["Admin", "Guest", "Finance", "HR", "IT-Helpdesk", "CEO", "Marketing"]

        # Insert the log and apply default color
        self.log_console.insert(tk.END, log_entry + "\n", 'normal')
        
        # Get start/end indices for the newly inserted line
        start_index = f"{self.log_console.index(tk.END)} - 1 line linestart"
        end_index = f"{self.log_console.index(tk.END)} - 1 line lineend"

        # Apply tags to keywords
        for keyword in anomaly_keywords:
            if keyword in log_entry:
                # Search for the keyword within the specific line range
                idx = self.log_console.search(keyword, start_index, stopindex=end_index, regexp=False)
                while idx:
                    end_idx = f"{idx}+{len(keyword)}c"
                    self.log_console.tag_add('anomaly', idx, end_idx)
                    idx = self.log_console.search(keyword, end_idx, stopindex=end_index, regexp=False)

        for keyword in user_keywords:
            if keyword in log_entry:
                idx = self.log_console.search(keyword, start_index, stopindex=end_index, regexp=False)
                while idx:
                    end_idx = f"{idx}+{len(keyword)}c"
                    self.log_console.tag_add('user', idx, end_idx)
                    idx = self.log_console.search(keyword, end_idx, stopindex=end_index, regexp=False)

        # Scroll to the bottom to show the newest log
        self.log_console.see(tk.END)


    def show_next_log(self):
        """Prepares and displays the next log entry, starting the timer."""
        if self.log_index >= len(self.log_sequence):
            return self.end_game()

        # Cancel any running timer from the previous log
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        
        log_entry, _ = self.log_sequence[self.log_index]
        self.highlight_log(f"INCOMING ({self.log_index + 1}/{len(self.log_sequence)}): {log_entry}")
        
        self.start_time = time.time()
        self.update_timer()


    def update_timer(self):
        """Updates the visual timer and progress bar every 50ms."""
        if not self.is_game_running:
            return

        time_elapsed = (time.time() - self.start_time) * 1000 # convert to ms
        time_left_ms = TIME_LIMIT_MS - time_elapsed
        
        self.progress_bar['value'] = TIME_LIMIT_MS - time_left_ms
        
        if time_left_ms <= 0:
            # Time's up! Process as a missed log.
            self.status_label.config(text="🔴 TIME OUT! Auto-Skipped Log.", foreground='#e74c3c')
            self.check_response(False, time_out=True)
            return

        # Update the timer label with remaining seconds
        self.timer_label.config(text=f"Time: {time_left_ms / 1000:.1f}s")

        # Schedule the next timer update
        self.timer_id = self.master.after(50, self.update_timer)


    def update_score(self):
        """Updates the score label."""
        self.score_label.config(text=f"Score: {self.score}")

    def check_response(self, player_alerted, time_out=False):
        """Handles the player's response (ALERT or SKIP)."""
        if not self.is_game_running:
            return

        # Stop the current timer loop
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        _, is_anomaly = self.log_sequence[self.log_index]
        time_taken = time.time() - self.start_time
        
        feedback_text = ""
        
        if time_out:
            # Penalize for being too slow
            self.score += PENALTY_TOO_SLOW
            feedback_text = f"❌ Too Slow! ({time_taken:.1f}s) - {PENALTY_TOO_SLOW} pt"
            
            # If it was an anomaly and they timed out (treated as skip)
            if is_anomaly:
                self.score += PENALTY_MISSED_ANOMALY
                feedback_text += f" + MISSED ANOMALY ({PENALTY_MISSED_ANOMALY} pt)"
            else:
                 feedback_text += " + Normal Traffic Skipped."

        elif player_alerted and is_anomaly:
            # Correctly identified anomaly
            self.score += POINTS_CORRECT_ALERT
            feedback_text = f"✅ CRITICAL ALERT: Correctly identified anomaly! (+{POINTS_CORRECT_ALERT} pts)"
            self.status_label.config(foreground='#2ecc71')

        elif not player_alerted and not is_anomaly:
            # Correctly skipped normal traffic
            self.score += POINTS_CORRECT_SKIP
            feedback_text = f"➡️ NORMAL TRAFFIC: Good job skipping. (+{POINTS_CORRECT_SKIP} pts)"
            self.status_label.config(foreground='#2ecc71')

        elif player_alerted and not is_anomaly:
            # False Positive
            self.score += PENALTY_FALSE_POSITIVE
            feedback_text = f"⚠️ FALSE POSITIVE: Log was normal. ({PENALTY_FALSE_POSITIVE} pts)"
            self.status_label.config(foreground='#f39c12')

        elif not player_alerted and is_anomaly:
            # Missed Anomaly
            self.score += PENALTY_MISSED_ANOMALY
            feedback_text = f"❌ MISSED ANOMALY: Security Breach! ({PENALTY_MISSED_ANOMALY} pts)"
            self.status_label.config(foreground='#e74c3c')

        
        # Display feedback and prepare for next log
        self.status_label.config(text=feedback_text)
        self.update_score()
        
        self.log_index += 1
        
        # Wait a moment for the user to read feedback before showing the next log
        self.alert_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        self.master.after(1500, self._proceed_to_next_log) # Wait 1.5 seconds

    def _proceed_to_next_log(self):
        """Re-enables buttons and calls show_next_log."""
        if self.is_game_running:
            self.alert_button.config(state=tk.NORMAL)
            self.skip_button.config(state=tk.NORMAL)
            self.status_label.config(foreground='#ecf0f1', text="Log stream active. Analyze incoming traffic.")
            self.show_next_log()


# --- START APPLICATION ---
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Apply a minimal style configuration to the root
    root.tk_setPalette(background='#2c3e50', foreground='#ecf0f1') 
    
    # Initialize the game
    game_app = LogAnalystGame(root)
    
    # Run the main event loop
    root.mainloop()

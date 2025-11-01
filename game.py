import time
import random

# A list of simple log entries (True = Anomaly, False = Normal)
LOG_ENTRIES = [
    ("[08:00:01] User: Guest, Event: File Read (index.html)", False),
    ("[08:00:15] User: User: Admin, Event: Successful Login", True),  # Anomaly: High-privilege action
    ("[08:01:03] User: IT-Helpdesk, Event: Network Scan", False),
    ("[08:01:30] User: Finance, Event: File Write (data.csv)", True), # Anomaly: Potential data exfiltration
    ("[08:02:10] User: Guest, Event: 5x Failed Login Attempt", True), # Anomaly: Brute force attempt
    ("[08:03:05] User: HR, Event: Successful Login", False),
    ("[08:04:20] User: Marketing, Event: File Read (promo.pdf)", False),
    ("[08:05:00] User: Admin, Event: File Delete (audit_log.bak)", True), # New Anomaly: Deleting audit files
]

# --- NEW FEATURE: START PROMPT ---

def display_instructions():
    """Displays game instructions and waits for the 'START' command."""
    print("\n" + "="*50)
    print("        WELCOME TO THE LOG ANALYST SIMULATOR")
    print("="*50)
    print("Your mission is to monitor the log stream for security anomalies.")
    print("\nRULES:")
    print("  1. When a log appears, you have **10 SECONDS** to respond.")
    print("  2. Type 'ALERT' (A) if the log indicates suspicious activity.")
    print("  3. Type 'SKIP' (S) if the log represents normal, expected traffic.")
    print("\nSCORING:")
    print("  ✅ Correct Alert: +10 pts")
    print("  ➡️ Correct Skip: +5 pt")
    print("  ⚠️ False Positive (Alerting on normal log): -5 pts")
    print("  ❌ Missed Anomaly (Skipping a breach): -10 pts")
    print("  ⏰ Too Slow (> 10s): -1 pt (and treated as SKIP)")
    print("\nCRITICAL ANOMALIES to Watch For:")
    print("  - Admin/Privileged User Activity (outside routine).")
    print("  - Multiple Failed Login Attempts.")
    print("  - Access/Write operations on critical data files.")
    print("-" * 50)
    
    # Wait for the user to start
    while True:
        user_input = input("TYPE 'START' TO BEGIN LOG STREAM MONITORING: ").strip().upper()
        if user_input == "START":
            print("\nLOG STREAM ACTIVATED... MONITORING NOW.")
            time.sleep(1)
            break
        else:
            print("Invalid command. Please type 'START' to begin.")


def run_game():
    """Main game logic, executed after instructions are passed."""
    score = 0
    
    # 1. Display instructions and wait for START
    display_instructions()
    
    # 2. Start the game flow
    random.shuffle(LOG_ENTRIES)
    
    for log, is_anomaly in LOG_ENTRIES:
        # Clear the screen (simulated with newlines for terminal)
        print("\n" * 2) 
        print("-" * 50)
        print(f"[{time.strftime('%H:%M:%S', time.localtime())}] Incoming Log: {log}")
        
        # Make it interactive: wait for user input
        start_time = time.time()
        
        # Use a simple input for flexibility
        player_action_raw = input("Action (ALERT/SKIP): ").strip().upper()
        
        # Normalize input for checking (A or S are shortcuts)
        if player_action_raw == "A":
            player_action = "ALERT"
        elif player_action_raw == "S":
            player_action = "SKIP"
        else:
            player_action = player_action_raw

        time_taken = time.time() - start_time
        
        # --- SCORING AND FEEDBACK ---
        
        # Check for slow response first
        if time_taken > 10:
            print(f"**⏰ Too Slow! Response time: {time_taken:.2f}s (Penalty: -1)**")
            score -= 1
            # Treat all slow responses as a SKIP (fail-safe)
            player_action = "SKIP"

        # Check the result
        if is_anomaly and player_action == "ALERT":
            print(f"✅ CRITICAL ALERT: Correctly identified anomaly! (+10 points)")
            score += 10
        elif is_anomaly and player_action == "SKIP":
            print(f"❌ MISSED ANOMALY! This was a security breach! (-10 points)")
            score -= 10
        elif not is_anomaly and player_action == "ALERT":
            print(f"⚠️ FALSE POSITIVE: This log was normal. (-5 points)")
            score -= 5
        elif not is_anomaly and player_action == "SKIP":
            # Only give positive score if not also penalized for time
            if time_taken <= 10:
                print(f"➡️ NORMAL TRAFFIC: Good job skipping. (+5 point)")
                score += 5
            else:
                 print(f"➡️ NORMAL TRAFFIC: Skip confirmed.")


        # Display current score
        print(f"Current Score: {score}")

    print("\n" + "="*50)
    print("             --- END OF SHIFT ---")
    print(f"             FINAL SCORE: {score}")
    print("="*50)

run_game()

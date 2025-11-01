import time
import random

# A list of simple log entries (True = Anomaly, False = Normal)
LOG_ENTRIES = [
    ("[08:00:01] User: Guest, Event: File Read (index.html)", False),
    ("[08:00:15] User: Admin, Event: Successful Login", True), # Anomaly: Admin shouldn't log in frequently
    ("[08:01:03] User: IT-Helpdesk, Event: Network Scan", False),
    ("[08:01:30] User: Finance, Event: File Write (data.csv)", True), # Anomaly: Write to critical file
    ("[08:02:10] User: Guest, Event: 5x Failed Login Attempt", True), # Anomaly: Brute force attempt
    ("[08:03:05] User: HR, Event: Successful Login", False),
]

def run_game():
    score = 0
    print("Welcome, Log Analyst! Type 'ALERT' for an anomaly, or 'SKIP' for normal.")
    print("----------------------------------------------------------------------")
    
    # Shuffle logs for replayability
    random.shuffle(LOG_ENTRIES)
    
    for log, is_anomaly in LOG_ENTRIES:
        print(f"\nIncoming Log: {log}")
        
        # Make it interactive: wait for user input
        start_time = time.time()
        player_action = input("Action (ALERT/SKIP): ").upper()
        time_taken = time.time() - start_time
        
        # Deduct score for slow response
        if time_taken > 3:
            print(f"**Too Slow! (-1 point for slow response)**")
            score -= 1

        # Check the result
        if is_anomaly and player_action == "ALERT":
            print(f"✅ CRITICAL ALERT: Correctly identified anomaly! (+10 points)")
            score += 10
        elif is_anomaly and player_action == "SKIP":
            print(f"❌ MISSED ANOMALY! This was a security breach! (-15 points)")
            score -= 15
        elif not is_anomaly and player_action == "ALERT":
            print(f"⚠️ FALSE POSITIVE: This log was normal. (-5 points)")
            score -= 5
        elif not is_anomaly and player_action == "SKIP":
            print(f"➡️ NORMAL TRAFFIC: Good job skipping. (+1 point)")
            score += 1
        
        # Display current score
        print(f"Current Score: {score}")

    print("\n--- GAME OVER ---")
    print(f"FINAL SCORE: {score}")

# Uncomment to run the game in your Python environment:
run_game()
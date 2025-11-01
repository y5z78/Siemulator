<!--I acknowledge the use of Gemini(https://gemini.google.com/app) to draft this README.md file after which I modified it to my discretion.-->

# Log Analyst: Siemulator (GUI)

**Repository Description:** A simple, interactive log analysis game focused on cybersecurity log review and **anomaly detection**. The program is built with **Python** and the **Tkinter** library.

---

## Project Overview

The **Log Analyst: Siemulator** game simulates a Security Operations Center (SOC) environment, challenging the user to quickly identify suspicious activity within a real-time stream of security logs. The goal is to enforce the principle of **speed and vigilance** in incident response.

This project demonstrates proficiency in Python programming, GUI development (Tkinter), and core cybersecurity analysis concepts. It also demonstrates proficiency in version control(git and github).

---

## Key Features

| Feature | Description |
| :--- | :--- |
| **Interactive GUI** | A clean, dark-themed interface built with Tkinter, providing a professional SOC dashboard feel. |
| **Time-Sensitive Response** | A strict **10-second** time limit per log entry, enforced by a visual progress bar and countdown timer. |
| **Syntax Highlighting** | Key terms like **Admin**, **Failed**, **Write**, and **Delete** are automatically highlighted in the log console for quick analysis. |
| **Scoring System** | Penalizes **False Positives** and heavily penalizes **Missed Anomalies** to simulate real-world risk. |
| **Clear Feedback** | Immediate, color-coded status messages (Green for Correct, Red for Incorrect) guide the player. |

---

## Scoring Breakdown

The game uses the following penalty and point system:

| Action | Points |
| :--- | :--- |
| **✅ Correct ALERT** (Anomaly Identified) | **+10** |
| **➡️ Correct SKIP** (Normal Traffic Skipped) | **+5** |
| **⚠️ False Positive** (Alerting on Normal) | **-5** |
| **❌ Missed Anomaly** (Skipping a Breach) | **-10** |
| **⏰ Too Slow** (>10 seconds) | **-1** (And treated as a SKIP) |

---

## Getting Started

### Prerequisites

You need **Python 3.x** installed. The project relies only on standard Python libraries (`tkinter`, `time`, `random`), so no external packages need to be installed.

### Execution

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_REPO_URL_HERE]
    ```
2.  **Run the Game:**
    ```bash
    python game.py
    ```
    *Note: Ensure the file is saved as `game.py`.*

---

## Game Instructions

1.  **Launch:** Run the script and click the **"Start Monitoring"** button.
2.  **Analyze:** A log entry will appear in the dark console, and the 10-second timer will start.
3.  **Act:**
    * Click **ALERT** for suspicious, malicious, or policy-violating activity.
    * Click **SKIP** for expected, routine, or benign activity.
4.  **Shift End:** The game concludes after all logs have been processed, and your final score will be displayed.
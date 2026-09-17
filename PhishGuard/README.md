# PhishGuard

## Overview

PhishGuard is a cybersecurity awareness game developed using Python and Pygame. The game simulates an email inbox where players must identify phishing and legitimate emails. Through interactive decision-making and immediate feedback, players learn common phishing indicators and safe email practices.

## Features

### Main Menu

* Start Game button
* Instructions button
* Simple navigation system

### Instructions Screen

* Displays gameplay instructions
* Explains game objectives and rules
* ESC key returns to the main menu

### Inbox System

* Loads email data from `emails.json`
* Displays emails in an inbox-style interface
* Shows sender and subject information
* Tracks reviewed and unread emails
* Displays remaining emails to review

### Email Viewer

* Displays:

  * Sender
  * Subject
  * Message content
  * Embedded link
* Links are highlighted in red as a potential phishing indicator
* Includes a Back button to return to the inbox
* Provides classification options for each email

### Email Classification

Players must decide whether an email is:

* **Phishing**
* **Legitimate**

Available actions:

* **Report Phishing**
* **Mark Safe**

### Feedback System

After each decision:

#### Correct Answer

* Displays "CORRECT"
* Awards 10 points
* Shows educational feedback

#### Incorrect Answer

* Displays "WRONG"
* Deducts 5 points
* Removes one life
* Triggers a red glitch visual effect

### Educational Learning

Each email includes:

* A cybersecurity tip
* Detailed reasons explaining why the email is phishing or legitimate
* Immediate feedback after every decision

### Score and Lives System

* Start with 3 lives
* Correct answer: +10 points
* Incorrect answer: -5 points
* Incorrect answers also remove a life
* Game ends when all lives are lost

### Results Screen

Displays:

* Final score
* Number of correct answers
* Number of incorrect answers
* Accuracy percentage
* Personalised mistake summary

### Game Over Screen

Displayed when all lives are lost.

Includes:

* Final score
* Failure message
* Play Again option
* Return to Main Menu option

---

## Technologies Used

* Python 3
* Pygame
* JSON

---

## Project Structure

```text
PhishGuard/
│
├── Programming-project.py
├── emails.json
└── README.md
```

---

## How to Run

### Prerequisites

Install Python 3 and Pygame.

```bash
pip install pygame
```

### Running the Game

Ensure `emails.json` is in the same directory as the game file.

Run:

```bash
python Programming-project.py
```

---

## Controls

| Action                   | Control          |
| ------------------------ | ---------------- |
| Start Game               | Left Mouse Click |
| Open Email               | Left Mouse Click |
| Report Phishing          | Left Mouse Click |
| Mark Safe                | Left Mouse Click |
| Return to Inbox          | Back Button      |
| Continue Feedback        | Left Mouse Click |
| Return from Instructions | ESC Key          |

---

## Error Handling

Version 5 includes safer file handling for email data.

The game:

* Loads `emails.json` using a path relative to the program file
* Detects missing email files
* Detects malformed JSON data
* Displays an error message and exits safely if loading fails

---

## Development Progress

### Version 1

Implemented the project foundation:

* Main menu
* Instructions screen
* Basic screen navigation

### Version 2

Added inbox functionality:

* Inbox interface
* Email loading from JSON
* Email viewing screen
* Navigation system

### Version 3

Added core gameplay:

* Email classification system
* Report Phishing action
* Mark Safe action
* Decision validation
* Feedback screen

### Version 4

Added progression and educational features:

* Score tracking
* Lives system
* Results screen
* Game Over screen
* Accuracy calculations
* Mistake analysis
* Educational tips
* Detailed phishing explanations
* Red glitch effect

### Version 5

Focused on usability, reliability, and maintainability:

* Fixed Back button navigation
* Improved button placement and screen layout
* Replaced multiple global variables with a central `game_state` dictionary
* Added safer relative-path loading for `emails.json`
* Added exception handling for missing or invalid email data
* Added function docstrings and code documentation
* Improved overall code organisation and readability

---

## Learning Outcomes

PhishGuard helps users learn to:

* Identify phishing indicators
* Recognise suspicious links and domains
* Evaluate email legitimacy
* Improve cybersecurity awareness
* Practice safe email handling techniques

---

## Author

Developed as part of a cybersecurity awareness educational project using Python and Pygame.

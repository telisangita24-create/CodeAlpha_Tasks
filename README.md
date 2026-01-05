# Code Alpha Tasks

A small repository that collects three beginner-friendly Python projects.  
Each project is self-contained and demonstrates core programming concepts with simple, practical tasks you can run locally.

## Projects included

- **TASK 2** — Stock Portfolio Tracker
- **TASK 3** — Task Automation with Python Scripts
- **TASK 4** — Basic Chatbot

---

## Quick setup (create repo & push)

### 1. Create a new GitHub repository named `Code-Alpha-Tasks`.

 2. Locally:
```bash
mkdir Code-Alpha-Tasks
cd Code-Alpha-Tasks
git init
Add files and folders for each project (examples below).
Commit and push:
git add .
git commit -m "Initial commit: add 4 projects (Task 1, 2, 3, 4)"
git branch -M main
git remote add origin https://github.com/<your-username>/Code-Alpha-Tasks.git
git push -u origin main


---


```bash
Recommended repository structure
Organize each task in its own folder:

Code-Alpha-Tasks/
├── TASK-1-Hangman_Game/
│   ├── Hangman_Game.py
│   ├── README.md
│
├── TASK-2-Stock-Portfolio-Tracker/
│   ├── Stock-Portfolio-Tracker.py
│   ├── README.md
│   └── requirements.txt
│
├── TASK-3-Task-Automation/
│   ├── Task-Automation.py
│   └── README.md
│
└── TASK-4-Chatbot/
    ├── Chatbot.py
    └── README.md




✅ README.md for TASK-1 (Hangman Game)

📄 TASK-1-Hangman-Game/README.md

# TASK 1: Hangman Game

## Description
This is a simple **text-based Hangman Game** built using Python.  
The player guesses a hidden word one letter at a time. Incorrect guesses are limited.

## Features
- Predefined list of words
- Maximum 6 incorrect guesses
- Console-based interaction
- Beginner-friendly logic

## Technologies Used
- Python

## How to Run
```bash
python Hangman_Game.py

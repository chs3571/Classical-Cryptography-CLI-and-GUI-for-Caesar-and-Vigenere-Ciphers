# Classical-Cryptography-CLI-and-GUI-for-Caesar-and-Vigenere-Ciphers
**Abstract**
    This project presents the design, development, and architectural analysis of 'Classical Cipher Studio', a dual-interface cryptographic system developed in Python. Classical cryptography is often perceived as an abstract, mathematical discipline, creating a barrier for novices and students. This project addresses this challenge by pairing a Command Line Interface (CLI) for automated operations with an intuitive Graphical User Interface (GUI) built with Tkinter, specifically designed for visual learning. Beyond standard symmetric encryption and decryption of Caesar and Vigenere ciphers, the tool implements advanced automated cryptanalysis capabilities. Specifically, it incorporates a 'Visual Crack' module that visually demonstrates brute force searching, letter frequency analysis, the Index of Coincidence (IoC) to detect key lengths, and Chi-squared variance calculations to recover keywords without prior knowledge. 
This document covers the end-to-end process: Linux operating environment setup, detailed code line by-line breakdown for beginners, methodology, experimental findings, and challenges encountered. 

**Introduction** 
**Background** 
      Cryptography has safeguarded human communications across history, evolving from ancient mechanical ciphers to modern mathematical encryption suites. Classical ciphers form the theoretical foundation of all modern confidentiality protocols: 
**Caesar Cipher:** A monoalphabetic substitution cipher where each character in the plaintext is shifted by a fixed numeric offset (key k) down the alphabet modulo 26. While historically significant, it has an extremely small keyspace of only 25 usable transformations, making it trivially susceptible to exhaustive brute-force search. 
**Vigenere Cipher:** Introduced to counteract the vulnerabilities of monoalphabetic ciphers, it utilizes a keyword to implement polyalphabetic substitution. Each letter of the key determines an independent Caesar shift for the corresponding plaintext letter. For centuries considered 'le chiffre indechiffrable' (the unbreakable cipher), it was eventually proven vulnerable through periodic statistical analysis pioneered by Charles Babbage and Friedrich Kasiski.

Problem Statement 
    While contemporary cybersecurity curricula introduce classical ciphers early on, beginners  frequently struggle to understand how statistical cryptanalysis breaks encryption in practice. Standard terminal tools output final plaintexts instantaneously, concealing the algorithmic mechanics of how an attacker reasons through statistical variance, calculates the Index of Coincidence, or evaluates letter frequency distributions. There is an educational requirement for a unified application that pairs functional CLI commands with an interactive GUI featuring a transparent 'hacker console' that displays real-time cryptanalysis steps.

**Objectives**
•	Develop an extensible Python toolkit comprising a CLI (‘classical_cipher.py’) and a GUI (‘cipher_gui.py’).
•	Maintain strict Separation of Concerns (SoC) by decoupling cryptographic math and cryptanalysis algorithms from GUI display logic.
•	Implement robust input sanitization and exception management across both CLI and Tkinter user interfaces.
•	Design a dedicated visual 'Cracking Visualisation' console that logs real-time calculations: IoC bar charts, Chi-squared error scores, candidate shifts, and final plaintext recovery.

**Lab/Environment Setup**
    Setting up the development lab requires configuring dependencies, folder structures, and virtual execution spaces. Below is the exact chronological sequence of terminal commands used, accompanied by beginner explanations.

**Step 1:** System Repository Update and Upgrade
Command: _sudo apt update && sudo apt upgrade -y_
Explanation: Refreshes the local package index against Kali mirrors and upgrades all packages to prevent compatibility conflicts.
    

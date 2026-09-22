# Classical-Cryptography-CLI-and-GUI-for-Caesar-and-Vigenere-Ciphers
**Abstract**
    This project presents the design, development, and architectural analysis of 'Classical Cipher Studio', a dual-interface cryptographic system developed in Python. Classical cryptography is often perceived as an abstract, mathematical discipline, creating a barrier for novices and students. This project addresses this challenge by pairing a Command Line Interface (CLI) for automated operations with an intuitive Graphical User Interface (GUI) built with Tkinter, specifically designed for visual learning. Beyond standard symmetric encryption and decryption of Caesar and Vigenere ciphers, the tool implements advanced automated cryptanalysis capabilities. Specifically, it incorporates a 'Visual Crack' module that visually demonstrates brute force searching, letter frequency analysis, the Index of Coincidence (IoC) to detect key lengths, and Chi-squared variance calculations to recover keywords without prior knowledge. This document covers the end-to-end process: Linux operating environment setup, detailed code line by-line breakdown for beginners, methodology, experimental findings, and challenges encountered. 

**Introduction** 

**Background** 
      Cryptography has safeguarded human communications across history, evolving from ancient mechanical ciphers to modern mathematical encryption suites. Classical ciphers form the theoretical foundation of all modern confidentiality protocols: 
      
**Caesar Cipher:** A monoalphabetic substitution cipher where each character in the plaintext is shifted by a fixed numeric offset (key k) down the alphabet modulo 26. While historically significant, it has an extremely small keyspace of only 25 usable transformations, making it trivially susceptible to exhaustive brute-force search. 

**Vigenere Cipher:** Introduced to counteract the vulnerabilities of monoalphabetic ciphers, it utilizes a keyword to implement polyalphabetic substitution. Each letter of the key determines an independent Caesar shift for the corresponding plaintext letter. For centuries considered 'le chiffre indechiffrable' (the unbreakable cipher), it was eventually proven vulnerable through periodic statistical analysis pioneered by Charles Babbage and Friedrich Kasiski.

**Problem Statement**
    While contemporary cybersecurity curricula introduce classical ciphers early on, beginners  frequently struggle to understand how statistical cryptanalysis breaks encryption in practice. Standard terminal tools output final plaintexts instantaneously, concealing the algorithmic mechanics of how an attacker reasons through statistical variance, calculates the Index of Coincidence, or evaluates letter frequency distributions. There is an educational requirement for a unified application that pairs functional CLI commands with an interactive GUI featuring a transparent 'hacker console' that displays real-time cryptanalysis steps.

**Objectives**
•	Develop an extensible Python toolkit comprising a CLI (‘classical_cipher.py’) and a GUI (‘cipher_gui.py’).
•	Maintain strict Separation of Concerns (SoC) by decoupling cryptographic math and cryptanalysis algorithms from GUI display logic.
•	Implement robust input sanitization and exception management across both CLI and Tkinter user interfaces.
•	Design a dedicated visual 'Cracking Visualisation' console that logs real-time calculations: IoC bar charts, Chi-squared error scores, candidate shifts, and final plaintext recovery.

**Lab/Environment Setup**
    Setting up the development lab requires configuring dependencies, folder structures, and virtual execution spaces. Below is the exact chronological sequence of terminal commands used, accompanied by beginner explanations.

**Step 1**: System Repository Update and Upgrade
**Command:** 
    
    sudo apt update && sudo apt upgrade -y

Explanation: Refreshes the local package index against Kali mirrors and upgrades all packages to prevent compatibility conflicts.

**Step 2**: Installing Python 3, Pip, and Venv
**Command:** 
    
    sudo apt install python3 python3-pip python3-venv -y
    
Explanation: Installs the Python 3 interpreter, the pip package manager, and the venv virtual environment module.

**Step 3**: Creating Project Directory Structure
**Command**: 
    
    mkdir -p ~/crypto-tool/{cli,gui,modern,cracking} && cd ~/crypto-tool

Explanation: Creates a structured folder hierarchy to separate CLI scripts (‘cli’), GUI applications (‘gui’), future modern cryptography ciphers (‘modern’), and cracking modules (‘cracking’).

**Step 4**: Creating and Activating Python Virtual Environment
**Command**

    python3 -m venv venv

**Command**: 
    
    source venv/bin/activate

Explanation: Creates an isolated sandbox (‘venv’) to keep application packages cleanly isolated from the system Python installation. The terminal prompt prepends ‘(venv)’ to signify active isolation.

**Step 5**: Installing the Tkinter GUI Library
**Command**: 
    
    sudo apt install python3-tk -y

Explanation: Tkinter is Python's native binding to the Tk GUI toolkit. Under Linux/Kali, it must be installed via system apt repositories so Python can render X11/desktop windows.

**Methodology**
    The application was developed following modular software design principles. The backend mathematics and cryptanalytic cracking engine reside in ‘~/crypto_tool/cli/classical_cipher.py’, while the user-facing GUI application resides in ‘~/crypto_tool/gui/cipher_gui.py’. The GUI imports functionality dynamically without code duplication

**Backend Engine: classical_cipher.py**  
    
    # Caesar Encryption and Decryption
    def caesar_encrypt(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)
    
    def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)
    
    # Vigenere Encryption and Decryption
    def vigenere_encrypt(text, key):
    key = key.lower()
    result, ki = [], 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)
    
    def vigenere_decrypt(text, key):
    key = key.lower()
    result, ki = [], 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)
    
    # Statistical Cryptanalysis Tools
    
    def index_of_coincidence(text):
    text = [c for c in text.lower() if c.isalpha()]
    n = len(text)
    if n < 2: return 0
    freq = {}
    for c in text: freq[c] = freq.get(c, 0) + 1
    return sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    
    def chi_squared(text):
    text = [c for c in text.lower() if c.isalpha()]
    n = len(text)
    if n == 0: return 1e9
    freq = {c: 0 for c in ALPHA}
    for c in text: freq[c] += 1
    score = 0
    for c in ALPHA:
        expected = ENGLISH_FREQ[c] / 100 * n
        score += (freq[c] - expected) ** 2 / expected
    return score

**Backend Engine**: Cipher_gui.py
   
    #!/usr/bin/env python3
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    import string, sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "cli"))
    from classical_cipher import (
        caesar_encrypt, caesar_decrypt, vigenere_encrypt, vigenere_decrypt,
        index_of_coincidence, chi_squared, ALPHA, ENGLISH_FREQ
    )
    class CipherGUI:
    def __init__(self, root):
            root.title("Classical Cipher Studio — Encrypt | Decrypt | Crack")
            root.geometry("1000x720")
            top 
    = ttk.Frame(root, padding=8); top.pack(fill="x")
            ttk.Label(top, text="Cipher:").pack(side="left")
            self.cipher = ttk.Combobox(top, values=["Caesar","Vigenere"], state="readonly", width=12)
            self.cipher.current(0); self.cipher.pack(side="left", padx=5)
            ttk.Label(top, text="Key:").pack(side="left")
            self.key_entry = ttk.Entry(top, width=20); self.key_entry.pack(side="left", padx=5)
            mid 
    = ttk.Frame(root, padding=8); mid.pack(fill="both", expand=True)
            ttk.Label(mid, text="Input").grid(row=0, column=0, sticky="w")
            ttk.Label(mid, text="Output").grid(row=0, column=1, sticky="w")
            self.input_box = scrolledtext.ScrolledText(mid, height=8, width=50)
            self.output_box = scrolledtext.ScrolledText(mid, height=8, width=50)
            self.input_box.grid(row=1, column=0, padx=5, pady=5)
            self.output_box.grid(row=1, column=1, padx=5, pady=5)
            btns 
    = ttk.Frame(root, padding=8); btns.pack(fill="x")
            ttk.Button(btns, text="Encrypt", command=self.encrypt).pack(side="left", padx=4)
            ttk.Button(btns, text="Decrypt", command=self.decrypt).pack(side="left", padx=4)
            ttk.Button(btns, text="Visual Crack (Brute / Freq)",
          command=self.visual_crack).pack(side="left", padx=4)
            ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=4)
            ttk.Label(root, text="Cracking Visualisation", font=("TkDefaultFont",10,"bold")).pack()
            self.viz = scrolledtext.ScrolledText(root, height=18, bg="#111", fg="#0f0",
     font=("Courier",10))
            self.viz.pack(fill="both", expand=True, padx=8, pady=6)
    def _get(self):
    return self.input_box.get("1.0","end").strip(), self.key_entry.get().strip()
    def encrypt(self):
            text, key = self._get()
    try:
    if self.cipher.get() == "Caesar":
       out = caesar_encrypt(text, int(key))
    else:
       out = vigenere_encrypt(text, key)
                self.output_box.delete("1.0","end"); self.output_box.insert("1.0", out)
    except Exception as e:
                messagebox.showerror("Error", str(e))
    def decrypt(self):
            text, key = self._get()
    try:
    if self.cipher.get() == "Caesar":
       out = caesar_decrypt(text, int(key))
    else:
       out = vigenere_decrypt(text, key)
                self.output_box.delete("1.0","end"); self.output_box.insert("1.0", out)
    except Exception as e:
                messagebox.showerror("Error", str(e))
    def visual_crack(self):
            text, _ = self._get()
            self.viz.delete("1.0","end")
    if self.cipher.get() == "Caesar":
                self._visual_caesar(text)
    else:
                self._visual_vigenere(text)
    def _visual_caesar(self, text):
            v 
    = self.viz
            v.insert("end", "=== CAESAR BRUTE FORCE ===\n")
            v.insert("end", f"Ciphertext: {text}\n\n")
            best_s, best_sc = 0, 1e18
    for s in range(26):
                dec 
    = caesar_decrypt(text, s)
                sc 
    = chi_squared(dec)
                marker 
    = ""
    if sc < best_sc:
       best_sc, best_s = sc, s
       marker = "  <-- best so far"
                v.insert("end", f"shift={s:2d} χ²={sc:8.2f} :: {dec}{marker}\n")
            v.insert("end", f"\n[✓] Most likely plaintext (shift={best_s}): "
    f"{caesar_decrypt(text, best_s)}\n")
    def _visual_vigenere(self, text):
            v 
    = self.viz
            v.insert("end", "=== VIGENERE VISUAL CRACK ===\n")
            v.insert("end", f"Ciphertext: {text}\n\n")
            v.insert("end", "--- Step 1: Index of Coincidence per key-length ---\n")
    (
    , "--- Step 1: Index of Coincidence per key-length ---\n")
            best_len, best_ic = 1, 0
    for kl in range(1, 16):
                ics 
    = [index_of_coincidence(text[i::kl]) for i in range(kl)]
                avg 
                bar 
    = sum(ics)/len(ics)
    = "#" * int(avg * 200)
                v.insert("end", f"  len={kl:2d} avgIC={avg:.4f} {bar}\n")
    if avg > best_ic:
       best_ic, best_len = avg, kl
            v.insert("end", f"\n[✓] Chosen key length: {best_len}\n\n")
            v.insert("end", "--- Step 2: Chi-squared per position ---\n")
            key 
    = ""
    for i in range(best_len):
                chunk 
    = text[i::best_len]
                best_s, best_sc = 0, 1e18
    for s in range(26):
       sc 
    = chi_squared(caesar_decrypt(chunk, s))
    if sc < best_sc:
                key 
           best_sc, best_s = sc, s
    += ALPHA[best_s]
                v.insert("end", f"  pos {i:2d} -> shift {best_s:2d} "
    f"-> '{ALPHA[best_s]}' (χ²={best_sc:.2f})\n")
            v.insert("end", f"\n[✓] Recovered key: {key}\n")
            v.insert("end", f"[✓] Plaintext: {vigenere_decrypt(text, key)}\n")
    def clear(self):
            self.input_box.delete("1.0","end")
            self.output_box.delete("1.0","end")
            self.viz.delete("1.0","end")
    if __name__ == "__main__":
        root = tk.Tk()
        CipherGUI(root)
        root.mainloop()

To make it easy I have described the entire gui script the purpose so people can learn and make changes where required

**Section 1: The Shebang and Imports (Lines 1 to 8)**
    #!/usr/bin/env python3: A shebang line informing Unix-based shells to execute the script using the Python 3 interpreter.
    import tkinter as tk: Imports Python's built-in GUI library and assigns it the standard alias ‘tk’.
    from tkinter import ttk, scrolledtext, messagebox: Imports ‘ttk’ (Themed Tkinter widgets like comboboxes), ‘scrolledtext’ (text areas with built-in scrollbars), and ‘messagebox’ (modal error popups).
    import string, sys, os: Utility modules. Specifically, ‘sys.path.append (os.path.join(os.path.dirname(__file__), '..', 'cli'))’ modifies Python's import search path so the GUI script in ‘gui/’ can directly import cryptographic functions from ‘cli/classical_cipher.py’.

**Section 2: Class Blueprint and Window Construction (Lines 10 to 13)**
    class CipherGUI:  Encapsulates the entire application state and widget hierarchy inside an object-oriented blueprint.
    def __init__(self, root): The constructor method executed when the app initializes. ‘self’ allows methods to access stored widgets and state.
    root.title('Classical Cipher Studio -- Encrypt | Decrypt | Crack'): Configures the window title bar.
    root.geometry('1000x720'): Sets initial desktop dimensions to 1000 pixels wide by 720 pixels tall.

**Section 3: Top Control Bar -- Dropdown and Key Entry (Lines 15 to 21)**
    top = ttk.Frame(root, padding=8); top.pack(fill='x'): Invisible container pinned to the top of the window, stretching horizontally.
    self.cipher = ttk.Combobox(top, values=['Caesar', 'Vigenere'], state='readonly', width=12): Dropdown selector allowing users to toggle between ciphers without invalid manual entries.
    self.key_entry = ttk.Entry(top, width=20): Single-line input field where users enter numeric shifts (e.g., 3) or keyword strings (e.g., lemon).

**Section 4: Middle Row -- Input and Output Text Areas (Lines 23 to 30)**
    mid = ttk.Frame(root, padding=8); mid.pack(fill='both', expand=True): Container configured to expand dynamically if the user resizes the window.
    ‘self.input_box’ and ‘self.output_box’: Created via ‘scrolledtext.ScrolledText(mid, height=8, width=50)’. Organized using ‘.grid(row=1, column=0)’ and ‘.grid(row=1, column=1)’ side-by-side to allow convenient text comparisons.

**Section 5: Control Action Buttons (Lines 32 to 37)**
    ttk.Button(btns, text='Encrypt', command=self.encrypt): Binds button press to the encryption routine. Note that ‘self.encrypt’ is passed as a function reference without parentheses so Tkinter executes it only when clicked.
    ttk.Button(btns, text='Visual Crack (Brute / Freq)', command=self.visual_crack): Triggers the cryptanalysis engine to break ciphers without user-supplied keys.
    Section 6: Hacker Console / Visualisation Area (Lines 39 to 43)
    self.viz = scrolledtext.ScrolledText(root, height=18, bg='#111', fg='#0f0', font=('Courier', 10)): Configures a dedicated terminal simulation window styled with a black background (‘#111’), bright green text (‘#0f0’), and a monospace font (‘Courier’) so tabular mathematical logs line up perfectly.
    Section 7: Helper and Event Processing Methods (Lines 45 to 70)
    _get(self): Reads current content using ‘self.input_box.get('1.0', 'end').strip()’, returning sanitized text and key tuples.
    ‘encrypt(self)’ and ‘decrypt(self): Wraps execution inside ‘try/except Exception as e:’ blocks. If an invalid key is supplied (e.g., non-numeric Caesar shift), a friendly error dialog is presented via ‘messagebox.showerror()’ instead of crashing the program.




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

        top = ttk.Frame(root, padding=8); top.pack(fill="x")
        ttk.Label(top, text="Cipher:").pack(side="left")
        self.cipher = ttk.Combobox(top, values=["Caesar","Vigenere"], state="readonly", width=12)
        self.cipher.current(0); self.cipher.pack(side="left", padx=5)
        ttk.Label(top, text="Key:").pack(side="left")
        self.key_entry = ttk.Entry(top, width=20); self.key_entry.pack(side="left", padx=5)

        mid = ttk.Frame(root, padding=8); mid.pack(fill="both", expand=True)
        ttk.Label(mid, text="Input").grid(row=0, column=0, sticky="w")
        ttk.Label(mid, text="Output").grid(row=0, column=1, sticky="w")
        self.input_box = scrolledtext.ScrolledText(mid, height=8, width=50)
        self.output_box = scrolledtext.ScrolledText(mid, height=8, width=50)
        self.input_box.grid(row=1, column=0, padx=5, pady=5)
        self.output_box.grid(row=1, column=1, padx=5, pady=5)

        btns = ttk.Frame(root, padding=8); btns.pack(fill="x")
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
        v = self.viz
        v.insert("end", "=== CAESAR BRUTE FORCE ===\n")
        v.insert("end", f"Ciphertext: {text}\n\n")
        best_s, best_sc = 0, 1e18
        for s in range(26):
            dec = caesar_decrypt(text, s)
            sc = chi_squared(dec)
            marker = ""
            if sc < best_sc:
                best_sc, best_s = sc, s
                marker = "  <-- best so far"
            v.insert("end", f"shift={s:2d} χ²={sc:8.2f} :: {dec}{marker}\n")
        v.insert("end", f"\n[✓] Most likely plaintext (shift={best_s}): "
                        f"{caesar_decrypt(text, best_s)}\n")

    def _visual_vigenere(self, text):
        v = self.viz
        v.insert("end", "=== VIGENERE VISUAL CRACK ===\n")
        v.insert("end", f"Ciphertext: {text}\n\n")
        v.insert("end", "--- Step 1: Index of Coincidence per key-length ---\n")
        best_len, best_ic = 1, 0
        for kl in range(1, 16):
            ics = [index_of_coincidence(text[i::kl]) for i in range(kl)]
            avg = sum(ics)/len(ics)
            bar = "#" * int(avg * 200)
            v.insert("end", f"  len={kl:2d} avgIC={avg:.4f} {bar}\n")
            if avg > best_ic:
                best_ic, best_len = avg, kl
        v.insert("end", f"\n[✓] Chosen key length: {best_len}\n\n")
        v.insert("end", "--- Step 2: Chi-squared per position ---\n")
        key = ""
        for i in range(best_len):
            chunk = text[i::best_len]
            best_s, best_sc = 0, 1e18
            for s in range(26):
                sc = chi_squared(caesar_decrypt(chunk, s))
                if sc < best_sc:
                    best_sc, best_s = sc, s
            key += ALPHA[best_s]
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

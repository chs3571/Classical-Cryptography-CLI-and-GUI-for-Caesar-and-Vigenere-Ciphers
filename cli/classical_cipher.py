#!/usr/bin/env python3
"""Classical cipher toolkit: Caesar + Vigenere"""
import argparse
import string

ALPHA = string.ascii_lowercase

# ---------- CAESAR ----------
def caesar_encrypt(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ---------- VIGENERE ----------
def vigenere_encrypt(text, key):
    key = key.lower()
    result, ki = [], 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord('a')
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)

def vigenere_decrypt(text, key):
    key = key.lower()
    result, ki = [], 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord('a')
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)

# ---------- BRUTE FORCE CAESAR ----------
def caesar_bruteforce(ciphertext):
    print("\n[+] Brute-forcing Caesar (all 26 shifts):")
    for s in range(26):
        print(f"  shift={s:2d} -> {caesar_decrypt(ciphertext, s)}")

# ---------- VIGENERE CRACKER (frequency analysis) ----------
ENGLISH_FREQ = {
    'a':8.17,'b':1.49,'c':2.78,'d':4.25,'e':12.70,'f':2.23,'g':2.02,
    'h':6.09,'i':6.97,'j':0.15,'k':0.77,'l':4.03,'m':2.41,'n':6.75,
    'o':7.51,'p':1.93,'q':0.10,'r':5.99,'s':6.33,'t':9.06,'u':2.76,
    'v':0.98,'w':2.36,'x':0.15,'y':1.97,'z':0.07
}

def index_of_coincidence(text):
    text = [c for c in text.lower() if c.isalpha()]
    n = len(text)
    if n < 2: return 0
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    return sum(f*(f-1) for f in freq.values()) / (n*(n-1))

def estimate_key_length(ciphertext, max_len=20):
    print("\n[+] Estimating Vigenere key length via Index of Coincidence:")
    best_len, best_ic = 1, 0
    for kl in range(1, max_len+1):
        ics = []
        for i in range(kl):
            chunk = ciphertext[i::kl]
            ics.append(index_of_coincidence(chunk))
        avg = sum(ics)/len(ics)
        print(f"  key length {kl:2d} -> avg IC = {avg:.4f}")
        if avg > best_ic:
            best_ic, best_len = avg, kl
    print(f"[+] Probable key length: {best_len}\n")
    return best_len

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

def crack_vigenere(ciphertext):
    keylen = estimate_key_length(ciphertext)
    key = ""
    print("[+] Recovering key using chi-squared frequency analysis:")
    for i in range(keylen):
        chunk = ciphertext[i::keylen]
        best_shift, best_score = 0, 1e9
        for s in range(26):
            decrypted = caesar_decrypt(chunk, s)
            sc = chi_squared(decrypted)
            if sc < best_score:
                best_score, best_shift = sc, s
        key += ALPHA[best_shift]
        print(f"  position {i}: shift={best_shift} -> letter '{ALPHA[best_shift]}' (χ²={best_score:.2f})")
    plaintext = vigenere_decrypt(ciphertext, key)
    print(f"\n[✓] Recovered key: {key}")
    print(f"[✓] Decrypted text: {plaintext}")
    return key, plaintext

# ---------- MAIN ----------
def main():
    p = argparse.ArgumentParser(description="Caesar / Vigenere cipher toolkit")
    p.add_argument("mode", choices=["caesar-enc","caesar-dec","caesar-brute",
                                     "vig-enc","vig-dec","vig-crack"])
    p.add_argument("text", help="Text to process")
    p.add_argument("-k","--key", help="Shift (int) or Vigenere key (str)", default=None)
    args = p.parse_args()

    if args.mode == "caesar-enc":
        print(caesar_encrypt(args.text, int(args.key)))
    elif args.mode == "caesar-dec":
        print(caesar_decrypt(args.text, int(args.key)))
    elif args.mode == "caesar-brute":
        caesar_bruteforce(args.text)
    elif args.mode == "vig-enc":
        print(vigenere_encrypt(args.text, args.key))
    elif args.mode == "vig-dec":
        print(vigenere_decrypt(args.text, args.key))
    elif args.mode == "vig-crack":
        crack_vigenere(args.text)

if __name__ == "__main__":
    main()

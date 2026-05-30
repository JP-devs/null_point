import hashlib
import itertools
import time
import zipfile
import io
import contextlib

class PasswordCracker:
    def __init__(self):
        self.found = False
        self.start_time = time.time()
        self.attempts = 0
        self.hash_type = ""
        self.hash_func = None

    def detect_hash(self, hash_str):
        hash_length = len(hash_str)
        if hash_length == 32 and all(c in "0123456789abcdef" for c in hash_str):
            return "md5", hashlib.md5
        elif hash_length == 40 and all(c in "0123456789abcdef" for c in hash_str):
            return "sha1", hashlib.sha1
        elif hash_length == 64 and all(c in "0123456789abcdef" for c in hash_str):
            return "sha256", hashlib.sha256
        elif hash_length == 128 and all(c in "0123456789abcdef" for c in hash_str):
            return "sha512", hashlib.sha512
        return "unknown", None

    def crack_hash(self, hash_str, wordlist=None, max_length=6):
        self.hash_type, self.hash_func = self.detect_hash(hash_str.lower())
        
        if self.hash_type == "unknown":
            print("[!] Could not determine hash type")
            return
            
        print(f"[i] Detected hash type: {self.hash_type.upper()}")
        print("[i] Starting cracking process...\n")
        
        if wordlist:
            self._crack_with_wordlist(hash_str, wordlist)
        else:
            self._brute_force(hash_str, max_length)
            
        self._print_stats()

    def _print_stats(self):
        if not self.found:
            print("\n[!] Password not found")
            
        elapsed = time.time() - self.start_time
        print(f"\n[+] Attempted {self.attempts} passwords in {elapsed:.2f} seconds")
        if elapsed > 0:
            print(f"[+] Speed: {self.attempts/elapsed:.2f} attempts per second")

    def _crack_with_wordlist(self, hash_str, wordlist):
        try:
            with open(wordlist, 'r', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    self.attempts += 1
                    
                    if self.attempts % 1000 == 0:
                        print(f"\rAttempts: {self.attempts}", end='')
                    
                    hashed = self.hash_func(password.encode()).hexdigest()
                    if hashed == hash_str.lower():
                        self.found = True
                        print(f"\n\n[+] Password found: {password}")
                        return
        except FileNotFoundError:
            print(f"[!] Wordlist file '{wordlist}' not found")

    def _brute_force(self, hash_str, max_length):
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        for length in range(1, max_length + 1):
            print(f"[i] Trying length {length}...")
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                self.attempts += 1
                
                if self.attempts % 10000 == 0:
                    print(f"\rAttempts: {self.attempts}", end='')
                
                hashed = self.hash_func(password.encode()).hexdigest()
                if hashed == hash_str.lower():
                    self.found = True
                    print(f"\n\n[+] Password found: {password}")
                    return

    def crack_zip(self, zip_file, wordlist=None, max_length=6):
        print(f"[i] Attempting to crack ZIP file: {zip_file}")
        if wordlist:
            self._wordlist_zip(zip_file, wordlist)
        else:
            self._brute_force_zip(zip_file, max_length)
        self._print_stats()

    def _wordlist_zip(self, zip_file, wordlist):
        try:
            with zipfile.ZipFile(zip_file) as zf, open(wordlist, 'r', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    self.attempts += 1
                    if self.attempts % 100 == 0:
                        print(f"\rAttempts: {self.attempts}", end='')
                    try:
                        zf.extractall(pwd=password.encode())
                        self.found = True
                        print(f"\n\n[+] Password found: {password}")
                        return
                    except (RuntimeError, zipfile.BadZipFile):
                        continue
        except Exception as e:
            print(f"[!] Error: {e}")

    def _brute_force_zip(self, zip_file, max_length):
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        try:
            zf = zipfile.ZipFile(zip_file)
        except Exception as e:
            print(f"[!] Error: {e}")
            return
            
        for length in range(1, max_length + 1):
            print(f"[i] Trying length {length}...")
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                self.attempts += 1
                if self.attempts % 1000 == 0:
                    print(f"\rAttempts: {self.attempts}", end='')
                try:
                    zf.extractall(pwd=password.encode())
                    self.found = True
                    print(f"\n\n[+] Password found: {password}")
                    return
                except (RuntimeError, zipfile.BadZipFile):
                    continue

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print("Null Point: Password Cracker")
        # Assuming format: mode:target:wordlist:length
        parts = args_str.split(':')
        mode = parts[0] if len(parts) > 0 else 'hash'
        target = parts[1] if len(parts) > 1 else ''
        wordlist = parts[2] if len(parts) > 2 else None
        length = int(parts[3]) if len(parts) > 3 else 6
        
        cracker = PasswordCracker()
        
        try:
            if mode == "hash":
                cracker.crack_hash(target, wordlist, length)
            elif mode == "zip":
                cracker.crack_zip(target, wordlist, length)
        except Exception as e:
            print(f"[!] Error: {e}")
            
    return f.getvalue()

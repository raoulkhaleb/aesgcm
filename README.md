# AES-256-GCM File Encryption Tool

A command-line file encryption tool built in Python. Encrypts and decrypts any file using **AES-256-GCM** with a password-derived key via **PBKDF2-HMAC-SHA256**. Built as a practical cybersecurity project at the end of the Python fundamentals module of the Technology Innovation Program (TIP).

---

## How It Works

```
file.pdf  +  password  →  AES-256-GCM  →  file.pdf.enc  (original deleted)
file.pdf.enc  +  correct password  →  file.pdf  (restored)
```

The tool works on **any file type** — text, images, documents, executables, archives.

---

## Features

- **AES-256-GCM** — authenticated encryption: encrypts and detects tampering in one step
- **PBKDF2-HMAC-SHA256** — derives a secure 32-byte key from your password
- **Random salt** — 16 bytes generated per encryption run, blocks rainbow table attacks
- **Random nonce** — 12 bytes generated per encryption run, ensures unique ciphertext every time
- **No key storage** — the key lives only in RAM during execution, never written to disk
- **Original file deleted** after encryption — no plaintext left on disk
- **Password hidden** from terminal using `getpass` — no shoulder surfing

---

## Security Design

```
Password + Salt (16 bytes)
        ↓
   PBKDF2-HMAC-SHA256 × 100,000 iterations
        ↓
   32-byte AES-256 key
        ↓
   AES-GCM encrypt (Nonce: 12 bytes)
        ↓
   [salt | nonce | ciphertext + auth tag]  →  file.enc
```

### .enc File Structure

| Bytes | Content | Purpose |
|-------|---------|---------|
| `[0:16]` | Salt | Re-derive the key on decryption |
| `[16:28]` | Nonce | GCM uniqueness guarantee |
| `[28:]` | Ciphertext + Auth Tag | Encrypted file + tamper detection |

Everything needed to decrypt is stored in the file — except the password.

---

## Requirements

- Python 3.7+
- `cryptography` library

Install the dependency:

```bash
pip install cryptography
```

---

## Usage

### Encrypt a file

```bash
python index.py
```

```
Encrypt or Decrypt? (e/d): e
File (.ext): secret.pdf
Password:
```

Output:

```
File Encrypted successfully!
File saved as 'secret.pdf.enc'
```

The original `secret.pdf` is deleted. Only `secret.pdf.enc` remains.

---

### Decrypt a file

```bash
python index.py
```

```
Encrypt or Decrypt? (e/d): d
File (.ext): secret.pdf.enc
Password:
```

Output:

```
File Decrypted Successfully!
File saved as 'secret.pdf'
```

The `.enc` file is deleted. The original file is fully restored.

---

### Wrong password

If the wrong password is entered during decryption, AES-GCM's authentication tag verification fails:

```
Decryption failed: ...
```

Nothing is written to disk. No corrupted output.

---

## Code Structure

```
index.py
├── get_key(password, salt)       # PBKDF2 key derivation
├── encrypt_file(filename, password)  # Read → generate salt/nonce → encrypt → write → delete original
└── decrypt_file(enc_filename, password)  # Read → slice → re-derive key → decrypt → restore
```

### Key derivation

```python
def get_key(password, salt):
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),  # string → bytes
        salt,               # random 16-byte salt
        100000              # 100,000 iterations
    )
    return key              # 32-byte key for AES-256
```

### Encryption output layout

```python
f.write(salt + nonce + ciphertext)
# [16 bytes] + [12 bytes] + [N bytes]
```

### Decryption input parsing

```python
salt       = data[:16]
nonce      = data[16:28]
ciphertext = data[28:]
```

---

## Why AES-GCM?

| Mode | Encrypts | Detects Tampering |
|------|----------|-------------------|
| ECB  | ✓ | ❌ (patterns leak) |
| CBC  | ✓ | ❌ (silent corruption) |
| **GCM** | ✓ | ✓ **(authentication tag)** |

GCM was chosen because it provides **authenticated encryption** — it encrypts the data and appends a 16-byte authentication tag. If even one byte of the `.enc` file is modified after encryption, decryption fails and nothing is written.

---

## Limitations

- **PBKDF2 vs Argon2** — PBKDF2 is CPU-bound. Modern GPUs can evaluate SHA-256 at high throughput. A future version would use **Argon2** (memory-hard, significantly more GPU-resistant).
- **Full file in RAM** — `f.read()` loads the entire file into memory. Very large files may crash the program if they exceed available RAM. A future version would use chunked/streaming processing.

---

## Libraries Used

| Library | Role |
|---------|------|
| `cryptography.hazmat` | AES-GCM encryption and decryption |
| `hashlib` | PBKDF2-HMAC-SHA256 key derivation |
| `os` | Secure random bytes (`os.urandom`), file deletion |
| `getpass` | Hidden password input |

> `os.urandom()` is used instead of Python's `random` module because `random` is predictable if the seed is known. `os.urandom()` reads from the OS-level CSPRNG (Cryptographically Secure Pseudo-Random Number Generator).

---

## Built With

- **Language:** Python 3
- **Algorithm:** AES-256-GCM
- **Key Derivation:** PBKDF2-HMAC-SHA256
- **Program:** Technology Innovation Program (TIP)
- **Author:** KANOBAYIRE Raoul Khaleb

---

## License

MIT License — free to use, modify, and distribute.

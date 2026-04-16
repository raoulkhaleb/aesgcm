from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import os
import getpass

def get_key(password, salt):
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
    )
    return key

def encrypt_file(filename, password):
    try:
        with open(filename, "rb") as f:
            plaintext = f.read()

        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = get_key(password, salt)

        aes = AESGCM(key)
        ciphertext = aes.encrypt(nonce, plaintext, None)

        enc_filename = filename + ".enc"
        with open(enc_filename, "wb") as f:
            f.write(salt + nonce + ciphertext)

        print("\nFile Encrypted successfully!")
        print(f"File saved as '{enc_filename}'")
        os.remove(filename)

    except Exception as e:
        print(f"\nEncryption failed: {e}")

def decrypt_file(enc_filename, password):
    try: 
        with open(enc_filename, "rb") as f:
            data = f.read()
            
            salt = data[:16]
            nonce = data[16:28]
            ciphertext = data[28:]

        key = get_key(password, salt)
        aes = AESGCM(key)

        plaintext = aes.decrypt(nonce, ciphertext, None)

        dec_filename = enc_filename[:-4] #removes .enc extension
        with open(dec_filename, "wb") as f:
            f.write(plaintext)
        
        print("\nFile Decrypted Successfully!")
        print(f"File saved as '{dec_filename}'")
        os.remove(enc_filename)

    except Exception as e:
        print(f"\nDecryption failed: {e}")


action = input("Encrypt or Decrypt? (e/d): ").lower()
filename = input("File (.ext): ")
password = getpass.getpass("Password: ")

if action == 'e':
    encrypt_file(filename, password)
elif action == 'd':
    decrypt_file(filename, password)
else:
    print("Invalid action")


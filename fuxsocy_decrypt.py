import os
import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

START_DIR = os.getcwd()
CS = 64*1024

def decrypt(root, filename, key):
    if (('fuxsocy.py' not in filename) and ('fsociety_key.dat' not in filename) and ('fuxsocy_decrypt.py' not in filename)):
        file_path = os.path.join(root, filename)
        try:
            with open(file_path, 'rb') as infile:
                file_size = int(infile.read(16))
                iv = infile.read(16)
                decryptor = AES.new(key, AES.MODE_CBC, iv)
                data = b''
                while True:
                    chunk = infile.read(CS)
                    if len(chunk) == 0:
                        break
                    data += decryptor.decrypt(chunk)
            with open(file_path, 'wb') as outfile:
                outfile.write(data[:file_size])
        except Exception as e:
            print(f"Error decrypting {file_path}: {e}")

def recurse(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            decrypt(root, file, key)

def load_key():
    if not os.path.exists('fsociety_key.dat'):
        print("Error: fsociety_key.dat not found!")
        sys.exit(1)
    with open('fsociety_key.dat', 'r') as f:
        password = f.read()
    return SHA256.new(password.encode('utf-8')).digest()

def main():
    print('Executing FuxSocy Decryptor')
    key = load_key()
    recurse(START_DIR, key)
    print('\nDecryption complete.')
    del key

if __name__ == '__main__':
    main()

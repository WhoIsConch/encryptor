import random
import os

NUMS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class WeakEncryptor:
    def __init__(self):
        self.key: str = self.get_key()
    
    def get_key(self) -> str:
        try:
            with open('key.key', 'r') as f:
                key = f.read()
            return key
        except FileNotFoundError:
            key = "".join(random.choice(NUMS) for _ in range(random.randrange(8, 32)))

            with open('key.key', 'w') as f:
                f.write(key)
            return key
    
    def encrypt(self, data: bytes):
        # Encrypt data in bytes
        return bytes([data[i] ^ int(self.key[i % len(self.key)]) for i in range(len(data))])

    def decrypt(self, data: bytes):
        # Decrypt data in bytes
        return bytes([data[i] ^ int(self.key[i % len(self.key)]) for i in range(len(data))])
    
    def encrypt_file(self, file_name: str):
        with open(file_name, 'rb') as f:
            data = f.read()

        with open(file_name, 'wb') as f:
            f.write(self.encrypt(data))
    
        return True
    
    def decrypt_file(self, file_name: str):
            with open(file_name, 'rb') as f:
                data = f.read()
    
            with open(file_name, 'wb') as f:
                f.write(self.decrypt(data))
        
            return True
        
    def encrypt_dir(self, dir_name: str):
        for file in os.listdir(dir_name):
            if os.path.isfile(os.path.join(dir_name, file)):
                self.encrypt_file(os.path.join(dir_name, file))

            elif os.path.isdir(os.path.join(dir_name, file)):
                self.encrypt_dir(os.path.join(dir_name, file))
            
    def decrypt_dir(self, dir_name: str):
        for file in os.listdir(dir_name):
            if os.path.isfile(os.path.join(dir_name, file)):
                self.decrypt_file(os.path.join(dir_name, file))

            elif os.path.isdir(os.path.join(dir_name, file)):
                self.decrypt_dir(os.path.join(dir_name, file))
        
    
if __name__ == "__main__":
    w = WeakEncryptor()
    w.encrypt_dir("src/data")
    print("Encrypted")
    w.decrypt_dir("src/data")
    print("Decrypted")



        

            
                
from cryptography.fernet import Fernet
import time
import os
import logging

class Encryptor(Fernet):
    def __init__(self, key=None, debug=False):
        if debug:
            logging.basicConfig(
                filename='log.log',
                level=logging.INFO,
                format='%(asctime)s:%(levelname)s:%(message)s'
            )
        else:
            logging.basicConfig(
                level=logging.ERROR,
                format='%(asctime)s:%(levelname)s:%(message)s'
            )

        self.logger = logging.getLogger(__name__)
        if key is None:
            if os.path.exists('key.key'):
                self.key = self.get_key()
            else:
                self.key = self.gen_key()
        else:
            self.key = key
        

        
        super().__init__(self.key)
    
    def gen_key(self):
        self.logger.info('Generating key...')
        key = Fernet.generate_key()

        with open('key.key', 'wb') as f:
            f.write(key)
        
        self.logger.info('Key generated.')
        return key
    
    def get_key(self):
        self.logger.info('Getting key...')
        with open('key.key', 'rb') as f:
            key = f.read()
    
        self.logger.info('Key retrieved.')
        return key
    
    def encrypt_file(self, file_name):
        self.logger.info(f'Encrypting {file_name}...')

        with open(file_name, 'rb') as f:
            data = f.read()

        with open(file_name, 'wb') as f:
            f.write(self.encrypt(data))
        
        self.logger.info(f'{file_name} encrypted.')
        return True
    
    def decrypt_file(self, file_name):
        self.logger.info(f'Decrypting {file_name}...')

        with open(file_name, 'rb') as f:
            data = f.read()

        with open(file_name, 'wb') as f:
            f.write(self.decrypt(data))
        
        self.logger.info(f'{file_name} decrypted.')
        return True
    
    def encrypt_dir(self, dir_name):
        self.logger.info(f'Encrypting {dir_name}...')

        for root, dirs, files in os.walk(dir_name):
            for file in files:
                self.encrypt_file(os.path.join(root, file))
            for dir in dirs:
                self.encrypt_dir(os.path.join(root, dir))

        self.logger.info(f'{dir_name} encrypted.')
        return True

    def decrypt_dir(self, dir_name):
        self.logger.info(f'Decrypting {dir_name}...')

        for root, dirs, files in os.walk(dir_name):
            for file in files:
                self.decrypt_file(os.path.join(root, file))
            for dir in dirs:
                self.decrypt_dir(os.path.join(root, dir))

        self.logger.info(f'{dir_name} decrypted.')
        return True

if __name__ == '__main__':
    encryptor = Encryptor()

    print('Encrypting...')
    t1 = time.time()
    encryptor.encrypt_dir('data')
    t2 = time.time()
    print('Encryption time:', t2 - t1)

    print('Decrypting...')
    t1 = time.time()
    encryptor.decrypt_dir('data')
    t2 = time.time()
    print('Decryption time:', t2 - t1)

    print('Done!')

    
'''
async
'''
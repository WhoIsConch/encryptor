from cryptography.fernet import Fernet
import os
import logging
from aiofiles import open as aopen
from pathlib import Path

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
    
    async def encrypt_file(self, file_name):
        self.logger.info(f'Encrypting {file_name}...')

        async with aopen(file_name, 'rb') as f:
            data = await f.read()

        async with aopen(file_name, 'wb') as f:
            await f.write(self.encrypt(data))
        
        self.logger.info(f'{file_name} encrypted.')
        return True
    
    async def decrypt_file(self, file_name):
        self.logger.info(f'Decrypting {file_name}...')

        async with aopen(file_name, 'rb') as f:
            data = await f.read()

        async with aopen(file_name, 'wb') as f:
            await f.write(self.decrypt(data))
        
        self.logger.info(f'{file_name} decrypted.')
        return True
    
    async def encrypt_dir(self, dir_name):
        self.logger.info(f'Encrypting {dir_name}...')

        path = Path(dir_name)

        for item in path.iterdir():
            if item.is_file():
                await self.encrypt_file(str(item))
            elif item.is_dir():
                await self.encrypt_dir(str(item))

        self.logger.info(f'{dir_name} encrypted.')
        return True

    async def decrypt_dir(self, dir_name):
        self.logger.info(f'Decrypting {dir_name}...')

        path = Path(dir_name)

        for item in path.iterdir():
            if item.is_file():
                await self.decrypt_file(str(item))
            elif item.is_dir():
                await self.decrypt_dir(str(item))

        self.logger.info(f'{dir_name} decrypted.')
        return True


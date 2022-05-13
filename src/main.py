import asyncio
import time
from encryptor import Encryptor


if __name__ == '__main__':
    encryptor = Encryptor()

    print('Encrypting...')
    t1 = time.time()
    asyncio.run(encryptor.encrypt_dir('data'))
    t2 = time.time()
    print('Encryption time:', t2 - t1)

    print('Decrypting...')
    t1 = time.time()
    asyncio.run(encryptor.decrypt_dir('data'))
    t2 = time.time()
    print('Decryption time:', t2 - t1)

    print('Done!')
import getpass
import os
from io import StringIO
from pathlib import Path

import pandas
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encode_your_csv(password) -> None:
    file_path = parent_directory / 'contacts.csv'

    df = pandas.read_csv(file_path)

    df_filtered = df[['First Name', 'Last Name', 'Birthday']]
    df_filtered = df_filtered.dropna(subset=['Birthday'])

    csv_buffer_var = StringIO()
    df_filtered.to_csv(csv_buffer_var, index=False)
    csv_content_bytes = csv_buffer_var.getvalue()

    encrypt_file(csv_content_bytes, password)

def encrypt_file(data: str, password: str) -> None:
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    data_to_encrypt = data.encode()

    encrypted_data = encryptor.update(data_to_encrypt) + encryptor.finalize()

    output_file = parent_directory / "encrypted_file.enc"
    with open(output_file, 'wb') as f:
        f.write(salt + iv + encrypted_data)


if __name__ == '__main__':
    current_script_path = Path(__file__)
    parent_directory = current_script_path.parent.parent
    user_input = getpass.getpass("Please enter a string: ")
    encode_your_csv(user_input)

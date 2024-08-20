import io
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.send_email import send_email


def decode_and_check(password: str) -> None:
    current_script_path = Path(__file__)
    parent_directory = current_script_path.parent.parent
    file_path = parent_directory / "encrypted_file.enc"

    with open(file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        encrypted_data = f.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        data_stream = io.BytesIO(decrypted_data)
        df = pd.read_csv(data_stream, encoding='ISO-8859-1', delimiter=',')
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV data: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce')

    today = datetime.today()

    birthdays_today = df[(df['Birthday'].dt.month == today.month) & (df['Birthday'].dt.day == today.day)]

    final_list = birthdays_today.to_dict('records')

    if not birthdays_today.empty:
        print("There seems to be something!")
        send_email(final_list)
    else:
        print("Guess today is chill!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <secret>")
        sys.exit(1)

    secret = sys.argv[1]
    decode_and_check(secret)

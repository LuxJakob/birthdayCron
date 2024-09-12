# Birthday Reminder Workflow

This project automatically decrypts a CSV file containing birthday information, checks for birthdays occurring today, and sends an email notification.

## Project Structure

- `encodeFile.py`: Encrypts the `contacts.csv` file containing birthday information.
- `main.py`: Decrypts the encrypted file, checks for birthdays, and triggers an email if a birthday is found.
- `send_email.py`: Sends an email notification when a birthday is found.
- `dailyCheck.yml`: GitHub Actions workflow for automatically running the script daily.

## Setup

1. Encrypt your contacts.csv
   ```bash
   python3 src/encodeFile.py
   ```
   ***IMPORTANT:*** Use the same Password as your GitHub Actions Secret!
2. Trigger Script via GitHub Action
3. Wait for Cronjob to trigger
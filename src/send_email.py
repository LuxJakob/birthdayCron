import os
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import requests


def send_email(list_of_people: List) -> None:
    port = 465
    smtp_server = "smtp.gmail.com"
    username = os.environ.get('MAIL_USERNAME')
    pwd_secure = os.environ.get('MAIL_PASSWORD')

    if username is None or pwd_secure is None:
        print("Error: MAIL_USERNAME or MAIL_PASSWORD is not set.")
        return

    today = datetime.today()

    subject = ""
    message_body = ""

    for entry in list_of_people:
        first_name = entry['First Name']
        last_name = entry['Last Name']
        birthday = entry['Birthday']

        age = today.year - birthday.year

        subject += f'{first_name} {last_name} '
        message_body += f'{first_name} wird heute {age} Jahre alt! <br><br>'

    subject += "hat heute Geburtstag!"

    message_body += 'Da wünsche ich alles Gute zum Geburtstag!<br>'
    message_body += fetch_quote()

    footer = '''<br><br>
    <span style="z-index:50;font-size:0.9em; font-weight: bold;">
        <img src="https://theysaidso.com/branding/theysaidso.png" height="20" width="20" alt="theysaidso.com"/>
        <a href="https://theysaidso.com" title="Powered by quotes from theysaidso.com" 
           style="color: #ccc; margin-left: 4px; vertical-align: middle;">They Said So®</a>
    </span>'''

    message_body += footer

    email_message = MIMEMultipart()
    email_message['From'] = username
    email_message['To'] = username
    email_message['Subject'] = subject

    email_message.attach(MIMEText(message_body, 'html'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, pwd_secure)
            server.sendmail(username, username, email_message.as_string())
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_quote() -> str:
    api_token_qod = os.environ.get('API_TOKEN_QOD')
    url = 'https://quotes.rest/qod?category=inspire&language=en'

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_token_qod}'
    }

    response = requests.get(url, headers=headers)

    final_quote = '''
        <p><strong>Bertolt Brecht:</strong></p>
        <blockquote style="margin-left: 20px;">
            <p>Und der Haifisch, der hat Zähne<br>
            Und die trägt er im Gesicht<br>
            Und Macheath, der hat ein Messer<br>
            Doch das Messer sieht man nicht.</p>
        </blockquote>
    '''

    if response.status_code == 200:
        data = response.json()

        quote_info = data['contents']['quotes'][0]
        author = quote_info['author']
        quote = quote_info['quote']

        final_quote = f'<br><br>{author}:<br>"{quote}<br><br>"'

    return final_quote

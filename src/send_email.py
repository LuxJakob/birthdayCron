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

    subject = create_subject(list_of_people)
    message_body = create_message_body(list_of_people)

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
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:  # pylint: disable=W0718
        print(f"An unexpected error occurred: {e}") # Fallback


def create_subject(list_of_people: List) -> str:
    subject = ""
    for entry in list_of_people:
        first_name = entry['First Name']
        last_name = entry['Last Name']
        subject += f'{first_name} {last_name} '
    subject += "hat heute Geburtstag! 🥳🤩"
    return subject


def create_message_body(list_of_people: List) -> str:
    message_body = ""
    today = datetime.today()
    for entry in list_of_people:
        birthday = entry['Birthday']
        age = today.year - birthday.year
        message_body += f'Glückwunsch! Du wirst heute {age} Jahre alt! 🐸<br>'

    message_body += 'Da wünsche ich alles Gute zum Geburtstag!<br><br>'
    message_body += fetch_random_gif()
    message_body += fetch_random_quote()
    message_body += fetch_random_advice()
    message_body += '''
    <div style="font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: left; font-size: 18px; 
    color: #333; padding: 20px; border-radius: 8px;">
        <p>Diese Mail erreicht dich via meines GitHub Cronjobs.</p>
        <p>Liebe Drücker,</p>
        <p>Jakob</p>
    </div>'''
    return message_body


def fetch_random_gif() -> str:
    api_token_tenor = os.environ.get('API_TOKEN_TENOR')
    search_term = "excited"
    client_key = "birthdayCron"
    country = "US"
    locale = "en_US"
    contentfilter = "low"
    media_filter = "gif"
    random = True
    lmt = 1
    response = requests.get(
        f"https://tenor.googleapis.com/v2/search?q={search_term}&key={api_token_tenor}&"
        f"client_key={client_key}&country={country}&locale={locale}&"
        f"contentfilter={contentfilter}&media_filter={media_filter}&"
        f"random={str(random).lower()}&limit={lmt}"
    )

    funny_gif = ''
    if response.status_code == 200:
        data = response.json()
        gif_url = data['results'][0]['media_formats']['gif']['url']
        funny_gif = (
            f'So fühle ich heute über deinen Tag:<br><img src="{gif_url}" alt="Funny GIF" />'
        )
        footer = '''<br>
            <div style="display: flex; align-items: center; font-size: 0.9em; font-weight: bold; z-index: 50;">
                <img src="https://www.gstatic.com/tenor/web/attribution/via_tenor_logo_blue.png"
                 height="20" width="95" alt="Tenor Logo"/>
                <a href="https://tenor.com/" title="Powered by Tenor"
                 style="color: #ccc; margin-left: 8px; text-decoration: none;"></a>
            </div><br>'''
        funny_gif += footer
    else:
        print(
            f'GIF was not found! {response.status_code} & {response.text}'
        )
    return funny_gif


def fetch_random_quote() -> str:
    url = 'https://favqs.com/api/qotd'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        author = data['quote']['author']
        quote = data['quote']['body']
    else:
        print(
            f'Quote was not found! {response.status_code} & {response.text}'
        )
        author = "Berthold Brecht"
        quote = '''Und der Haifisch, der hat Zähne<br>
        Und die trägt er im Gesicht<br>
        Und Macheath, der hat ein Messer<br>
        Doch das Messer sieht man nicht.'''

    formatted_quote = (
        f'Außerdem habe ich dieses Zitat für dich:'
        f'<p><strong>{author}:</strong></p>'
        f'<blockquote style=margin-left: 20px;><p>{quote}</p></blockquote>'
    )

    return formatted_quote


def fetch_random_advice() -> str:
    url = 'https://api.adviceslip.com/advice'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        advice = data['slip']['advice']

        formatted_advice = (
            f'<p>Wichtiges Wissen für dein neues Lebensjahr:</p>'
            f'<p>{advice}:</p><br><br>'
        )
        return formatted_advice

    return ''

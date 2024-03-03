import email
import os
import poplib
import re
from email.parser import Parser

import settings
from client_reader import ClientReader


class POP3Client(ClientReader):
    server = settings.pop3_server
    port = settings.pop3_port
    username = settings.email_login
    password = settings.email_password

    def __get_all_emails(self):
        pop3_server = poplib.POP3_SSL(self.server, self.port)
        pop3_server.user(self.username)
        pop3_server.pass_(self.password)

        emails = []
        num_messages = len(pop3_server.list()[0])

        for i in range(1, num_messages):
            try:
                response, lines, octets = pop3_server.retr(i)
                message_info = pop3_server.retr(i)
                message_data = b'\r\n'.join(lines).decode('utf-8')

                email = Parser().parsestr(message_data)

                emails.append(email)
            except Exception as e:
                pass

        pop3_server.quit()
        return emails

    """ Найти письмо по его порядковому номеру """
    def __find_email_by_idx(self, idx) -> str:
        messages = self.__get_all_emails()
        return messages[idx]

    def print_all_emails(self):
        messages = self.__get_all_emails()
        for idx, message in enumerate(messages):
            # Extract relevant information from message object
            sender = re.sub(r'"(.*?)"', '', message.get("From")).replace('\t', '')
            subject = decode_subject(message.get("Subject"))

            print(f'\nПисьмо #{idx}: \nОт: {sender}\nТема: {subject}\n')

    def open_email(self, email_id: str):
        message = self.__find_email_by_idx(email_id)
        path = message["Return-path"]
        header = email.header.decode_header(message["Subject"])[0][0].decode()

        print(f'\nПисьмо #{email_id}: \nОт: {path}\nТема: {header}\nСодержание: ')

        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            filename = part.get_filename()
            if filename:
                filepath = os.path.join('downloads', filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"[Файл сохранен как: {filepath}]")
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                charset = part.get_content_charset()
                if charset:
                    body = body.decode(charset)
                else:
                    body = body.decode()
                print(body)

def decode_subject(subject):
    if subject:
        decoded_subject = email.header.decode_header(subject)[0][0].decode()
        return decoded_subject
    else:
        return "[Without Subject]"
import email
import email.header
import email.utils
import imaplib
import os

import settings
from client_reader import ClientReader

class IMAPClient(ClientReader):
    server = settings.imap_server
    port = settings.imap_port
    username = settings.email_login
    password = settings.email_password

    """ Получить все письма с почты """
    def __get_all_emails(self):
        imap = imaplib.IMAP4_SSL(self.server)
        imap.login(self.username, self.password)
        imap.select("INBOX")

        status, email_ids = imap.search(None, "ALL")
        if status == "OK":
            emails = []
            for email_id in email_ids[0].split():
                status, message_data = imap.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    emails.append(email.message_from_bytes(message_data[0][1]))
            return emails
        else:
            return []

    """ Найти письмо по его порядковому номеру """
    def __find_email_by_idx(self, idx) -> str:
        messages = self.__get_all_emails()
        return messages[idx]

    """ Вывести письма """
    def print_all_emails(self):
        messages = self.__get_all_emails()
        for idx, message in enumerate(messages):
            path = message["Return-path"]
            header = email.header.decode_header(message["Subject"])[0][0].decode()
            print(f'\nПисьмо #{idx}: \nОт: {path}\nТема: {header}\n')


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

    def send_email(self):
        pass
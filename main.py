import imap_client
import pop3_client
import settings
import os

from smtp_client import SMTPClient

clear = lambda: os.system('cls')
protocol = settings.imap_name

def set_protocol(_protocol):
    global protocol
    protocol = _protocol

def print_menu(options):
    for i, option in enumerate(options):
        print(f"{option}")

def get_user_input(options):
    while True:
        choice = input("Введите номер пункта меню: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Неверный номер пункта.")
        except ValueError:
            print("Введите число.")

def match_protocol() -> object:
    match protocol:
        case 'imap':
            return imap_client.IMAPClient()
        case 'pop3':
            return pop3_client.POP3Client()

def incoming_emails():
    client = match_protocol()
    client.print_all_emails()

    idx = input("Введите ID письма для открытия (Enter для выхода) ")
    if idx is "":
        return

    idx = int(idx)
    client.open_email(idx)

def write_email():
    client = SMTPClient()

    send_to = input("Введите почту получателя: ")
    subject = input("Введите тему сообщения: ")
    text = input("Введите текст сообщения: ")
    files_string = input("Введите через пробел файлы из папки 'files': ")

    folder_path = "files"
    files_list = []
    files_names = files_string.split()
    files = os.listdir(folder_path)

    for file_name in files_names:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files_list.append(file_path)

    print("Были прикреплены следующие файлы: " + str(files_list))

    client.send_email(send_to='thebooom@yandex.ru', subject_text=subject, body_text=text, files=files_list)
    print('Письмо было доставлено')

def open_settings():
    options = ['Выберите протокол чтения: \n', '1. IMAP', '2. POP3', '3. Назад\n']
    while True:
        print_menu(options)
        choice = get_user_input(options)
        if choice == len(options):
            break
        match choice:
            case 1:
                set_protocol(settings.imap_name)
                return
            case 2:
                set_protocol(settings.pop3_name)
                return
            case 3:
                return

def main():
    while True:
        options = ["Меню почтового клиента: ", f"Протокол отправки: {settings.smtp_name}", f"Протокол чтения: {protocol}\n", "1. Входящие письма",
                   "2. Написать письмо", "3. Настройки", "4. Выход\n"]
        print_menu(options)
        choice = get_user_input(options)
        if choice == len(options):
            break
        match choice:
            case 1:
                incoming_emails()
            case 2:
                write_email()
            case 3:
                open_settings()
            case 4:
                exit(0)
        input("Нажмите для продолжения ")
        clear()

if __name__ == "__main__":
    main()

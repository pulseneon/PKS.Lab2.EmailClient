import imap_client
import settings
import os

clear = lambda: os.system('cls')

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
    match settings.protocol:
        case 'imap':
            return imap_client.IMAPClient()
        case 'smtp':
            pass
        case 'pop3':
            pass

def incoming_emails():
    client = match_protocol()
    client.print_all_emails()

    idx = input("Введите ID письма для открытия (Enter для выхода) ")
    if idx is "":
        return

    idx = int(idx)
    client.open_email(idx)

def main():
    options = ["Меню почтового клиента: ", f"Текущий протокол: {settings.protocol}\n", "1. Входящие письма", "2. Непрочитанные письма", "3. Написать письмо", "4. Настройки", "5. Выход\n"]
    while True:
        print_menu(options)
        choice = get_user_input(options)
        if choice == len(options):
            break
        match choice:
            case 1:
                incoming_emails()

        input("Нажмите для продолжения ")
        clear()

if __name__ == "__main__":
    main()

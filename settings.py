email_login = 'testpost_1@rambler.ru'
email_password = 'GaPDX8Ajb73HS'

protocol = 'imap'

imap_server = 'imap.rambler.ru'
imap_port = 993

smtp_server = 'smtp.rambler.ru'
smtp_port = 465

pop3_server = 'pop.rambler.ru'
pop3_port = 995


def set_protocol(_protocol):
    global protocol
    protocol = _protocol

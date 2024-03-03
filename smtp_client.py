import settings
from client_writer import ClientWritter
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class SMTPClient(ClientWritter):
    server = settings.smtp_server
    port = settings.smtp_port
    username = settings.email_login
    password = settings.email_password

    def send_email(self, send_to, subject_text, body_text, files=None):
       message = MIMEMultipart()
       message["From"] = self.username
       message["To"] = send_to
       message["Subject"] = subject_text

       message.attach(MIMEText(body_text, "plain"))

       for f in files or []:
           with open(f, "rb") as fil:
               part = MIMEApplication(
                   fil.read(),
                   Name=basename(f)
               )

           part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
           message.attach(part)

       smtp = smtplib.SMTP_SSL(self.server, self.port)
       smtp.login(self.username, self.password)
       print(message)
       result = smtp.sendmail(self.username, send_to, msg=message.as_string(message))
       print(result)

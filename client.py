from abc import ABC, abstractmethod

class Client(ABC):
    @abstractmethod
    def print_all_emails(self):
        pass

    @abstractmethod
    def open_email(self, email_id: str):
        pass
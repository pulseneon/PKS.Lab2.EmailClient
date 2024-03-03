from abc import ABC, abstractmethod

class ClientReader(ABC):
    @abstractmethod
    def print_all_emails(self):
        pass

    @abstractmethod
    def open_email(self, email_id: str):
        pass
from abc import ABC, abstractmethod

class ClientWritter(ABC):
    @abstractmethod
    def send_email(self):
        pass
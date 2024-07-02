import os

class Utils:
    @staticmethod
    def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')
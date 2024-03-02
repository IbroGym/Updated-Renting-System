#calculator.py
class Arithmetic:
    def __init__(self):
        pass

    def add(self, num1, num2):
        return num1 + num2

    def subtract(self, num1, num2):
        return num1 - num2

    def multiply(self, num1, num2):
        return num1 * num2

    def divide(self, num1, num2):
        if num2 == 0:
            return "Cannot divide by zero"
        else:
            return num1 / num2


class Double(Arithmetic):
    def __init__(self):
        super().__init__()

    def twox(self, digit):
        return digit * 2


class Even(Arithmetic):
    def __init__(self):
        super().__init__()

    def isEven(self, digit):
        return digit % 2 == 0


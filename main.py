import random as rn
import string

class Picker:
    lsit_of_ASCII = list(string.printable)

    def __init__(self):
        # Last ASCII signs are not really usefull
        del self.lsit_of_ASCII[-6:]

    def pick_random(self):
        random_choice = rn.choice(self.lsit_of_ASCII)
        self.lsit_of_ASCII.remove(random_choice)
        return random_choice


class Card:
    list_of_ascii_uppercase = list(string.ascii_uppercase)
    list_of_digits = list(string.digits)

    def __init__(self, number_of_lines_horizontal = 0, number_of_lines_vertical = 0):
        self.number_of_lines_horizontal = number_of_lines_horizontal
        self.number_of_lines_vertical = number_of_lines_vertical

        self.rescale_list(len(string.ascii_uppercase), self.number_of_lines_horizontal, self.list_of_ascii_uppercase)
        self.rescale_list(len(string.digits), number_of_lines_vertical, self.list_of_digits)

    def rescale_list(self, ascii_number, number_of_lines, list_of_content):
        if number_of_lines > ascii_number:
            number_of_lines = ascii_number-1
        if number_of_lines != 0:
            del list_of_content[-number_of_lines:]

    def field(self):
        print(self.list_of_ascii_uppercase)
        print(self.list_of_digits)


# class Generator:


def main():
    c = Card()
    p = Picker()
    print(c.field())

if __name__ == '__main__':
    main()

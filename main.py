import random as rn
import string
from enum import Enum
import sys
import os


class Picker:
    list_of_ASCII = list(string.printable)

    def __init__(self):
        # Last ASCII signs are not really usefull
        del self.list_of_ASCII[-6:]

    def pick_random(self):
        try:
            random_choice = rn.choice(self.list_of_ASCII)
            self.list_of_ASCII.remove(random_choice)
        except IndexError:
            self.list_of_ASCII = list(string.printable)
            del self.list_of_ASCII[-6:]
            random_choice = rn.choice(self.list_of_ASCII)
            self.list_of_ASCII.remove(random_choice)
        return random_choice


class Single:
    def __init__(self, length):
        self.length = length

    def get_single_password(self):
        p = Picker()
        password = ""
        for i in range(self.length):
            # random_ascii = p.pick_random()
            password += p.pick_random()
        return password

    def console_single(self):
        clear()
        password = self.get_single_password()
        print("Your generated is:" + "\n" + str(password))



class Card:
    def __init__(self, number_of_lines_horizontal = 0, number_of_lines_vertical = 0):
        self.list_of_ascii_uppercase = list(string.ascii_uppercase)
        self.list_of_digits = list(string.digits)
        self.number_of_lines_horizontal = number_of_lines_horizontal
        self.number_of_lines_vertical = number_of_lines_vertical

        self.rescale_list(len(string.ascii_uppercase), self.number_of_lines_horizontal, self.list_of_ascii_uppercase)
        self.rescale_list(len(string.digits), number_of_lines_vertical, self.list_of_digits)

    def rescale_list(self, ascii_number, number_of_lines, list_of_content):
        number_of_lines = number_of_lines
        if number_of_lines > ascii_number:
            number_of_lines = ascii_number
        n = ascii_number - number_of_lines
        if n != 0:
            del list_of_content[-n:]
        return list_of_content

    def field(self):
        field = []
        p = Picker()
        counter = 0
        self.list_of_ascii_uppercase.insert(0, "/")
        for i in range(len(self.list_of_digits)):
            row = []
            for j in range(len(self.list_of_ascii_uppercase)-1):
                random_choice = p.pick_random()
                row.append(random_choice)
            row.insert(0, self.list_of_digits[counter])
            counter += 1
            field.append(row)
        counter = 0
        return field

    # vlt. eher in die CommandLine packen damit besser Logik von Output getrennt ist
    def console_card(self):
        field = self.field()

        clear()
        self.draw_line()
        top_row = " ".join(self.list_of_ascii_uppercase)
        print(top_row)
        for i in field:
            row_string = " ".join(i)
            print(row_string)
        self.draw_line()

    def draw_line(self):
        print("--"*int(self.number_of_lines_horizontal+1))


class Image:
    pass

class MenuItem(Enum):
    SINGLE_CONSOLE = 1
    CARD_CONSOLE = 2
    IMAGE = 3


class OutOfRange(Exception):
    pass


class CommandLine:
    # menu_Items = MenuItem()

    def __init__(self):
        pass

    def menu(self):
        generate_type_choice = self.generate_type_choice()
        self.validate_choice(generate_type_choice)

    def generate_type_choice(self):
        clear()
        print("Bitte wähle einen Menüpunkt aus indem du die vorranstehende Zahl angibst.")
        print("(1). Generate Single Line Password.")
        print("(2). Generate Password Card.")
        print("(3). Generate Password Image.")

        return self.validate_input(MenuItem.SINGLE_CONSOLE.value, MenuItem.IMAGE.value)

    def card_line_choice(self):
        clear()
        print("Wie viele Reihen soll deine Passwort Karte haben? MAX: 26")
        number_of_rows = self.validate_input(1, 26)
        print("Wie viele Spalten soll deine Passwort Karte haben? MAX: 10")
        number_of_columns = self.validate_input(1, 10)

        return (number_of_rows, number_of_columns)

    def validate_choice(self, menu_choice):
        if menu_choice == MenuItem.SINGLE_CONSOLE.value:
            self.create_single()
        elif menu_choice == MenuItem.CARD_CONSOLE.value:
            self.create_card()
        elif menu_choice == MenuItem.IMAGE.value:
            pass
        else:
            print("Command not found")

    # vlt. Validate Klasse
    def validate_input(self, min_range_number, max_range_number):
        while True:
            try:
                response = int(input("-> "))
                if response > max_range_number:
                    raise OutOfRange
                break
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print("Please enter a number.")
            except OutOfRange:
                print("Please enter a value from "+ str(min_range_number) +"-"+ str(max_range_number) +".")

        return response

    def create_single(self):
        s = Single(10)
        s.console_single()

    def create_card(self):
        number_of_lines = self.card_line_choice()
        c = Card(number_of_lines[0],number_of_lines[1])
        c.console_card()

    def create_image(self):
        i = Image()


def exit():
    return sys.exit()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    c = CommandLine()
    c.menu()

if __name__ == '__main__':
    main()

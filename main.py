import random as rn
import string
from enum import Enum
import sys
import os
from PIL import Image, ImageDraw, ImageFont


class OutOfRange(Exception):
    pass


class Utils:
    def exit(self):
        return sys.exit()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")


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

    def data(self):
        p = Picker()
        # password = ""
        data = []
        password = []
        for i in range(self.length):
            # password += p.pick_random()
            password.append(p.pick_random())
        data.append(password)
        return data


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

    def data(self):
        data = []
        p = Picker()
        counter = 0
        self.list_of_ascii_uppercase.insert(0, "/")
        data.append(self.list_of_ascii_uppercase)
        for i in range(len(self.list_of_digits)):
            row = []
            for j in range(len(self.list_of_ascii_uppercase)-1):
                random_choice = p.pick_random()
                row.append(random_choice)
            row.insert(0, self.list_of_digits[counter])
            counter += 1
            data.append(row)
        counter = 0
        return data


class ImageMaker: # ImageMaker
    def __init__(self, data=[]):
        self.data = data
        self.image = self.make_image()
        self.remove_old_image()

    def get_size(self):
        row_length = len(self.data[0])
        column_length = len(self.data)

        row_size = 20 + (row_length*10)
        column_size = 20 + (column_length*10)
        return (row_size, column_size)

    def make_image(self):
        size = self.get_size()
        return Image.new("RGB", size, color="white") # (290, 130)

    def draw_text(self):
        d = ImageDraw.Draw(self.image)
        # font = ImageFont.truetype("arial.ttf", 15)

        counter_column = 10
        for i in self.data:
            counter_row = 10
            for j in i:
                d.text((counter_row, counter_column), j, (73, 109, 137)) # , font=font
                counter_row += 10
            counter_row = 10
            counter_column += 10

    def remove_old_image(self):
        image_path = "./password.png"
        if os.path.isfile(image_path):
            os.remove(image_path)

    def save_image(self):
        self.image.save("password.png")

class MenuTyp(Enum):
    SINGLE = 1
    CARD = 2

class MenuFormat(Enum):
    CONSOLE = 1
    IMAGE = 2

class MenuItem(Enum):
    SINGLE_CONSOLE = 1
    SINGLE_IMAGE = 2
    CARD_CONSOLE = 3
    CARD_IMAGE = 4 # 2


class Validate(Utils):
    def validate_menu(self, menu_typ, menu_format):
        if menu_typ == MenuTyp.SINGLE.value and menu_format == MenuFormat.CONSOLE.value:
            self.create_single_console()
        elif menu_typ == MenuTyp.SINGLE.value and menu_format == MenuFormat.IMAGE.value:
            self.create_single_image()
        elif menu_typ == MenuTyp.CARD.value and menu_format == MenuFormat.CONSOLE.value:
            self.create_card_console()
        elif menu_typ == MenuTyp.CARD.value and menu_format == MenuFormat.IMAGE.value:
            self.create_card_image()
        else:
            print("Command not found")

    def validate_input(self, min_range_number=1, max_range_number=1, range=True):
        while True:
            try:
                response = int(input("-> "))
                if range == True and response > max_range_number:
                    raise OutOfRange
                break
            except KeyboardInterrupt:
                self.exit()
            except ValueError:
                print("Please enter a number.")
            except OutOfRange:
                print("Please enter a value from "+ str(min_range_number) +"-"+ str(max_range_number) +".")

        return response


class CommandLine(Validate):
    def __init__(self):
        pass

    def menu(self):
        generate_type_choice = self.generate_type_choice()
        generate_format_choice = self.generate_format_choice()
        self.validate_menu(generate_type_choice, generate_format_choice)

    def generate_type_choice(self):
        self.clear()
        print("Please choose one of the following options by providing the respective number.")
        print("(1). Generate Single Line Password.")
        print("(2). Generate Password Card.")

        return self.validate_input(MenuTyp.SINGLE.value, MenuTyp.CARD.value)

    def generate_format_choice(self):
        print("Please choose one of the following options to specify the output type by providing the respective number.")
        print("(1). Output in Console.")
        print("(2). Output in Image.")

        return self.validate_input(MenuFormat.CONSOLE.value, MenuFormat.IMAGE.value)

    def card_line_choice(self):
        self.clear()
        print("How many rows should your password card consist of? MAX: 26")
        number_of_rows = self.validate_input(range=False)
        print("How many columns should your password card consist of? MAX: 10")
        number_of_columns = self.validate_input(range=False)

        return (number_of_rows, number_of_columns)

    def single_length_choice(self):
        self.clear()
        print("How long should your password be?")
        length = self.validate_input(range=False)

        return length

    def create_single_data(self):
        length = self.single_length_choice()
        s = Single(length)
        data = s.data()
        return data

    def create_single_console(self):
        data = self.create_single_data()
        password = "".join(data[0])
        self.clear()
        print("Your generated password is:" + "\n" + str(password))

    def create_single_image(self):
        data = self.create_single_data()
        i = ImageMaker(data=data)
        i.draw_text()
        i.save_image()

    def create_card_data(self):
        number_of_lines = self.card_line_choice()
        c = Card(number_of_lines[0],number_of_lines[1])
        data = c.data()
        return data

    def create_card_console(self):
        data = self.create_card_data()
        number_of_lines_horizontal = len(data[0])

        self.clear()
        self.draw_line_comsole(number_of_lines_horizontal)
        for i in data:
            row_string = " ".join(i)
            print(row_string)
        self.draw_line_comsole(number_of_lines_horizontal)

    def create_card_image(self):
        data = self.create_card_data()
        i = ImageMaker(data=data)
        i.draw_text()
        i.save_image()

    def draw_line_comsole(self, number_of_lines_horizontal):
        print("--"*int(number_of_lines_horizontal))


def main():
    c = CommandLine()
    c.menu()

if __name__ == '__main__':
    main()

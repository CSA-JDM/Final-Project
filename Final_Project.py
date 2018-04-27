# Jacob Meadows
# 4th Period, Computer Programming
# April 16th, 2018
"""
This will be taking place over the next few weeks, with minor reviews put in place at the end of each week.
You will also have to show me progress each week on the program.
You are welcome to use research, but I will not be able to answer very specific questions
(this is a review, I can't reteach you things you should already know).
I need a proposal from you in regards what you want to do with Python.
This will need to cover everything we have done this year (from simple printing to loops to classes and reading/writing
files).
Of course a common one is simple games, but ones that are useful in everyday life would be great too
(maybe terminal programs to reserve airplanes or rental cars, inventory/cash register, etc).
This proposal must be completed BEFORE class on Wednesday.
You can ask me ideas for what to do, you can ask each other as well.
Look online for ideas as well.
Proposal should be professional, slide show with examples.
Must be an in depth description of what you want to do, why, what it will do, and how it is a useful program.
It will also need a time line of what you will have done and when.
"""
import string
import turtle
import time
import random
import mp3play


class App:
    def __init__(self):
        self.screen = Screen(self)
        self.screen.main_window.tracer(False)
        self.screen.main_window.title("In Memoriam")
        self.screen.main_window.onkey(self.screen.main_window.bye, "Escape")

        sayo_nara = Audio(r'C:\Users\Jacob\Documents\GitHub\Final-Project\Sayo-nara.mp3')
        sayo_nara.play()
        self.screen.main_window.ontimer(sayo_nara.play, 157000)

        self.menu_state = None

        self.username_state = False
        self.username_ = None

        self.main_sequence_state = False
        self.main_sequence_text = None
        self.main_sequence_type = None

        self.main_loop()

        self.screen.main_window.listen()
        self.screen.main_window.update()
        self.screen.main_window.mainloop()

    def main_loop(self):
        self.screen.main_window.resetscreen()
        for turtle_ in self.screen.main_window.turtles():
            turtle_.hideturtle()
        if self.menu_state is not False:
            self.menu()
        if self.username_state is True:
            self.username()
        if self.main_sequence_state is True:
            self.main_sequence()
        self.current_time()
        self.screen.main_window.ontimer(self.main_loop, 500)

    def menu(self):
        if self.menu_state is None:
            title_text = self.screen.write(position=(10, 50), text="In Memoriam", font=("Times New Roman", 30, "bold"))
            self.screen.main_window.onclick(self.screen.check_pos_menu)

            new_game_button = Button(self, position=(10, 150), rect_sides=(130, 30, 130, 30), text="New Game")
            load_game_button = Button(self, position=(10, 225), rect_sides=(135, 30, 135, 30), text="Load Game")
            quit_button = Button(self, position=(10, 300), rect_sides=(60, 30, 60, 30), text="Quit")
            self.screen.buttons += [new_game_button, load_game_button, quit_button]

            self.screen.main_window_canvas.bind("<Motion>", self.screen.highlighter)
            self.menu_state = True
        elif self.menu_state is True:
            for button_ in self.screen.buttons:
                button_.update()
            title_text = self.screen.write(position=(10, 50), text="In Memoriam", font=("Times New Roman", 30, "bold"))

    def username(self):
        if self.username_state is False:
            self.username_ = TextInput(self.screen, (100, 50), (315, 30, 315, 30))
            self.menu_state = False
            self.username_state = True
        self.screen.write(position=(10, 48), text="Name:", font=("Times New Roman", 20, "normal"))
        self.username_.update()
        self.screen.main_window_canvas.unbind("<Motion>")
        self.screen.main_window.onkey(self.main_sequence, "Return")

    def main_sequence(self):
        if self.main_sequence_state is False:
            self.username_state = False
            self.username_.active = False
            self.main_sequence_text = TextBox(self.screen, (100, 500), (1000, 1000, 1000, 1000),
                                              f"Hello, {self.username_.type_string}, and welcome to 'In Memoriam.'")
            self.main_sequence_type = TextInput(self.screen, (100, 530), (1000, 30, 1000, 30))
            self.main_sequence_state = True
        self.main_sequence_text.update(self.main_sequence_type.type_string)
        self.main_sequence_type.update()

    def current_time(self):
        time_button = Button(self, position=(960, 710), rect_sides=(315, 30, 315, 30), text=time.asctime())

    def save(self):
        pass


class Screen:
    def __init__(self, app):
        self.app = app
        self.main_window = turtle.Screen()
        self.main_window_canvas = self.main_window.getcanvas()

        self.main_window.setup(1280, 720)
        self.main_window.setworldcoordinates(0, 720, 1280, 0)

        self.x = 0
        self.y = 0

        self.buttons = []

    def check_pos_menu(self, x, y):
        if 10 < x < 140 and 120 < y < 150:
            self.app.username()
            self.main_window.resetscreen()
            for turtle_ in self.main_window.turtles():
                turtle_.hideturtle()
        elif 10 < x < 70 and 270 < y < 300:
            self.app.screen.main_window.bye()

    @staticmethod
    def write(position=(0, 0), text="", font=("Times New Roman", 30, "normal"), color="black"):
        write_turtle = turtle.Turtle(visible=False)
        write_turtle.speed(0)
        write_turtle.up()
        write_turtle.color(color)
        write_turtle.up()
        write_turtle.goto(position)
        write_turtle.write(text, font=font, move=True)
        return write_turtle

    @staticmethod
    def draw_rect(position=(0, 0), sides=(0, 0, 0, 0), color="black", fill=False):
        write_turtle = turtle.Turtle(visible=False)
        write_turtle.speed(0)
        write_turtle.up()
        write_turtle.color(color)
        if fill is True:
            write_turtle.begin_fill()
        write_turtle.seth(0)
        write_turtle.up()
        write_turtle.goto(position[0], position[1]-5)
        write_turtle.down()
        for side in sides:
            write_turtle.forward(side)
            write_turtle.right(90)
        write_turtle.up()
        if write_turtle.filling():
            write_turtle.end_fill()
        return write_turtle

    def highlighter(self, event=None):
        if event is not None:
            self.x = event.x
            self.y = event.y
        for button in self.buttons:
            if button.position[0]*2 < self.x < (button.position[0]*2)+button.rect_sides[0] and \
                    (button.position[1]+5)-button.rect_sides[1] < self.y < button.position[1]+5:
                button.text_text.clear()
                self.draw_rect(position=(button.position[0]-5, button.position[1]+3), sides=button.rect_sides,
                               fill=True)
                self.write(position=button.position, text=button.text, font=button.font, color="white")
                button.highlighted = True
                break
            else:
                if button.highlighted is True:
                    self.main_window.resetscreen()
                    button.highlighted = False
                    self.app.menu()
                    break


class Button:
    def __init__(self, app, position=(0, 0), rect_sides=(0, 0, 0, 0), text="",
                 font=("Times New Roman", 20, "normal"), color="black"):
        self.app = app
        self.position = position
        self.rect_sides = rect_sides
        self.text = text
        self.font = font
        self.color = color
        self.highlighted = False

        self.text_text = self.app.screen.write(position=self.position, text=self.text, font=self.font, color=self.color)
        self.rect = self.app.screen.draw_rect(position=(self.position[0]-5, self.position[1]+3), sides=self.rect_sides)

    def update(self):
        if self.highlighted is True:
            self.app.screen.highlighter()
            self.app.current_time()
        else:
            self.text_text = self.app.screen.write(position=self.position, text=self.text, font=self.font,
                                                   color=self.color)
            self.rect = self.app.screen.draw_rect(position=(self.position[0] - 5, self.position[1] + 3),
                                                  sides=self.rect_sides)


class TextInput:
    def __init__(self, screen, position=(-5, 0), rect_sides=(0, 0, 0, 0)):
        self.screen = screen
        self.type_turtle = turtle.Turtle(visible=False)
        self.type_turtle.speed(0)
        self.type_turtle.up()

        self.type_string = ""
        self.orig_position = position
        self.rect_sides = rect_sides
        self.pos = position[0]+2, position[1]-3
        self.active = True

        self.rect_ = self.screen.draw_rect(position=(self.orig_position[0]-5, self.orig_position[1]+3),
                                           sides=self.rect_sides)

        for letter in (f"{string.ascii_letters}{string.digits}" + "!@#$%^&*()_+?><:|[];',./\\{}=" + '"'):
            self.screen.main_window.onkey(
                lambda letter_=letter: self.add_string(letter_, font=("Times New Roman", 20, "normal")), letter
            )
        self.screen.main_window.onkey(
            lambda space="space": self.add_string(" ", font=("Times New Roman", 20, "normal")), "space"
        )
        self.screen.main_window.onkey(
            lambda minus="minus": self.add_string("-", font=("Times New Roman", 20, "normal")), "minus"
        )
        self.screen.main_window.onkey(self.delete_string, "BackSpace")

        self.selector_state = False
        self.selector()

    def add_string(self, text="", font=("Times New Roman", 20, "normal")):
        if self.active is True:
            self.type_string += text
            self.type_turtle.goto(self.pos)
            self.type_turtle.clear()
            self.type_turtle.write(self.type_string, font=font, move=True)

    def delete_string(self, font=("Times New Roman", 20, "normal")):
        if self.active is True:
            self.type_string = self.type_string[:-1]
            self.type_turtle.goto(self.pos)
            self.type_turtle.clear()
            self.type_turtle.write(self.type_string, font=font, move=True)

    def update(self, font=("Times New Roman", 20, "normal")):
        self.type_turtle.goto(self.pos)
        self.type_turtle.clear()
        self.type_turtle.write(self.type_string, font=font, move=True)
        self.screen.draw_rect(position=(self.orig_position[0]-5, self.orig_position[1]+3), sides=self.rect_sides)

    def selector(self):
        if self.active is True:
            if self.selector_state is False:
                self.type_turtle.goto(self.pos)
                self.type_turtle.clear()
                self.type_turtle.write(self.type_string+"|", font=("Times New Roman", 20, "normal"), move=True)
                self.selector_state = True
            elif self.selector_state is True:
                self.type_turtle.goto(self.pos)
                self.type_turtle.clear()
                self.type_turtle.write(self.type_string, font=("Times New Roman", 20, "normal"), move=True)
                self.selector_state = False
            self.screen.main_window.ontimer(self.selector, 500)


class TextBox:
    def __init__(self, screen, position=(-5, 0), rect_sides=(0, 0, 0, 0), text="",
                 font=("Times New Roman", 20, "normal"), color="black"):
        self.screen = screen
        self.position = position
        self.rect_sides = rect_sides
        self.text = text
        self.font = font
        self.color = color

        self.text_text = self.screen.write(position=(self.position[0]+2, self.position[1]-3), text=self.text,
                                           font=self.font, color=self.color)
        self.rect = self.screen.draw_rect(position=(position[0] - 5, position[1] + 3), sides=self.rect_sides)

    def update(self, text):
        self.text += f"\n{text}"
        self.text_text = self.screen.write(position=(self.position[0]+2, self.position[1]-3), text=self.text,
                                           font=self.font, color=self.color)
        self.rect = self.screen.draw_rect(position=(self.position[0] - 5, self.position[1] + 3), sides=self.rect_sides)


class Character:
    def __init__(self):
        self.character = turtle.Turtle()


class Item:
    def __init__(self):
        pass


class Area:
    def __init__(self, screen):
        self.screen = screen
        self.draw_turtle = turtle.Turtle(visible=False)
        self.draw_turtle.up()

    def draw_tree(self, position=(0, 0)):
        self.draw_turtle.down()
        self.screen.draw_rect(position=position, sides=(20, 60, 20, 60), color="brown", fill=True)
        self.draw_turtle.up()
        self.draw_turtle.seth(90)
        self.draw_turtle.goto(position[0], position[1]+30)
        self.draw_turtle.down()
        self.draw_turtle.begin_fill()
        self.draw_turtle.color("green")
        # Not done with this part.
        self.draw_turtle.end_fill()


class Audio:
    def __init__(self, file):
        self.file = mp3play.load(file)

    def play(self):
        self.file.play()


if __name__ == "__main__":
    session = App()
    session.save()

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
import ctypes
import turtle
import time
import random


class App:
    def __init__(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        self.screen = Screen(self)
        self.screen.main_window.screensize(screensize[0], screensize[1])
        self.screen.main_window.tracer(0, 0)
        self.screen.main_window.title("In Memoriam")
        self.screen.main_window.onkey(self.screen.main_window.bye, "Escape")

        self.menu()

        self.screen.main_window.listen()
        self.screen.main_window.update()
        self.screen.write_turtle.showturtle()
        self.screen.main_window.mainloop()

    def menu(self):
        self.screen.write(position=(-380, 280), text="In Memoriam", font=("Times New Roman", 30, "bold"))
        self.screen.main_window.onclick(self.screen.check_pos_menu)

        new_game_button = Button(self, position=(-380, 200), rect_sides=(130, 30, 130, 30), text="New Game")
        load_game_button = Button(self, position=(-380, 150), rect_sides=(135, 30, 135, 30), text="Load Game")
        quit_button = Button(self, position=(-380, 100), rect_sides=(60, 30, 60, 30), text="Quit")
        buttons = [new_game_button, load_game_button, quit_button]

        for button in buttons:
            self.screen.main_window_canvas.bind("<Motion>", button.highlighter)

    def save(self):
        pass


class Screen:
    def __init__(self, app):
        self.app = app
        self.main_window = turtle.Screen()
        self.main_window_canvas = self.main_window.getcanvas()

        self.write_turtle = turtle.Turtle()
        self.write_turtle.hideturtle()
        self.write_turtle.speed(0)
        self.write_turtle.up()

    def check_pos_menu(self, x, y):
        if -380 < x < -255 and 200 < y < 230:
            self.main_window.reset()
            self.write(position=(-380, 280), text="Name:", font=("Times New Roman", 20, "normal"))
            TextBox(self, (-300, 280), (400, 30, 400, 30))
            self.main_window_canvas.unbind("<Motion>")

    def write(self, position=(0, 0), text="", font=("Times New Roman", 30, "normal"), color="black"):
        self.write_turtle.color(color)
        self.write_turtle.up()
        self.write_turtle.goto(position)
        self.write_turtle.write(text, font=font, move=True)

    def draw_rect(self, position=(0, 0), sides=(0, 0, 0, 0), color="black", fill=False):
        self.write_turtle.color(color)
        if fill is True:
            self.write_turtle.begin_fill()
        self.write_turtle.seth(0)
        self.write_turtle.up()
        self.write_turtle.goto(position[0], position[1]+30)
        self.write_turtle.down()
        for side in sides:
            self.write_turtle.forward(side)
            self.write_turtle.right(90)
        self.write_turtle.up()
        if self.write_turtle.filling():
            self.write_turtle.end_fill()


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

        self.app.screen.write(position=self.position, text=self.text, font=self.font, color=self.color)
        self.app.screen.draw_rect(position=(position[0] - 5, position[1]), sides=self.rect_sides)

    def highlighter(self, event):
        if self.position[0]+388 < event.x < self.position[0]+388+self.rect_sides[0] and \
                self.position[1]+100 < event.y < self.position[1]+100+self.rect_sides[1]:
            self.app.screen.draw_rect(position=(self.position[0]-5, self.position[1]), sides=self.rect_sides, fill=True)
            self.app.screen.write(position=self.position, text=self.text, font=self.font, color="white")
            self.highlighted = True
        else:
            if self.highlighted is True:
                self.app.screen.write_turtle.clear()
                self.app.menu()
                self.highlighted = False


class TextBox:
    def __init__(self, screen, position=(-5, 0), rect_sides=(0, 0, 0, 0)):
        self.screen = screen
        self.type_turtle = turtle.Turtle()
        self.type_turtle.hideturtle()
        self.type_turtle.speed(0)
        self.type_turtle.up()

        self.screen.draw_rect(position=position, sides=rect_sides)

        self.type_string = ""
        self.pos = position[0]+5, position[1]

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
        self.type_string += text
        self.type_turtle.goto(self.pos)
        self.type_turtle.clear()
        self.type_turtle.write(self.type_string, font=font, move=True)

    def delete_string(self):
        self.type_string = self.type_string[:-1]
        self.type_turtle.goto(self.pos)
        self.type_turtle.clear()
        self.type_turtle.write(self.type_string, font=("Times New Roman", 20, "normal"), move=True)

    def selector(self):
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


class Character:
    def __init__(self):
        self.character = turtle.Turtle()


class Item:
    def __init__(self):
        pass


class Area:
    def __init__(self, screen):
        self.screen = screen
        self.draw_turtle = turtle.Turtle()
        self.draw_turtle.hideturtle()
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
    def __init__(self):
        pass


session = App()
session.save()

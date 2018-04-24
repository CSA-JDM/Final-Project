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

PERSONAL NOTE: Mr. Davis said he wasn't expecting nor wanting visuals (that helps a lot).

"""
import string
import turtle
import time
import random


class App:
    def __init__(self):
        self.screen = Screen(self)
        self.screen.main_window.tracer(0, 0)
        self.screen.main_window.title("In Memoriam")
        self.screen.main_window.onkey(self.screen.main_window.bye, "Escape")

        self.menu()
        self.current_time()

        self.screen.main_window.listen()
        self.screen.main_window.update()
        self.screen.main_window.mainloop()

    def menu(self):
        self.screen.write(position=(10, 100), text="In Memoriam", font=("Times New Roman", 30, "bold"))
        self.screen.main_window.onclick(self.screen.check_pos_menu)

        new_game_button = Button(self, position=(10, 200), rect_sides=(75, 50, 75, 50), text="New Game")
        load_game_button = Button(self, position=(10, 300), rect_sides=(80, 50, 80, 50), text="Load Game")
        quit_button = Button(self, position=(10, 400), rect_sides=(40, 50, 40, 50), text="Quit")
        self.screen.buttons += [new_game_button, load_game_button, quit_button]

        self.screen.main_window_canvas.bind("<Motion>", self.screen.highlighter)

    def current_time(self):
        full_time = time.asctime()
        time_button = Button(self, position=(500, 1000), rect_sides=(180, 50, 180, 50), text=full_time)

    def save(self):
        pass


class Screen:
    def __init__(self, app):
        self.app = app
        self.main_window = turtle.Screen()
        self.main_window_canvas = self.main_window.getcanvas()

        self.main_window.setup(1280, 720)
        self.main_window.setworldcoordinates(0, 1280, 720, 0)

        self.write_turtle = turtle.Turtle()
        self.write_turtle.hideturtle()
        self.write_turtle.speed(0)
        self.write_turtle.up()
        self.buttons = []

    def check_pos_menu(self, x, y):
        print(x, y)
        if 5 < x < 80 and 145 < y < 195:
            self.main_window.reset()
            self.write(position=(10, 95), text="Name:", font=("Times New Roman", 20, "normal"))
            TextBox(self, (60, 100), (300, 55, 300, 55))
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
        self.write_turtle.goto(position[0], position[1]-5)
        self.write_turtle.down()
        for side in sides:
            self.write_turtle.forward(side)
            self.write_turtle.right(90)
        self.write_turtle.up()
        if self.write_turtle.filling():
            self.write_turtle.end_fill()

    def highlighter(self, event):
        for button in self.buttons:
            if button.position[0]+10 < event.x < (button.position[0]+button.rect_sides[0]) and \
                    button.position[1]/2 < event.y < (button.position[1]+button.rect_sides[1])/2:
                print(event.x, event.y)
                print(button.position)
                self.draw_rect(position=(button.position[0]-5, button.position[1]), sides=button.rect_sides, fill=True)
                self.write(position=button.position, text=button.text, font=button.font, color="white")
                button.highlighted = True
                break
            else:
                if button.highlighted is True:
                    self.write_turtle.clear()
                    self.app.menu()
                    button.highlighted = False


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
        self.app.screen.draw_rect(position=(position[0]-5, position[1]), sides=self.rect_sides)


class TextBox:
    def __init__(self, screen, position=(-5, 0), rect_sides=(0, 0, 0, 0)):
        self.screen = screen
        self.type_turtle = turtle.Turtle()
        self.type_turtle.hideturtle()
        self.type_turtle.speed(0)
        self.type_turtle.up()

        self.screen.draw_rect(position=position, sides=rect_sides)

        self.type_string = ""
        self.pos = position[0]+5, position[1]-5

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

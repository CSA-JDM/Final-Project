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
        self.screen = Screen(self, "In Memoriam")
        self.start_time = time.time()
        self.frame_counter = 0

        sayo_nara = Audio(r'C:\Users\Jacob\Documents\GitHub\Final-Project\Sayo-nara.mp3')
        sayo_nara.play()
        self.screen.main_window.ontimer(sayo_nara.play, 157000)

        self.menu()
        self.main_loop()

        self.screen.main_window.listen()
        self.screen.main_window.mainloop()

    def main_loop(self, loop=True):
        self.frame_counter += 1
        # self.screen.main_window_canvas.delete("all")
        refresher = self.screen.main_window_canvas.create_rectangle(0, 0, 1280, 720, width=0, fill="white")
        # turtles = self.screen.main_window.turtles()
        # for _ in range(len(turtles)):
        #    turtles[0].clear()
        #    del turtles[0]
        for button_ in self.screen.buttons:
            button_.update()
        for text_box_ in self.screen.text_boxes:
            text_box_.update()
        for text_input_ in self.screen.text_inputs:
            self.screen.text_inputs[text_input_].update()
        self.current_time()
        print(round(self.frame_counter/(time.time()-self.start_time)))
        items = self.screen.main_window_canvas.find_all()
        for item in items[:items.index(refresher)+1]:
            self.screen.main_window_canvas.delete(item)
        if loop is True:
            self.screen.main_window.ontimer(self.main_loop, 1)

    def menu(self):
        self.screen.clear_all()
        self.screen.text_boxes += [TextBox(self.screen, position=(10, 50), text="In Memoriam",
                                           font=("Times New Roman", 30, "bold"))]

        self.screen.buttons += [Button(self, position=(10, 150), rect_sides=(130, 30, 130, 30), text="New Game")]
        self.screen.buttons += [Button(self, position=(10, 225), rect_sides=(135, 30, 135, 30), text="Load Game")]
        self.screen.buttons += [Button(self, position=(10, 300), rect_sides=(60, 30, 60, 30), text="Quit")]

        self.screen.main_window.onclick(lambda x, y: self.screen.check_pos(x, y, ((10, 140), (120, 150)),
                                                                           self.new_game))
        self.screen.main_window.onclick(lambda x, y: self.screen.check_pos(x, y, ((10, 145), (195, 225)),
                                                                           self.load_game), add=True)
        self.screen.main_window.onclick(lambda x, y: self.screen.check_pos(x, y, ((10, 70), (270, 300)),
                                                                           self.screen.main_window.bye), add=True)
        self.screen.main_window_canvas.bind("<Motion>", self.screen.highlighter)

    def username(self):
        self.screen.text_inputs["username"] = TextInput(self.screen, (100, 52), (315, 30, 315, 30))
        self.screen.text_boxes += [TextBox(self.screen, position=(10, 50), text="Name:",
                                           font=("Times New Roman", 20, "normal"))]
        self.screen.buttons += [Button(self, position=(960, 650), rect_sides=(135, 30, 135, 30), text="Load Game")]
        self.screen.buttons += [Button(self, position=(1100, 650), rect_sides=(60, 30, 60, 30), text="Quit")]

        self.screen.main_window.onclick(lambda x, y: self.screen.check_pos(x, y, ((960, 1095), (620, 650)),
                                                                           self.load_game))
        self.screen.main_window.onclick(lambda x, y: self.screen.check_pos(x, y, ((1100, 1170), (620, 650)),
                                                                           self.screen.main_window.bye))

        self.screen.main_window.onkey(self.main_sequence, "Return")

    def main_sequence(self):
        self.screen.main_window.onkey(None, "Return")
        username = self.screen.text_inputs["username"].type_string
        self.screen.text_inputs["username"].active = False
        self.screen.clear_all()
        self.screen.buttons += [Button(self, position=(960, 650), rect_sides=(135, 30, 135, 30), text="Load Game")]
        self.screen.buttons += [Button(self, position=(1100, 650), rect_sides=(60, 30, 60, 30), text="Quit")]
        self.screen.text_boxes += [TextBox(self.screen, (100, 550), (1000, 500, 1000, 500),
                                           f'Hello, {username}, '
                                           'and welcome to "In Memoriam."')]
        self.screen.text_inputs["user input"] = TextInput(self.screen, (100, 580), (1000, 30, 1000, 30))

    def current_time(self):
        TextBox(self.screen, position=(960, 710), rect_sides=(310, 30, 310, 30), text=time.asctime())

    def new_game(self):
        self.screen.clear_all()
        self.username()
        self.screen.main_window.resetscreen()
        for turtle_ in self.screen.main_window.turtles():
            turtle_.hideturtle()

    def load_game(self):
        pass

    def save(self):
        pass


class Screen:
    def __init__(self, app, title):
        self.app = app
        self.main_window = turtle.Screen()
        self.main_window_canvas = self.main_window.getcanvas()

        self.main_window.setup(1280, 720, starty=40)
        self.main_window.setworldcoordinates(0, 720, 1280, 0)
        self.main_window.tracer(False)
        self.main_window.title(title)
        self.main_window.onkey(self.main_window.bye, "Escape")

        self.x = 0
        self.y = 0

        self.buttons = []
        self.text_boxes = []
        self.text_inputs = {}

    def highlighter(self, event=None):
        if event is not None:
            self.x = event.x
            self.y = event.y
        for button in self.buttons:
            if button.position[0] < self.x < button.position[0]+button.rect_sides[0] and \
                    button.position[1]-button.rect_sides[1] < self.y < button.position[1]:
                button.text_text.clear()
                button.rect.clear()
                button.text_text = self.draw_rect(position=(button.position[0]-5, button.position[1]+3),
                                                  sides=button.rect_sides, fill=True)
                button.rect = self.write(position=button.position, text=button.text, font=button.font, color="white")
                button.highlighted = True
                break
            else:
                if button.highlighted is True:
                    self.main_window.resetscreen()
                    button.highlighted = False
                    break

    def clear_all(self):
        turtles = self.main_window.turtles()
        for _ in range(len(turtles)):
            turtles[0].clear()
            del turtles[0]
        self.buttons = []
        self.text_boxes = []
        self.text_inputs = {}

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

    @staticmethod
    def check_pos(x, y, cords, func):
        if cords[0][0] < x < cords[0][1] and cords[1][0] < y < cords[1][1]:
            func()


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

    def update(self):
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

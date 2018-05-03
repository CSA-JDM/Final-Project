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
        # Screen
        self.screen = Screen(self, "In Memoriam")

        # Audio
        # sayo_nara = Audio(r'C:\Users\Jacob\Documents\GitHub\Final-Project\Sayo-nara.mp3')
        # sayo_nara.play()
        # self.screen.main_window.ontimer(sayo_nara.play, 157000)

        # Initial Time Update
        self.time_label = None
        self.time_update()

        # Main Loop
        self.frame_counter = 0
        self.start_time = time.time()

        self.loop = Status()
        self.menu = Status()
        self.username = Status()
        self.main_sequence = Status()

        # Initial Frame Update
        self.frame_box = TextBox(self.screen, position=(1195, 30), rect_sides=(75, 35, 75, 35), text="0")

        self.buttons = {}
        self.text_boxes = {}
        self.text_inputs = {}

        while self.loop.state:
            self.frame_counter += 1
            self.current_time()
            # Menu portion
            if self.menu.deployed is False:
                self.menu_()
            # Username portion
            if self.menu.state is False:
                if self.username.deployed is False:
                    self.time_update()
                    self.username_()
                # Main sequence portion
                if self.username.state is False:
                    if self.main_sequence.deployed is False:
                        self.time_update()
                        self.main_sequence_()

            if f"{round(self.frame_counter/(time.time()-self.start_time))}" != self.frame_box.text:
                self.screen.main_window_canvas.delete(self.frame_box.text_text_item)
                self.screen.main_window_canvas.delete(self.frame_box.rect_item)
                self.frame_box = TextBox(self.screen, position=(1195, 30),
                                         rect_sides=(75, 35, 75, 35),
                                         text=f"{round(self.frame_counter/(time.time()-self.start_time))}")

            self.screen.main_window.listen()
            self.screen.main_window.update()

    def time_update(self):
        ltime = time.localtime()
        year, month, day, hour, minute, second = ltime[:6]
        self.time_label = TextBox(self.screen, position=(1130, 710),
                                  rect_sides=(140, 65, 140, 65), text=f"  {hour}:{minute}:{second}\n"
                                                                      f"{month}/{day}/{year}")

    def current_time(self):
        the_time = time.localtime()
        time_str = list(the_time[:6])
        for msrmnt in range(len(time_str)):
            if len(str(time_str[msrmnt])) < 2:
                time_str.insert(msrmnt+1, "0" + str(time_str[msrmnt]))
                del time_str[msrmnt]
        if f"  {time_str[3]}:{time_str[4]}:{time_str[5]}\n{time_str[1]}/{time_str[2]}/{time_str[0]}" !=\
                self.time_label.text:
            # print(self.screen.main_window_canvas.find_all())
            self.screen.main_window_canvas.delete(self.time_label.text_text_item)
            self.screen.main_window_canvas.delete(self.time_label.rect_item)
            # print(self.screen.main_window_canvas.find_all())
            self.time_label.text_text.clear()
            total_turtles = self.screen.main_window.turtles()
            del [total_turtles[total_turtles.index(self.time_label.rect)],
                 total_turtles[total_turtles.index(self.time_label.text_text)]]
            self.time_label = TextBox(self.screen, position=(1130, 710),
                                      rect_sides=(140, 65, 140, 65),
                                      text=f"  {time_str[3]}:{time_str[4]}:{time_str[5]}\n"
                                           f"{time_str[1]}/{time_str[2]}/{time_str[0]}")

    def menu_(self):
        TextBox(self.screen, position=(10, 50), text="In Memoriam", font=("Times New Roman", 30, "bold"))

        self.buttons["new_button"] = Button(self, position=(10, 150), rect_sides=(130, 30, 130, 30),
                                            text="New Game")
        self.buttons["load_button"] = Button(self, position=(10, 225), rect_sides=(135, 30, 135, 30),
                                             text="Load Game")
        self.buttons["quit_button"] = Button(self, position=(10, 300), rect_sides=(60, 30, 60, 30),
                                             text="Quit")

        self.screen.main_window.onclick(
            lambda x, y:
            [
                self.screen.check_pos(x, y, ((10, 140), (120, 150)), lambda: setattr(self.menu, "state", False)),
                self.screen.check_pos(x, y, ((10, 145), (195, 225)), self.load_game),
                self.screen.check_pos(x, y, ((10, 70), (270, 300)), lambda: setattr(self.loop, "state", False))
            ]
        )
        self.screen.main_window_canvas.bind("<Motion>", lambda event: self.screen.highlighter(
            buttons=(self.buttons.items()), event=event))
        setattr(self.menu, "deployed", True)

    def username_(self):
        self.screen.main_window_canvas.delete("all")
        total_turtles = self.screen.main_window.turtles()
        del [total_turtles[total_turtles.index(self.buttons["new_button"].rect)],
             total_turtles[total_turtles.index(self.buttons["new_button"].text_text)]]
        del self.buttons["new_button"]

        self.text_boxes["name_label"] = TextBox(self.screen, position=(10, 50), text="Name:",
                                                font=("Times New Roman", 20, "normal"))
        self.text_inputs["username_input"] = TextInput(self.screen, (100, 52), (315, 30, 315, 30))
        self.buttons["load_button"].move_to((915, 710))
        self.buttons["quit_button"].move_to((1060, 710))
        self.screen.main_window_canvas.bind("<Motion>", lambda event: self.screen.highlighter(
            buttons=(self.buttons.items()), event=event), add=False)
        self.screen.main_window.onclick(
            lambda x, y:
            [
                self.screen.check_pos(x, y, ((915, 1050), (680, 710)), self.load_game),
                self.screen.check_pos(x, y, ((1060, 1120), (680, 710)),
                                      lambda: setattr(self.loop, "state", False))
            ],
            add=False
        )
        self.screen.main_window.onkey(lambda: setattr(self.username, "state", False), "Return")
        setattr(self.username, "deployed", True)

    def main_sequence_(self):
        self.screen.main_window_canvas.delete("all")
        self.buttons["load_button"].update()
        self.buttons["quit_button"].update()
        self.screen.main_window.onkey(None, "Return")
        inputted_username = self.text_inputs["username_input"].type_string
        setattr(self.text_inputs["username_input"], "active", False)
        self.text_boxes["main_textbox"] = TextBox(self.screen, (20, 550), (1000, 500, 1000, 500),
                                                  f'Hello, {inputted_username}, and welcome to "In Memoriam."')
        self.text_boxes["speaker"] = TextBox(self.screen, (20, 85), (1000, 35, 1000, 35), "Speaker: ")
        main_input = TextInput(self.screen, (20, 580), (1000, 30, 1000, 30))
        TextBox(self.screen, position=(1030, 580),
                rect_sides=(240, 530, 240, 530), text="Health: 100/100\n"
                                                      "Stamina: 100/100\n"
                                                      "Mana: 20/20\n\n"
                                                      "Inventory:\n"
                                                      "Nothing...\n\n\n\n\n\n\n\n\n\n")
        self.screen.main_window.onkey(
            lambda: [
                self.text_boxes["main_textbox"].update(main_input.type_string),
                main_input.clear()
            ],
            "Return")
        setattr(self.main_sequence, "deployed", True)

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
        self.main_window.tracer(0, 0)
        self.main_window.title(title)
        self.main_window.onkey(self.main_window.bye, "Escape")

    @staticmethod
    def highlighter(buttons, event):
        for button in buttons:
            button = button[1]
            if button.position[0] < event.x < button.position[0]+button.rect_sides[0] and \
                    button.position[1]-button.rect_sides[1] < event.y < button.position[1]:
                if button.highlighted is False:
                    button.update(fill=True, color="white")
                    setattr(button, "highlighted", True)
            else:
                if button.highlighted is True:
                    button.update()
                    setattr(button, "highlighted", False)

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

    def update(self, fill=False, color="black"):
        self.text_text.clear()
        self.rect.clear()
        setattr(self, "rect", self.app.screen.draw_rect(position=(self.position[0] - 5,
                                                                  self.position[1] + 3),
                                                        sides=self.rect_sides, fill=fill))
        setattr(self, "text_text", self.app.screen.write(position=self.position, text=self.text,
                                                         font=self.font, color=color))

    def move_to(self, position):
        self.position = position
        self.update()


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
        self.rect_item = self.screen.main_window_canvas.find_all()[-1]

        for letter in (f"{string.ascii_letters}{string.digits}" + "!@#$%^&*()_+?><:|[];',./\\{}=" + '"'):
            self.screen.main_window.onkeypress(
                lambda letter_=letter: self.add_string(letter_, font=("Times New Roman", 20, "normal")), letter
            )
        self.screen.main_window.onkeypress(
            lambda space="space": self.add_string(" ", font=("Times New Roman", 20, "normal")), "space"
        )
        self.screen.main_window.onkeypress(
            lambda minus="minus": self.add_string("-", font=("Times New Roman", 20, "normal")), "minus"
        )
        self.screen.main_window.onkeypress(self.delete_string, "BackSpace")

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

    def clear(self):
        self.type_string = ""

    def selector(self):
        if self.active is True:
            if self.selector_state is True:
                self.type_turtle.goto(self.pos)
                self.type_turtle.clear()
                self.type_turtle.write(self.type_string+"|", font=("Times New Roman", 20, "normal"), move=True)
                self.selector_state = False
            elif self.selector_state is False:
                self.type_turtle.goto(self.pos)
                self.type_turtle.clear()
                self.type_turtle.write(self.type_string, font=("Times New Roman", 20, "normal"), move=True)
                self.selector_state = True
            self.screen.main_window.ontimer(self.selector, 500)

    def move_to(self, position):
        self.orig_position = position
        self.pos = position[0] + 2, position[1] - 3


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
        self.text_text_item = self.screen.main_window_canvas.find_all()[-1]
        self.rect = self.screen.draw_rect(position=(position[0] - 5, position[1] + 3), sides=self.rect_sides)
        self.rect_item = self.screen.main_window_canvas.find_all()[-1]

    def update(self, new_text=""):
        if new_text != "":
            self.text += f"\n{new_text}"
        self.text_text.clear()
        self.rect.clear()
        self.text_text = self.screen.write(position=(self.position[0]+2, self.position[1]-3), text=self.text,
                                           font=self.font, color=self.color)
        self.rect = self.screen.draw_rect(position=(self.position[0] - 5, self.position[1] + 3), sides=self.rect_sides)

    def move_to(self, position):
        self.position = position


class Status:
    def __init__(self):
        self.state = True
        self.deployed = False


class Character:
    def __init__(self, name, health, stamina, mana):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.mana = mana


class Item:
    def __init__(self):
        pass


class Area:
    def __init__(self, screen):
        self.screen = screen
        self.draw_turtle = turtle.Turtle(visible=False)
        self.draw_turtle.up()


class Audio:
    def __init__(self, file):
        self.file = mp3play.load(file)

    def play(self):
        self.file.play()


if __name__ == "__main__":
    session = App()
    session.save()

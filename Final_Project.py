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
import turtle
import time
import string
import mp3play


class App:
    def __init__(self):
        # Root Initialization
        self.root = turtle._Root()
        self.root.config(width=1280, height=720)
        self.root.bind("<Escape>", lambda args: self.root.destroy())
        self.root.title("In Memoriam")

        # Canvas Initialization
        self.canvas = turtle.Canvas(self.root)
        self.canvas.config(width=1280, height=720)
        self.canvas.place(x=0, y=0)

        # Audio Initialization
        #   sayo_nara = Audio(self.root, r"..\Final-Project\Sayo-nara.mp3")
        #   sayo_nara.play(loop=True)

        # Item Dictionaries
        self.buttons = {
            "Main Sequence": {
                "Menu": {
                    "new_game_button": Button(self.canvas, x=10, y=110, length=130, height=35,
                                              text="New Game",
                                              command=self.username),
                    "load_game_button": Button(self.canvas, x=10, y=185, length=135, height=35, text="Load Game",
                                               command=None),
                    "quit_button": Button(self.canvas, x=10, y=260, length=60, height=35, text="Quit",
                                          command=self.root.destroy)
                }
            },
            "Fight Sequence": {

            }
        }
        self.text_boxes = {
            "Main Sequence": {
                "Menu": {
                    "title_text_box": TextBox(self.canvas, x=10, y=10, text="In Memoriam",
                                              font=("Times New Roman", 30, "bold"))
                },
                "Time": {
                    "time_text_box": TextBox(
                        self.canvas, x=1170, y=650, length=110, height=65,
                        text=f"{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}\n"
                             f"{time.localtime()[1]}/{time.localtime()[2]}/{time.localtime()[0]}"
                    )
                }
            },
            "Fight Sequence": {

            }
        }
        self.text_inputs = {
            "Main Sequence": {

            },
            "Fight Sequence": {

            }
        }

        # Main Sequence
        self.time_update()
        self.root.mainloop()

    def time_update(self):
        current_time = list(time.localtime()[:6])
        if len(str(current_time[3])) < 2:
            current_time[3] = "0" + str(current_time[3])
        if len(str(current_time[4])) < 2:
            current_time[4] = "0" + str(current_time[4])
        if len(str(current_time[5])) < 2:
            current_time[5] = "0" + str(current_time[5])
        self.text_boxes["Main Sequence"]["Time"]["time_text_box"].update(
            text=f"{current_time[3]}:{current_time[4]}:{current_time[5]}\n"
                 f"{current_time[1]}/{current_time[2]}/{current_time[0]}"
        )
        self.root.after(1, self.time_update)

    def username(self):
        self.clear_all()
        self.buttons["Main Sequence"]["Username Input"] = {
            "back_button": Button(self.canvas, x=10, y=680, length=65, height=35, text="Back",
                                  command=None),
            "load_game_button": self.buttons["Main Sequence"]["Menu"]["load_game_button"].update(x=950, y=680),
            "quit_button": self.buttons["Main Sequence"]["Menu"]["quit_button"].update(x=1095, y=680)
        }
        self.text_boxes["Main Sequence"]["Username Input"] = {
            "username_text_box": TextBox(self.canvas, x=10, y=30, text="Username:")
        }
        self.text_inputs["Main Sequence"]["Username Input"] = {
            "username_text_input": TextInput(
                self.canvas, x=145, y=30, length=500, height=35, command=lambda event: [
                    self.main_sequence(),
                    setattr(self.text_inputs["Main Sequence"]["Username Input"]["username_text_input"], "active", False)
                ]
            )
        }

    def main_sequence(self):
        self.clear_all()
        main_portion = MainSequence(
            self.canvas, 10, 10,
            self.text_inputs["Main Sequence"]["Username Input"]['username_text_input'].text,
            self.buttons, self.text_boxes, self.text_inputs
        )

    def clear_all(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind_all("<Key>")
        self.canvas.unbind_all("<Return>")

    def save(self):
        pass


class CanvasObject:
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, command=None, tags=None):
        self.canvas = canvas
        self.x = x - 5
        self.y = y
        self.length = length
        self.height = height
        self.text = text
        self.font = font
        self.width = width
        self.command = command
        self.tags = tags
        self.text_item = self.write(tags=self.tags)
        if length > 0 and height > 0:
            self.rect_item = self.make_rect(tags=self.tags)
        else:
            self.rect_item = 0

    def update(self, x=None, y=None, length=None, height=None, text=None, add=False):
        if text is not None:
            if add:
                self.text += f"\n{text}"
            elif not add:
                self.text = text
        if length is not None:
            self.length = length
        if height is not None:
            self.height = height
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.canvas.delete(self.text_item)
        self.canvas.delete(self.rect_item)
        self.text_item = self.write(tags=self.tags)
        self.rect_item = self.make_rect(tags=self.tags)

    def make_rect(self, fill=None, tags=None):
        return self.canvas.create_rectangle(self.x, self.y, self.x + self.length, self.y + self.height,
                                            fill=fill, tags=tags)

    def make_line(self, x1, y1, x2, y2, fill="black", tags=None):
        return self.canvas.create_line(x1, y1, x2, y2, width=20, fill=fill, tags=tags)

    def write(self, text=None, fill="black", tags=None):
        if text is None:
            text = self.text
        if self.length > 0 and self.height > 0:
            return self.canvas.create_text(self.x+5, self.y+3, text=text,
                                           anchor="nw", font=self.font, width=self.length,
                                           fill=fill, tags=tags)
        else:
            return self.canvas.create_text(self.x + 5, self.y + 3, text=text,
                                           anchor="nw", font=self.font, width=self.width, fill=fill,
                                           tags=tags)

    def check_pos(self, func, event):
        if self.x < event.x < self.x+self.length and self.y < event.y < self.y+self.height:
            func()


class Button(CanvasObject):
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, command=None, tags=None):
        super().__init__(canvas, x=x, y=y, length=length, height=height, text=text, font=font, width=width,
                         command=command, tags=tags)
        self.canvas.bind("<Motion>", self.highlighter, add=True)
        if self.command is not None:
            self.canvas.bind("<Button-1>", lambda event: self.check_pos(self.command, event), add=True)
        self.highlighted = False

    def update(self, x=None, y=None, length=None, height=None, text=None, add=False):
        super().update(x, y, length, height, text, add)
        self.canvas.bind("<Motion>", self.highlighter, add=True)
        if self.command is not None:
            self.canvas.bind("<Button-1>", lambda event: self.check_pos(self.command, event), add=True)
        self.highlighted = False

    def highlighter(self, event):
        if self.x-5 < event.x < self.x-5+self.length and self.y-3 < event.y < self.y-3+self.height:
            self.canvas.delete(self.text_item)
            self.canvas.delete(self.rect_item)
            self.rect_item = self.make_rect(fill="black")
            self.text_item = self.write(fill="white", tags=self.tags)
            self.highlighted = True
        else:
            if self.highlighted:
                self.canvas.delete(self.text_item)
                self.canvas.delete(self.rect_item)
                self.text_item = self.write(tags=self.tags)
                self.rect_item = self.make_rect(tags=self.tags)
                self.highlighted = False


class TextBox(CanvasObject):
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, command=None, tags=None):
        super().__init__(canvas, x=x, y=y, length=length, height=height, text=text, font=font, width=width,
                         command=command, tags=tags)
        if self.command is not None:
            self.command()


class TextInput(CanvasObject):
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, command=None, tags=None):
        super().__init__(canvas, x=x, y=y, length=length, height=height, text=text, font=font, width=width,
                         command=command, tags=tags)
        self.canvas.bind_all("<Key>", self.check_key)
        self.active = True
        if self.command is not None:
            self.canvas.bind_all("<Return>", lambda event: self.command(event))
        self.selected = False
        self.selector()

    def update(self, x=None, y=None, length=None, height=None, text=None, add=False):
        super().update(x, y, length, height, text, add)
        if self.command is not None:
            self.canvas.unbind_all("<Return>")
            self.canvas.bind_all("<Return>", lambda event: self.command(event))

    def check_key(self, event):
        if event.char in f"{string.ascii_letters}{string.digits} !@#$%^&*()_+-=[];'\\:|,./<>?" + '"{}':
            self.add_string(event.char)
        elif event.keysym == "BackSpace":
            self.delete_string()

    def add_string(self, char):
        self.text += char
        self.canvas.delete(self.text_item)
        self.canvas.delete(self.rect_item)
        self.text_item = self.write(tags=self.tags)
        self.rect_item = self.make_rect(tags=self.tags)

    def delete_string(self):
        self.text = self.text[:-1]
        self.canvas.delete(self.text_item)
        self.canvas.delete(self.rect_item)
        self.text_item = self.write(tags=self.tags)
        self.rect_item = self.make_rect(tags=self.tags)

    def selector(self):
        if self.active:
            if not self.selected:
                self.canvas.unbind_all("<Key>")
                self.canvas.bind_all("<Key>", self.check_key)
                self.canvas.delete(self.text_item)
                self.canvas.delete(self.rect_item)
                if self.command is not None:
                    self.canvas.unbind_all("<Return>")
                    self.canvas.bind_all("<Return>", lambda event: self.command(event))
                self.text_item = self.write(text=self.text+"|", tags=self.tags)
                self.rect_item = self.make_rect(tags=self.tags)
                self.selected = True
            elif self.selected:
                self.update()
                self.selected = False
            self.canvas.after(500, self.selector)


class MainSequence:
    def __init__(self, canvas, x, y, username, buttons, text_boxes, text_inputs):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.username = username
        self.buttons = buttons
        self.text_boxes = text_boxes
        self.text_inputs = text_inputs

        self.buttons["Main Sequence"]["Main Portion"] = {
            "load_game_button": self.buttons["Main Sequence"]["Menu"]["load_game_button"].update(),
            "quit_button": self.buttons["Main Sequence"]["Menu"]["quit_button"].update()
        }
        self.text_boxes["Main Sequence"]["Main Portion"] = {
            "main_portion_text_box": TextBox(self.canvas, x=self.x, y=self.y, length=930, height=620,
                                             text=f"Hello, {self.username}, and welcome to 'In Memoriam!'"),
            "inventory_text_box": TextBox(self.canvas, x=955, y=10, length=325, height=620,
                                          text="              Inventory:\n\n"
                                               "Health Potion\n"
                                               "Stick")
        }
        self.text_inputs["Main Sequence"]["Main Portion"] = {
            "main_portion_text_input": TextInput(canvas, x=x, y=y+630, length=930, height=35,
                                                 command=lambda event: self.check_typed())
        }

        self.health_bar_text_box = TextBox(self.canvas, x=10, y=680, length=460, height=35,
                                           text="Health:")
        self.health_bar_text_box.make_line(93, 698, 460, 698, fill="red")

        self.mana_bar_text_box = TextBox(self.canvas, x=480, y=680, length=460, height=35,
                                         text="Mana:")
        self.mana_bar_text_box.make_line(550, 698, 930, 698, fill="blue")

        self.commands = {
            ("help", "support", "aide", "aid", "commands"):
                lambda: self.text_boxes["Main Sequence"]["Main Portion"]["text_box"].update(text="Help? HAH", add=True),
            ("clear", "clear screen", "clear all", "clearall", "clearscreen", "cls", "clr"):
                lambda: self.text_boxes["Main Sequence"]["Main Portion"]["text_box"].update(text="Screen cleared."),
            ("attack", "fight"):
                lambda: FightSequence(self, self.buttons)
        }

    def check_typed(self):
        for command in self.commands:
            if self.text_inputs["Main Sequence"]["Main Portion"]["text_input"].text.lower() in command:
                self.commands[command]()
        command_keys = []
        for command in self.commands:
            command_keys += command
        if self.text_inputs["Main Sequence"]["Main Portion"]["text_input"].text.lower() not in command_keys:
            self.text_boxes["Main Sequence"]["Main Portion"]["text_box"].update(
                text="Unknown command/input. If lost, type 'help'.", add=True
            )
        self.text_inputs["Main Sequence"]["Main Portion"]["text_input"].update(text="")


class FightSequence:
    def __init__(self, main_sequence, buttons):
        self.main_sequence = main_sequence
        self.ms_buttons = buttons
        self.buttons = {}
        self.enemy = Enemy(self.main_sequence, "Goblin", "Enemy")
        self.main_sequence.text_box.update(y=110, height=520,
                                           text=f"You have encountered {self.enemy.type} {self.enemy.name}!")
        setattr(self.main_sequence.text_input, "active", False)
        self.main_sequence.canvas.after(
            0, lambda: [
                self.main_sequence.canvas.unbind_all("<Key>"),
                self.main_sequence.canvas.unbind_all("<Return>"),
                self.main_sequence.canvas.itemconfig(self.main_sequence.text_input.text_item,
                                                     state="hidden"),
                self.main_sequence.canvas.itemconfig(self.main_sequence.text_input.rect_item,
                                                     state="hidden")
            ]
        )
        self.buttons["fight_button"] = Button(self.main_sequence.canvas, x=10, y=640, length=100, height=35,
                                              text="Fight")
        self.buttons["magic_button"] = Button(self.main_sequence.canvas, x=120, y=640, length=100, height=35,
                                              text="Magic")
        self.buttons["items_button"] = Button(self.main_sequence.canvas, x=230, y=640, length=100, height=35,
                                              text="Items")
        self.buttons["run_button"] = Button(self.main_sequence.canvas, x=340, y=640, length=100, height=35, text="Run",
                                            command=self.end_fight)

    def end_fight(self):
        for x in self.buttons:
            self.main_sequence.canvas.delete(self.buttons[x].text_item)
            self.main_sequence.canvas.delete(self.buttons[x].rect_item)
        self.main_sequence.canvas.unbind("<Motion>")
        self.main_sequence.canvas.unbind("<Button-1>")
        self.ms_buttons["Main Sequence"]["Menu"]["load_game_button"].update()
        self.ms_buttons["Main Sequence"]["Menu"]["quit_button"].update()
        self.main_sequence.canvas.after(
            0, lambda: [
                self.main_sequence.text_input.update(),
                self.main_sequence.canvas.bind_all(
                    "<Key>",
                    self.main_sequence.text_input.check_key
                ),
                setattr(self.main_sequence.text_input, "active", True),
                self.main_sequence.text_box.update(
                    y=10, height=620,
                    text="FIGHT RESULTS GO HERE"
                ),
                self.enemy.enemy_game_over()
            ]
        )


class Character:
    def __init__(self, main_sequence, type_):
        self.main_sequence = main_sequence
        self.type = type_
        self.character_type = {
            "Player": {
                "Health": 100,
                "Mana": 20,
                "Items": self.main_sequence.inventory_text_box.text.split("\n")[2:]
            },
            "NPC": {},
            "Boss": {},
            "Enemy": {
                "Health": 100,
                "Mana": 10,
                "Items": None
            }
        }

        self.health = self.character_type[self.type]["Health"]
        self.mana = self.character_type[self.type]["Mana"]
        self.items = self.character_type[self.type]["Items"]


class Enemy(Character):
    def __init__(self, main_sequence, name, type_):
        super().__init__(main_sequence, type_)
        self.name = name
        self.text_boxes = {
            "name_text_box":
                TextBox(self.main_sequence.canvas, x=10, y=10, length=460, height=35,
                        text=f"Name: {self.name}"),
            "health_bar_text_box":
                TextBox(self.main_sequence.canvas, x=10, y=60, length=460, height=35,
                        text="Health:"),
            "mana_bar_text_box":
                TextBox(self.main_sequence.canvas, x=480, y=60, length=460, height=35,
                        text="Mana:")
        }

        self.health_bar = self.text_boxes["health_bar_text_box"].make_line(93, 77, 460, 77, fill="red")

        self.mana_bar = self.text_boxes["mana_bar_text_box"].make_line(550, 77, 930, 77, fill="blue")

    def enemy_game_over(self):
        for x in self.text_boxes:
            self.main_sequence.canvas.delete(self.text_boxes[x].text_item)
            self.main_sequence.canvas.delete(self.text_boxes[x].rect_item)
        self.main_sequence.canvas.delete(self.health_bar)
        self.main_sequence.canvas.delete(self.mana_bar)


class Audio:
    def __init__(self, root, file):
        self.root = root
        self.file = mp3play.load(file)

    def play(self, loop=False):
        self.file.play()
        if loop:
            self.root.after(157000, self.play)


if __name__ == "__main__":
    session = App()
    session.save()

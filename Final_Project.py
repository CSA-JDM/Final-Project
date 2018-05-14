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
from Canvas_Objects import *
import random
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
        sayo_nara = Audio(self.root, r"..\Final-Project\Sayo-nara.mp3")
        sayo_nara.play(loop=True)

        # Item Dictionaries
        self.buttons = {}
        self.text_boxes = {}
        self.text_inputs = {}

        # Time Text Box Initialization
        current_time = time.localtime()
        self.text_boxes["time_text_box"] = TextBox(
            self.canvas, x=1140, y=650, length=140, height=65,
            text=f"  {current_time[3]}:{current_time[4]}:{current_time[5]}\n"
                 f"{current_time[1]}/{current_time[2]}/{current_time[0]}"
        )

        # Main Sequence
        self.menu()
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
        if len(str(current_time[1])) < 2:
            current_time[1] = "0" + str(current_time[1])
            if len(str(current_time[2])) < 2:
                current_time[2] = "0" + str(current_time[2])
        self.text_boxes["time_text_box"].update(
            text=f"  {current_time[3]}:{current_time[4]}:{current_time[5]}\n"
                 f"{current_time[1]}/{current_time[2]}/{current_time[0]}"
        )
        self.root.after(1, self.time_update)

    def menu(self):
        self.clear_all()
        self.text_boxes["title_text_box"] = TextBox(self.canvas, x=10, y=10, text="In Memoriam",
                                                    font=("Times New Roman", 30, "bold"))
        self.buttons["new_game_button"] = Button(self.canvas, x=10, y=110, length=130, height=35, text="New Game",
                                                 command=self.username)
        self.buttons["load_game_button"] = Button(self.canvas, x=10, y=185, length=135, height=35, text="Load Game",
                                                  command=None)
        self.buttons["quit_button"] = Button(self.canvas, x=10, y=260, length=60, height=35, text="Quit",
                                             command=lambda event: self.root.destroy())

    def username(self, *args):
        self.clear_all()
        self.text_boxes["title_text_box"] = TextBox(self.canvas, x=10, y=30, text="Username:",
                                                    font=("Times New Roman", 20, "normal"))
        self.text_inputs["username_text_input"] = TextInput(
            self.canvas, x=145, y=30, length=500, height=35,
            command=lambda event: [self.main_sequence(),
                                   setattr(self.text_inputs["username_text_input"], "active", False)])
        self.buttons["back_button"] = Button(self.canvas, x=10, y=680, length=65, height=35, text="Back",
                                             command=lambda event: [
                                                 self.menu(), setattr(self.text_inputs["username_text_input"], "active",
                                                                      False)])
        self.buttons["load_game_button"].update(x=920, y=680)
        self.buttons["quit_button"].update(x=1065, y=680)

    def main_sequence(self):
        self.clear_all()
        self.main_user_input = MainSequence(self.canvas, 10, 10, self.text_inputs['username_text_input'].text,
                                            self.buttons)
        self.buttons["load_game_button"].update()
        self.buttons["quit_button"].update()

    def clear_all(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind_all("<Key>")
        self.canvas.unbind_all("<Return>")

    def save(self):
        pass


class MainSequence:
    def __init__(self, canvas, x, y, username, buttons):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.username = username
        self.buttons = buttons

        self.text_box = TextBox(canvas, x=x, y=y, length=900, height=620,
                                text=f"Hello, {self.username}, and welcome to 'In Memoriam!'")
        self.text_input = TextInput(canvas, x=x, y=y+630, length=900, height=35,
                                    command=lambda event: self.check_typed())

        self.inventory_text_box = TextBox(self.canvas, x=925, y=10, length=325, height=620,
                                          text="               Inventory\n\n")

        self.inventory = {
            "Health Potion": 1,
            "Mana Potion": 1
        }
        self.inventory_buttons = {}
        item_space = 35
        for item in self.inventory:
            self.inventory_buttons[item] = Button(self.canvas, x=945, y=35+item_space, length=285, height=25,
                                                  font=("Times New Roman", 15, "normal"),
                                                  text=f"{item} x{self.inventory[item]}",
                                                  command=lambda event, item_=item: self.item_options(item_, event))
            item_space += 35

        self.health_bar_text_box = TextBox(self.canvas, x=10, y=680, length=445, height=35,
                                           text="Health:")
        self.health_bar_line = self.health_bar_text_box.make_line(93, 698, 445, 698, fill="red")

        self.mana_bar_text_box = TextBox(self.canvas, x=465, y=680, length=445, height=35,
                                         text="Mana:")
        self.mana_bar_line = self.mana_bar_text_box.make_line(535, 698, 900, 698, fill="blue")

    def check_typed(self):
        if self.text_input.text != "":
            self.commands = {
                ("help", "support", "aide", "aid", "commands"):
                    lambda: self.text_box.update(text="Available commands:\n"
                                                      "'clear' - clears the screen\n"
                                                      "'fight' - enters a random encounter\n"
                                                      "'help' - pulls up this text", add=True),
                ("clear", "clear screen", "clear all", "clearall", "clearscreen", "cls", "clr"):
                    lambda: [self.canvas.dchars(self.text_box.text_item, 0, len(self.text_box.text)),
                             setattr(self.text_box, "text", "")],
                ("attack", "fight"):
                    lambda: FightSequence(self),
                (f"add {' '.join([x for x in self.text_input.text.lower().split()[1:]])}",):
                    lambda: self.inventory_update(
                        text=(f"{' '.join([x.title() for x in self.text_input.text.lower().split()[1:]])}", 1)
                    ),
                (f"remove {' '.join([x for x in self.text_input.text.lower().split()[1:]])}",):
                    lambda: self.inventory_update(
                        text=(f"{' '.join([x.title() for x in self.text_input.text.lower().split()[1:]])}", 1),
                        add=False
                    )
            }
            for command in self.commands:
                if self.text_input.text.lower() in command:
                    self.commands[command]()
            command_keys = []
            for y in [x for x in list(self.commands.keys())]:
                command_keys += y
            if self.text_input.text.lower() not in command_keys:
                self.text_box.update(text="Unknown command/input. If lost, type 'help'.", add=True)
            self.text_input.update(text="")

    def inventory_update(self, text=None, add=True):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        for button in self.inventory_buttons:
            self.canvas.delete(self.inventory_buttons[button].text_item)
            self.canvas.delete(self.inventory_buttons[button].rect_item)

        if text is not None:
            if add is True:
                if text[0] not in self.inventory:
                    self.inventory[text[0]] = text[1]
                elif text[0] in self.inventory:
                    self.inventory[text[0]] += 1
            else:
                if text[0] in self.inventory:
                    if self.inventory[text[0]] > 0:
                        self.inventory[text[0]] -= 1
                        if self.inventory[text[0]] <= 0:
                            del self.inventory[text[0]]

        self.inventory_buttons = {}
        item_space = 35
        for item in self.inventory:
            self.inventory_buttons[item] = Button(self.canvas, x=945, y=35 + item_space, length=285, height=25,
                                                  font=("Times New Roman", 15, "normal"),
                                                  text=f"{item} x{self.inventory[item]}",
                                                  command=lambda event, item_=item: self.item_options(item_, event))
            item_space += 35
        self.buttons["load_game_button"].update()
        self.buttons["quit_button"].update()

    def item_options(self, item, event):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.buttons["load_game_button"].update()
        self.buttons["quit_button"].update()
        self.inventory_buttons[f"use_button_{item}"] = Button(self.canvas, event.x, event.y, length=40, height=25,
                                                              font=("Times New Roman", 15, "normal"), text="Use",
                                                              command=lambda event2:
                                                              self.inventory_update(text=(item, 1), add=False))


class FightSequence:
    def __init__(self, main_sequence):
        self.main_sequence = main_sequence
        self.buttons = {}
        self.names = ["Goblin", "Wolf", "Slime", "Skeleton", "Zombie"]
        self.enemy = Enemy(self.main_sequence, self.names[random.randint(0, len(self.names)-1)])
        self.main_sequence.text_box.update(y=110, height=520,
                                           text=f"Encounter: {self.enemy.type} {self.enemy.name}!\n"
                                                "You have the initial action.")
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
        self.buttons["fight_button"] = Button(self.main_sequence.canvas, x=10, y=640, length=65, height=35,
                                              text="Fight", command=lambda event: self.attack_attempt(event))
        self.buttons["magic_button"] = Button(self.main_sequence.canvas, x=135, y=640, length=80, height=35,
                                              text="Magic", command=None)
        self.buttons["run_button"] = Button(self.main_sequence.canvas, x=1070, y=640, length=60, height=35,
                                            text="Run", command=self.end_fight)

    def attack_attempt(self, *args):
        self.main_sequence.canvas.unbind("<Motion>")
        self.buttons["run_button"].update()
        self.main_sequence.buttons["load_game_button"].update()
        self.main_sequence.buttons["quit_button"].update()
        self.buttons["melee_button"] = Button(self.main_sequence.canvas, 10, 595, length=80, height=35,
                                              text="Melee")
        self.buttons["ranged_button"] = Button(self.main_sequence.canvas, 110, 595, length=95, height=35,
                                               text="Ranged")

    def end_fight(self, *args):
        for x in self.buttons:
            self.main_sequence.canvas.delete(self.buttons[x].text_item)
            self.main_sequence.canvas.delete(self.buttons[x].rect_item)
        self.main_sequence.canvas.unbind("<Motion>")
        self.main_sequence.canvas.unbind("<Button-1>")
        self.main_sequence.buttons["load_game_button"].update()
        self.main_sequence.buttons["quit_button"].update()
        self.main_sequence.canvas.after(
            0, lambda: [
                self.main_sequence.text_input.update(),
                self.main_sequence.canvas.bind_all(
                    "<Key>",
                    self.main_sequence.text_input.check_key
                ),
                setattr(self.main_sequence.text_input, "active", True),
                self.main_sequence.text_input.selector(),
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
                "Items": self.main_sequence.inventory_text_box.text.split("\n")[2:],
                "Agility": 0,
                "Attack": 0,
                "Defense": 0,
                "Luck": 0
            },
            "NPC": {},
            "Boss": {},
            "Enemy": {
                "Health": 100,
                "Mana": 10,
                "Items": None,
                "Agility": 0,
                "Attack": 0,
                "Defense": 0,
                "Luck": 0
            }
        }

        self.health = self.character_type[self.type]["Health"]
        self.mana = self.character_type[self.type]["Mana"]
        self.items = self.character_type[self.type]["Items"]


class Enemy(Character):
    def __init__(self, main_sequence, name):
        super().__init__(main_sequence, "Enemy")
        self.name = name
        self.text_boxes = {
            "name_text_box":
                TextBox(self.main_sequence.canvas, x=10, y=10, length=445, height=35,
                        text=f"Name: {self.name}"),
            "health_bar_text_box":
                TextBox(self.main_sequence.canvas, x=10, y=60, length=445, height=35,
                        text="Health:"),
            "mana_bar_text_box":
                TextBox(self.main_sequence.canvas, x=465, y=60, length=445, height=35,
                        text="Mana:")
        }

        self.health_bar = self.text_boxes["health_bar_text_box"].make_line(93, 77, 445, 77, fill="red")

        self.mana_bar = self.text_boxes["mana_bar_text_box"].make_line(535, 77, 900, 77, fill="blue")

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

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
from Canvas_Objects import *
import Final_Project
import random


class MainSequence:
    def __init__(self, canvas, x, y, username, buttons):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.username = username
        self.buttons = buttons
        self.inventory = {
            "Health Potion": 1,
            "Mana Potion": 1
        }
        self.player = Character(self, "Player")
        self.player_health_bar_meter = 352
        self.in_fight = False
        self.update_items = [
            self.buttons["load_game_button"],
            self.buttons["quit_button"]
        ]

        self.text_box = TextBox(canvas, x=x, y=y, length=900, height=620,
                                text=f"Hello, {self.username}, and welcome to 'In Memoriam!'")
        self.text_input = TextInput(canvas, x=x, y=y+630, length=900, height=35,
                                    command=lambda event: self.check_typed())

        self.inventory_text_box = TextBox(self.canvas, x=925, y=10, length=355, height=620,
                                          text="               Inventory\n\n")

        self.inventory_buttons = {}
        item_space = 35
        for item in self.inventory:
            self.inventory_buttons[item] = Button(self.canvas, x=945, y=35+item_space, length=285, height=25,
                                                  font=("Times New Roman", 15, "normal"),
                                                  text=f"{item} x{self.inventory[item]}",
                                                  command=lambda event, item_=item: self.item_options(item_, event))
            item_space += 35
            self.update_items += [self.inventory_buttons[item]]

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
                    lambda: setattr(self, "in_fight", FightSequence(self)),
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
            if self.inventory_buttons[button] in self.update_items:
                del self.update_items[self.update_items.index(self.inventory_buttons[button])]

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
            self.update_items += [self.inventory_buttons[item]]
        self.update_all()

    def item_options(self, item, event):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.buttons["load_game_button"].update()
        self.buttons["quit_button"].update()
        if self.in_fight:
            for button in self.in_fight.buttons.values():
                button.update()
        self.inventory_buttons[f"use_button_{item}"] = Button(
            self.canvas, event.x, event.y, length=40, height=25, font=("Times New Roman", 15, "normal"), text="Use",
            command=lambda event2: self.inventory_update(text=(item, 1), add=False))

    def update_all(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        for item in self.update_items:
            item.update()
        if self.in_fight:
            for button in self.in_fight.buttons.values():
                button.update()


class FightSequence:
    def __init__(self, main_sequence):
        self.main_sequence = main_sequence
        self.buttons = {}
        self.counter = 1
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
                                              text="Fight", command=lambda event: self.attack_menu(event))
        self.buttons["magic_button"] = Button(self.main_sequence.canvas, x=135, y=640, length=80, height=35,
                                              text="Magic", command=None)
        self.buttons["run_button"] = Button(self.main_sequence.canvas, x=1070, y=640, length=60, height=35,
                                            text="Run", command=self.end_fight)
        self.main_sequence.update_items += [x for x in self.buttons.values()]

    def attack_menu(self, *args):
        self.main_sequence.update_all()
        self.buttons["melee_button"] = Button(self.main_sequence.canvas, 10, 595, length=80, height=35,
                                              text="Melee", command=self.melee_menu)
        self.buttons["ranged_button"] = Button(self.main_sequence.canvas, 110, 595, length=95, height=35,
                                               text="Ranged", command=self.ranged_menu)

    def melee_menu(self, *args):
        self.main_sequence.update_all()
        self.buttons["light_button"] = Button(self.main_sequence.canvas, 10, 550, length=150, height=35,
                                              text="Light Attack", command=lambda event: self.attack_chance(.75, .5))
        self.buttons["medium_button"] = Button(self.main_sequence.canvas, 170, 550, length=180, height=35,
                                               text="Medium Attack", command=lambda event: self.attack_chance(.5, .75))
        self.buttons["heavy_button"] = Button(self.main_sequence.canvas, 360, 550, length=160, height=35,
                                              text="Heavy Attack", command=lambda event: self.attack_chance(.25, 1))

    def ranged_menu(self, *args):
        pass

    def attack_chance(self, type_chance, type_nerf):
        old_health = self.enemy.health
        if type_chance*(self.main_sequence.player.agility*.2) > round(random.randint(0, 100) * 0.01, 2):
            if self.enemy.health - self.main_sequence.player.attack * type_nerf > 0:
                self.enemy.health -= self.main_sequence.player.attack * type_nerf
            else:
                self.enemy.health = 0
            self.main_sequence.canvas.delete(self.enemy.health_bar)
            try:
                self.enemy.health_bar_meter = self.enemy.health_bar_meter * (self.enemy.health / old_health)
                self.enemy.health_bar = self.enemy.text_boxes["health_bar_text_box"].make_line(
                    93, 77, 93 + self.enemy.health_bar_meter, 77, fill="red"
                )
                self.main_sequence.text_box.update(
                    text=f"You dealt {self.main_sequence.player.attack * type_nerf} damage to the {self.enemy.name}!",
                    add=True
                )
            except ZeroDivisionError:
                self.end_fight("Won")
        else:
            if self.main_sequence.text_box.text.split("\n")[-1] == "You missed!" or \
                    self.main_sequence.text_box.text.split("\n")[-1] == f"You missed! x{self.counter}":
                self.counter += 1
                self.main_sequence.text_box.text = "\n".join(self.main_sequence.text_box.text.split("\n")[:-1]) +\
                                                   f"\nYou missed! x{self.counter}"
                self.main_sequence.text_box.update()
            else:
                self.counter = 1
                self.main_sequence.text_box.update(text="You missed!", add=True)

        old_health_p = self.main_sequence.player.health
        if type_chance * (self.enemy.agility * .2) > round(random.randint(0, 100) * 0.01, 2):
            if self.main_sequence.player.health - self.enemy.attack * type_nerf > 0:
                self.main_sequence.player.health -= self.enemy.attack * type_nerf
            else:
                self.main_sequence.player.health = 0
            self.main_sequence.canvas.delete(self.main_sequence.health_bar_line)
            try:
                self.main_sequence.player_health_bar_meter *= (self.main_sequence.player.health / old_health_p)
                self.main_sequence.player.health_bar_line =\
                    self.main_sequence.health_bar_text_box.make_line(
                        93, 698, 93 + self.main_sequence.player_health_bar_meter, 698, fill="red"
                    )
                self.main_sequence.text_box.update(
                    text=f"The {self.enemy.name} dealt {self.main_sequence.player.attack * type_nerf} damage to you!",
                    add=True
                )
            except ZeroDivisionError:
                self.end_fight("You Lost!")
        else:
            if self.main_sequence.text_box.text.split("\n")[-1] == f"The {self.enemy.name} missed!" or \
                    self.main_sequence.text_box.text.split("\n")[-1] ==\
                    f"The {self.enemy.name} missed! x{self.counter}":
                self.counter += 1
                self.main_sequence.text_box.text = "\n".join(
                    self.main_sequence.text_box.text.split("\n")[:-1]) +\
                    f"\nThe {self.enemy.name} missed! x{self.counter}"
                self.main_sequence.text_box.update()
            else:
                self.counter = 1
                self.main_sequence.text_box.update(text=f"The {self.enemy.name} missed!", add=True)

        if "melee_button" in self.buttons:
            del self.buttons["melee_button"]
        if "ranged_button" in self.buttons:
            del self.buttons["ranged_button"]
        if "light_button" in self.buttons:
            del self.buttons["light_button"]
        if "medium_button" in self.buttons:
            del self.buttons["medium_button"]
        if "heavy_button" in self.buttons:
            del self.buttons["heavy_button"]
        self.main_sequence.update_all()

    def end_fight(self, end_text=None, *args):
        for x in self.buttons:
            self.main_sequence.canvas.delete(self.buttons[x].text_item)
            self.main_sequence.canvas.delete(self.buttons[x].rect_item)
            if self.buttons[x] in self.main_sequence.update_items:
                del self.main_sequence.update_items[self.main_sequence.update_items.index(self.buttons[x])]
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
                    text=end_text
                ),
                self.enemy.enemy_game_over(),
                setattr(self.main_sequence, "in_fight", False),
                self.main_sequence.inventory_update()
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
                "Items": self.main_sequence.inventory,
                "Agility": 5,
                "Attack": 5,
                "Defense": 5,
                "Luck": 2
            },
            "NPC": {},
            "Boss": {},
            "Enemy": {
                "Health": 100,
                "Mana": 10,
                "Items": None,
                "Agility": 5,
                "Attack": 5,
                "Defense": 5,
                "Luck": 2
            }
        }

        self.health = self.character_type[self.type]["Health"]
        self.mana = self.character_type[self.type]["Mana"]
        self.items = self.character_type[self.type]["Items"]
        self.agility = self.character_type[self.type]["Agility"]
        self.attack = self.character_type[self.type]["Attack"]
        self.defense = self.character_type[self.type]["Defense"]
        self.luck = self.character_type[self.type]["Luck"]


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
        self.health_bar_meter = 352

        self.mana_bar = self.text_boxes["mana_bar_text_box"].make_line(535, 77, 900, 77, fill="blue")

    def enemy_game_over(self):
        for x in self.text_boxes:
            self.main_sequence.canvas.delete(self.text_boxes[x].text_item)
            self.main_sequence.canvas.delete(self.text_boxes[x].rect_item)
        self.main_sequence.canvas.delete(self.health_bar)
        self.main_sequence.canvas.delete(self.mana_bar)

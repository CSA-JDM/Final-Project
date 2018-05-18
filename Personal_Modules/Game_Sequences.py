# Jacob Meadows
# 4th Period, Computer Programming
# April 15th, 2018
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
from .Canvas_Objects import *
import random
import time


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
        self.level = 1
        self.in_fight = False
        self.update_items = [
            self.buttons["load_game_button"],
            self.buttons["save_game_button"],
            self.buttons["quit_button"]
        ]

        self.text_box = TextBox(canvas, x=x, y=y, length=900, height=600,
                                text=f"Hello, {self.username}, and welcome to 'In Memoriam!'\n"
                                     "Currently, you can only experience and interact in random encounters by typing "
                                     "'fight', but I plan on adding more over time.")
        self.text_input = TextInput(canvas, x=x, y=y+605, length=900, height=35,
                                    command=lambda event: self.check_typed())

        self.inventory_text_box = TextBox(self.canvas, x=925, y=10, length=355, height=600,
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

        self.health_bar_text_box = TextBox(self.canvas, x=10, y=655, length=445, height=35,
                                           text="Health:")
        self.health_bar_line = self.health_bar_text_box.make_line(93, 673, 445, 673, fill="red", width=20)

        self.mana_bar_text_box = TextBox(self.canvas, x=465, y=655, length=445, height=35,
                                         text="Mana:")
        self.mana_bar_line = self.mana_bar_text_box.make_line(535, 673, 900, 673, fill="blue", width=20)

        self.exp_bar_text_box = TextBox(self.canvas, x=10, y=695, length=1270, height=20,
                                        font=("Times New Roman", 10, "normal"), text=f"Level: {self.level}")

        self.exp_bar_line = self.exp_bar_text_box.make_line(60, 705, 1265, 705, fill="gray", width=10)

    def check_typed(self):
        self.text_input.text = self.text_input.text.strip(" ")
        if self.text_input.text != "":
            self.commands = {
                ("help", "support", "aide", "aid", "commands"):
                    lambda: self.text_box.update(text="Available commands:\n"
                                                      "'clear' - clears the screen\n"
                                                      "'fight' - enters a random encounter\n"
                                                      "'help' - pulls up this text", add=True)
                    if self.text_box.text.count("\n") < 15
                    else self.text_box.update(text="Available commands:\n"
                                                   "'clear' - clears the screen\n"
                                                   "'fight' - enters a random encounter\n"
                                                   "'help' - pulls up this text", add=False),
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
                    ),
                ("print items",):
                    lambda: self.text_box.update(text=str(list(self.canvas.find_all())), add=True)
                    if self.text_box.text.count("\n") < 15
        else self.text_box.update(text=str(list(self.canvas.find_all())), add=False)
            }
            for command in self.commands:
                if self.text_input.text.lower() in command:
                    self.commands[command]()
            command_keys = []
            for y in [x for x in list(self.commands.keys())]:
                command_keys += y
            if self.text_input.text.lower() not in command_keys:
                if self.text_box.text.count("\n") < 17:
                    self.text_box.update(text="Unknown command/input. If lost, type 'help'.", add=True)
                else:
                    self.text_box.update(text="Unknown command/input. If lost, type 'help'.", add=False)
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


class FightSequence:
    def __init__(self, main_sequence):
        self.main_sequence = main_sequence
        self.buttons = {}
        self.counter = 1
        self.names = ["Goblin", "Wolf", "Slime", "Skeleton", "Zombie"]
        self.enemy = Enemy(self.main_sequence, self.names[random.randint(0, len(self.names)-1)])
        self.main_sequence.text_box.update(y=110, height=500,
                                           text=f"Encounter: Level 1 {self.enemy.type} {self.enemy.name}!\n"
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
        self.buttons["fight_button"] = Button(self.main_sequence.canvas, x=10, y=615, length=65, height=35,
                                              text="Fight", command=lambda event: self.attack_menu())
        self.buttons["magic_button"] = Button(self.main_sequence.canvas, x=135, y=615, length=80, height=35,
                                              text="Magic", command=None)
        self.buttons["run_button"] = Button(self.main_sequence.canvas, x=1072, y=615, length=55, height=35,
                                            text="Run", command=lambda event: self.end_fight("You ran away!"))
        self.main_sequence.update_items += [x for x in self.buttons.values()]

    def attack_menu(self):
        self.main_sequence.update_all()
        TextBox(self.main_sequence.canvas, 10, 420, length=900, height=190)
        TextBox(self.main_sequence.canvas, 10, 420, text="Melee Options:")
        TextBox(self.main_sequence.canvas, 10, 510, text="Ranged Options:")
        self.buttons["light_button"] = Button(self.main_sequence.canvas, 10, 465, length=150, height=35,
                                              text="Light Attack", command=lambda event: self.attack_chance(.75, .5),
                                              highlighted_command=lambda event: self.attack_stats((.75, .5), event))
        self.buttons["medium_button"] = Button(self.main_sequence.canvas, 170, 465, length=180, height=35,
                                               text="Medium Attack", command=lambda event: self.attack_chance(.5, .75),
                                               highlighted_command=lambda event: self.attack_stats((.5, .75), event))
        self.buttons["heavy_button"] = Button(self.main_sequence.canvas, 360, 465, length=155, height=35,
                                              text="Heavy Attack", command=lambda event: self.attack_chance(.25, 1),
                                              highlighted_command=lambda event: self.attack_stats((.25, 1), event))
        self.buttons["light_arrow_button"] = Button(
            self.main_sequence.canvas, 10, 555, length=150, height=35, text="Light Arrow",
            command=lambda event: self.attack_chance(.75, .5),
            highlighted_command=lambda event: self.attack_stats((.75, .5), event)
        )

    def attack_chance(self, type_chance, type_nerf):
        old_health = self.enemy.health
        if type_chance*(self.main_sequence.player.agility*.2) > round(random.randint(0, 100) * 0.01, 2):
            if self.enemy.health - round(self.main_sequence.player.attack * type_nerf) > 0:
                self.enemy.health -= round(self.main_sequence.player.attack * type_nerf)
            else:
                self.enemy.health = 0
            self.main_sequence.canvas.delete(self.enemy.health_bar)
            try:
                self.enemy.health_bar_meter = self.enemy.health_bar_meter * (self.enemy.health / old_health)
                self.enemy.health_bar = self.enemy.text_boxes["health_bar_text_box"].make_line(
                    93, 77, 93 + self.enemy.health_bar_meter, 77, fill="red", width=20
                )
                if self.main_sequence.text_box.text.count("\n") < 15:
                    self.main_sequence.text_box.update(
                        text=f"You dealt {round(self.main_sequence.player.attack * type_nerf)} "
                             f"damage to the {self.enemy.name}!",
                        add=True
                    )
                else:
                    self.main_sequence.text_box.update(
                        text=f"You dealt {round(self.main_sequence.player.attack * type_nerf)} "
                             f"damage to the {self.enemy.name}!",
                        add=False
                    )
            except ZeroDivisionError:
                self.end_fight("You Won!")
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
                return
        else:
            if self.main_sequence.text_box.text.split("\n")[-1] == "You missed!" or \
                    self.main_sequence.text_box.text.split("\n")[-1] == f"You missed! x{self.counter}":
                self.counter += 1
                self.main_sequence.text_box.text = "\n".join(self.main_sequence.text_box.text.split("\n")[:-1]) +\
                                                   f"\nYou missed! x{self.counter}"
                self.main_sequence.text_box.update()
            else:
                self.counter = 1
                if self.main_sequence.text_box.text.count("\n") < 15:
                    self.main_sequence.text_box.update(text="You missed!", add=True)
                else:
                    self.main_sequence.text_box.update(text="You missed!", add=False)
        self.main_sequence.canvas.update()
        time.sleep(2)

        old_health_p = self.main_sequence.player.health
        enemy_types = ((.75, .5), (.5, .75), (.25, 1))
        current_type = enemy_types[random.randint(0, 2)]
        if current_type[0] * (self.enemy.agility * .2) > round(random.randint(0, 100) * 0.01, 2):
            if self.main_sequence.player.health - round(self.enemy.attack * current_type[1]) > 0:
                self.main_sequence.player.health -= round(self.enemy.attack * current_type[1])
            else:
                self.main_sequence.player.health = 0
            self.main_sequence.canvas.delete(self.main_sequence.health_bar_line)
            try:
                self.main_sequence.player_health_bar_meter *= (self.main_sequence.player.health / old_health_p)
                self.main_sequence.health_bar_line =\
                    self.main_sequence.health_bar_text_box.make_line(
                        93, 673, 93 + self.main_sequence.player_health_bar_meter, 673, fill="red", width=20
                    )
                if self.main_sequence.text_box.text.count("\n") < 15:
                    self.main_sequence.text_box.update(
                        text=f"The {self.enemy.name} dealt {round(self.enemy.attack * current_type[1])} "
                             f"damage to you!",
                        add=True
                    )
                else:
                    self.main_sequence.text_box.update(
                        text=f"The {self.enemy.name} dealt {round(self.enemy.attack * current_type[1])} "
                             f"damage to you!",
                        add=False
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
                if self.main_sequence.text_box.text.count("\n") < 15:
                    self.main_sequence.text_box.update(text=f"The {self.enemy.name} missed!", add=True)
                else:
                    self.main_sequence.text_box.update(text=f"The {self.enemy.name} missed!", add=False)

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

    def attack_stats(self, type_, event):
        return TextBox(
            self.main_sequence.canvas, event.x+5, event.y, 255, 65, f"Chance to hit: {int(type_[0]*100)}%\n"
                                                                    f"Power of attack: {int(type_[1]*100)}%"
        )

    def end_fight(self, end_text=None):
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
                        text=f"Name: {self.name}, Level: 1"),
            "health_bar_text_box":
                TextBox(self.main_sequence.canvas, x=10, y=60, length=445, height=35,
                        text="Health:"),
            "mana_bar_text_box":
                TextBox(self.main_sequence.canvas, x=465, y=60, length=445, height=35,
                        text="Mana:")
        }

        self.health_bar = self.text_boxes["health_bar_text_box"].make_line(93, 77, 445, 77, fill="red", width=20)
        self.health_bar_meter = 352

        self.mana_bar = self.text_boxes["mana_bar_text_box"].make_line(535, 77, 900, 77, fill="blue", width=20)

    def enemy_game_over(self):
        for x in self.text_boxes:
            self.main_sequence.canvas.delete(self.text_boxes[x].text_item)
            self.main_sequence.canvas.delete(self.text_boxes[x].rect_item)
        self.main_sequence.canvas.delete(self.health_bar)
        self.main_sequence.canvas.delete(self.mana_bar)

# Jacob Meadows
# 4th Period, Computer Programming
# April 16th, 2018
"""
# Description
A simple RPG with the goal being to escape a monster-infested region.

# License Preamble
This file is part of In Memoriam.

    In Memoriam is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    In Memoriam is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with In Memoriam.  If not, see <http://www.gnu.org/licenses/>.
"""
import Personal_Modules.Canvas_Objects as Canvas_Objects
import Personal_Modules.mp3play as mp3play
import turtle
import time
import random


class App:
    def __init__(self):
        # Root Initialization
        self.root = turtle._Root()
        self.root.config(width=1280, height=720)
        self.root.bind("<Escape>", lambda args: self.root.destroy())
        self.root.title("In Memoriam")

        # Canvas Initialization
        self.canvas = turtle.Canvas(self.root)
        self.canvas.config(width=1280, height=720, background="white")
        self.canvas.place(x=0, y=0)

        # Audio Initialization
        sayo_nara = Audio(self.root, r"..\Final-Project\Music\Sayo-nara.mp3")
        sayo_nara.play(loop=True)

        # Item Dictionaries
        self.buttons = {}
        self.text_boxes = {}
        self.text_inputs = {}

        # Time Text Box Initialization
        current_time = time.localtime()
        self.text_boxes["time_text_box"] = Canvas_Objects.TextBox(
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
        self.time_var = self.root.after(1, self.time_update)

    def menu(self):
        self.clear_all()
        self.text_boxes["title_text_box"] = Canvas_Objects.TextBox(self.canvas, x=10, y=10, text="In Memoriam",
                                                                   font=("Times New Roman", 30, "bold"))
        self.buttons["new_game_button"] = Canvas_Objects.Button(self.canvas, x=10, y=110, length=130, height=35,
                                                                text="New Game", command=lambda event: self.username())
        self.buttons["load_game_button"] = Canvas_Objects.Button(self.canvas, x=10, y=185, length=135, height=35,
                                                                 text="Load Game",
                                                                 command=lambda event: self.save_load())
        self.buttons["quit_button"] = Canvas_Objects.Button(self.canvas, x=10, y=260, length=60, height=35, text="Quit",
                                                            command=lambda event: self.root.destroy())

    def username(self):
        self.clear_all()
        self.text_boxes["title_text_box"] = Canvas_Objects.TextBox(self.canvas, x=10, y=30, text="Username:",
                                                                   font=("Times New Roman", 20, "normal"))
        self.text_inputs["username_text_input"] = Canvas_Objects.TextInput(
            self.canvas, x=145, y=30, length=500, height=35,
            command=lambda event: [self.main_sequence(),
                                   setattr(self.text_inputs["username_text_input"], "active", False)])
        self.buttons["back_button"] = Canvas_Objects.Button(self.canvas, x=10, y=680, length=65, height=35, text="Back",
                                                            command=lambda event: [
                                                                self.menu(), setattr(
                                                                    self.text_inputs["username_text_input"], "active",
                                                                    False)])
        self.buttons["load_game_button"].update(x=920, y=680)
        self.buttons["quit_button"].update(x=1065, y=680)

    def main_sequence(self):
        self.clear_all()
        self.buttons["save_game_button"] = Canvas_Objects.Button(self.canvas, x=927, y=615, length=130, height=35,
                                                                 text="Save Game",
                                                                 command=lambda event: self.save_load())
        self.main_user_input = MainSequence(
            self, self.canvas, 10, 10, self.text_inputs['username_text_input'].text, self.buttons
        )
        self.text_boxes["time_text_box"].update(y=625)
        self.buttons["load_game_button"].update(y=655)
        self.buttons["quit_button"].update(y=655)

    def clear_all(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind_all("<Key>")
        self.canvas.unbind_all("<Return>")

    def save_load(self):
        self.save_feature = Canvas_Objects.TextBox(
            self.canvas, x=510, y=230, length=235, height=100,
            text="It's a quick game; you'll be able to finish it without this.")
        self.canvas.update()
        time.sleep(3)
        self.canvas.delete(self.save_feature.text_item)
        self.canvas.delete(self.save_feature.rect_item)


class MainSequence:
    def __init__(self, app, canvas, x, y, username, buttons):
        self.app = app
        self.canvas = canvas
        self.x = x
        self.y = y
        self.username = username
        self.buttons = buttons
        self.inventory = {
            "Health Potion": 10,
            "Mana Potion": 10
        }
        self.level = 1
        self.player = Character(self, "Player", self.level)
        self.player_health_bar_meter = 352
        self.in_fight = False
        self.update_items = [
            self.buttons["load_game_button"],
            self.buttons["save_game_button"],
            self.buttons["quit_button"]
        ]

        self.boss_name = ['Goblin', 'Wolf', 'Slime', 'Skeleton', 'Zombie'][random.randint(0, 4)]

        self.text_box = Canvas_Objects.TextBox(
            canvas, x=x, y=y, length=900, height=600,
            text=f"Hello, {self.username}, and welcome to 'In Memoriam!'\n"
                 "Awakening in an isolated region, you notice the only way available passage is\n"
                 f"blocked by an extremely tough looking {self.boss_name}.\n"
                 "At your current state, you don't appear to be fully prepared to win against him\n"
                 "should a fight arise.\n"
                 "To fix that, you can run into random encounters by typing 'fight', which rewards\n"
                 "you with experience points.\n"
                 "With enough experience points, you can level up and increase your stats;\n"
                 "including your strength, health, mana, and agility!\n"
                 f"When you feel as though you're strong enough, you can fight the {self.boss_name}\n"
                 "by typing 'fight boss'.\n"
                 "Good luck, and have fun!")
        self.text_input = Canvas_Objects.TextInput(canvas, x=x, y=y + 605, length=900, height=35,
                                                   command=lambda event: self.check_typed())

        self.inventory_text_box = Canvas_Objects.TextBox(self.canvas, x=925, y=10, length=355, height=600,
                                                         text="               Inventory\n\n")

        self.inventory_buttons = {}
        item_space = 35
        for item in self.inventory:
            self.inventory_buttons[item] = Canvas_Objects.Button(
                self.canvas, x=945, y=35 + item_space, length=285, height=25, font=("Times New Roman", 15, "normal"),
                text=f"{item} x{self.inventory[item]}",
                command=lambda event, item_=item: self.item_options(item_, event)
            )
            item_space += 35
            self.update_items += [self.inventory_buttons[item]]

        self.health_bar_text_box = Canvas_Objects.TextBox(self.canvas, x=10, y=655, length=445, height=35,
                                                          text="Health:")
        self.health_bar_line = self.health_bar_text_box.make_line(93, 673, 445, 673, fill="red", width=20)

        self.mana_bar_text_box = Canvas_Objects.TextBox(self.canvas, x=465, y=655, length=445, height=35,
                                                        text="Mana:")
        self.mana_bar_line = self.mana_bar_text_box.make_line(535, 673, 900, 673, fill="blue", width=20)
        self.player_mana_bar_meter = 365

        self.exp_bar_text_box = Canvas_Objects.TextBox(
            self.canvas, x=10, y=695, length=1270, height=20, font=("Times New Roman", 10, "normal"),
            text=f"Level: {self.level}"
        )
        self.experience = 0

        self.exp_bar_line = self.exp_bar_text_box.make_line(60, 705, 1265, 705, fill="gray", width=10)
        self.filling_exp_bar_line = self.exp_bar_text_box.make_line(60, 705, 60, 705, fill="yellow", width=10)

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
                    lambda: setattr(self, "in_fight", FightSequence(
                        self, lambda: Enemy(
                            self, ["Goblin", "Wolf", "Slime", "Skeleton", "Zombie"][random.randint(0, 4)]
                        )
                    )),
                ("attack boss", "fight boss"):
                    lambda: setattr(self, "in_fight", FightSequence(self, lambda: Boss(self, self.boss_name))),
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
                if self.text_box.text.count("\n") < 18:
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
            self.inventory_buttons[item] = Canvas_Objects.Button(
                self.canvas, x=945, y=35 + item_space, length=285, height=25, font=("Times New Roman", 15, "normal"),
                text=f"{item} x{self.inventory[item]}",
                command=lambda event, item_=item: self.item_options(item_, event)
            )
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
        self.inventory_buttons[f"use_button_{item}"] = Canvas_Objects.Button(
            self.canvas, event.x, event.y, length=40, height=25, font=("Times New Roman", 15, "normal"), text="Use",
            command=lambda event2: [
                self.inventory_update(text=(item, 1), add=False),
                [
                    setattr(self.player, "old_health", self.player.health),
                    setattr(self.player, "health",
                            self.player.health + self.player.attack * .75)
                    if self.player.health + self.player.attack * .75 <= self.player.orig_health
                    else None,
                    setattr(self, "player_health_bar_meter",
                            self.player_health_bar_meter *
                            (self.player.health / self.player.old_health)),
                    self.canvas.delete(self.health_bar_line),
                    setattr(self, "health_bar_line", self.health_bar_text_box.make_line(
                        93, 673, 93 + self.player_health_bar_meter, 673, fill="red", width=20
                    ))
                ] if item == "Health Potion"
                else [
                    setattr(self.player, "old_mana", self.player.mana),
                    setattr(self.player, "mana",
                            self.player.mana + self.player.attack * .75)
                    if self.player.mana + self.player.attack * .75 <= 20
                    else setattr(self.player, "mana", 20),
                    setattr(self, "player_mana_bar_meter",
                            self.player_mana_bar_meter *
                            (self.player.mana / self.player.old_mana)),
                    self.canvas.delete(self.mana_bar_line),
                    setattr(self, "mana_bar_line", self.mana_bar_text_box.make_line(
                        535, 673, 535 + self.player_mana_bar_meter, 673, fill="blue", width=20
                    ))
                ]
            ])

    def update_all(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        for item in self.update_items:
            item.update()


class FightSequence:
    def __init__(self, main_sequence, func):
        self.main_sequence = main_sequence
        self.buttons = {}
        self.counter = 1
        self.enemy = func()
        if self.enemy.type == "Boss":
            pass
        self.main_sequence.text_box.update(y=110, height=500,
                                           text=f"Encounter: Level {self.enemy.level} "
                                                f"{self.enemy.type} {self.enemy.name}!\n"
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
        self.buttons["fight_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, x=10, y=615, length=65, height=35, text="Fight",
            command=lambda event: self.attack_menu()
        )
        self.buttons["magic_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, x=830, y=615, length=80, height=35, text="Magic",
            command=lambda event: self.mana_menu()
        )
        self.buttons["run_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, x=1072, y=615, length=55, height=35, text="Run",
            command=lambda event: self.end_fight("You ran away!"))
        self.main_sequence.update_items += [x for x in self.buttons.values()]

    def attack_menu(self):
        self.main_sequence.update_all()
        Canvas_Objects.TextBox(self.main_sequence.canvas, 10, 420, length=450, height=190)
        Canvas_Objects.TextBox(self.main_sequence.canvas, 10, 420, text="Melee Options:")
        Canvas_Objects.TextBox(self.main_sequence.canvas, 10, 510, text="Ranged Options:")
        self.buttons["light_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 10, 465, length=50, height=35, text="Jab",
            command=lambda event: self.attack_chance(.65, .5),
            highlighted_command=lambda event: self.attack_stats((.65, .5), event)
        )
        self.buttons["medium_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 70, 465, length=70, height=35, text="Slash",
            command=lambda event: self.attack_chance(.5, .75),
            highlighted_command=lambda event: self.attack_stats((.5, .75), event)
        )
        self.buttons["heavy_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 150, 465, length=65, height=35, text="Bash",
            command=lambda event: self.attack_chance(.25, 1.25),
            highlighted_command=lambda event: self.attack_stats((.25, 1.25), event)
        )
        self.buttons["aimed_shot_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 10, 555, length=145, height=35, text="Aimed Shot",
            command=lambda event: self.attack_chance(.7, .4),
            highlighted_command=lambda event: self.attack_stats((.7, .4), event)
        )
        self.buttons["power_shot_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 165, 555, length=140, height=35, text="Power Shot",
            command=lambda event: self.attack_chance(.5, .75),
            highlighted_command=lambda event: self.attack_stats((.5, .75), event)
        )

    def mana_menu(self):
        self.main_sequence.update_all()
        Canvas_Objects.TextBox(self.main_sequence.canvas, 460, 420, length=450, height=190)
        Canvas_Objects.TextBox(self.main_sequence.canvas, 460, 420, text="Elemental Options:")
        Canvas_Objects.TextBox(self.main_sequence.canvas, 460, 510, text="Other Options:")
        self.buttons["fire_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 460, 465, length=110, height=35, text="Fire Ball",
            command=lambda event: [
                self.attack_chance(.75, 1.25),
                [
                    setattr(self.main_sequence.player, "old_mana", self.main_sequence.player.mana),
                    setattr(self.main_sequence.player, "mana",
                            self.main_sequence.player.mana - self.main_sequence.player.attack * .25),
                    setattr(self.main_sequence, "player_mana_bar_meter",
                            self.main_sequence.player_mana_bar_meter *
                            (self.main_sequence.player.mana / self.main_sequence.player.old_mana)),
                    self.main_sequence.canvas.delete(self.main_sequence.mana_bar_line),
                    setattr(self.main_sequence, "mana_bar_line", self.main_sequence.mana_bar_text_box.make_line(
                        535, 673, 535 + self.main_sequence.player_mana_bar_meter, 673, fill="blue", width=20
                    ))
                ]
                ]if self.main_sequence.player.mana - (self.main_sequence.player.attack * .25) > 0 else None,
            highlighted_command=lambda event: self.attack_stats((.75, 1.25), event)
        )
        self.buttons["ice_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 580, 465, length=115, height=35, text="Ice Shard",
            command=lambda event: [
                self.attack_chance(.75, 1.25),
                [
                    setattr(self.main_sequence.player, "old_mana", self.main_sequence.player.mana),
                    setattr(self.main_sequence.player, "mana",
                            self.main_sequence.player.mana - self.main_sequence.player.attack * .25),
                    setattr(self.main_sequence, "player_mana_bar_meter",
                            self.main_sequence.player_mana_bar_meter *
                            (self.main_sequence.player.mana / self.main_sequence.player.old_mana)),
                    self.main_sequence.canvas.delete(self.main_sequence.mana_bar_line),
                    setattr(self.main_sequence, "mana_bar_line", self.main_sequence.mana_bar_text_box.make_line(
                        535, 673, 535 + self.main_sequence.player_mana_bar_meter, 673, fill="blue", width=20
                    ))
                ]
                ]if self.main_sequence.player.mana - (self.main_sequence.player.attack * .25) > 0 else None,
            highlighted_command=lambda event: self.attack_stats((.75, 1.25), event)
        )
        self.buttons["lightning_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 705, 465, length=170, height=35, text="Lightning Bolt",
            command=lambda event: [
                self.attack_chance(.75, 1.25),
                [
                    setattr(self.main_sequence.player, "old_mana", self.main_sequence.player.mana),
                    setattr(self.main_sequence.player, "mana",
                            self.main_sequence.player.mana - self.main_sequence.player.attack * .25),
                    setattr(self.main_sequence, "player_mana_bar_meter",
                            self.main_sequence.player_mana_bar_meter *
                            (self.main_sequence.player.mana / self.main_sequence.player.old_mana)),
                    self.main_sequence.canvas.delete(self.main_sequence.mana_bar_line),
                    setattr(self.main_sequence, "mana_bar_line", self.main_sequence.mana_bar_text_box.make_line(
                        535, 673, 535 + self.main_sequence.player_mana_bar_meter, 673, fill="blue", width=20
                    ))
                ]
                ]if self.main_sequence.player.mana - (self.main_sequence.player.attack * .25) > 0 else None,
            highlighted_command=lambda event: self.attack_stats((.75, 1.25), event)
        )
        self.buttons["heal_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 460, 555, length=65, height=35, text="Heal",
            command=lambda event: [
                [
                    setattr(self.main_sequence.player, "old_mana", self.main_sequence.player.mana),
                    setattr(self.main_sequence.player, "mana",
                            self.main_sequence.player.mana - (self.main_sequence.player.attack * .25)),
                    setattr(self.main_sequence, "player_mana_bar_meter",
                            self.main_sequence.player_mana_bar_meter *
                            (self.main_sequence.player.mana / self.main_sequence.player.old_mana)),
                    self.main_sequence.canvas.delete(self.main_sequence.mana_bar_line),
                    setattr(self.main_sequence, "mana_bar_line", self.main_sequence.mana_bar_text_box.make_line(
                        535, 673, 535 + self.main_sequence.player_mana_bar_meter, 673, fill="blue", width=20
                    ))
                ],
                setattr(self.main_sequence.player, "old_health", self.main_sequence.player.health),
                setattr(self.main_sequence.player, "health",
                        self.main_sequence.player.health + self.main_sequence.player.attack * .4)
                if self.main_sequence.player.health +
                self.main_sequence.player.attack * .4 <= self.main_sequence.player.orig_health
                else None,
                setattr(self.main_sequence, "player_health_bar_meter",
                        self.main_sequence.player_health_bar_meter *
                        (self.main_sequence.player.health / self.main_sequence.player.old_health)),
                self.main_sequence.canvas.delete(self.main_sequence.health_bar_line),
                setattr(self.main_sequence, "health_bar_line", self.main_sequence.health_bar_text_box.make_line(
                    93, 673, 93 + self.main_sequence.player_health_bar_meter, 673, fill="red", width=20
                ))
            ]if self.main_sequence.player.mana - (self.main_sequence.player.attack * .25) > 0 else None,
            highlighted_command=lambda event: self.attack_stats((.75, -.4), event, target="Player")
        )
        self.buttons["shield_button"] = Canvas_Objects.Button(
            self.main_sequence.canvas, 535, 555, length=80, height=35, text="Shield",
            command=lambda event: [
                self.attack_chance(.75, 0),
                [
                    setattr(self.main_sequence.player, "old_mana", self.main_sequence.player.mana),
                    setattr(self.main_sequence.player, "mana",
                            self.main_sequence.player.mana - self.main_sequence.player.attack * .25)
                    if self.main_sequence.player.mana - self.main_sequence.player.attack * .25 > 0 else None,
                    setattr(self, "player_mana_bar_meter",
                            self.main_sequence.player_mana_bar_meter *
                            (self.main_sequence.player.mana / self.main_sequence.player.old_mana)),
                    self.main_sequence.canvas.delete(self.main_sequence.mana_bar_line),
                    setattr(self, "mana_bar_line", self.main_sequence.mana_bar_text_box.make_line(
                        535, 673, 535 + self.main_sequence.player_mana_bar_meter, 673, fill="blue", width=20
                    ))
                ]
                ]if self.main_sequence.player.mana - (self.main_sequence.player.attack * .25) > 0 else None,
            highlighted_command=lambda event: self.attack_stats((.75, 0), event)
        )

    def attack_chance(self, type_chance, type_nerf):
        old_health = self.enemy.health
        if type_chance * (self.main_sequence.player.agility * .12) > round(random.randint(0, 100) * 0.01, 2):
            if self.enemy.health - round(self.main_sequence.player.attack * type_nerf) > 0:
                self.enemy.health -= round(self.main_sequence.player.attack * type_nerf)
            else:
                self.enemy.health = 0
                self.end_fight("You Won!")
                self.main_sequence.experience += 1000 / self.main_sequence.level
                if 60 + self.main_sequence.experience < 1265:
                    self.main_sequence.canvas.delete(self.main_sequence.filling_exp_bar_line)
                    self.main_sequence.filling_exp_bar_line = self.main_sequence.exp_bar_text_box.make_line(
                        60, 705, 60 + self.main_sequence.experience, 705, fill="yellow", width=10
                    )
                else:
                    self.main_sequence.level += 1
                    self.main_sequence.player.attack += 3
                    self.main_sequence.player.agility += 2
                    self.main_sequence.player.orig_health += 20
                    self.main_sequence.player.mana = 20
                    self.main_sequence.player_mana_bar_meter = 365
                    self.main_sequence.canvas.delete(self.main_sequence.mana_bar_line)
                    self.main_sequence.mana_bar_line = \
                        self.main_sequence.mana_bar_text_box.make_line(
                            535, 673, 535 + self.main_sequence.player_mana_bar_meter, 673, fill="blue", width=20
                        )
                    self.main_sequence.player.health = self.main_sequence.player.orig_health
                    self.main_sequence.player_health_bar_meter = 352
                    self.main_sequence.canvas.delete(self.main_sequence.health_bar_line)
                    self.main_sequence.health_bar_line = \
                        self.main_sequence.health_bar_text_box.make_line(
                            93, 673, 93 + self.main_sequence.player_health_bar_meter, 673, fill="red", width=20
                        )
                    self.main_sequence.experience = 0
                    self.main_sequence.exp_bar_text_box.update(text=f"Level: {self.main_sequence.level}")
                    self.main_sequence.exp_bar_line = self.main_sequence.exp_bar_text_box.make_line(
                        60, 705, 1265, 705, fill="gray", width=10
                    )
                    self.main_sequence.filling_exp_bar_line = self.main_sequence.exp_bar_text_box.make_line(
                        60, 705, 60, 705, fill="yellow", width=10
                    )
                delete_these = []
                for button in self.buttons:
                    if button not in ["fight_button", "magic_button", "run_button"]:
                        delete_these += [button]
                for item in delete_these:
                    del self.buttons[item]
                self.main_sequence.update_all()
                return
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
                delete_these = []
                for button in self.buttons:
                    if button not in ["fight_button", "magic_button", "run_button"]:
                        delete_these += [button]
                for item in delete_these:
                    del self.buttons[item]
                self.main_sequence.update_all()
                return
        else:
            if self.main_sequence.text_box.text.split("\n")[-1] == "You missed!" or \
                    self.main_sequence.text_box.text.split("\n")[-1] == f"You missed! x{self.counter}":
                self.counter += 1
                self.main_sequence.text_box.text = "\n".join(self.main_sequence.text_box.text.split("\n")[:-1]) + \
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
        enemy_types = ((.65, .5), (.5, .75), (.25, 1.25))
        current_type = enemy_types[random.randint(0, 2)]
        if current_type[0] * (self.enemy.agility * .12) > round(random.randint(0, 100) * 0.01, 2):
            if self.main_sequence.player.health - round(self.enemy.attack * current_type[1]) > 0:
                self.main_sequence.player.health -= round(self.enemy.attack * current_type[1])
            else:
                self.main_sequence.player.health = 100
                self.end_fight("You Lost!")
            self.main_sequence.canvas.delete(self.main_sequence.health_bar_line)
            try:
                self.main_sequence.player_health_bar_meter *= (self.main_sequence.player.health / old_health_p)
                self.main_sequence.health_bar_line = \
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
                self.main_sequence.player.health = 100
                self.end_fight("You Lost!")
        else:
            if self.main_sequence.text_box.text.split("\n")[-1] == f"The {self.enemy.name} missed!" or \
                self.main_sequence.text_box.text.split("\n")[-1] == \
                    f"The {self.enemy.name} missed! x{self.counter}":
                self.counter += 1
                self.main_sequence.text_box.text = "\n".join(
                    self.main_sequence.text_box.text.split("\n")[:-1]) + \
                    f"\nThe {self.enemy.name} missed! x{self.counter}"
                self.main_sequence.text_box.update()
            else:
                self.counter = 1
                if self.main_sequence.text_box.text.count("\n") < 15:
                    self.main_sequence.text_box.update(text=f"The {self.enemy.name} missed!", add=True)
                else:
                    self.main_sequence.text_box.update(text=f"The {self.enemy.name} missed!", add=False)

        delete_these = []
        for button in self.buttons:
            if button not in ["fight_button", "magic_button", "run_button"]:
                delete_these += [button]
        for item in delete_these:
            del self.buttons[item]
        self.main_sequence.update_all()

    def attack_stats(self, type_, event, target="Enemy"):
        return Canvas_Objects.TextBox(
            self.main_sequence.canvas, event.x + 5, event.y, 255, 100,
            f"Chance to Hit: {round(type_[0]*self.main_sequence.player.agility*.12*100)}%\n"
            f"Target: {target}\n"
            f"Damage: {round(type_[1]*self.main_sequence.player.attack)}"
            if round(type_[0] * self.main_sequence.player.agility * .12 * 100) < 100
            else "Chance to Hit: 100%\n"
                 f"Target: {target}\n"
                 f"Damage: {round(type_[1]*self.main_sequence.player.attack)}"
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
                setattr(self.main_sequence.text_input, "active", True) if self.enemy.type == "Enemy" else None,
                self.main_sequence.text_input.selector(),
                self.main_sequence.text_box.update(
                    y=10, height=620,
                    text=end_text
                ),
                self.enemy.enemy_game_over(end_text),
                self.main_sequence.app.root.after_cancel(self.main_sequence.app.time_var)
                if self.enemy.type == "Boss" else None,
                setattr(self.main_sequence, "in_fight", False),
                self.main_sequence.inventory_update() if self.enemy.type == "Enemy" else None
            ]
        )


class Character:
    def __init__(self, main_sequence, type_, level):
        self.main_sequence = main_sequence
        self.type = type_
        self.orig_health = 100
        self.health = self.orig_health
        self.mana = 20
        self.items = None
        self.agility = 10
        self.attack = 10
        self.defense = 10
        self.luck = 2
        self.level = level
        self.stats = {
            "Health": self.health,
            "Mana": self.mana,
            "Items": self.items,
            "Agility": self.agility,
            "Attack": self.attack,
            "Defense": self.defense,
            "Luck": self.luck
        }


class Enemy(Character):
    def __init__(self, main_sequence, name):
        super().__init__(main_sequence, "Enemy", 1)
        self.name = name
        self.text_boxes = {
            "name_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=10, y=10, length=445, height=35,
                                       text=f"Name: {self.name}, Level: 1"),
            "health_bar_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=10, y=60, length=445, height=35,
                                       text="Health:"),
            "mana_bar_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=465, y=60, length=445, height=35,
                                       text="Mana:")
        }

        self.health_bar = self.text_boxes["health_bar_text_box"].make_line(93, 77, 445, 77, fill="red", width=20)
        self.health_bar_meter = 352

        self.mana_bar = self.text_boxes["mana_bar_text_box"].make_line(535, 77, 900, 77, fill="blue", width=20)

    def enemy_game_over(self, *args):
        for x in self.text_boxes:
            self.main_sequence.canvas.delete(self.text_boxes[x].text_item)
            self.main_sequence.canvas.delete(self.text_boxes[x].rect_item)
        self.main_sequence.canvas.delete(self.health_bar)
        self.main_sequence.canvas.delete(self.mana_bar)


class Boss(Character):
    def __init__(self, main_sequence, name):
        super().__init__(main_sequence, "Boss", 5)
        self.name = name
        self.health = 1000
        self.mana = 200
        self.items = None
        self.agility = 100
        self.attack = 100
        self.defense = 100
        self.luck = 20
        self.text_boxes = {
            "name_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=10, y=10, length=445, height=35,
                                       text=f"Name: {self.name}, Level: {self.level}"),
            "health_bar_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=10, y=60, length=445, height=35,
                                       text="Health:"),
            "mana_bar_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=465, y=60, length=445, height=35,
                                       text="Mana:")
        }

        self.health_bar = self.text_boxes["health_bar_text_box"].make_line(93, 77, 445, 77, fill="red", width=20)
        self.health_bar_meter = 352

        self.mana_bar = self.text_boxes["mana_bar_text_box"].make_line(535, 77, 900, 77, fill="blue", width=20)

    def enemy_game_over(self, result=None):
        if result == "You Won!":
            self.main_sequence.canvas.delete("all")
            victory = Canvas_Objects.TextBox(
                self.main_sequence.canvas, 10, 10, 1270, 700, text="YOU WIN!", font=("Times New Roman", 193, "bold"),
                command=lambda: [
                    self.main_sequence.canvas.bind_all(
                        "<Button-1>", lambda args: self.main_sequence.canvas.master.destroy()
                    )
                ]
            )
        else:
            for x in self.text_boxes:
                self.main_sequence.canvas.delete(self.text_boxes[x].text_item)
                self.main_sequence.canvas.delete(self.text_boxes[x].rect_item)
            self.main_sequence.canvas.delete(self.health_bar)
            self.main_sequence.canvas.delete(self.mana_bar)


class Audio:
    def __init__(self, root, file):
        self.root = root
        try:
            self.file = mp3play.load(file)
        except AttributeError:
            self.file = None
        self.loop = True

    def play(self, loop=None):
        if self.file is not None:
            if loop is not None:
                self.loop = loop
            self.file.play()
            if self.loop:
                self.root.after(157000, self.play)


if __name__ == "__main__":
    session = App()

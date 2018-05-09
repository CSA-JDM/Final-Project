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
        sayo_nara = Audio(self.root, r"..\Final-Project\Sayo-nara.mp3")
        sayo_nara.play(loop=True)

        # Item Dictionaries
        self.buttons = {}
        self.text_boxes = {}
        self.text_inputs = {}

        # Time Text Box Initialization
        current_time = time.localtime()
        self.text_boxes["time_text_box"] = TextBox(
            self.canvas, x=1170, y=650, length=110, height=65,
            text=f"{current_time[3]}:{current_time[4]}:{current_time[5]}\n"
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
        self.text_boxes["time_text_box"].update(
            text=f"{current_time[3]}:{current_time[4]}:{current_time[5]}\n"
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
                                             command=self.root.destroy)

    def username(self):
        self.clear_all()
        self.text_boxes["title_text_box"] = TextBox(self.canvas, x=10, y=30, text="Username:",
                                                    font=("Times New Roman", 20, "normal"))
        self.text_inputs["username_text_input"] = TextInput(
            self.canvas, x=145, y=30, length=500, height=35,
            command=lambda event: [self.main_sequence(),
                                   setattr(self.text_inputs["username_text_input"], "active", False)])
        self.buttons["back_button"] = Button(self.canvas, x=10, y=680, length=65, height=35, text="Back",
                                             command=self.menu)
        self.buttons["load_game_button"].update(x=950, y=680)
        self.buttons["quit_button"].update(x=1095, y=680)

    def main_sequence(self):
        self.clear_all()
        self.main_user_input = MainSequence(self.canvas, self.text_inputs['username_text_input'].text, 10, 10)
        self.text_boxes["inventory_text_box"] = TextBox(self.canvas, x=955, y=10, length=325, height=620,
                                                        text="Inventory:")
        self.text_boxes["health_bar_text_box"] = TextBox(self.canvas, x=10, y=680, length=460, height=35,
                                                         text="Health:")
        self.text_boxes["health_bar_text_box"].make_line(93, 698, 460, 698, fill="red")
        self.text_boxes["mana_bar_text_box"] = TextBox(self.canvas, x=480, y=680, length=460, height=35,
                                                       text="Mana:")
        self.text_boxes["mana_bar_text_box"].make_line(550, 698, 930, 698, fill="blue")
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

    def update(self, x=None, y=None, text=None, add=False):
        if text is not None:
            if add:
                self.text += f"\n{text}"
            elif not add:
                self.text = text
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

    def update(self, x=None, y=None, text=None, add=False):
        super().update(x, y, text, add)
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

    def update(self, x=None, y=None, text=None, add=False):
        super().update(x, y, text, add)
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
    def __init__(self, canvas, username, x=None, y=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.username = username
        if self.x is not None and self.y is not None:
            self.text_box = TextBox(canvas, x=x, y=y, length=930, height=620,
                                    text=f"Hello, {self.username} and welcome to 'In Memoriam!'")
            self.text_input = TextInput(canvas, x=x, y=y+630, length=930, height=35,
                                        command=self.check_typed)

        self.commands = {
            ("help", "support", "aide", "aid", "commands"): lambda: self.text_box.update(text="Help? HAH", add=True),
            ("clear", "clear screen", "clear all", "clearall", "clearscreen", "cls", "clr"):
                lambda: self.text_box.update(text="Screen cleared.")
        }

    def check_typed(self, *args):
        for command in self.commands:
            if self.text_input.text.lower() in command:
                self.commands[command]()
        command_keys = []
        for command in self.commands:
            command_keys += command
        print(command_keys)
        if self.text_input.text.lower() not in command_keys:
            self.text_box.update(text="Unknown command/input. If lost, type 'help'.", add=True)
        self.text_input.update(text="")


class FightSequence(MainSequence):
    def __init__(self, canvas, username):
        super().__init__(canvas, username)
        print("successful")


class Character:
    def __init__(self):
        self.character_type = {
            "Player": [],
            "NPC": [],
            "Boss": [],
            "Enemy": []
        }


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

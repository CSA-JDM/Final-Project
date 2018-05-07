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

        # Item Dictionaries
        self.buttons = {}
        self.text_boxes = {}
        self.text_inputs = {}

        self.text_boxes["time_text_box"] = TextBox(
            self.canvas, x=1200, y=10, length=60, height=35,
            text=f"{time.localtime()[:]}"
        )

        # Main Sequence
        self.menu()
        self.time_update()
        #    Song length (in milliseconds): 157000
        self.root.mainloop()

    def time_update(self):
        current_time = time.localtime()[:6]
        self.canvas.delete(self.text_boxes["time_text_box"].text_item)
        self.canvas.delete(self.text_boxes["time_text_box"].rect_item)
        self.text_boxes["time_text_box"] = TextBox(
            self.canvas, x=1170, y=650, length=110, height=65,
            text=f"{current_time[3]}:{current_time[4]}:{current_time[5]}\n"
                 f"{current_time[1]}/{current_time[2]}/{current_time[0]}"
        )
        self.root.after(1000, self.time_update)


    def menu(self):
        self.text_boxes["title_text_box"] = TextBox(self.canvas, x=15, y=10, text="In Memoriam",
                                                    font=("Times New Roman", 30, "bold"))
        self.buttons["new_game_button"] = Button(self.canvas, x=15, y=110, length=130, height=35, text="New Game",
                                                 command=None)
        self.buttons["load_game_button"] = Button(self.canvas, x=15, y=185, length=135, height=35, text="Load Game",
                                                  command=None)
        self.buttons["quit_button"] = Button(self.canvas, x=15, y=260, length=60, height=35, text="Quit",
                                             command=self.root.destroy)

    def save(self):
        pass


class CanvasObject:
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, tags=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.text = text
        self.font = font
        self.width = width
        self.tags = tags

    @staticmethod
    def make_rect(canvas, x=0.0, y=0.0, length=0.0, height=0.0, fill=None, tags=None):
        return canvas.create_rectangle(x, y, x + length, y + height, fill=fill, tags=tags)

    @staticmethod
    def write(canvas, x=0.0, y=0.0, text="", font=("Times New Roman", 20, "normal"), width=0.0, fill="black",
              tags=None):
        return canvas.create_text(x, y, text=text, anchor="nw", font=font, width=width, fill=fill, tags=tags)

    @staticmethod
    def check_pos(x_start, y_start, length, height, func, event):
        if x_start < event.x < x_start+length and y_start < event.y < y_start+height:
            func()


class TextBox(CanvasObject):
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, tags=None):
        super().__init__(canvas, x=x, y=y, length=length, height=height, text=text, font=font, width=width, tags=tags)
        self.text_item = self.write(self.canvas, self.x, self.y, self.text, self.font, self.width, self.tags)
        if length > 0 and height > 0:
            self.rect_item = self.make_rect(self.canvas, self.x-5, self.y-3, self.length, self.height)


class Button(CanvasObject):
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, command=None, tags=None):
        super().__init__(canvas, x=x, y=y, length=length, height=height, text=text, font=font, width=width, tags=tags)
        self.text_item = self.write(self.canvas, self.x, self.y, self.text, self.font, self.width, self.tags)
        self.rect_item = self.make_rect(self.canvas, self.x-5, self.y-3, self.length, self.height)
        self.command = command
        self.canvas.bind("<Motion>", self.highlighter, add=True)
        if self.command is not None:
            self.canvas.bind("<Button-1>", lambda event: self.check_pos(self.x-5, self.y-3, self.length, self.height,
                                                                        self.command, event))
        self.highlighted = False

    def highlighter(self, event):
        if self.x-5 < event.x < self.x-5+self.length and self.y-3 < event.y < self.y-3+self.height:
            self.canvas.delete(self.text_item)
            self.canvas.delete(self.rect_item)
            self.rect_item = self.make_rect(self.canvas, self.x-5, self.y-3, self.length, self.height, fill="black")
            self.text_item = self.write(self.canvas, self.x, self.y, self.text, self.font, self.width, "white",
                                        self.tags)
            self.highlighted = True
        else:
            if self.highlighted:
                self.canvas.delete(self.text_item)
                self.canvas.delete(self.rect_item)
                self.text_item = self.write(self.canvas, self.x, self.y, self.text, self.font, self.width, self.tags)
                self.rect_item = self.make_rect(self.canvas, self.x-5, self.y-3, self.length, self.height)
                self.highlighted = False


if __name__ == "__main__":
    session = App()
    session.save()

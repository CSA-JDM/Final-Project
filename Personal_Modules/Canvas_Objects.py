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
        if length > 0 and height > 0:
            self.rect_item = self.make_rect(tags=self.tags)
        else:
            self.rect_item = 0
        self.text_item = self.write(tags=self.tags)

    def update(self, x=None, y=None, length=None, height=None, text=None, add=False):
        if text is not None:
            if add:
                if self.text != "":
                    self.text += f"\n{text}"
                elif self.text == "":
                    self.text += f"{text}"
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
        self.rect_item = self.make_rect(tags=self.tags)
        self.text_item = self.write(tags=self.tags)

    def make_rect(self, fill="white", tags=None):
        return self.canvas.create_rectangle(self.x, self.y, self.x + self.length, self.y + self.height,
                                            fill=fill, tags=tags)

    def make_line(self, x1, y1, x2, y2, width=1, fill="black", tags=None):
        return self.canvas.create_line(x1, y1, x2, y2, width=width, fill=fill, tags=tags)

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
            func(event)


class Button(CanvasObject):
    def __init__(self, canvas, x=0.0, y=0.0, length=0.0, height=0.0, text="", font=("Times New Roman", 20, "normal"),
                 width=0.0, command=None, highlighted_command=None, tags=None):
        super().__init__(canvas, x=x, y=y, length=length, height=height, text=text, font=font, width=width,
                         command=command, tags=tags)
        self.highlighted_command = highlighted_command
        self.canvas.bind("<Motion>", lambda event: self.highlighter(self.highlighted_command, event),
                         add=True)
        if self.command is not None:
            self.canvas.bind("<Button-1>", lambda event: [
                self.canvas.delete(self.highlighted_command_object.text_item)
                if self.highlighted_command_object is not None
                else None,
                self.canvas.delete(self.highlighted_command_object.rect_item)
                if self.highlighted_command_object is not None
                else None,
                self.check_pos(self.command, event)
            ], add=True)
        self.highlighted_command_object = None
        self.highlighted = False

    def update(self, x=None, y=None, length=None, height=None, text=None, add=False):
        super().update(x, y, length, height, text, add)
        self.canvas.bind("<Motion>", lambda event: self.highlighter(self.highlighted_command, event), add=True)
        if self.command is not None:
            self.canvas.bind("<Button-1>", lambda event: [
                self.canvas.delete(self.highlighted_command_object.text_item)
                if self.highlighted_command_object is not None
                else None,
                self.canvas.delete(self.highlighted_command_object.rect_item)
                if self.highlighted_command_object is not None
                else None,
                self.check_pos(self.command, event)
            ], add=True)
        if self.highlighted_command_object is not None:
            self.canvas.delete(self.highlighted_command_object.text_item)
            self.canvas.delete(self.highlighted_command_object.rect_item)
        self.highlighted = False

    def highlighter(self, highlighted_command=None, event=None):
        if self.x-5 < event.x < self.x-5+self.length and self.y-3 < event.y < self.y-3+self.height:
            self.canvas.delete(self.text_item)
            self.canvas.delete(self.rect_item)
            self.rect_item = self.make_rect(fill="black")
            self.text_item = self.write(fill="white", tags=self.tags)
            if self.highlighted_command_object is not None:
                self.canvas.delete(self.highlighted_command_object.text_item)
                self.canvas.delete(self.highlighted_command_object.rect_item)
            if highlighted_command is not None:
                self.highlighted_command_object = highlighted_command(event)
            self.highlighted = True
        else:
            if self.highlighted:
                self.canvas.delete(self.text_item)
                self.canvas.delete(self.rect_item)
                self.rect_item = self.make_rect(tags=self.tags)
                self.text_item = self.write(tags=self.tags)
                if self.highlighted_command_object is not None:
                    self.canvas.delete(self.highlighted_command_object.text_item)
                    self.canvas.delete(self.highlighted_command_object.rect_item)
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
        self.rect_item = self.make_rect(tags=self.tags)
        self.text_item = self.write(tags=self.tags)

    def delete_string(self):
        self.text = self.text[:-1]
        self.canvas.delete(self.text_item)
        self.canvas.delete(self.rect_item)
        self.rect_item = self.make_rect(tags=self.tags)
        self.text_item = self.write(tags=self.tags)

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
                self.rect_item = self.make_rect(tags=self.tags)
                self.text_item = self.write(text=self.text+"|", tags=self.tags)
                self.selected = True
            elif self.selected:
                self.update()
                self.selected = False
            self.canvas.after(500, self.selector)

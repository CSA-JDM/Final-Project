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
import time
import random
import turtle


class App:
    def __init__(self):
        self.screen = turtle.Screen()
        turtle.tracer(0, 0)
        self.turtle_ = turtle.Turtle()
        self.turtle_.hideturtle()
        self.turtle_.up()
        self.turtle_.goto(30, -10)
        self.turtle_.down()
        typing = Type()
        next_pos = typing.letter_a((-50, 0), 50)
        typing.letter_a(next_pos, 50)
        self.turtle_.write("Hello, world!", font=("Times New Roman", 30, "normal"))
        turtle.update()
        turtle.mainloop()

    def save(self):
        pass


class Type:
    def __init__(self):
        self.turtle_ = turtle.Turtle()
        self.turtle_.hideturtle()

    def letter_a(self, position, size):
        x_pos, y_pos = position[0], position[1]
        self.turtle_.up()
        self.turtle_.goto(x_pos, y_pos)
        self.turtle_.down()
        self.turtle_.left(70)
        self.turtle_.forward(size)
        top_a = self.turtle_.pos()
        self.turtle_.right(140)
        self.turtle_.forward(size+1)
        new_pos = self.turtle_.pos()
        self.turtle_.up()
        self.turtle_.goto(x_pos+((top_a[0]-x_pos)/2), y_pos+((top_a[1]-y_pos)/2))
        self.turtle_.down()
        self.turtle_.left(70)
        self.turtle_.forward((((top_a[0]-x_pos)*1.5)+((top_a[0]-x_pos)/2))/2)
        return new_pos[0]+5, new_pos[1]+1

    def letter_b(self, position, size):
        x_pos, y_pos = position[0], position[1]
        self.turtle_.up()
        self.turtle_.goto(x_pos, y_pos)
        self.turtle_.down()
        self.turtle_.left(90)
        self.turtle_.forward(size)


class Character:
    def __init__(self):
        pass


class Object:
    def __init__(self):
        pass


class Item:
    def __init__(self):
        pass


class Area:
    def __init__(self):
        pass


class Audio:
    def __init__(self):
        pass


session = App()
session.save()

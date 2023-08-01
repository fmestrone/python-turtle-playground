from turtle import *
from random import random

# Logo, very old programming language, lots of fun with turtle graphics
# https://en.wikipedia.org/wiki/Logo_(programming_language)

pencolor("blue")
forward(100)
right(random() * 180)
backward(100)
left(random() * 180)
pencolor("red")
forward(100)

clearscreen()

# spiral
for steps in range(35):
    for c in ('blue', 'red', 'green'):
        color(c)
        forward(steps)
        right(30)

penup()
goto(0, 0)
pendown()
print(pos())

# filled star
color('red')
fillcolor('yellow')
begin_fill()
while True:
    forward(200)
    left(170)
    if abs(pos()) < 1:
        break
end_fill()

# Two turtles drawing in parallel
# I want to draw two rectangles in parallel, one red, one blue

# Approach 1 - I just go for it

clearscreen()

pencolor("red")
forward(100)

penup()
backward(100)
right(90)
forward(200)
left(90)
pendown()

pencolor("blue")
forward(100)

penup()
left(90)
forward(200)
pendown()
pencolor("red")
forward(100)

penup()
backward(300)
pendown()
pencolor("blue")
forward(100)

penup()
forward(200)
left(90)
pendown()
pencolor("red")
forward(100)

penup()
backward(100)
right(90)
backward(200)

pencolor("blue")
pendown()
left(90)
forward(100)

penup()
left(90)
backward(200)
pendown()
pencolor("red")
forward(100)

penup()
forward(100)

pencolor("blue")
pendown()
forward(100)

penup()
home()

# Approach 2 - variables

clearscreen()

posRed = (0, 0)
headingRed = 0

posBlue = (200, 0)
headingBlue = 0

penup()
goto(posRed)
setheading(headingRed)
pendown()
pencolor("red")
forward(100)
posRed = pos()
headingRed -= 90

penup()
goto(posBlue)
setheading(headingBlue)
pendown()
pencolor("blue")
forward(100)
posBlue = pos()
headingBlue -= 90

penup()
goto(posRed)
setheading(headingRed)
pendown()
pencolor("red")
forward(100)
posRed = pos()
headingRed -= 90

penup()
goto(posBlue)
setheading(headingBlue)
pendown()
pencolor("blue")
forward(100)
posBlue = pos()
headingBlue -= 90

penup()
goto(posRed)
setheading(headingRed)
pendown()
pencolor("red")
forward(100)
posRed = pos()
headingRed -= 90

penup()
goto(posBlue)
setheading(headingBlue)
pendown()
pencolor("blue")
forward(100)
posBlue = pos()
headingBlue -= 90

penup()
goto(posRed)
setheading(headingRed)
pendown()
pencolor("red")
forward(100)
posRed = pos()
headingRed -= 90

penup()
goto(posBlue)
setheading(headingBlue)
pendown()
pencolor("blue")
forward(100)
posBlue = pos()
headingBlue -= 90

# Approach 3 - OOP

clearscreen()

turtleRed = Turtle()
turtleRed.pencolor("red")

turtleBlue = Turtle()
turtleBlue.pencolor("blue")

turtleRed.penup()
turtleRed.goto(0, 0)
turtleRed.setheading(0)
turtleRed.pendown()

turtleBlue.penup()
turtleBlue.goto(200, 0)
turtleRed.setheading(0)
turtleBlue.pendown()

turtleRed.forward(100)
turtleBlue.forward(100)

turtleRed.left(90)
turtleBlue.left(90)

turtleRed.forward(100)
turtleBlue.forward(100)

turtleRed.left(90)
turtleBlue.left(90)

turtleRed.forward(100)
turtleBlue.forward(100)

turtleRed.left(90)
turtleBlue.left(90)

turtleRed.forward(100)
turtleBlue.forward(100)

import sys
from tkinter import END

import pygments.lexers
import tkinter as tk
import tkinter.ttk as tkk
import tkinter.messagebox as msgbox
from io import StringIO
from chlorophyll import CodeView

from turtle import Turtle, TurtleScreen

config = {
    "clear_after_execute": True,
    "pop_up_on_stdout": True,
    "pop_up_on_stderr": True,
    "single_pane": False,
}

canvas_locals = {}
canvas_globals = {}

command_history = []
stdout_console = []
stderr_console = []


def setup_turtle_context():
    if config["single_pane"]:
        turtle_canvas = tk.Canvas(root, height=600, width=800)
        turtle_canvas.pack()
        turtle_screen = TurtleScreen(turtle_canvas)
        Turtle._screen = turtle_screen

    turtle_commands = """
from turtle import *
from random import random

# makes sure the screen pops up and the turtle shows
home()
"""
    exec(turtle_commands, canvas_globals, canvas_locals)


def add_command_history(command):
    command_history.append(command)


def add_stdout_entry(message):
    stdout_console.append(message)
    if message:
        print("TURTLE_STDOUT: ", message)
        if config["pop_up_on_stdout"]:
            msgbox.showerror(title="Turtle Says", message=message)


def add_stderr_entry(err, cmd):
    stderr_console.append({
        "error": err,
        "command": cmd
    })
    if err:
        print("TURTLE_STDERR: ", err)
        if config["pop_up_on_stdout"]:
            msgbox.showinfo(title="Turtle Has A Problem!", message=err)


def execute():
    turtle_command = code_view.get("1.0", "end-1c")
    old_stdout = sys.stdout
    turtle_stdout = sys.stdout = StringIO()
    try:
        exec(turtle_command, canvas_globals, canvas_locals)
    except Exception as err:
        sys.stdout = old_stdout
        add_stdout_entry(turtle_stdout.getvalue())
        add_stderr_entry(err, turtle_command)
    else:
        sys.stdout = old_stdout
        add_command_history(turtle_command)
        add_stdout_entry(turtle_stdout.getvalue())
        if config["clear_after_execute"]:
            code_view.delete('1.0', END)


def show_last_command():
    code_view.delete('1.0', END)
    code_view.insert("1.0", command_history[-1])


root = tk.Tk()
root.title("Python Turtle Editor")
editor = tkk.PanedWindow(root, height=600, width=800)
editor.pack()

code_view = CodeView(editor, lexer=pygments.lexers.PythonLexer, color_scheme="monokai", font=("Courier New", 17))
code_view.pack()

button = tkk.Button(editor, text="Last Command", command=lambda: show_last_command())
button.pack()
button = tkk.Button(editor, text="Execute", command=lambda: execute())
button.pack()

setup_turtle_context()

root.mainloop()

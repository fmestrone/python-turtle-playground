import sys
import pygments.lexers
import tomllib

import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as tkk

from io import StringIO
from turtle import Turtle, TurtleScreen
from chlorophyll import CodeView
from textwrap import dedent

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

current_turtle_canvas_size = (0, 0)


def setup_turtle_context():
    turtle_commands = """\
        from turtle import *
        from random import random

        # makes sure the screen pops up and the turtle shows
        home()
    """
    exec(dedent(turtle_commands), canvas_globals, canvas_locals)


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
            code_view.delete('1.0', "end")


def on_turtle_canvas_resize(event):
    global current_turtle_canvas_size
    cw, ch = current_turtle_canvas_size[0], current_turtle_canvas_size[1]
    nw, nh = event.width, event.height
    if event.widget == turtle_canvas and (cw != nw or ch != nh):
        turtle_canvas.config(scrollregion=(-nw // 2, -nh // 2, nw // 2, nh // 2))
        current_turtle_canvas_size = (nw, nh)


def show_last_command():
    code_view.delete('1.0', "end")
    code_view.insert("1.0", command_history[-1])


try:
    with open("playground.toml", "rb") as cfgfile:
        cfgdata = tomllib.load(cfgfile)
        config |= cfgdata
except OSError:
    pass

root = tk.Tk()
root.title("Python Turtle Editor")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

editor_area = tkk.Frame(root)
editor_area.grid(row=0, column=0, sticky="NSEW")
editor_area.columnconfigure(0, weight=1)
if config["single_pane"]:
    editor_area.columnconfigure(1, weight=2)
editor_area.rowconfigure(0, weight=1)
editor_area.rowconfigure(1, weight=0)
editor_area.rowconfigure(2, weight=0)

code_view = CodeView(editor_area, lexer=pygments.lexers.PythonLexer, color_scheme="monokai",
                     font=("Courier New", 17), width=50)
code_view.grid(row=0, column=0, sticky="NSEW")

if config["single_pane"]:
    turtle_canvas = tk.Canvas(editor_area, width=900)
    turtle_canvas.grid(row=0, rowspan=3, column=1, sticky="NSEW")
    turtle_canvas.bind('<Configure>', on_turtle_canvas_resize)
    turtle_screen = TurtleScreen(turtle_canvas)
    Turtle._screen = turtle_screen

button = tkk.Button(editor_area, text="Last Command", command=lambda: show_last_command())
button.grid(row=1, column=0)

button = tkk.Button(editor_area, text="Execute", command=lambda: execute())
button.grid(row=2, column=0)

setup_turtle_context()

root.mainloop()

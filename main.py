from tkinter import *
import math

master = Tk()
master.title("2D Shape Engine")

# Main layout
frame = Frame(master)
frame.pack()

canvas = Canvas(frame, width=500, height=500, bg="white")
canvas.grid(row=0, column=0)

square_list = Listbox(frame, height=15)
square_list.grid(row=0, column=1, padx=10)

control_frame = Frame(frame)
control_frame.grid(row=0, column=2, padx=10)

# Square list
square_list = Listbox(frame, height=15)
square_list.grid(row=0, column=1, padx=10)


# Variables
scale_var = IntVar(value=100)
rotate_var = IntVar(value=0)
move_x_var = IntVar(value=250)
move_y_var = IntVar(value=250)


# Store squares
squares = []

# Current selected square index
selected_index = None

button_frame = Frame(master)
button_frame.pack()




def draw_squares():

    canvas.delete("square")

    for index, square in enumerate(squares):

        size = square["size"] * square["scale"]

        outline = "red" if index == selected_index else "black"

        if square["type"] == "square":

            points = [
                (-size/2, -size/2),
                (size/2, -size/2),
                (size/2, size/2),
                (-size/2, size/2)
            ]

            angle = math.radians(square["rotation"])

            rotated = []

            for x, y in points:
                new_x = x * math.cos(angle) - y * math.sin(angle)
                new_y = x * math.sin(angle) + y * math.cos(angle)
                rotated.extend([
                    square["x"] + new_x,
                    square["y"] + new_y
                ])

            canvas.create_polygon(
                rotated,
                fill=square["color"],
                outline=outline,
                width=3,
                tags="square"
            )

        elif square["type"] == "triangle":

            points = [
                (0, -size/2),
                (-size/2, size/2),
                (size/2, size/2)
            ]

            angle = math.radians(square["rotation"])

            rotated = []

            for x, y in points:
                new_x = x * math.cos(angle) - y * math.sin(angle)
                new_y = x * math.sin(angle) + y * math.cos(angle)
                rotated.extend([
                    square["x"] + new_x,
                    square["y"] + new_y
                ])

            canvas.create_polygon(
                rotated,
                fill=square["color"],
                outline=outline,
                width=3,
                tags="square"
            )

        elif square["type"] == "circle":

            r = size / 2

            canvas.create_oval(
                square["x"] - r,
                square["y"] - r,
                square["x"] + r,
                square["y"] + r,
                fill=square["color"],
                outline=outline,
                width=3,
                tags="square"
            )

def add_square():

    new_square = {
        "type": "square",
        "x": 250,
        "y": 250,
        "size": 100,
        "scale": 1,
        "rotation": 0,
        "color": "skyblue"
    }

    squares.append(new_square)

    square_list.insert(END, "Square " + str(len(squares)))

    square_list.selection_clear(0, END)
    square_list.selection_set(END)

    select_square(None)


def select_square(event):

    global selected_index

    selection = square_list.curselection()

    if not selection:
        return

    selected_index = selection[0]

    square = squares[selected_index]

    # Update sliders
    scale_var.set(int(square["scale"] * 100))
    rotate_var.set(square["rotation"])
    move_x_var.set(square["x"])
    move_y_var.set(square["y"])

    draw_squares()



def update_sliders(value):

    if selected_index is None:
        return

    square = squares[selected_index]

    square["scale"] = scale_var.get() / 100
    square["rotation"] = rotate_var.get()
    square["x"] = move_x_var.get()
    square["y"] = move_y_var.get()

    draw_squares()

def delete_square():
    global selected_index

    if selected_index is None:
        return

    # Remove from the data list
    squares.pop(selected_index)

    # Remove from the Listbox
    square_list.delete(selected_index)

    if not squares:
        # No squares left
        selected_index = None
    else:
        # Select the previous item if possible
        if selected_index >= len(squares):
            selected_index = len(squares) - 1

        square_list.selection_set(selected_index)

        # Update sliders for the new selection
        select_square(None)

    draw_squares()

def change_color(color):

    if selected_index is None:
        return

    squares[selected_index]["color"] = color
    draw_squares()

def add_triangle():

    triangle = {
        "type": "triangle",
        "x": 250,
        "y": 250,
        "size": 100,
        "scale": 1,
        "rotation": 0,
        "color": "lightgreen"
    }

    squares.append(triangle)

    square_list.insert(END, "Triangle " + str(len(squares)))

    square_list.selection_clear(0, END)
    square_list.selection_set(END)

    select_square(None)

def add_circle():

    circle = {
        "type": "circle",
        "x": 250,
        "y": 250,
        "size": 100,
        "scale": 1,
        "rotation": 0,
        "color": "lightblue"
    }

    squares.append(circle)

    square_list.insert(END, "Circle " + str(len(squares)))

    square_list.selection_clear(0, END)
    square_list.selection_set(END)

    select_square(None)



# Connect list click
square_list.bind("<<ListboxSelect>>", select_square)


# Sliders

Scale(
    control_frame,
    from_=10,
    to=300,
    label="Scale",
    variable=scale_var,
    command=update_sliders
).pack()


Scale(
    control_frame,
    from_=0,
    to=360,
    label="Rotation",
    variable=rotate_var,
    command=update_sliders
).pack()


Scale(
    control_frame,
    from_=0,
    to=500,
    label="Move X",
    orient=HORIZONTAL,
    variable=move_x_var,
    command=update_sliders
).pack()


Scale(
    control_frame,
    from_=0,
    to=500,
    label="Move Y",
    orient=HORIZONTAL,
    variable=move_y_var,
    command=update_sliders
).pack()



Button(
    button_frame,
    text="Add Square",
    command=add_square
).grid(row=0, column=0, padx=5, pady=5)

Button(
    button_frame,
    text="Delete Shape",
    command=delete_square
).grid(row=0, column=1, padx=5, pady=5)


Button(
    button_frame,
    text="Red",
    command=lambda: change_color("red")
).grid(row=1, column=0, padx=5, pady=5)

Button(
    button_frame,
    text="Green",
    command=lambda: change_color("green")
).grid(row=1, column=1, padx=5, pady=5)

Button(
    button_frame,
    text="Blue",
    command=lambda: change_color("blue")
).grid(row=1, column=2, padx=5, pady=5)

Button(
    button_frame,
    text="Yellow",
    command=lambda: change_color("yellow")
).grid(row=1, column=3, padx=5, pady=5)


Button(
    button_frame,
    text="Add Triangle",
    command=add_triangle
).grid(row=2, column=0, padx=5, pady=5)

Button(
    button_frame,
    text="Add Circle",
    command=add_circle
).grid(row=2, column=1, padx=5, pady=5)

# First square
add_square()


mainloop()

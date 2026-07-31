from tkinter import *
import math

master = Tk()
master.title("2D Shape Engine")

# Main layout
frame = Frame(master)
frame.pack()

canvas = Canvas(frame, width=300, height=300, bg="white")
canvas.grid(row=0, column=0)

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


def draw_squares():
    canvas.delete("square")

    for index, square in enumerate(squares):

        size = square["size"] * square["scale"]

        points = [
            (-size/2, -size/2),
            (size/2, -size/2),
            (size/2, size/2),
            (-size/2, size/2)
        ]

        angle = math.radians(square["rotation"])

        rotated_points = []

        for x, y in points:
            new_x = x * math.cos(angle) - y * math.sin(angle)
            new_y = x * math.sin(angle) + y * math.cos(angle)

            rotated_points.append(
                (
                    square["x"] + new_x,
                    square["y"] + new_y
                )
            )

        flat_points = []

        for x, y in rotated_points:
            flat_points.extend([x, y])


        outline = "red" if index == selected_index else "black"

        canvas.create_polygon(
            flat_points,
            fill="skyblue",
            outline=outline,
            width=3,
            tags="square"
        )


def add_square():

    new_square = {
        "x": 250,
        "y": 250,
        "size": 100,
        "scale": 1,
        "rotation": 0
    }

    squares.append(new_square)

    square_list.insert(
        END,
        "Square " + str(len(squares))
    )

    # Select new square
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



# Connect list click
square_list.bind("<<ListboxSelect>>", select_square)


# Sliders

Scale(
    master,
    from_=10,
    to=300,
    label="Scale",
    variable=scale_var,
    command=update_sliders
).pack()


Scale(
    master,
    from_=0,
    to=360,
    label="Rotation",
    variable=rotate_var,
    command=update_sliders
).pack()


Scale(
    master,
    from_=0,
    to=500,
    label="Move X",
    orient=HORIZONTAL,
    variable=move_x_var,
    command=update_sliders
).pack()


Scale(
    master,
    from_=0,
    to=500,
    label="Move Y",
    orient=HORIZONTAL,
    variable=move_y_var,
    command=update_sliders
).pack()



Button(
    master,
    text="Add Square",
    command=add_square
).pack()


# First square
add_square()


mainloop()

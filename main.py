from tkinter import *
import math

master = Tk()
master.title("2D Shape Engine")

# Shape properties
square = {
    "x": 250,
    "y": 250,
    "size": 100,
    "scale": 1,
    "rotation": 0
}

canvas = Canvas(master, width=300, height=300, bg="white")
canvas.pack()

# Variables
scale_var = IntVar(value=100)
rotate_var = IntVar(value=0)
move_x_var = IntVar(value=250)
move_y_var = IntVar(value=250)


def draw_square():
    canvas.delete("square")

    size = square["size"] * square["scale"]

    # Original square points
    points = [
        (-size/2, -size/2),
        (size/2, -size/2),
        (size/2, size/2),
        (-size/2, size/2)
    ]

    angle = math.radians(square["rotation"])

    rotated_points = []

    # Rotate every point
    for x, y in points:
        new_x = x * math.cos(angle) - y * math.sin(angle)
        new_y = x * math.sin(angle) + y * math.cos(angle)

        rotated_points.append(
            (square["x"] + new_x,
             square["y"] + new_y)
        )

    # Flatten points for tkinter
    flat_points = []
    for p in rotated_points:
        flat_points.extend(p)

    canvas.create_polygon(
        flat_points,
        fill="skyblue",
        outline="black",
        width=2,
        tags="square"
    )


def update_sliders(value):
    square["scale"] = scale_var.get() / 100
    square["rotation"] = rotate_var.get()
    square["x"] = move_x_var.get()
    square["y"] = move_y_var.get()

    draw_square()


# Scale slider
Scale(
    master,
    from_=10,
    to=300,
    label="Scale",
    variable=scale_var,
    command=update_sliders
).pack()


# Rotation slider
Scale(
    master,
    from_=0,
    to=360,
    label="Rotation",
    variable=rotate_var,
    command=update_sliders
).pack()


# X movement
Scale(
    master,
    from_=0,
    to=500,
    orient=HORIZONTAL,
    label="Move X",
    variable=move_x_var,
    command=update_sliders
).pack()


# Y movement
Scale(
    master,
    from_=0,
    to=500,
    orient=HORIZONTAL,
    label="Move Y",
    variable=move_y_var,
    command=update_sliders
).pack()


draw_square()

mainloop()

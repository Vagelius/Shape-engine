from tkinter import *
from tkinter import ttk, filedialog, colorchooser
import math
import json
import copy as copy_module
from PIL import ImageGrab


# ---------------------------------------------------------------------------
# Window setup
# ---------------------------------------------------------------------------

master = Tk()
master.title("2D Shape Engine")
master.configure(bg="#f4f5f7")
master.resizable(False, False)

# --- A simple, cohesive color palette used across the whole UI -------------
BG_APP = "#f4f5f7"
BG_PANEL = "#ffffff"
BG_CANVAS = "#ffffff"
ACCENT = "#4a6cf7"
ACCENT_DARK = "#3b57d1"
TEXT_DARK = "#22262b"
TEXT_MUTED = "#6b7280"
BORDER = "#e2e4e9"

FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_HEADING = ("Segoe UI", 11, "bold")

# ---------------------------------------------------------------------------
# ttk styling — this is what makes the buttons/sliders look modern instead
# of the default grey OS widgets. ttk.Style lets you theme every widget
# class in one place instead of setting options on each button separately.
# ---------------------------------------------------------------------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "App.TFrame",
    background=BG_APP
)

style.configure(
    "Panel.TFrame",
    background=BG_PANEL,
    relief="flat"
)

style.configure(
    "TLabel",
    background=BG_PANEL,
    foreground=TEXT_DARK,
    font=FONT_MAIN
)

style.configure(
    "Heading.TLabel",
    background=BG_PANEL,
    foreground=TEXT_DARK,
    font=FONT_HEADING
)

# Primary action button (blue, filled)
style.configure(
    "Accent.TButton",
    background=ACCENT,
    foreground="white",
    font=FONT_BOLD,
    padding=(10, 8),
    borderwidth=0,
    focusthickness=0,
    relief="flat"
)
style.map(
    "Accent.TButton",
    background=[("active", ACCENT_DARK), ("pressed", ACCENT_DARK)]
)

# Secondary / neutral button
style.configure(
    "Ghost.TButton",
    background=BG_PANEL,
    foreground=TEXT_DARK,
    font=FONT_MAIN,
    padding=(10, 8),
    borderwidth=1,
    relief="solid"
)
style.map(
    "Ghost.TButton",
    background=[("active", "#eef0f4")],
    bordercolor=[("!disabled", BORDER)]
)

# Destructive button (delete)
style.configure(
    "Danger.TButton",
    background="#fdecec",
    foreground="#c62828",
    font=FONT_BOLD,
    padding=(10, 8),
    borderwidth=0,
    relief="flat"
)
style.map(
    "Danger.TButton",
    background=[("active", "#f9d4d4")]
)

style.configure(
    "TScale",
    background=BG_PANEL,
    troughcolor="#e6e8ee"
)

style.configure(
    "TLabelframe",
    background=BG_PANEL,
    bordercolor=BORDER,
    relief="solid"
)
style.configure(
    "TLabelframe.Label",
    background=BG_PANEL,
    foreground=TEXT_MUTED,
    font=("Segoe UI", 9, "bold")
)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

frame = ttk.Frame(master, style="App.TFrame", padding=12)
frame.pack()

# --- Canvas panel -----------------------------------------------------------
canvas_panel = ttk.Frame(frame, style="Panel.TFrame", padding=2)
canvas_panel.grid(row=0, column=0, sticky="n")

canvas = Canvas(canvas_panel, width=500, height=500, bg=BG_CANVAS,
                 highlightthickness=1, highlightbackground=BORDER)
canvas.pack()

# --- Right side: shape list + controls stacked in one panel ----------------
side_panel = ttk.Frame(frame, style="Panel.TFrame")
side_panel.grid(row=0, column=1, padx=(12, 0), sticky="n")

ttk.Label(side_panel, text="Shapes", style="Heading.TLabel").pack(
    anchor="w", pady=(0, 4)
)

list_frame = ttk.Frame(side_panel, style="Panel.TFrame")
list_frame.pack(fill="x")

square_list = Listbox(
    list_frame, height=10, width=22,
    bg="#fafbfc", fg=TEXT_DARK,
    selectbackground=ACCENT, selectforeground="white",
    highlightthickness=1, highlightbackground=BORDER,
    relief="flat", font=FONT_MAIN, activestyle="none"
)
square_list.pack(side="left", fill="both")

list_scroll = ttk.Scrollbar(list_frame, orient=VERTICAL, command=square_list.yview)
list_scroll.pack(side="right", fill="y")
square_list.config(yscrollcommand=list_scroll.set)

control_frame = ttk.Frame(side_panel, style="Panel.TFrame")
control_frame.pack(fill="x", pady=(12, 0))

# --- Bottom panel: add/edit/color/copy buttons ------------------------------
button_panel = ttk.Frame(master, style="App.TFrame", padding=(12, 0, 12, 12))
button_panel.pack(fill="x")


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

scale_var = IntVar(value=100)
rotate_var = IntVar(value=0)
move_x_var = IntVar(value=250)
move_y_var = IntVar(value=250)

squares = []
selected_index = None
clipboard_shape = None   # holds a copied shape's data for paste


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def draw_squares():

    canvas.delete("square")

    for index, square in enumerate(squares):

        size = square["size"] * square["scale"]

        outline = ACCENT if index == selected_index else "black"
        width = 3 if index == selected_index else 2

        if square["type"] == "square":

            points = [
                (-size / 2, -size / 2),
                (size / 2, -size / 2),
                (size / 2, size / 2),
                (-size / 2, size / 2)
            ]

            angle = math.radians(square["rotation"])
            rotated = []

            for x, y in points:
                new_x = x * math.cos(angle) - y * math.sin(angle)
                new_y = x * math.sin(angle) + y * math.cos(angle)
                rotated.extend([square["x"] + new_x, square["y"] + new_y])

            canvas.create_polygon(
                rotated, fill=square["color"], outline=outline,
                width=width, tags="square"
            )

        elif square["type"] == "triangle":

            points = [
                (0, -size / 2),
                (-size / 2, size / 2),
                (size / 2, size / 2)
            ]

            angle = math.radians(square["rotation"])
            rotated = []

            for x, y in points:
                new_x = x * math.cos(angle) - y * math.sin(angle)
                new_y = x * math.sin(angle) + y * math.cos(angle)
                rotated.extend([square["x"] + new_x, square["y"] + new_y])

            canvas.create_polygon(
                rotated, fill=square["color"], outline=outline,
                width=width, tags="square"
            )

        elif square["type"] == "circle":

            r = size / 2

            canvas.create_oval(
                square["x"] - r, square["y"] - r,
                square["x"] + r, square["y"] + r,
                fill=square["color"], outline=outline,
                width=width, tags="square"
            )


# ---------------------------------------------------------------------------
# Shape creation / selection / deletion
# ---------------------------------------------------------------------------

def _add_shape(shape_type, color):

    shape = {
        "type": shape_type,
        "x": 250,
        "y": 250,
        "size": 100,
        "scale": 1,
        "rotation": 0,
        "color": color
    }

    squares.append(shape)
    square_list.insert(END, shape_type.capitalize() + " " + str(len(squares)))
    square_list.selection_clear(0, END)
    square_list.selection_set(END)

    select_square(None)


def add_square():
    _add_shape("square", "skyblue")


def add_triangle():
    _add_shape("triangle", "lightgreen")


def add_circle():
    _add_shape("circle", "lightblue")


def select_square(event):

    global selected_index

    selection = square_list.curselection()

    if not selection:
        return

    selected_index = selection[0]
    square = squares[selected_index]

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

    squares.pop(selected_index)
    square_list.delete(selected_index)

    if not squares:
        selected_index = None
    else:
        if selected_index >= len(squares):
            selected_index = len(squares) - 1

        square_list.selection_set(selected_index)
        select_square(None)

    draw_squares()


def change_color(color):

    if selected_index is None:
        return

    squares[selected_index]["color"] = color
    draw_squares()


def choose_custom_color():

    if selected_index is None:
        return

    rgb, hex_color = colorchooser.askcolor(
        title="Choose a color",
        initialcolor=squares[selected_index]["color"]
    )

    if hex_color:
        change_color(hex_color)


# ---------------------------------------------------------------------------
# Copy / paste
# ---------------------------------------------------------------------------

def copy_shape(event=None):

    global clipboard_shape

    if selected_index is None:
        return

    clipboard_shape = copy_module.deepcopy(squares[selected_index])


def paste_shape(event=None):

    if clipboard_shape is None:
        return

    new_shape = copy_module.deepcopy(clipboard_shape)
    new_shape["x"] = min(new_shape["x"] + 20, 500)
    new_shape["y"] = min(new_shape["y"] + 20, 500)

    squares.append(new_shape)
    square_list.insert(END, new_shape["type"].capitalize() + " " + str(len(squares)))
    square_list.selection_clear(0, END)
    square_list.selection_set(END)

    select_square(None)


def duplicate_shape():
    """Copy then immediately paste the selected shape."""
    copy_shape()
    paste_shape()


# ---------------------------------------------------------------------------
# Save / open
# ---------------------------------------------------------------------------

def save_project():

    file = filedialog.asksaveasfilename(
        defaultextension=".spza",
        filetypes=[("Shape Project", "*.spza"), ("PNG Image", "*.png")]
    )

    if not file:
        return

    if file.endswith(".spza"):
        with open(file, "w") as f:
            json.dump(squares, f, indent=4)
        print("Project saved")

    elif file.endswith(".png"):
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        image = ImageGrab.grab((x, y, x + width, y + height))
        image.save(file)
        print("PNG saved")


def open_project():

    file = filedialog.askopenfilename(filetypes=[("Shape Project", "*.spza")])

    if not file:
        return

    with open(file, "r") as f:
        loaded = json.load(f)

    squares.clear()
    square_list.delete(0, END)

    for shape in loaded:
        squares.append(shape)
        square_list.insert(END, shape["type"].capitalize())

    draw_squares()


def save_image():

    file = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")]
    )

    if not file:
        return

    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    image = ImageGrab.grab((x, y, x + width, y + height))
    image.save(file)
    print("Image saved:", file)


# ---------------------------------------------------------------------------
# Bindings
# ---------------------------------------------------------------------------

square_list.bind("<<ListboxSelect>>", select_square)
master.bind("<Control-c>", copy_shape)
master.bind("<Control-v>", paste_shape)
master.bind("<Delete>", lambda e: delete_square())


# ---------------------------------------------------------------------------
# Sliders (styled ttk.Scale + a live value label so numbers are readable)
# ---------------------------------------------------------------------------

def _labeled_scale(parent, text, var, from_, to, orient=VERTICAL):

    row = ttk.Frame(parent, style="Panel.TFrame")
    row.pack(fill="x", pady=4)

    header = ttk.Frame(row, style="Panel.TFrame")
    header.pack(fill="x")

    ttk.Label(header, text=text).pack(side="left")
    value_label = ttk.Label(header, text=str(var.get()), foreground=TEXT_MUTED)
    value_label.pack(side="right")

    def on_change(v):
        value_label.config(text=str(var.get()))
        update_sliders(v)

    scale = ttk.Scale(
        row, from_=from_, to=to, orient=HORIZONTAL,
        variable=var, command=on_change
    )
    scale.pack(fill="x")

    return scale


_labeled_scale(control_frame, "Scale", scale_var, 10, 300)
_labeled_scale(control_frame, "Rotation", rotate_var, 0, 360)
_labeled_scale(control_frame, "Move X", move_x_var, 0, 500)
_labeled_scale(control_frame, "Move Y", move_y_var, 0, 500)


# ---------------------------------------------------------------------------
# Color palette — a grid of clickable swatches instead of 4 plain buttons
# ---------------------------------------------------------------------------

PALETTE_COLORS = [
    "#e74c3c", "#e67e22", "#f1c40f", "#2ecc71",
    "#1abc9c", "#3498db", "#9b59b6", "#fd79a8",
    "#8d6e63", "#95a5a6", "#2c3e50", "#ffffff",
]

palette_section = ttk.Frame(button_panel, style="App.TFrame")
palette_section.grid(row=0, column=0, sticky="nw", padx=(0, 20))

ttk.Label(
    palette_section, text="Color palette",
    background=BG_APP, foreground=TEXT_DARK, font=FONT_BOLD
).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 6))

for i, color in enumerate(PALETTE_COLORS):
    swatch = Button(
        palette_section,
        bg=color, activebackground=color,
        width=2, height=1, relief="flat",
        highlightthickness=1, highlightbackground=BORDER,
        cursor="hand2",
        command=lambda c=color: change_color(c)
    )
    swatch.grid(row=1 + i // 6, column=i % 6, padx=3, pady=3)

ttk.Button(
    palette_section, text="Custom\u2026", style="Ghost.TButton",
    command=choose_custom_color
).grid(row=1, column=6, rowspan=2, padx=(10, 0), sticky="ns")


# ---------------------------------------------------------------------------
# Action buttons, grouped by purpose
# ---------------------------------------------------------------------------

actions_section = ttk.Frame(button_panel, style="App.TFrame")
actions_section.grid(row=0, column=1, sticky="nw")

# Add shapes
add_row = ttk.Frame(actions_section, style="App.TFrame")
add_row.pack(anchor="w", pady=(0, 6))

ttk.Button(add_row, text="+ Square", style="Accent.TButton",
           command=add_square).pack(side="left", padx=(0, 6))
ttk.Button(add_row, text="+ Triangle", style="Accent.TButton",
           command=add_triangle).pack(side="left", padx=(0, 6))
ttk.Button(add_row, text="+ Circle", style="Accent.TButton",
           command=add_circle).pack(side="left")

# Edit shapes (copy / paste / duplicate / delete)
edit_row = ttk.Frame(actions_section, style="App.TFrame")
edit_row.pack(anchor="w", pady=(0, 6))

ttk.Button(edit_row, text="Copy  (Ctrl+C)", style="Ghost.TButton",
           command=copy_shape).pack(side="left", padx=(0, 6))
ttk.Button(edit_row, text="Paste  (Ctrl+V)", style="Ghost.TButton",
           command=paste_shape).pack(side="left", padx=(0, 6))
ttk.Button(edit_row, text="Duplicate", style="Ghost.TButton",
           command=duplicate_shape).pack(side="left", padx=(0, 6))
ttk.Button(edit_row, text="Delete", style="Danger.TButton",
           command=delete_square).pack(side="left")

# File actions
file_row = ttk.Frame(actions_section, style="App.TFrame")
file_row.pack(anchor="w")

ttk.Button(file_row, text="Save", style="Ghost.TButton",
           command=save_project).pack(side="left", padx=(0, 6))
ttk.Button(file_row, text="Open", style="Ghost.TButton",
           command=open_project).pack(side="left", padx=(0, 6))
ttk.Button(file_row, text="Export PNG", style="Ghost.TButton",
           command=save_image).pack(side="left")


# ---------------------------------------------------------------------------
# First square, so the canvas isn't empty on launch
# ---------------------------------------------------------------------------

add_square()

mainloop()

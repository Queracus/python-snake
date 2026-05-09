import tkinter as tk
from tkinter import ttk
from controls import ControlScheme


class MainMenu:
    def __init__(self, root: tk.Tk, on_start: callable):
        self.root = root
        self.on_start = on_start
        self.selected_level = tk.IntVar(value=1)
        self.selected_controls = tk.IntVar(value=0)

        self._create_menu_frame()
        self._create_widgets()

    def _create_menu_frame(self):
        self.menu_frame = tk.Frame(self.root, bg="#2d2d2d", width=400, height=400)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        self.menu_frame.pack_propagate(False)

    def _create_widgets(self):
        title = tk.Label(
            self.menu_frame,
            text="SNAKE",
            font=("Arial", 48, "bold"),
            bg="#2d2d2d",
            fg="#00ff00"
        )
        title.pack(pady=40)

        level_label = tk.Label(
            self.menu_frame,
            text="Select Level:",
            font=("Arial", 14),
            bg="#2d2d2d",
            fg="white"
        )
        level_label.pack(pady=10)

        level_combo = ttk.Combobox(
            self.menu_frame,
            textvariable=self.selected_level,
            values=list(range(1, 11)),
            state="readonly",
            font=("Arial", 12),
            width=10
        )
        level_combo.pack()
        level_combo.current(0)

        control_label = tk.Label(
            self.menu_frame,
            text="Control Scheme:",
            font=("Arial", 14),
            bg="#2d2d2d",
            fg="white"
        )
        control_label.pack(pady=20)

        control_frame = tk.Frame(self.menu_frame, bg="#2d2d2d")
        control_frame.pack()

        arrows_radio = tk.Radiobutton(
            control_frame,
            text="Arrow Keys",
            variable=self.selected_controls,
            value=0,
            font=("Arial", 12),
            bg="#2d2d2d",
            fg="white",
            selectcolor="#444444"
        )
        arrows_radio.pack(side=tk.LEFT, padx=10)

        wasd_radio = tk.Radiobutton(
            control_frame,
            text="WASD",
            variable=self.selected_controls,
            value=1,
            font=("Arial", 12),
            bg="#2d2d2d",
            fg="white",
            selectcolor="#444444"
        )
        wasd_radio.pack(side=tk.LEFT, padx=10)

        start_button = tk.Button(
            self.menu_frame,
            text="Start Game",
            font=("Arial", 16, "bold"),
            bg="#00aa00",
            fg="white",
            width=12,
            height=2,
            command=self._on_start_clicked
        )
        start_button.pack(pady=40)

    def _on_start_clicked(self):
        level = self.selected_level.get()
        control_scheme = (
            ControlScheme.ARROWS if self.selected_controls.get() == 0
            else ControlScheme.WASD
        )
        self.hide()
        self.on_start(level, control_scheme)

    def show(self):
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.menu_frame.pack_forget()


def create_menu(root: tk.Tk, on_start: callable) -> MainMenu:
    return MainMenu(root, on_start)
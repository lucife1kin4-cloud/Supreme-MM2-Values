import json
import tkinter as tk
from tkinter import colorchooser, ttk
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = APP_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "text_color": "#FFFFFF",
    "font_family": "Arial",
    "font_size": 14,
    "refresh_minutes": 5,
    "display_enabled": True,
    "source": "Supreme Values",
}


def load_settings():
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        loaded = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        settings = DEFAULT_SETTINGS.copy()
        settings.update(loaded)
        return settings
    except (OSError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    SETTINGS_FILE.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


class SupremeMM2App:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()

        self.root.title("Supreme MM2 Values")
        self.root.geometry("560x430")
        self.root.minsize(480, 380)
        self.root.configure(bg="#17191F")

        self.text_color = tk.StringVar(value=self.settings["text_color"])
        self.font_family = tk.StringVar(value=self.settings["font_family"])
        self.font_size = tk.IntVar(value=int(self.settings["font_size"]))
        self.refresh_minutes = tk.IntVar(
            value=int(self.settings["refresh_minutes"])
        )
        self.display_enabled = tk.BooleanVar(
            value=bool(self.settings["display_enabled"])
        )
        self.source = tk.StringVar(value=self.settings["source"])

        self._configure_theme()
        self._build_header()
        self._build_tabs()
        self._build_status()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_preview()

    def _configure_theme(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TNotebook",
            background="#17191F",
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            background="#292D36",
            foreground="#E8EAF0",
            padding=(18, 9),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#414856")],
            foreground=[("selected", "#FFFFFF")],
        )
        style.configure(
            "TCombobox",
            fieldbackground="#292D36",
            background="#292D36",
            foreground="#FFFFFF",
        )

    def _build_header(self):
        header = tk.Frame(self.root, bg="#17191F")
        header.pack(fill="x", padx=18, pady=(16, 10))

        tk.Label(
            header,
            text="SUPREME",
            bg="#17191F",
            fg="#FFFFFF",
            font=("Arial", 18, "bold"),
        ).pack(side="left")

        tk.Label(
            header,
            text="MM2 VALUES",
            bg="#17191F",
            fg="#AAB2C0",
            font=("Arial", 18, "bold"),
        ).pack(side="left", padx=(7, 0))

        self.enabled_label = tk.Label(
            header,
            text="ON" if self.display_enabled.get() else "OFF",
            bg="#17191F",
            fg="#67D391" if self.display_enabled.get() else "#F08A8A",
            font=("Arial", 10, "bold"),
        )
        self.enabled_label.pack(side="right")

    def _build_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=5)

        self.appearance_tab = tk.Frame(self.tabs, bg="#20232B")
        self.values_tab = tk.Frame(self.tabs, bg="#20232B")

        self.tabs.add(self.appearance_tab, text="Appearance")
        self.tabs.add(self.values_tab, text="Values")

        self._build_appearance_tab()
        self._build_values_tab()

    def _section_label(self, parent, text):
        return tk.Label(
            parent,
            text=text,
            bg="#20232B",
            fg="#AAB2C0",
            font=("Arial", 9, "bold"),
        )

    def _build_appearance_tab(self):
        tab = self.appearance_tab

        self._section_label(tab, "TRADE DISPLAY").pack(
            anchor="w", padx=20, pady=(18, 8)
        )

        toggle = tk.Checkbutton(
            tab,
            text="Enable value display",
            variable=self.display_enabled,
            command=self.on_display_toggle,
            bg="#20232B",
            fg="#FFFFFF",
            activebackground="#20232B",
            activeforeground="#FFFFFF",
            selectcolor="#343A46",
            font=("Arial", 11),
        )
        toggle.pack(anchor="w", padx=20, pady=4)

        controls = tk.Frame(tab, bg="#20232B")
        controls.pack(fill="x", padx=20, pady=12)

        tk.Label(
            controls, text="Text color", bg="#20232B", fg="#FFFFFF"
        ).grid(row=0, column=0, sticky="w", pady=8)

        tk.Button(
            controls,
            text="Choose color",
            command=self.choose_color,
            bg="#343A46",
            fg="#FFFFFF",
            activebackground="#454D5D",
            activeforeground="#FFFFFF",
            relief="flat",
        ).grid(row=0, column=1, sticky="e", padx=8)

        tk.Label(
            controls, text="Font", bg="#20232B", fg="#FFFFFF"
        ).grid(row=1, column=0, sticky="w", pady=8)

        font_box = ttk.Combobox(
            controls,
            textvariable=self.font_family,
            values=("Arial", "Verdana", "Tahoma", "Calibri"),
            state="readonly",
            width=17,
        )
        font_box.grid(row=1, column=1, sticky="e", padx=8)
        font_box.bind("<<ComboboxSelected>>", lambda _event: self.update_preview())

        tk.Label(
            controls, text="Text size", bg="#20232B", fg="#FFFFFF"
        ).grid(row=2, column=0, sticky="w", pady=8)

        size_box = ttk.Spinbox(
            controls,
            from_=9,
            to=30,
            textvariable=self.font_size,
            width=6,
            command=self.update_preview,
        )
        size_box.grid(row=2, column=1, sticky="e", padx=8)
        size_box.bind("<KeyRelease>", lambda _event: self.update_preview())

        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        self.preview = tk.Label(
            tab,
            text="YOU  —     THEM  —     +0",
            bg="#14161B",
            fg=self.text_color.get(),
            font=(self.font_family.get(), self.font_size.get(), "bold"),
            padx=12,
            pady=15,
        )
        self.preview.pack(fill="x", padx=20, pady=(8, 15))

    def _build_values_tab(self):
        tab = self.values_tab

        self._section_label(tab, "VALUE SOURCE").pack(
            anchor="w", padx=20, pady=(18, 8)
        )

        tk.Label(
            tab,
            text="Price provider",
            bg="#20232B",
            fg="#FFFFFF",
            font=("Arial", 10),
        ).pack(anchor="w", padx=20, pady=(5, 3))

        source_box = ttk.Combobox(
            tab,
            textvariable=self.source,
            values=("Supreme Values",),
            state="readonly",
        )
        source_box.pack(fill="x", padx=20)

        tk.Label(
            tab,
            text="Automatic refresh",
            bg="#20232B",
            fg="#FFFFFF",
            font=("Arial", 10),
        ).pack(anchor="w", padx=20, pady=(18, 5))

        refresh_box = ttk.Combobox(
            tab,
            textvariable=self.refresh_minutes,
            values=(5, 10),
            state="readonly",
            width=8,
        )
        refresh_box.pack(anchor="w", padx=20)

        tk.Label(
            tab,
            text=(
                "Live price loading will be added in Part 2. "
                "This setting is saved locally."
            ),
            bg="#20232B",
            fg="#AAB2C0",
            justify="left",
            wraplength=450,
            font=("Arial", 9),
        ).pack(anchor="w", padx=20, pady=18)

    def _build_status(self):
        footer = tk.Frame(self.root, bg="#17191F")
        footer.pack(fill="x", padx=18, pady=(5, 12))

        self.status_label = tk.Label(
            footer,
            text="Part 1 · Interface ready · Live values not connected",
            bg="#17191F",
            fg="#AAB2C0",
            font=("Arial", 8),
        )
        self.status_label.pack(side="left")

        tk.Button(
            footer,
            text="Save settings",
            command=self.save_current_settings,
            bg="#365EBA",
            fg="#FFFFFF",
            activebackground="#4773D6",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=12,
            pady=6,
        ).pack(side="right")

    def choose_color(self):
        selected = colorchooser.askcolor(
            color=self.text_color.get(),
            title="Choose value text color",
        )[1]
        if selected:
            self.text_color.set(selected)
            self.update_preview()

    def update_preview(self):
        try:
            size = max(9, min(30, int(self.font_size.get())))
        except (ValueError, tk.TclError):
            size = 14

        if hasattr(self, "preview"):
            self.preview.config(
                fg=self.text_color.get(),
                font=(self.font_family.get(), size, "bold"),
            )

    def on_display_toggle(self):
        enabled = self.display_enabled.get()
        self.enabled_label.config(
            text="ON" if enabled else "OFF",
            fg="#67D391" if enabled else "#F08A8A",
        )

    def save_current_settings(self):
        try:
            size = max(9, min(30, int(self.font_size.get())))
            refresh = int(self.refresh_minutes.get())
            if refresh not in (5, 10):
                refresh = 5
        except (ValueError, tk.TclError):
            size, refresh = 14, 5

        self.settings = {
            "text_color": self.text_color.get(),
            "font_family": self.font_family.get(),
            "font_size": size,
            "refresh_minutes": refresh,
            "display_enabled": self.display_enabled.get(),
            "source": self.source.get(),
        }

        try:
            save_settings(self.settings)
            self.status_label.config(text="Settings saved")
        except OSError as error:
            self.status_label.config(text=f"Save error: {error}")

    def on_close(self):
        self.save_current_settings()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = SupremeMM2App(window)
    window.mainloop()

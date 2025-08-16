import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, Menu, filedialog
import os, time, subprocess, random

class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Keyboard")
        self.geometry("800x300")
        self.configure(bg="white")

        self.press_time = None
        self.update_job = None
        self.key_buttons = {}
        self.key_map = {}
        self.current_key = None

        self.label = ttk.Label(self, text="Press a key", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.create_keyboard()
        self.bind("<KeyPress>", self.on_real_key_press)
        self.bind("<KeyRelease>", self.on_real_key_release)

    def create_keyboard(self):
        keys_rows = [
            ['Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'],
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
            ['CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
            ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Win', 'Menu', 'Ctrl']
        ]

        self.key_map = {
            'Escape': 'Esc', 'F1': 'F1', 'F2': 'F2', 'F3': 'F3', 'F4': 'F4', 'F5': 'F5', 
            'F6': 'F6', 'F7': 'F7', 'F8': 'F8', 'F9': 'F9', 'F10': 'F10', 'F11': 'F11', 'F12': 'F12',
            '`': '`', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', 
            '8': '8', '9': '9', '0': '0', '-': '-', '=': '=', 'BackSpace': 'Backspace',
            'Tab': 'Tab', 'q': 'Q', 'w': 'W', 'e': 'E', 'r': 'R', 't': 'T', 'y': 'Y', 
            'u': 'U', 'i': 'I', 'o': 'O', 'p': 'P', '[': '[', ']': ']', '\\': '\\',
            'Caps_Lock': 'CapsLock', 'a': 'A', 's': 'S', 'd': 'D', 'f': 'F', 'g': 'G', 
            'h': 'H', 'j': 'J', 'k': 'K', 'l': 'L', ';': ';', '\'': '\'', 'Return': 'Enter',
            'Shift_L': 'Shift', 'Shift_R': 'Shift', 'z': 'Z', 'x': 'X', 'c': 'C', 'v': 'V', 
            'b': 'B', 'n': 'N', 'm': 'M', ',': ',', '.': '.', '/': '/', 
            'Control_L': 'Ctrl', 'Control_R': 'Ctrl', 'Super_L': 'Win', 'Super_R': 'Win', 
            'Alt_L': 'Alt', 'Alt_R': 'Alt', 'space': 'Space', 'Menu': 'Menu'
        }

        for row_keys in keys_rows:
            frame = tk.Frame(self, bg="white")
            frame.pack(fill='x', padx=5)
            for key in row_keys:
                width = 5
                if key in ['Backspace', 'CapsLock', 'Enter', 'Shift', 'Space']:
                    width = 8 if key != 'Space' else 40
                btn = ttk.Button(frame, text=key, width=width)
                btn.pack(side='left', padx=2, pady=2)
                btn.bind("<ButtonPress-1>", lambda e, k=key: self.on_press(k))
                btn.bind("<ButtonRelease-1>", lambda e, k=key: self.on_release(k))
                self.key_buttons[key] = btn

    def on_real_key_press(self, event):
        key = event.keysym
        if key in self.key_map:
            display_key = self.key_map[key]
            self.current_key = display_key
            self.key_buttons[display_key].config(style='Pressed.TButton')
            self.press_time = time.time()
            self.update_label(display_key, 0.0)
            self.schedule_update(display_key)

    def on_real_key_release(self, event):
        if self.current_key and self.current_key in self.key_buttons:
            self.key_buttons[self.current_key].config(style='TButton')
            elapsed = time.time() - self.press_time
            self.update_label(self.current_key, elapsed)
            self.press_time = None
            if self.update_job is not None:
                self.after_cancel(self.update_job)
                self.update_job = None
            self.after(1000, self.clear_label)
            self.current_key = None

    def on_press(self, key):
        self.press_time = time.time()
        self.key_buttons[key].config(style='Pressed.TButton')
        self.update_label(key, 0.0)
        self.schedule_update(key)

    def on_release(self, key):
        if self.press_time is None:
            return
        self.key_buttons[key].config(style='TButton')
        elapsed = time.time() - self.press_time
        self.update_label(key, elapsed)
        self.press_time = None
        if self.update_job is not None:
            self.after_cancel(self.update_job)
            self.update_job = None
        self.after(1000, self.clear_label)

    def update_label(self, key, elapsed):
        ascii_code = ord(key[0]) if len(key) == 1 and key.isprintable() else 'N/A'
        self.label.config(text=f"Key Pressed: {key} (ASCII: {ascii_code}, Held for {elapsed:.2f} s)")

    def clear_label(self):
        self.label.config(text="Press a key")

    def schedule_update(self, key):
        if self.press_time is None:
            return
        elapsed = time.time() - self.press_time
        self.update_label(key, elapsed)
        self.update_job = self.after(100, lambda: self.schedule_update(key))

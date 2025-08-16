import tkinter as tk
from tkinter import ttk
from mouse_driver import MouseDriverEmulator
from keyboard_driver import VirtualKeyboard
from disk_driver import DiskDriverEmulator

# Main GUI Menu (unchanged)
class EmulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Driver Emulator")

        tk.Label(root, text="Select Emulator:", font=("Arial", 12)).pack(pady=10)
        tk.Button(root, text="Mouse Driver Emulator", command=self.run_mouse).pack(fill='x', padx=20, pady=5)
        tk.Button(root, text="Keyboard Driver Emulator", command=self.run_keyboard).pack(fill='x', padx=20, pady=5)
        tk.Button(root, text="Disk Driver Emulator", command=self.run_disk).pack(fill='x', padx=20, pady=5)
        tk.Button(root, text="Exit", command=root.quit).pack(fill='x', padx=20, pady=5)

    def run_mouse(self):
        win = tk.Toplevel(self.root)
        win.title("Mouse Driver Emulator")
        emulator = MouseDriverEmulator(win)
        tk.Button(win, text="Move", command=emulator.move_mouse).pack(fill='x')
        tk.Button(win, text="Click", command=emulator.click_mouse).pack(fill='x')
        tk.Button(win, text="Scroll", command=emulator.scroll_mouse).pack(fill='x')
        tk.Button(win, text="Position", command=emulator.get_position).pack(fill='x')

    def run_keyboard(self):
        win = VirtualKeyboard()
        style = ttk.Style()
        style.configure('Pressed.TButton', background='lightgreen')
        win.mainloop()

    def run_disk(self):
        win = tk.Toplevel(self.root)
        emulator = DiskDriverEmulator(win)
        tk.Button(win, text="Write Block", command=emulator.write_block).pack(fill='x')
        tk.Button(win, text="Read Block", command=emulator.read_block).pack(fill='x')
        tk.Button(win, text="Copy Block", command=emulator.copy_block).pack(fill='x')
        tk.Button(win, text="Defragment Disk", command=emulator.defragment_disk).pack(fill='x')
        tk.Button(win, text="Format Disk", command=emulator.format_disk).pack(fill='x')
        tk.Button(win, text="Free Block", command=emulator.free_block).pack(fill='x')
        tk.Button(win, text="Move Block", command=emulator.move_block).pack(fill='x')


def main():
    root = tk.Tk()
    app = EmulatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
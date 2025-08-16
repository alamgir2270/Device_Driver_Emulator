import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, Menu, filedialog
import os, time, subprocess, random

# Mouse Driver Emulator (unchanged)
class MouseDriverEmulator:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=600, height=400, bg="#e0f7fa")
        self.canvas.pack()

        self.mouse = self.canvas.create_oval(290, 190, 310, 210, fill="blue", outline="black")
        self.click_label = self.canvas.create_text(300, 20, text="", fill="black", font=("Arial", 12, "bold"))
        self.position_label = self.canvas.create_text(300, 380, text="Position: (300, 200)", fill="gray", font=("Arial", 10))

        self.canvas.bind("<Motion>", self.track_mouse_position)
        self.canvas.bind("<Button-1>", self.show_position_on_click)

    def update_position_label(self):
        coords = self.canvas.coords(self.mouse)
        x = int((coords[0] + coords[2]) / 2)
        y = int((coords[1] + coords[3]) / 2)
        self.canvas.itemconfig(self.position_label, text=f"Position: ({x}, {y})")

    def track_mouse_position(self, event):
        self.canvas.itemconfig(self.position_label, text=f"Position: ({event.x}, {event.y})")

    def show_position_on_click(self, event):
        x, y = event.x, y = event.y
        self.canvas.itemconfig(self.click_label, text=f"Clicked at ({x}, {y})")
        self.master.after(1500, lambda: self.canvas.itemconfig(self.click_label, text=""))

    def move_mouse(self):
        x = simpledialog.askinteger("Move Mouse", "Enter X position (0-600):")
        y = simpledialog.askinteger("Move Mouse", "Enter Y position (0-400):")
        if x is not None and y is not None:
            self.canvas.coords(self.mouse, x - 10, y - 10, x + 10, y + 10)
            self.canvas.coords(self.click_label, x, y - 25)
            self.canvas.coords(self.position_label, x, y + 25)
            self.update_position_label()
            print(f"Mouse moved to ({x}, {y})")

    def click_mouse(self):
        click_type = simpledialog.askstring("Click", "Enter click type (left/right):")
        if not click_type:
            return

        click_type = click_type.lower()
        valid_clicks = {"left", "right"}
        if click_type not in valid_clicks:
            messagebox.showerror("Error", "Invalid click type. Choose left/right.")
            return

        colors = {"left": "green", "right": "red"}
        messages = {
            "left": "Left Click!",
            "right": "Right Click!"
        }

        original_color = self.canvas.itemcget(self.mouse, "fill")
        new_color = colors[click_type]
        self.canvas.itemconfig(self.mouse, fill=new_color)
        self.canvas.itemconfig(self.click_label, text=messages[click_type])

        self.master.after(500, lambda: self.canvas.itemconfig(self.mouse, fill=original_color))
        self.master.after(1500, lambda: self.canvas.itemconfig(self.click_label, text=""))

        print(f"Mouse {click_type} clicked")

        if click_type == "left":
            file_path = filedialog.askopenfilename(title="Select file to open")
            if not file_path:
                return
            if not os.path.isfile(file_path):
                messagebox.showerror("Error", "Selected file does not exist.")
                return
            self.selected_file = file_path
            code_path = "/usr/bin/code"
            try:
                subprocess.run([code_path, file_path], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to open file in VS Code:\n{e}")

        elif click_type == "right":
            if not hasattr(self, 'selected_file') or not self.selected_file:
                messagebox.showinfo("Info", "No file selected to run. Please select a file first using left click.")
                return
            
            def run_code():
                if not self.selected_file.endswith('.py'):
                    messagebox.showerror("Error", "Selected file is not a Python file.")
                    return
                
                try:
                    subprocess.Popen(['python3', self.selected_file])
                    messagebox.showinfo("Running", f"Running {self.selected_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to run code:\n{e}")

            menu = Menu(self.master, tearoff=0)
            menu.add_command(label="Run Code", command=run_code)
            try:
                x = self.master.winfo_pointerx()
                y = self.master.winfo_pointery()
                menu.tk_popup(x, y)
            finally:
                menu.grab_release()

    def scroll_mouse(self):
        amount = simpledialog.askinteger("Scroll", "Enter scroll amount (+/-):")
        if amount is None or amount == 0:
            return

        coords = self.canvas.coords(self.mouse)
        x = int((coords[0] + coords[2]) / 2)
        y = int((coords[1] + coords[3]) / 2)
        new_y = y - amount
        new_y = max(10, min(390, new_y))

        delta_y = new_y - y
        self.canvas.move(self.mouse, 0, delta_y)
        self.canvas.move(self.click_label, 0, delta_y)
        self.canvas.move(self.position_label, 0, delta_y)
        self.update_position_label()

        trail_color = "purple" if amount > 0 else "cyan"
        trail = self.canvas.create_line(x, y, x, new_y, arrow=tk.LAST, fill=trail_color, width=2, dash=(4, 2))

        scroll_text = f"Scrolled {'Up' if amount > 0 else 'Down'}: {abs(amount)}"
        self.canvas.itemconfig(self.click_label, text=scroll_text)

        self.master.after(1200, lambda: self.canvas.delete(trail))
        self.master.after(1500, lambda: self.canvas.itemconfig(self.click_label, text=""))

        print(f"Mouse scrolled by {amount} steps")

    def get_position(self):
        self.update_position_label()
        coords = self.canvas.coords(self.mouse)
        x = int((coords[0] + coords[2]) / 2)
        y = int((coords[1] + coords[3]) / 2)
        print(f"Current Mouse Position: ({x}, {y})")

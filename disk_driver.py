import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, Menu, filedialog
import os, time, subprocess, random

class DiskDriverEmulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Disk Driver Emulator")
        self.disk = ["" for _ in range(1024)]
        self.cache = {}
        self.block_widgets = []

        self.canvas = tk.Canvas(master, width=600, height=200, bg="#e0e0e0")
        self.canvas.pack(pady=10)

        self.output_text = tk.Text(master, height=8, width=60)
        self.output_text.pack(pady=5)

        self.create_disk_map()

    def create_disk_map(self):
        self.block_widgets = []
        for i in range(60):
            x = (i % 10) * 58 + 10
            y = (i // 10) * 30 + 10
            rect = self.canvas.create_rectangle(
                x, y, x + 50, y + 25, fill="white", outline="black"
            )
            text = self.canvas.create_text(
                x + 25, y + 12.5, text=f"Block {i}", font=("Arial", 8)
            )
            self.block_widgets.append((rect, text))
        self.canvas.create_text(
            300, 190, text="White: Empty | Green: Data | Red: Cached",
            font=("Arial", 8)
        )

    def update_disk_map(self):
        for i in range(60):
            rect, _ = self.block_widgets[i]
            if i in self.cache:
                color = "red"
            elif self.disk[i]:
                color = "green"
            else:
                color = "white"
            self.canvas.itemconfig(rect, fill=color)

    def update_output(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def write_block(self):
        block_id = simpledialog.askinteger("Write Block", "Enter block ID (0-1023):")
        data = simpledialog.askstring("Write Block", "Enter data:")
        if block_id is not None and data is not None and 0 <= block_id < 1024:
            self.disk[block_id] = data
            self.cache[block_id] = data
            self.update_disk_map()
            self.update_output(f"Wrote to block {block_id}: {data}")

    def read_block(self):
        block_id = simpledialog.askinteger("Read Block", "Enter block ID (0-1023):")
        if block_id is not None and 0 <= block_id < 1024:
            data = self.cache.get(block_id) or self.disk[block_id]
            self.update_output(f"Read block {block_id}: {data}")

    def copy_block(self):
        src = simpledialog.askinteger("Copy Block", "Enter source block ID (0-1023):")
        if src is None or src < 0 or src >= 1024:
            messagebox.showerror("Error", "Invalid source block ID.")
            return
        dest_input = simpledialog.askstring("Copy Block", "Enter destination block IDs (comma-separated, 0-1023):")
        if not dest_input:
            return
        try:
            dest_blocks = [int(x.strip()) for x in dest_input.split(',')]
            for dest in dest_blocks:
                if dest < 0 or dest >= 1024:
                    raise ValueError("Destination block ID out of range.")
                if self.disk[dest]:
                    raise ValueError(f"Destination block {dest} is not empty.")
            for dest in dest_blocks:
                self.disk[dest] = self.disk[src]
                if src in self.cache:
                    self.cache[dest] = self.disk[src]
                self.update_disk_map()
                self.update_output(f"Copied data from block {src} to block {dest}.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def defragment_disk(self):
        new_disk = ["" for _ in range(1024)]
        new_cache = {}
        next_free = 0
        for i in range(1024):
            if self.disk[i]:
                new_disk[next_free] = self.disk[i]
                if i in self.cache:
                    new_cache[next_free] = self.cache[i]
                next_free += 1
        self.disk = new_disk
        self.cache = new_cache
        self.update_disk_map()
        self.update_output("Disk defragmented. Data moved to lowest-indexed blocks.")

    def format_disk(self):
        self.disk = ["" for _ in range(1024)]
        self.cache.clear()
        self.update_disk_map()
        self.update_output("Disk formatted.")

    def free_block(self):
        block_input = simpledialog.askstring("Free Blocks", "Enter block IDs to free (comma-separated, 0-1023):")
        if not block_input:
            return
        try:
            block_ids = [int(x.strip()) for x in block_input.split(',')]
            freed_blocks = []
            ignored_blocks = []
            for block_id in block_ids:
                if block_id < 0 or block_id >= 1024:
                    raise ValueError(f"Block ID {block_id} out of range.")
                if self.disk[block_id]:
                    self.disk[block_id] = ""
                    if block_id in self.cache:
                        del self.cache[block_id]
                    freed_blocks.append(block_id)
                else:
                    ignored_blocks.append(block_id)
            self.update_disk_map()
            if freed_blocks:
                self.update_output(f"Freed blocks: {', '.join(map(str, freed_blocks))}")
            if ignored_blocks:
                self.update_output(f"Ignored empty blocks: {', '.join(map(str, ignored_blocks))}")
            if not freed_blocks and not ignored_blocks:
                self.update_output("No blocks were freed or ignored.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def move_block(self):
        src_input = simpledialog.askstring("Move Blocks", "Enter source block IDs (comma-separated, 0-1023):")
        if not src_input:
            return
        try:
            src_blocks = [int(x.strip()) for x in src_input.split(',')]
            for src in src_blocks:
                if src < 0 or src >= 1024:
                    raise ValueError("Source block ID out of range.")
            dest_start = simpledialog.askinteger("Move Blocks", "Enter starting destination block ID (0-1023):")
            if dest_start is None or dest_start < 0 or dest_start >= 1024:
                raise ValueError("Invalid starting destination block ID.")
            dest_blocks = list(range(dest_start, dest_start + len(src_blocks)))
            if dest_blocks[-1] >= 1024:
                raise ValueError("Destination blocks exceed disk size.")
            for dest in dest_blocks:
                if self.disk[dest]:
                    raise ValueError(f"Destination block {dest} is not empty.")
            for src, dest in zip(src_blocks, dest_blocks):
                self.disk[dest] = self.disk[src]
                self.disk[src] = ""
                if src in self.cache:
                    self.cache[dest] = self.cache[src]
                    del self.cache[src]
                self.update_output(f"Moved data from block {src} to block {dest}.")
            self.update_disk_map()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")


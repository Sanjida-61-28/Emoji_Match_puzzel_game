import tkinter as tk
from tkinter import messagebox
import random
import time
import sys

# -------------------------------
# Configuration
# -------------------------------
LEVELS = [
    {"size": 4, "emojis": ["🍎","🍌","🍇","🍉","🍓","🍒","🥝","🍍"]},  # 4x4 → 8 pairs
    {"size": 6, "emojis": ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐸","🐵","🐔","🐧","🐦","🦉","🦄"]},  # 6x6 → 18 pairs
    {"size": 6, "emojis": ["⚽","🏀","🏈","⚾","🎾","🏐","🏉","🎱","🏓","🏸","🥅","🎯","🏹","🪀","🎳","🥏","🛼","🛹"]},  # 6x6 → 18 pairs
    {"size": 8, "emojis": ["🍔","🍕","🌭","🍟","🥪","🥗","🍣","🍤","🍩","🍪","🍰","🎂","🍫","🍿","🥟","🥞","🧁","🥧","🍜","🍲","🥣","🥠","🥡","🍝","🍛","🍚","🍙","🍘","🥮","🫔","🥯","🫓"]},  # 8x8 → 32 pairs
    {"size": 8, "emojis": ["🚗","🚕","🚙","🚌","🚎","🏎️","🚓","🚑","🚒","🚐","🛻","🚚","🚛","🚜","🛺","🛵","🏍️","🛶","⛵","🚤","🛥️","🛳️","✈️","🚁","🛸","🚀","🛻","🚲","🛴","🛹"]},  # 8x8 → 32 pairs
]

BUTTON_FONT = ("Arial", 24)
DELAY = 700
BUTTON_COLOR = "#87CEEB"
HOVER_COLOR = "#B0E0E6"
MATCH_COLOR = "#32CD32"
BUTTON_SIZE = 60  # pixels

# -------------------------------
# Game Class
# -------------------------------
class EmojiMatchGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Emoji Match Game - Modern Circular")
        self.level_index = 0
        self.buttons = []
        self.first = None
        self.second = None
        self.matches = 0
        self.moves = 0
        self.score = 0
        self.level_moves = 0
        self.level_start_time = time.time()
        self.start_time = time.time()
        self.create_controls()
        self.load_level()
        self.update_timer()

    # --- Controls ---
    def create_controls(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=10)
        self.score_label = tk.Label(self.top_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(side="left", padx=10)
        self.moves_label = tk.Label(self.top_frame, text="Moves: 0", font=("Arial", 14))
        self.moves_label.pack(side="left", padx=10)
        self.timer_label = tk.Label(self.top_frame, text="Time: 0s", font=("Arial", 14))
        self.timer_label.pack(side="left", padx=10)

        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.pack(pady=10)
        self.restart_btn = tk.Button(self.bottom_frame, text="Restart", font=("Arial", 12), bg="#FFA500", command=self.restart_game)
        self.restart_btn.pack(side="left", padx=10)
        self.quit_btn = tk.Button(self.bottom_frame, text="Quit", font=("Arial", 12), bg="#FF4500", command=self.quit_game)
        self.quit_btn.pack(side="left", padx=10)

    # --- Load Level ---
    def load_level(self):
        if hasattr(self, "button_frame"):
            self.button_frame.destroy()
        self.buttons.clear()
        self.first = self.second = None
        self.matches = 0
        self.level_moves = 0
        self.level_start_time = time.time()
        self.update_labels()

        level = LEVELS[self.level_index]
        self.grid_size = level["size"]

        # Duplicate emojis for pairs and shuffle
        emoji_list = level["emojis"][: (self.grid_size**2)//2]
        self.tile_emojis = emoji_list * 2
        random.shuffle(self.tile_emojis)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                index = r*self.grid_size + c
                canvas = tk.Canvas(self.button_frame, width=BUTTON_SIZE, height=BUTTON_SIZE, highlightthickness=0, bg=self.master["bg"])
                oval = canvas.create_oval(5,5,BUTTON_SIZE-5,BUTTON_SIZE-5, fill=BUTTON_COLOR, outline="")
                canvas.grid(row=r, column=c, padx=5, pady=5)
                canvas.index = index
                canvas.revealed = False
                canvas.oval = oval
                canvas.bind("<Button-1>", lambda e, b=index: self.on_click(b))
                canvas.bind("<Enter>", lambda e, c=canvas: self.on_hover(c, True))
                canvas.bind("<Leave>", lambda e, c=canvas: self.on_hover(c, False))
                self.buttons.append(canvas)

    # --- Hover Effect ---
    def on_hover(self, canvas, enter):
        if not canvas.revealed:
            color = HOVER_COLOR if enter else BUTTON_COLOR
            canvas.itemconfig(canvas.oval, fill=color)

    # --- Tile Click ---
    def on_click(self, index):
        btn = self.buttons[index]
        if btn.revealed or self.second is not None:
            return
        btn.revealed = True
        btn.delete("all")
        btn.create_oval(5,5,BUTTON_SIZE-5,BUTTON_SIZE-5, fill="white", outline="")
        btn.create_text(BUTTON_SIZE//2, BUTTON_SIZE//2, text=self.tile_emojis[index], font=BUTTON_FONT, tags="emoji_text")
        if not self.first:
            self.first = btn
        else:
            self.second = btn
            self.moves += 1
            self.level_moves += 1
            self.update_labels()
            self.master.after(DELAY, self.check_match)

    # --- Check Match ---
    def check_match(self):
        if self.first and self.second:
            if self.tile_emojis[self.first.index] == self.tile_emojis[self.second.index]:
                self.matches += 1
                self.score += 10
                self.animate_match(self.first)
                self.animate_match(self.second)
            else:
                self.hide_tile(self.first)
                self.hide_tile(self.second)
            self.first = self.second = None
            self.update_labels()
            if self.matches == (self.grid_size**2)//2:
                # Level completed
                level_time = int(time.time() - self.level_start_time)
                messagebox.showinfo(
                    f"Level {self.level_index+1} Complete",
                    f"Congratulations! You completed Level {self.level_index+1}!\n"
                    f"Moves: {self.level_moves}\n"
                    f"Time: {level_time}s\n"
                    f"Points: {self.score}"
                )
                self.level_index += 1
                if self.level_index < len(LEVELS):
                    self.load_level()
                else:
                    total_time = int(time.time() - self.start_time)
                    messagebox.showinfo(
                        "All Levels Completed",
                        f"How do you solve puzzles so fast? Are you secretly a robot? 🤖😊\n\n"
                        f"Total Moves: {self.moves}\n"
                        f"Total Points: {self.score}\n"
                        f"Total Time: {total_time}s"
                    )
                    self.master.quit()

    # --- Hide Tile ---
    def hide_tile(self, canvas):
        canvas.revealed = False
        canvas.delete("all")
        canvas.create_oval(5,5,BUTTON_SIZE-5,BUTTON_SIZE-5, fill=BUTTON_COLOR, outline="")

    # --- Animate Match ---
    def animate_match(self, canvas):
        BLINK_COLOR = "#FFFF00"  # yellow
        FINAL_COLOR = MATCH_COLOR
        text_items = canvas.find_withtag("emoji_text")

        def flash(count=0):
            if count >= 6:
                canvas.itemconfig(canvas.oval, fill=FINAL_COLOR)
                for t in text_items:
                    canvas.itemconfig(t, fill="black")
                return
            color = BLINK_COLOR if count % 2 == 0 else FINAL_COLOR
            canvas.itemconfig(canvas.oval, fill=color)
            for t in text_items:
                canvas.itemconfig(t, fill=color)
            canvas.after(150, lambda: flash(count+1))

        flash()

    # --- Update Labels ---
    def update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.moves_label.config(text=f"Moves: {self.moves}")

    # --- Timer ---
    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s")
        self.master.after(1000, self.update_timer)

    # --- Restart ---
    def restart_game(self):
        self.level_index = 0
        self.score = 0
        self.moves = 0
        self.start_time = time.time()
        self.load_level()
        self.update_labels()

    # --- Quit ---
    def quit_game(self):
        self.master.destroy()
        sys.exit()

# -------------------------------
# Run Game
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = EmojiMatchGame(root)
    root.mainloop()

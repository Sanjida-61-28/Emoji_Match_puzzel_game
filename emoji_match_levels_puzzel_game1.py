import tkinter as tk
from tkinter import messagebox
import random
import time
import sys

# -------------------------------
# Configuration
# -------------------------------
LEVELS = [
    {"size": 4, "emojis": ["🍎","🍌","🍇","🍉","🍓","🍒","🥝","🍍"]},  # 4x4
    {"size": 6, "emojis": ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐸","🐵","🐔","🐧","🐦","🦉","🦄"]},  # 6x6
    {"size": 6, "emojis": ["⚽","🏀","🏈","⚾","🎾","🏐","🏉","🎱","🏓","🏸","🥅","🎯","🏹","🪀","🎳","🥏","🛼","🛹"]},  # 6x6
    {"size": 8, "emojis": ["🍔","🍕","🌭","🍟","🥪","🥗","🍣","🍤","🍩","🍪","🍰","🎂","🍫","🍿","🥟","🥞","🧁","🥧","🍜","🍲","🥣","🥠","🥡","🍝","🍛","🍚","🍙","🍘","🥮","🫔","🥯","🫓"]},  # 8x8
    {"size": 8, "emojis": ["🚗","🚕","🚙","🚌","🚎","🏎️","🚓","🚑","🚒","🚐","🛻","🚚","🚛","🚜","🛺","🛵","🏍️","🛶","⛵","🚤","🛥️","🛳️","✈️","🚁","🛸","🚀","🛻","🚲","🛴","🛹"]},  # 8x8
]

BUTTON_FONT = ("Arial", 24)
DELAY = 700  # milliseconds
BUTTON_COLOR = "#87CEEB"       # Initial tile color
MATCH_COLOR = "#32CD32"        # Color when tiles match
BUTTON_SIZE = 4                # Button width

# -------------------------------
# Game Class
# -------------------------------
class EmojiMatchGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Emoji Match Game - 5 Levels")
        self.level_index = 0
        self.buttons = []
        self.first = None
        self.second = None
        self.matches = 0
        self.moves = 0
        self.score = 0
        self.start_time = time.time()
        self.create_controls()
        self.load_level()
        self.update_timer()

    # --- Controls for score, moves, timer, restart, quit ---
    def create_controls(self):
        # Top frame
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=10)

        self.score_label = tk.Label(self.top_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(side="left", padx=10)

        self.moves_label = tk.Label(self.top_frame, text="Moves: 0", font=("Arial", 14))
        self.moves_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(self.top_frame, text="Time: 0s", font=("Arial", 14))
        self.timer_label.pack(side="left", padx=10)

        # Bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.pack(pady=10)

        self.restart_btn = tk.Button(self.bottom_frame, text="Restart", font=("Arial", 12), bg="#FFA500", command=self.restart_game)
        self.restart_btn.pack(side="left", padx=10)

        self.quit_btn = tk.Button(self.bottom_frame, text="Quit", font=("Arial", 12), bg="#FF4500", command=self.quit_game)
        self.quit_btn.pack(side="left", padx=10)

    # --- Load a level ---
    def load_level(self):
        # Clear previous grid
        if hasattr(self, "button_frame"):
            self.button_frame.destroy()
        self.buttons.clear()
        self.first = self.second = None
        self.matches = 0
        self.moves = 0
        self.update_labels()

        level = LEVELS[self.level_index]
        self.grid_size = level["size"]

        # Prepare emojis
        emoji_list = level["emojis"][:(self.grid_size**2)//2]
        self.tile_emojis = emoji_list * 2
        random.shuffle(self.tile_emojis)

        # Create button grid
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                index = r*self.grid_size + c
                btn = tk.Button(
                    self.button_frame,
                    text="",
                    width=BUTTON_SIZE,
                    height=2,
                    font=BUTTON_FONT,
                    bg=BUTTON_COLOR,
                    activebackground=BUTTON_COLOR,
                    relief="raised",
                    bd=3,
                    command=lambda b=index: self.on_click(b)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                btn.index = index
                btn.revealed = False
                self.buttons.append(btn)

    # --- Tile click ---
    def on_click(self, index):
        btn = self.buttons[index]
        if btn.revealed or self.second is not None:
            return
        btn.config(text=self.tile_emojis[index])
        btn.revealed = True
        if not self.first:
            self.first = btn
        else:
            self.second = btn
            self.moves += 1
            self.update_labels()
            self.master.after(DELAY, self.check_match)

    # --- Check for matches ---
    def check_match(self):
        if self.first and self.second:
            if self.tile_emojis[self.first.index] == self.tile_emojis[self.second.index]:
                self.matches += 1
                self.score += 10
                self.first.config(bg=MATCH_COLOR)
                self.second.config(bg=MATCH_COLOR)
            else:
                self.first.config(text="", bg=BUTTON_COLOR)
                self.second.config(text="", bg=BUTTON_COLOR)
                self.first.revealed = False
                self.second.revealed = False
            self.first = self.second = None
            self.update_labels()
            if self.matches == (self.grid_size**2)//2:
                messagebox.showinfo("Level Complete", f"Level {self.level_index+1} completed!")
                self.level_index += 1
                if self.level_index < len(LEVELS):
                    self.load_level()
                else:
                    total_time = int(time.time() - self.start_time)
                    messagebox.showinfo("Congratulations!", f"You completed all levels!\nScore: {self.score}\nMoves: {self.moves}\nTime: {total_time}s")
                    self.master.quit()

    # --- Update score/moves labels ---
    def update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.moves_label.config(text=f"Moves: {self.moves}")

    # --- Timer ---
    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s")
        self.master.after(1000, self.update_timer)

    # --- Restart game ---
    def restart_game(self):
        self.level_index = 0
        self.score = 0
        self.moves = 0
        self.start_time = time.time()
        self.load_level()
        self.update_labels()

    # --- Quit game ---
    def quit_game(self):
        self.master.destroy()
        sys.exit()

# -------------------------------
# Run the Game
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = EmojiMatchGame(root)
    root.mainloop()

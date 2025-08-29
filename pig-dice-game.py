import tkinter as tk
import random
import time
from threading import Thread

class PigGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pig Dice Game 🎲")

        # Game settings
        self.target_score = 100   # Will change based on level
        self.timer_seconds = 15   # Time limit per turn
        self.time_left = self.timer_seconds

        # Player data
        self.scores = [0, 0]
        self.turn_score = 0
        self.current_player = 0
        self.timer_running = False

        # ===== Top Menu (Level Selection) =====
        menu = tk.Menu(root)
        root.config(menu=menu)

        level_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Level", menu=level_menu)
        level_menu.add_command(label="Easy (50)", command=lambda: self.set_level(50))
        level_menu.add_command(label="Medium (100)", command=lambda: self.set_level(100))
        level_menu.add_command(label="Hard (150)", command=lambda: self.set_level(150))

        # ===== Scoreboard =====
        self.score_frame = tk.Frame(root, pady=10)
        self.score_frame.grid(row=0, column=0, columnspan=3)

        self.score_labels = [
            tk.Label(self.score_frame, text="Player 1: 0", font=("Arial", 16), fg="blue"),
            tk.Label(self.score_frame, text="Player 2: 0", font=("Arial", 16), fg="green")
        ]
        self.score_labels[0].pack(side="left", padx=20)
        self.score_labels[1].pack(side="right", padx=20)

        # Turn Info
        self.turn_label = tk.Label(root, text="Player 1's Turn", font=("Arial", 18, "bold"))
        self.turn_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Dice Display
        self.dice_label = tk.Label(root, text="🎲", font=("Arial", 100))
        self.dice_label.grid(row=2, column=1, pady=20)

        # Turn Score
        self.turn_score_label = tk.Label(root, text="Turn Score: 0", font=("Arial", 14))
        self.turn_score_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Timer
        self.timer_label = tk.Label(root, text=f"⏳ Time Left: {self.time_left}", font=("Arial", 14), fg="red")
        self.timer_label.grid(row=4, column=0, columnspan=3, pady=5)

        # Buttons
        self.roll_button = tk.Button(root, text="Roll", font=("Arial", 14), command=self.animate_dice)
        self.roll_button.grid(row=5, column=0, pady=20)

        self.hold_button = tk.Button(root, text="Hold", font=("Arial", 14), command=self.hold)
        self.hold_button.grid(row=5, column=2, pady=20)

        # Restart button
        self.restart_button = tk.Button(root, text="Restart", font=("Arial", 12), command=self.restart_game)
        self.restart_button.grid(row=6, column=1, pady=10)

        # Start first timer
        self.start_timer()

    # ===== Level Handling =====
    def set_level(self, score):
        self.target_score = score
        self.restart_game()

    # ===== Timer Handling =====
    def start_timer(self):
        self.time_left = self.timer_seconds
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.timer_label.config(text=f"⏳ Time Left: {self.time_left}")
            if self.time_left > 0:
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.switch_player()

    def stop_timer(self):
        self.timer_running = False

    # ===== Dice Roll with Animation =====
    def animate_dice(self):
        Thread(target=self._roll_animation).start()

    def _roll_animation(self):
        for _ in range(10):  # Quick animation
            dice_num = random.randint(1, 6)
            self.update_dice(dice_num)
            time.sleep(0.1)
        # Final roll result
        dice_num = random.randint(1, 6)
        self.update_dice(dice_num)
        self.process_roll(dice_num)

    def update_dice(self, number):
        dice_faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
        self.dice_label.config(text=dice_faces[number-1])
        self.root.update_idletasks()

    # ===== Game Logic =====
    def process_roll(self, number):
        if number == 1:
            self.turn_score = 0
            self.turn_score_label.config(text="Turn Score: 0")
            self.switch_player()
        else:
            self.turn_score += number
            self.turn_score_label.config(text=f"Turn Score: {self.turn_score}")

    def hold(self):
        self.scores[self.current_player] += self.turn_score
        self.turn_score = 0
        self.turn_score_label.config(text="Turn Score: 0")

        # Update score
        self.score_labels[self.current_player].config(
            text=f"Player {self.current_player+1}: {self.scores[self.current_player]}"
        )

        if self.scores[self.current_player] >= self.target_score:
            self.turn_label.config(text=f"🏆 Player {self.current_player+1} Wins! 🏆")
            self.roll_button.config(state="disabled")
            self.hold_button.config(state="disabled")
            self.stop_timer()
        else:
            self.switch_player()

    def switch_player(self):
        self.stop_timer()
        self.current_player = 1 - self.current_player
        self.turn_label.config(text=f"Player {self.current_player+1}'s Turn")
        self.start_timer()

    def restart_game(self):
        self.scores = [0, 0]
        self.turn_score = 0
        self.current_player = 0
        self.roll_button.config(state="normal")
        self.hold_button.config(state="normal")

        # Reset labels
        self.score_labels[0].config(text="Player 1: 0")
        self.score_labels[1].config(text="Player 2: 0")
        self.turn_score_label.config(text="Turn Score: 0")
        self.turn_label.config(text="Player 1's Turn")
        self.dice_label.config(text="🎲")

        # Restart timer
        self.start_timer()


if __name__ == "__main__":
    root = tk.Tk()
    game = PigGame(root)
    root.mainloop()


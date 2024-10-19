# Jan Bauer, 8.E, 8.10.2024
# Měření reakční doby

import tkinter as tk
from tkinter import messagebox
import random
import time


class Keyboardking(tk.Tk):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class Tk
        self.title("Reakční doba")

        # Initialize values
        self.canvas_width = 800
        self.canvas_height = 400
        self.max_score = float('inf')  # Highscore starts as infinity
        self.best_player = "N/A"  # No player yet

        # Game state
        self.running = False
        self.start_time = 0
        self.target_circle = None

        # Create menu
        menu_bar = tk.Menu()
        self.config(menu=menu_bar)

        # Name/nick
        tk.Label(text="Zadejte své jméno:").pack()
        self.name_entry = tk.Entry()
        self.name_entry.pack()

        # Canvas for drawing the game
        self.canvas = tk.Canvas(width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Score and player name
        self.score_label = tk.Label(text="Aktuální highscore: N/A - Hráč: N/A")
        self.score_label.pack()

        # START button
        self.start_button = tk.Button(text="START", command=self.start_game)
        self.start_button.pack()

        self.show_rules()  # Show rules immediately

        # Reaction time information
        self.reaction_time_label = tk.Label(text="Vaše reakční doba: N/A")
        self.reaction_time_label.pack()

    def start_game(self):
        # Start the game
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showwarning("Chyba", "Prosím, zadejte své jméno.")
            return

        self.running = True
        self.canvas.delete("all")  # Clear canvas
        self.reaction_time_label.config(text="Vaše reakční doba: N/A")
        delay = random.uniform(1, 3)  # Random delay between 1 and 3 seconds
        self.after(int(delay * 1000), self.show_target)

    def show_target(self):
        # Display target circle after random delay
        if not self.running:
            return

        self.canvas.delete("all")
        radius = random.randint(20, 50)  # Random size for the circle
        x = random.randint(radius, self.canvas_width - radius)
        y = random.randint(radius, self.canvas_height - radius)

        self.target_circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red")
        self.start_time = time.time()  # Record the start time of the reaction
        self.canvas.bind("<Button-1>", self.check_click)

    def check_click(self, event):
        # Check if the player clicked inside the circle
        if not self.running or self.target_circle is None:
            return

        # Get circle coordinates
        x1, y1, x2, y2 = self.canvas.coords(self.target_circle)
        radius = (x2 - x1) / 2  # Radius of the circle
        center_x = (x1 + x2) / 2  # Center coordinates of the circle
        center_y = (y1 + y2) / 2

        # Click coordinates
        click_x = event.x
        click_y = event.y

        # Calculate distance from the click to the center of the circle
        distance_squared = (click_x - center_x) ** 2 + (click_y - center_y) ** 2

        # Compare distance with the circle's radius
        if distance_squared <= radius ** 2:
            self.end_game()  # Click was inside the circle

    def end_game(self):
        # End the game and evaluate the result
        self.running = False
        reaction_time = (time.time() - self.start_time) * 1000  # Convert to milliseconds
        self.reaction_time_label.config(text=f"Vaše reakční doba: {reaction_time:.2f} ms")
        self.canvas.unbind("<Button-1>")

        # Update highscore
        if reaction_time < self.max_score:
            self.max_score = reaction_time
            self.best_player = self.player_name
            messagebox.showinfo("Nové highscore!", f"Gratulujeme {self.player_name}, máte nové nejlepší skóre: {reaction_time:.2f} ms!")
            self.score_label.config(text=f"Aktuální highscore: {self.max_score:.2f} ms - Hráč: {self.best_player}")

    def show_rules(self):
        # Create a custom Toplevel window for displaying rules
        rules_window = tk.Toplevel(self)
        rules_window.title("Pravidla hry")
        rules_window.geometry("300x250+100+100")  # Width x Height + x_offset + y_offset
        rules_window.attributes('-topmost', True)  # Make the rules window always on top

        # Add rules text
        rules_text = ("Pravidla hry:\n\n"
                      "1. Zadejte své jméno/nick.\n"
                      "2. Stiskněte tlačítko START pro začátek kola.\n"
                      "3. Po náhodné době se objeví červená tečka.\n"
                      "4. Klikněte co nejrychleji na tečku.\n"
                      "5. Vaše reakční doba bude zobrazena.\n"
                      "6. Nejlepší hráč a jeho skóre je zobrazeno.")
        tk.Label(rules_window, text=rules_text, justify=tk.LEFT).pack(pady=10)

        # Close button for the rules window
        close_button = tk.Button(rules_window, text="Zavřít", command=rules_window.destroy)
        close_button.pack(pady=10)

    def run(self):
        self.mainloop()  # Start the main loop of the application


if __name__ == "__main__":
    game = Keyboardking()
    game.run()

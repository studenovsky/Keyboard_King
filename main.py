# Jan Bauer, Jaroslav Studenovský 8.E, 19.10.2024
# Hra na mačkání kláves

import tkinter
import tkinter.messagebox
import time
import random
from tkinter import PhotoImage, Label, Button, Toplevel

##### Deklarace tříd
class App(tkinter.Tk):
    def __init__(self, titulek, sirka, vyska):
        super().__init__()
        # Definování potřebných proměnných pro správnou funkčnost programu
        self.vyska, self.sirka = vyska, sirka
        self.pocet_kol = random.randint(2, 6)
        self.timer_id = None
        self.highscore = 1000
        self.jmeno = ""
        self.klavesy = ["s","d","f","j","k","l"]
        self.barvy = ["violet", "blue", "cyan", "green", "yellow", "red"]
        self.polomer = 13
        self.x, self.y = 50, 15
        self.tag = ""
        self.pressed_key = ""
        self.blocked = False
        self.kola = 5
        self.skore = 0
        self.kruh_barva = "red"


        # nastavení titulku okna
        self.title(titulek)
        self.iconbitmap("1.ico")
        # konfigurace layoutu =================================================
        self.rowconfigure(0, weight=1, minsize=15, pad=3)
        self.rowconfigure(1, weight=1, minsize=20, pad=3)
        self.columnconfigure(0, weight=1, minsize=50, pad=3)
        self.columnconfigure(1, weight=1, minsize=50, pad=3)

        # vytvoření plátna
        self.canvas = tkinter.Canvas(self, width=sirka, height=vyska, relief="sunken")
        self.canvas.grid(row=1, column=0, columnspan=2)
        # MENU ================================================================
        self.menubar = tkinter.Menu(self)
        fileMenu = tkinter.Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label="Ukončení", command=self.ukonci)
        self.menubar.add_cascade(label="Soubor", menu=fileMenu)

        helpMenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="Nápověda", command=self.show_rules)
        helpMenu.add_separator()
        helpMenu.add_command(label="O hře", command=self.about)
        self.config(menu=self.menubar)


        # Víme že funguje
        self.bind_events()
        self.create_labels()  # vytvoření nápisů
        # Vázání událostí
        self.canvas.bind("<KeyPress>", lambda event: self.key_press(event))
        self.canvas.focus_set()
        self.vykresli_obdelnik()

        self.kolo()
        self.tik()
        self.auto_unblock()



    def tik(self):
        """Obsluha časovače"""
         # Tečka klesá dolu dokud není dole
        if self.y < self.y_obdelniku - 20:
            self.y += 20

        # Když je dole tak se vrátí tečka nahoru a začátek nového kola
        else:
            self.y = 15 # vrati se tecka nahoru
            self.kolo() # nevim
            self.kola -= 1 # odectu kolo
            self.napis.config(text=f"Zbývající kola: {self.kola}") # prepisu kolo
        
        # Přičtení bodu když uživatel zmáčkne správnou klávesu
        if self.tag != "": # kdyz sviti nejaky obdelnik
            if self.pressed_key == self.tag: # kdyz zmacknu spravnou klavesu
                self.skore += 1 #prictu skore
                self.body.config(text=f"Skóre: {self.skore}") # vykreslim skore
                self.kruh_barva = "black" # prebarvim kruh na cerno na 
                self.canvas.itemconfig("circle", fill=self.kruh_barva) # prebarvim kruh na cerno ted
                self.pressed_key = "" #zresetuju

            if self.pressed_key != self.tag and self.pressed_key != "": # kdyz zmacknu spatnou klavesu
                self.canvas.itemconfig(self.tag, fill="black") # prebarvim obdelnik na cerno
 
        print("autoblock " + str(self.blocked))
        self.vykresli_tecku() # Vykreslení tečky
        if self.kola == 0:
            self.game_over()
        else:
            self.after(30*self.kola, self.tik)

    def auto_unblock(self):
        """Kazdou sekundu odblokuji mackani"""
        self.pressed_key = "" # vynuluje se zmacknuta klavesa
        self.interval = 1000
        self.blocked = False
        self.kolo()
        self.vykresli_tecku()
        self.after(self.interval, self.auto_unblock)
        print("Auto unblock se spustil")


    def kolo(self):
        """dela zmeny pri zmene pozice kolecka"""
        # vytvari uklada novou pozici z moznych 6
        self.kruh_barva = "red"
        self.canvas.itemconfig(self.tag, fill="white")#odbarveni posledniho obdelniku
        # Nahodne vybrani hodnot pro dane kolo
        rand_pozice = random.randint(0,5) # vybereme novy obdelnik co se ma zmacknout
        color = self.barvy[rand_pozice]
        self.tag = self.klavesy[rand_pozice]
        self.pozice_tecky = self.coords_array[rand_pozice]

        # Prebarveni obdelniku
        self.canvas.itemconfig(self.tag, fill=color) # nabarvime novy obdelnik

    def vykresli_tecku(self):
        """Vykreslení tečky"""
        self.canvas.delete("circle")  # Smazání předchozí tečky
        self.tecka = self.canvas.create_oval(self.pozice_tecky-self.polomer, self.y - self.polomer, self.pozice_tecky + self.polomer, self.y + self.polomer, fill=self.kruh_barva, tag = "circle")  # Vykreslení tečky
    

    def key_press(self,event):
        """Kdyz zmacknu cokoliv tak zablokuju mackani"""
        if self.blocked == False:
            self.pressed_key = event.char
            self.blocked = True


    def vykresli_obdelnik(self):
        """Vykreslí na začátku 6 bílých obdélníků"""
        # Hodnoty pro rovnoměrné vykreslení pro 6 obdélníků na šířce 500px
        self.y_obdelniku = self.vyska - 20
        obdelnik_width = 25
        obdelnik_height = 10
        self.coords_array = [] # X souřadnice středů obdélníků -> vykreslení kolečka

        for i in range(1,7):
            #Výpočet první x souřadnice
            coords = (3*i-2)*obdelnik_width+obdelnik_width
            # Uložení středu obdélníku
            self.coords_array.append(round(coords + obdelnik_width / 2))
            # Vykreslení obdélníku
            self.obdelnik=self.canvas.create_rectangle(coords, self.y_obdelniku, coords+obdelnik_width, self.y_obdelniku+obdelnik_height,tag=f"{self.klavesy[i-1]}")

    def bind_events(self):
        """Navázání událostí a jejich obsluhy"""
        self.canvas.bind("q", self.ukonci)  # ukončení programu klávesou q
        self.canvas.focus_set()

    def create_buttons(self):
        """Vytvoření tlačítek"""
        
        self.tlacitko = tkinter.Button(self, text="Start", command=self.start)
        self.buttonquit = tkinter.Button(self, text="Quit", command=self.ukonci)
        self.tlacitko.grid(row=1, column=0, padx=3, sticky="wse")
        self.buttonquit.grid(row=3, column=0, padx=3, pady=5, sticky="wse")

    def show_rules(self):
        """Zobrazení pravidel hry"""
        tkinter.messagebox.showinfo("Pravidla hry", "Pravidla hry:\n\n"
                                    "1. Zadejte své jméno/nick.\n"
                                    "2. Stiskněte tlačítko START pro začátek kola.\n"
                                    "3. Po náhodné době se objeví červená tečka.\n"
                                    "4. Klikněte co nejrychleji na tečku.\n"
                                    "5. Vaše reakční doba bude zobrazena.\n"
                                    "6. Nejlepší hráč a jeho skóre je zobrazeno.")
    def create_labels(self):
        """Vytvoření nápisů"""
        # Jméno
        self.napis = tkinter.Label(self, text=f"Zbývající kola: {self.kola}", font=("Arial", 15, "bold"), fg="white", bg="blue") 
        self.napis.grid(row=0, column=0, sticky="we")
        
        self.body = tkinter.Label(self, text=f"Skóre: {self.skore}", font=("Arial", 15, "bold"), fg="white", bg="red") 
        self.body.grid(row=0, column=1, sticky="we")
        
    def about(self):
        # Create a new window (Toplevel is like a popup window)
        messagebox = Toplevel(self)
        messagebox.title("Nápověda")
        messagebox.iconbitmap("1.ico")
        
        # Set the window size
        messagebox.geometry("1000x600")

        # Load an image (GIF or PNG natively supported by tkinter)
        img = PhotoImage(file="1.png")  # Use a .gif or .png image

        # Add the image to a Label and pack it
        img_label = Label(messagebox, image=img)
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.pack(pady=10)

        # Add a text message
        text_label = Label(messagebox, text=
                           "↑ O autorech ↑\n\n"
                           "Hra Keyboard King \n"
                           "Verze hry: 1.0 \n"
                           )
        text_label.pack(pady=10)

        # Add an OK button to close the dialog
        ok_button = Button(messagebox, text="OK", command=messagebox.destroy)
        ok_button.pack(pady=10) 

    def game_over(self):
        # Create a new window (Toplevel is like a popup window)
        messagebox = Toplevel(self)
        messagebox.title("Konec Hry")
        messagebox.iconbitmap("1.ico")
        
        # Set the window size
        messagebox.geometry("1000x560")

        # Load an image (GIF or PNG natively supported by tkinter)
        img = PhotoImage(file="game-over.png")  # Use a .gif or .png image

        # Add the image to a Label and pack it
        img_label = Label(messagebox, image=img)
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.pack(pady=10)
        
        # Add an OK button to close the dialog
        ok_button = Button(messagebox, text="OK", command=messagebox.destroy)
        ok_button.pack(pady=10) 

    def ukonci(self, event=None):
        """Ukončení aplikace"""
        if tkinter.messagebox.askyesno("Ukončení", "Opravdu chcete ukončit aplikaci?"):
            self.destroy()
            exit(0)

    def run(self):
        """Spustí hlavní smyčku aplikace"""
        self.mainloop()

##### HLAVNÍ PROGRAM
if __name__ == "__main__":
    app = App("Keyboard King", 500, 700)
    # rozběhneme aplikaci
    app.run()
# konec
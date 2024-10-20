# Jan Bauer <bauerj@jirovcovka.net> , Jaroslav Studenovský <studenovskyj@jirovcovka.net>, 8.E, 19.10.2024
# Keyboard KKING - Hra na mačkání kláves

import tkinter
import tkinter.messagebox
import random
from tkinter import PhotoImage, Label, Button, Toplevel

##### Deklarace tříd
class App(tkinter.Tk):
    def __init__(self, titulek, sirka, vyska):
        super().__init__()
        # Definování potřebných proměnných pro správnou funkčnost programu + legenda jednotlivých proměnných
        self.vyska, self.sirka = vyska, sirka  # Nastavení velikosti okna
        self.pocet_kol = random.randint(2, 6)  # Počet kol je náhodně vybrán
        self.klavesy = ["s","d","f","j","k","l"]  # Klávesy, které budou uživatelem mačkány
        self.barvy = ["violet", "blue", "cyan", "green", "yellow", "red"]  # Barvy obdélníků
        self.polomer = 13  # Poloměr tečky
        self.x, self.y = 50, 15  # Výchozí pozice tečky
        self.tag = ""  # Uloží klávesu, která byla rozsvícena
        self.pressed_key = ""  # Uloží klávesu, kterou uživatel zmáčkl
        self.blocked = False  # Indikátor, zda je vstup blokován
        self.kola = 10  # Celkový počet kol
        self.skore = 0  # Počáteční skóre
        self.kruh_barva = "red"  # Barva tečky

        # nastavení titulku okna
        self.title(titulek)
        self.iconbitmap("1.ico") # Nastavení ikony okna

        # konfigurace layoutu
        self.rowconfigure(0, weight=1, minsize=15, pad=3)
        self.rowconfigure(1, weight=1, minsize=20, pad=3)
        self.columnconfigure(0, weight=1, minsize=50, pad=3)
        self.columnconfigure(1, weight=1, minsize=50, pad=3)

        # vytvoření plátna
        self.canvas = tkinter.Canvas(self, width=sirka, height=vyska, relief="sunken")
        self.canvas.grid(row=1, column=0, columnspan=2)
        
        # MENU (navigation)
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

        self.create_labels()  # Vytvoření nápisů
        self.canvas.bind("<KeyPress>", lambda event: self.key_press(event)) # Vázání událostí na plátno
        self.canvas.focus_set()

        # Vykreslení základních prvků
        self.vykresli_obdelnik() # Vykreslení obdélníků

        # Spuštění hlavních herních funkcí
        self.pohyb_tecky() # Nastavení počáteční pozice tečky
        self.tik() # Spuštění animace tečky
        self.auto_unblock() # Periodické odblokování stisku kláves

    def tik(self):
        """Funkce časovače, která animuje pohyb tečky směrem dolů"""

        # Pohyb tečky směrem dolů
        if self.y < self.y_obdelniku - 20:
            self.y += 20

        # Když je tečka dole tak se vrátí nahoru a začne nové kolo
        else:
            self.y = 15 # Reset pozice tečky
            self.pohyb_tecky() # Přesun tečky na novou pozici
            self.kola -= 1 # Odečtení kola
            self.napis.config(text=f"Zbývající kola: {self.kola}") # Aktualizace nápisu s počtem kol
        
        # Přičtení bodu když uživatel zmáčkne správnou klávesu
        if self.tag != "": # Kontrola, zda je nějaký obdélník rozsvícen
            if self.pressed_key == self.tag: # Uživatel stiskl správnou klávesu
                self.skore += 1 # Přičtení bodu
                self.body.config(text=f"Skóre: {self.skore}") # Aktualizace skóre
                self.kruh_barva = "black" 
                self.canvas.itemconfig("circle", fill=self.kruh_barva) # Změna barvy tečky na černou 
                self.pressed_key = "" # Reset stisknuté klávesy

            if self.pressed_key != self.tag and self.pressed_key != "": # Uživatel stiskl špatnou klávesu
                self.canvas.itemconfig(self.tag, fill="black") # Obdélník zčerná

        self.vykresli_tecku() # Vykreslení tečky

        if self.kola == 0: # Pokud už nejsou žádná kola, hra končí
            self.game_over()
        else:
            self.after(30*self.kola, self.tik) # Pokračování animace

    def auto_unblock(self):
        """Automatické odblokování stisku kláves každou sekundu"""
        # Deklarace potřebných proměnných
        self.pressed_key = ""
        self.interval = 1000
        self.blocked = False

        self.pohyb_tecky() # Přesun tečky na novou pozici
        self.vykresli_tecku()
        self.after(self.interval, self.auto_unblock) # Znovu spuštění této funkce po 1 sekundě

    def pohyb_tecky(self):
        """Nastavení pozice tečky, """
        # vytvari uklada novou pozici z moznych 6
        self.kruh_barva = "red"
        self.canvas.itemconfig(self.tag, fill="white")#odbarveni posledniho obdelniku

        # Nahodne vybrani hodnot pro dane kolo
        rand_pozice = random.randint(0,5) # vybereme novy obdelnik co se ma zmacknout
        color = self.barvy[rand_pozice] # vybereme novou barvu pro obdélník
        self.tag = self.klavesy[rand_pozice] # uložíme tag obdélníku, který bude rozsvícen
        self.pozice_tecky = self.coords_array[rand_pozice]
        self.canvas.itemconfig(self.tag, fill=color) # Nabarvení obdélníku

    def vykresli_tecku(self):
        """Vykreslení tečky a smazání předchozí tečky"""
        self.canvas.delete("circle")  # Smazání předchozí tečky
        self.tecka = self.canvas.create_oval(self.pozice_tecky-self.polomer, self.y - self.polomer, self.pozice_tecky + self.polomer, self.y + self.polomer, fill=self.kruh_barva, tag = "circle")  # Vykreslení tečky

    def key_press(self,event):
        """Zpracování stisku kláves"""
        if not self.blocked: # Pokud není vstup blokován
            self.pressed_key = event.char
            self.blocked = True # Blokování vstupu po stisknutí klávesy

    def vykresli_obdelnik(self):
        """Vykreslí na začátku 6 bílých obdélníků"""
        # Hodnoty pro rovnoměrné vykreslení pro 6 obdélníků na šířce 500px
        self.y_obdelniku = self.vyska - 20
        obdelnik_width = 25
        obdelnik_height = 10
        self.coords_array = [] # X souřadnice středů obdélníků -> důležité pro vykreslení kolečka

        for i in range(1,7):
            # Výpočet x souřadnic pro každý obdélník
            coords = (3*i-2)*obdelnik_width+obdelnik_width
            self.coords_array.append(round(coords + obdelnik_width / 2))
            self.obdelnik=self.canvas.create_rectangle(coords, self.y_obdelniku, coords+obdelnik_width, self.y_obdelniku+obdelnik_height,tag=f"{self.klavesy[i-1]}")

    def show_rules(self):
        """Zobrazení pravidel hry"""
        tkinter.messagebox.showinfo("Pravidla hry", "Pravidla hry:\n\n"
                                    "1.  hra \"rozsvítí\" v dolní části obrazovky jeden ze šesti obdélníku, každému obdélníku z leva odpovídají klávesy S D F J K L.\n\n"
                                    "2. hra se hraje na přednastavený počet kol (10), přičemž kolo je vždy naznačeno padajícím barevným kruhem z horní části okna.\n\n"
                                    "3. jakmile uživatel stiskne po \"rozsvícení\" obdélníku klávesu, nemůže se již opravit - tento stav je uživateli indikován tak, že se příslušný obdélník změní na černý.\n\n"
                                    "4. podaří-li se uživateli stisknout správnou klávesu získá bod, tento stav je indikován změnou skóre a zároveň barvy padajícího kruhu na černou).\n\n"
                                    "5. obdélníky se budou \"přepínat\" v pravidelných intervalech.\n\n"
                                    "6. Nahoře obrazovky vidíte počet zbývajících kol a dosud dosažené skóre.")
    def create_labels(self):
        """Vytvoření popisků v horní části okna"""
        # Počet kol
        self.napis = tkinter.Label(self, text=f"Zbývající kola: {self.kola}", font=("Arial", 15, "bold"), fg="white", bg="blue") 
        self.napis.grid(row=0, column=0, sticky="we")
        
        # Skóre
        self.body = tkinter.Label(self, text=f"Skóre: {self.skore}", font=("Arial", 15, "bold"), fg="white", bg="red") 
        self.body.grid(row=0, column=1, sticky="we")
        
    def about(self):
        """"Zobrazení informací o hře"""
        # Vytvoření nového okna
        messagebox = Toplevel(self)
        messagebox.title("Nápověda")
        messagebox.iconbitmap("1.ico")
        messagebox.geometry("1000x600")

        # Načtení obrázku
        img = PhotoImage(file="1.png")
        img_label = Label(messagebox, image=img)
        img_label.image = img
        img_label.pack(pady=10)

        # Text s informacemi o nás
        text_label = Label(messagebox, text=
                           "↑ O autorech ↑\n\n"
                           "Hra Keyboard King \n"
                           "Verze hry: 1.0 \n"
                           "Autoři: Jarda Studenovský a Honza Bauer \n"
                           )
        text_label.pack(pady=10)

        # Přidání tlačítka OK pro zavření okna
        ok_button = Button(messagebox, text="OK", command=messagebox.destroy)
        ok_button.pack(pady=10) 

    def game_over(self):
        # Vytvoření nového okna
        messagebox = Toplevel(self)
        messagebox.title("Konec Hry")
        messagebox.iconbitmap("1.ico")
        messagebox.geometry("1000x560")

        # Načtení obrázku
        img = PhotoImage(file="game-over.png")
        img_label = Label(messagebox, image=img)
        img_label.image = img
        img_label.pack(pady=10)
        
        # # Přidání tlačítka OK pro zavření okna
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
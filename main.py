import tkinter as tk
import json
import tkinter as tk
import tkinterhtml as html

class GridApp:
    def __init__(self, root):
        self.root = root
        self.rows = 3
        self.columns = 3
        self.grid_frame = None
        self.create_widgets()

    def create_widgets(self):
        if self.grid_frame:
            # If grid already exists, destroy it before creating a new one
            self.grid_frame.destroy()

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        for row in range(self.rows):
            for column in range(self.columns):
                label = tk.Label(self.grid_frame, text=f"R{row+1}C{column+1}", 
                                 borderwidth=1, relief="solid", width=10, height=5)
                label.grid(row=row, column=column)

        self.button = tk.Button(self.root, text="Change Dimensions", command=self.change_dimensions)
        self.button.pack(pady=10)

    def change_dimensions(self):
        self.rows += 1
        self.columns += 1
        self.create_widgets()

class SequenceApp:
    def __init__(self, root):
        self.root = root
        self.sequence = [
            '1. Declare spells and melee movement',
            '2. Initiative: Each side rolls 1d6.',
            '3. Winning side acts:',
            '  a. Monster morale',
            '  b. Movement',
            '  c. Missile attacks',
            '  d. Spell casting',
            '  e. Melee attacks',
            '4. Other sides act: In initiative order.'
        ]
        self.index = 0
        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10, padx=10)

        for i, step in enumerate(self.sequence):
            self.listbox.insert(i, step)

        self.button = tk.Button(self.root, text="Next Step", command=self.next_step)
        self.button.pack(pady=10)

        self.listbox.selection_set(self.index)

    def next_step(self):
        self.index = (self.index + 1) % len(self.sequence)  # Cycling through the sequence
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.index)

class MonstersApp:
    def __init__(self, root, filename):
        self.root = root
        self.monsters = self.read_monsters(filename)

        self.listbox = tk.Listbox(self.root)
        self.listbox.bind('<<ListboxSelect>>', self.display_monster)
        self.listbox.pack(side='left', fill='y')

        for monster in self.monsters:
            self.listbox.insert(tk.END, monster['name'])

        self.text = tk.Text(self.root)
        self.text.pack(side='right', fill='both', expand=True)

        self.display_full = True  # start with full display
        self.switch_button = tk.Button(self.root, text="Switch Display", command=self.switch_display)
        self.switch_button.pack()

    def extract_relevant_data(self, d):
        relevant_keys = {'_id', 'name', 'permission', 'type', 'data'}
        relevant_data_keys = {'retainer', 'hp', 'ac', 'aac', 'thac0', 'saves', 'movement', 'initiative', 'spells', 'details', 'attacks'}

        new_d = {k: v for k, v in d.items() if k in relevant_keys}
        if 'data' in new_d:
            new_d['data'] = {k: v for k, v in new_d['data'].items() if k in relevant_data_keys}
        return new_d

    def read_monsters(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            monsters = [json.loads(line) for line in f]
        monsters = [self.extract_relevant_data(monster) for monster in monsters]
        return monsters

    def display_monster(self, event=None):
        if event is None:  # No event provided, use current selection
            try:
                selection = self.listbox.curselection()
            except tk.TclError:  # No selection, can't display anything
                return
        else:  # Event provided, use its selection
            selection = event.widget.curselection()

        if selection:
            index = selection[0]
            monster = self.monsters[index]
            self.text.delete('1.0', tk.END)
            if self.display_full:
                self.display_full_json(monster)
            else:
                self.display_selected_features(monster)

    def display_full_json(self, monster):
        self.text.insert(tk.END, json.dumps(monster, indent=4))

    def display_selected_features(self, monster):
        selected_features = {
            "name": monster["name"],
            "hp": monster["data"]["hp"]["value"],
            "hd": monster["data"]["hp"]["hd"],
            "ac": monster["data"]["ac"]["value"],
            "aac": monster["data"]["aac"]["value"],
            "thac0": monster["data"]["thac0"]["value"],
            "bba": monster["data"]["thac0"]["bba"],
            "saves": monster["data"]["saves"],
            "movement": {
                "base": monster["data"]["movement"]["base"],
                "encounter": monster["data"]["movement"]["encounter"],
            },
            "details": monster["data"]["details"],
            "alignment": monster["data"]["details"]["alignment"],
            "xp": monster["data"]["details"]["xp"],
            "treasure": monster["data"]["details"]["treasure"],
            "appearing": monster["data"]["details"]["appearing"],
            "morale": monster["data"]["details"]["morale"],
        }
        self.text.insert(tk.END, json.dumps(selected_features, indent=4))

    def switch_display(self):
        self.display_full = not self.display_full
        self.display_monster(None)  # re-display the current monster

class AbilitiesApp:
    def __init__(self, root, filename):
        self.root = root
        self.abilities = self.read_abilities(filename)

        self.listbox = tk.Listbox(self.root)
        self.listbox.bind('<<ListboxSelect>>', self.display_ability)
        self.listbox.pack(side='left', fill='y')

        for ability in self.abilities:
            self.listbox.insert(tk.END, ability['name'])

        self.html_display = html.HtmlFrame(self.root)
        self.html_display.pack(side='right', fill='both', expand=True)

    def read_abilities(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            abilities = [json.loads(line) for line in f]
        return abilities

    def display_ability(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            ability = self.abilities[index]
            description = ability['data']['description']
            print('debug description:', description)
            # self.html_display.set_content(description)

# Creating root for GridApp
root1 = tk.Tk()
root1.title("GridApp")
app1 = GridApp(root1)

# Creating Toplevel for SequenceApp
root2 = tk.Toplevel(root1)
root2.title("SequenceApp")
app2 = SequenceApp(root2)

# Creating Toplevel for MonstersApp
root3 = tk.Toplevel(root1)
root3.title("MonstersApp")
app3 = MonstersApp(root3, 'monsters.db')

# Creating Toplevel for AbilitiesApp
root4 = tk.Toplevel(root1)
root4.title("AbilitiesApp")
app4 = AbilitiesApp(root4, 'abilities-cleric.db')

root1.mainloop()
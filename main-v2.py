import sys
import json
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QSplitter, QPushButton
from PyQt5.QtWidgets import QLabel, QTextEdit, QHBoxLayout, QListWidgetItem, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

class DiceRollerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dice Roller')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.textbox = QLineEdit(self)
        self.textbox.returnPressed.connect(self.on_click)
        self.layout.addWidget(self.textbox)

        self.roll_button = QPushButton('Roll Dice', self)
        self.roll_button.clicked.connect(self.on_click)
        self.layout.addWidget(self.roll_button)

        self.result_label = QLabel(self)
        self.layout.addWidget(self.result_label)

    def on_click(self):
        dice_string = self.textbox.text().strip()

        try:
            if dice_string[0].lower() == 'd':
                num_dice = 1
                num_sides = int(dice_string[1:])
            else:
                num_dice, num_sides = map(int, dice_string.split('d'))

            if len(str(num_dice)) > 6 or len(str(num_sides)) > 6:
                raise ValueError

            roll_result = sum(random.randint(1, num_sides) for _ in range(num_dice))
            self.result_label.setText(f'You rolled: {roll_result}')

        except ValueError:
            self.result_label.setText('Invalid Input')

class MoraleCheckWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Roll Dice")
        self.button.setShortcut('Ctrl+R')
        self.button.clicked.connect(self.roll_dice)

        self.result_label = QLabel("")

        font = self.result_label.font()
        font.setPointSize(16)
        self.result_label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def roll_dice(self):
        dice_roll_1 = random.randint(1, 6)
        dice_roll_2 = random.randint(1, 6)
        result = dice_roll_1 + dice_roll_2

        self.result_label.setText(str(result))

class InitiativeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Decide Initiative")
        self.button.setShortcut('Ctrl+I')
        self.button.clicked.connect(self.decide_initiative)

        self.result_label = QLabel("")

        font = self.result_label.font()
        font.setPointSize(16)
        self.result_label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def decide_initiative(self):
        party_number = random.randint(1, 6)
        enemy_number = random.randint(1, 6)

        if party_number > enemy_number:
            result = "PARTY"
        elif enemy_number > party_number:
            result = "ENEMY"
        else:
            result = "DRAW"

        self.result_label.setText(result)

class SequenceItem(QWidget):
    def __init__(self, sequence_text):
        super().__init__()

        self.sequence_label = QLabel(sequence_text)

        layout = QHBoxLayout()
        layout.addWidget(self.sequence_label)
        self.setLayout(layout)

class SequenceApp(QWidget):
    def __init__(self):
        super().__init__()

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

        self.listbox = QListWidget()
        for i, step in enumerate(self.sequence):
            item = QListWidgetItem()
            sequence_item_widget = SequenceItem(step)
            item.setSizeHint(sequence_item_widget.sizeHint())
            self.listbox.addItem(item)
            self.listbox.setItemWidget(item, sequence_item_widget)

        self.listbox.currentRowChanged.connect(self.change_widget)

        self.button = QPushButton("Next Step")
        self.button.setShortcut('Ctrl+N')
        self.button.clicked.connect(self.next_step)

        self.widget_holder = QWidget()
        self.widget_layout = QVBoxLayout()
        self.widget_holder.setLayout(self.widget_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.listbox, 1)
        layout.addWidget(self.widget_holder, 1)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.listbox.setCurrentRow(self.index)

    def next_step(self):
        self.index = (self.index + 1) % len(self.sequence)  # Cycling through the sequence
        self.listbox.setCurrentRow(self.index)

    def change_widget(self):
        # remove the old widgets
        for i in reversed(range(self.widget_layout.count())): 
            self.widget_layout.itemAt(i).widget().setParent(None)

        if self.listbox.currentRow() == 1:
            self.widget_layout.addWidget(InitiativeWidget())
        elif self.listbox.currentRow() == 3:
            self.widget_layout.addWidget(MoraleCheckWidget())

class AbilitiesApp(QMainWindow):
    def __init__(self, filename):
        super().__init__()

        self.abilities = self.read_abilities(filename)
        self.initUI()

        # Adding DiceRollerWidget
        self.dice_roller = DiceRollerWidget()
        self.dice_roller.hide()  # Hide it initially

        # We are adding DiceRollerApp to the QVBoxLayout
        self.layout.addWidget(self.dice_roller)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            if self.dice_roller.isVisible():
                self.dice_roller.hide()
            else:
                self.dice_roller.show()
                self.dice_roller.textbox.setFocus()  # Set focus to the text box
        super().keyPressEvent(event)  # Call the original keyPressEvent

    def initUI(self):
        self.listbox = QListWidget()
        self.listbox.itemSelectionChanged.connect(self.display_ability)
        for ability in self.abilities:
            self.listbox.addItem(ability['name'])

        self.init_html_display()
        self.sequence_app = SequenceApp()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.sequence_app)
        splitter.addWidget(self.listbox)
        splitter.addWidget(self.html_display)

        # Here is the QVBoxLayout
        self.layout = QVBoxLayout()
        self.layout.addWidget(splitter)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

    def init_html_display(self):
        self.html_display = QWebEngineView()
        self.html_display.setHtml('')

    def read_abilities(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            abilities = [json.loads(line) for line in f]
        return abilities

    def display_ability(self):
        selected_items = self.listbox.selectedItems()
        if selected_items:
            selected_ability_name = selected_items[0].text()
            selected_ability = next((ability for ability in self.abilities if ability['name'] == selected_ability_name), None)
            if selected_ability:
                description = selected_ability['data']['description']
                print('debug description:', description)
                self.html_display.setHtml(description)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    abilities_app = AbilitiesApp("abilities-cleric.db")
    # abilities_app = SequenceApp()
    abilities_app.show()
    sys.exit(app.exec_())
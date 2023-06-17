import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QSplitter, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

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
            self.listbox.addItem(step)

        self.button = QPushButton("Next Step")
        self.button.clicked.connect(self.next_step)

        layout = QVBoxLayout()
        layout.addWidget(self.listbox)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.listbox.setCurrentRow(self.index)

    def next_step(self):
        self.index = (self.index + 1) % len(self.sequence)  # Cycling through the sequence
        self.listbox.setCurrentRow(self.index)

class AbilitiesApp(QMainWindow):
    def __init__(self, filename):
        super().__init__()

        self.abilities = self.read_abilities(filename)
        self.initUI()

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

        layout = QVBoxLayout()
        layout.addWidget(splitter)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
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
    abilities_app.show()
    sys.exit(app.exec_())
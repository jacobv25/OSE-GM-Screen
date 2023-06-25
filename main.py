import sys
import json
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QSplitter, QPushButton
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QListWidgetItem, QLineEdit, QTextEdit, QCompleter
import subprocess
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint

srd_url = 'https://oldschoolessentials.necroticgnome.com/srd/index.php/Main_Page'
generator_url = 'https://oldschoolessentials.necroticgnome.com/generators/'
path_to_board = "C:\\dev\\workspace\\DM Screen\\venv\\Scripts\\python.exe"
board = "battle_map.py"

class WebViewer(QWebEngineView):
    def __init__(self, url):
        super().__init__()
        self.load(QUrl(url))

    def search(self, query):
        js_fill = f"document.getElementById('searchInput').value = '{query}';"
        js_click = "document.getElementById('searchGoButton').click();"
        
        # Fill the search bar
        self.page().runJavaScript(js_fill)
        
        # Click the search button
        self.page().runJavaScript(js_click)

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        
        self.drawing = False
        self.last_point = QPoint()
        
        self.image = QPixmap(self.size())
        self.image.fill(Qt.white)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

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

class AbilitiesApp(QWidget):  
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

        # QVBoxLayout for AbilitiesApp
        self.layout = QVBoxLayout()
        self.layout.addWidget(splitter)
        self.setLayout(self.layout)  # set the layout

class ConsoleTerminal(QWidget):
    def __init__(self, web_viewer):
        super().__init__()

        # Create the QTextEdit widget for command history and output
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Create the QLineEdit widget for command input
        self.line_edit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

        # Web viewer reference
        self.web_viewer = web_viewer

        # Define commands
        self.commands = {
            "roll": self.roll_dice,
            "clear": self.clear_console,
            "search": self.search_web,
            "show": self.show_module,            
            "hide": self.hide_module            
        }

        # Initialize command history and history position
        self.command_history = []
        self.history_pos = 0

        # Add autocompletion
        self.completer = QCompleter(list(self.commands.keys()))
        self.line_edit.setCompleter(self.completer)

        # Connect the returnPressed signal to the execute_command function
        self.line_edit.returnPressed.connect(self.execute_command)


    def execute_command(self):
        # Get the command text from the line_edit widget
        text = self.line_edit.text()

        # Clear the line_edit widget
        self.line_edit.clear()

        # Add command to history and reset history position
        self.command_history.append(text)
        self.history_pos = len(self.command_history)

        # Split the command into a list of words
        words = text.split()

        if len(words) == 0:
            # No command was entered
            return

        # The command is the first word
        command = words[0]

        # The rest of the words are the arguments
        args = words[1:]

        if command not in self.commands:
            # Unknown command
            self.text_edit.append(f"Unknown command: {command}")
            return

        try:
            # Try to execute the command
            self.commands[command](*args)
        except Exception as e:
            # If something went wrong, display the error to the user
            self.text_edit.append(str(e))

    def keyPressEvent(self, event):
        # If up or down key is pressed, navigate through command history
        if event.key() == Qt.Key_Up:
            if self.history_pos > 0:
                self.history_pos -= 1
                self.line_edit.setText(self.command_history[self.history_pos])
        elif event.key() == Qt.Key_Down:
            if self.history_pos < len(self.command_history) - 1:
                self.history_pos += 1
                self.line_edit.setText(self.command_history[self.history_pos])
            elif self.history_pos == len(self.command_history) - 1:
                self.history_pos += 1
                self.line_edit.clear()
        else:
            super(ConsoleTerminal, self).keyPressEvent(event)

    def roll_dice(self, dice):
        try:
            _, sides = dice.split('d')
            sides = int(sides)
            result = random.randint(1, sides)
            self.text_edit.append(f"You rolled a {result} on a {dice}.")
        except ValueError:
            self.text_edit.append(f"Invalid dice format: {dice}. Please use 'dx' format, where x is the number of sides.")
    
    def clear_console(self):
        self.text_edit.clear()

    def search_web(self, query):
        self.web_viewer.search(''.join(query))

    def show_module(self, module_name):
        # Get the module object from the module dictionary passed by the CoreApp
        module = self.module_dict.get(module_name)

        if module is not None:
            # If the module is hidden, show it
            if not module.isVisible():
                module.show()
                self.text_edit.append(f"{module_name} module is now visible.")
        else:
            self.text_edit.append(f"Unknown module: {module_name}")

    def hide_module(self, module_name):
        # Get the module object from the module dictionary passed by the CoreApp
        module = self.module_dict.get(module_name)

        if module is not None:
            # If the module is visible, hide it
            if module.isVisible():
                module.hide()
                self.text_edit.append(f"{module_name} module is now hidden.")
        else:
            self.text_edit.append(f"Unknown module: {module_name}")

class CoreApp(QMainWindow):
    def __init__(self, *widgets):
        super().__init__()
        self.widgets = widgets
        self.dice_roller = DiceRollerWidget()
        self.dice_roller.hide()
        
        # check if web_viewer is the first widget
        if not isinstance(widgets[0], WebViewer):
            #throw exception
            raise Exception("WebViewer must be the first widget")
        # check if console_terminal is the last widget
        if not isinstance(widgets[-1], ConsoleTerminal):
            # throw exception
            raise Exception("ConsoleTerminal must be the last widget")
        
        self.web_viewer = widgets[0]
        self.console_terminal = widgets[-1]
        self.console_textbox = widgets[-1].line_edit
        self.initUI(*widgets, self.dice_roller)
        
        # Create the module dictionary and pass it to the console terminal
        self.module_dict = {
            "dice_roller": self.dice_roller,
            "web_viewer": self.web_viewer,
            # add more modules here
        }
        self.console_terminal.module_dict = self.module_dict

    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key_T and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.AltModifier:
            self.console_textbox.setFocus()
        
        if event.key() == Qt.Key_B and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            subprocess.Popen([path_to_board, board])
            
        if event.key() == Qt.Key_G and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            url = QUrl(generator_url)
            self.web_viewer.load(url)
            
        if event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            url = QUrl(srd_url)
            self.web_viewer.load(url)
        
        if event.key() == Qt.Key_D and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            if self.dice_roller.isVisible():
                self.dice_roller.hide()
            else:
                self.dice_roller.show()
                self.dice_roller.textbox.setFocus()  # Set focus to the text box
        
        super().keyPressEvent(event)  # Call the original keyPressEvent

    def initUI(self, *widgets):
        splitter = QSplitter(Qt.Horizontal)

        # Add each widget to the splitter
        for widget in widgets:
            splitter.addWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(splitter)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Initialize each of your application components here
    sequence_app = SequenceApp()
    canvas_app = Canvas()
    
    web_viewer = WebViewer(srd_url)
    console_terminal = ConsoleTerminal(web_viewer)
    
    # console_terminal must be last in the list of widgets
    core_app = CoreApp(web_viewer, console_terminal)
    core_app.show()

    sys.exit(app.exec_())

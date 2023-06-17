import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class HtmlDisplayApp(QMainWindow):
    def __init__(self):
        super(HtmlDisplayApp, self).__init__()

        self.initUI()

    def initUI(self):
        self.html_display = QWebEngineView()

        layout = QVBoxLayout()
        layout.addWidget(self.html_display)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.display_html()

    def display_html(self):
        html_content = """
        <p style="box-sizing: border-box; user-select: text; color: #191813;">A cleric may establish or build a stronghold. So long as the cleric is currently in favour with their god, a stronghold may be bought or built at half the normal price, due to divine intervention.</p>
        <p style="box-sizing: border-box; user-select: text; color: #191813;">Once a stronghold is established, the cleric will attract followers (5d6 &times; 10 fighters of level 1&ndash;2). These troops are completely devoted to the cleric, never checking morale. The referee decides which proportions of followers are 1st and 2nd level and which are bowmen, infantry, etc.</p>
        """
        self.html_display.setHtml(html_content)


def main():
    app = QApplication(sys.argv)
    ex = HtmlDisplayApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, QEventLoop

class SaveWebPage(QWebEngineView):
    def __init__(self):
        super(SaveWebPage, self).__init__()
        self.loadFinished.connect(self._on_load_finished)

    def load_page(self, url):
        self.load(QUrl(url))
        # Since page loading is asynchronous, we spin an event loop
        loop = QEventLoop()
        self.loadFinished.connect(loop.quit)
        loop.exec_()

    def _on_load_finished(self):
        self.page().saveToMimeData(self.page().profile().defaultProfile().downloadRequested)

class MainWindow(QWebEngineView):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set the url for the webpage
        self.setUrl(QUrl("https://oldschoolessentials.necroticgnome.com/srd/index.php/Cleric"))

        # Save the webpage
        self.webSaver = SaveWebPage()
        self.webSaver.load_page("https://oldschoolessentials.necroticgnome.com/srd/index.php/Cleric")

def main():
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create and display the main window
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

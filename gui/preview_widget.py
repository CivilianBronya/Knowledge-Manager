from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
import markdown2

class PreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Markdown 预览"))
        self.browser = QTextBrowser()
        self.browser.setStyleSheet("background-color: #f9f9f9;")
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def render_markdown(self, text):
        html = markdown2.markdown(text)
        self.browser.setHtml(html)

    def clear(self):
        self.browser.clear()

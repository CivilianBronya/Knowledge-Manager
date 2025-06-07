from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtCore import Qt

from gui.find_bar import FindBar
from core.highlighter import KeywordHighlighter


class  EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_find()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Markdown 编辑器"))

        self.find_bar = FindBar()
        self.find_bar.hide()

        self.text_edit = QTextEdit()
        self.highlighter = KeywordHighlighter(self.text_edit.document())

        self.layout.addWidget(self.find_bar)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def init_find(self):
        self.find_bar.search_triggered.connect(self.search)
        self.find_bar.next_triggered.connect(self.find_next)
        self.find_bar.prev_triggered.connect(self.find_prev)
        self.find_bar.closed.connect(self.hide_find_bar)

        self.last_keyword = ""
        self.last_cursor_pos = 0

    def get_text(self):
        return self.text_edit.toPlainText()

    def set_text(self, text):
        self.text_edit.setPlainText(text)
        self.clear_highlight()

    def clear(self):
        self.text_edit.clear()
        self.clear_highlight()

    def show_find_bar(self):
        self.find_bar.show()
        self.find_bar.setFocus()
        self.find_bar.raise_()

    def hide_find_bar(self):
        self.find_bar.hide()
        self.clear_highlight()

    def search(self, keyword):
        self.last_keyword = keyword
        self.last_cursor_pos = 0
        self.highlighter.set_keywords([keyword])
        self.find_next()

    def find_next(self):
        if not self.last_keyword:
            return
        doc = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        found = doc.find(self.last_keyword, pos)
        if found.isNull():
            # 循环查找
            found = doc.find(self.last_keyword, 0)
        if not found.isNull():
            self.text_edit.setTextCursor(found)

    def find_prev(self):
        if not self.last_keyword:
            return
        doc = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        pos = cursor.position()
        found = doc.find(self.last_keyword, pos, QTextDocument.FindBackward)
        if found.isNull():
            # 循环查找
            end_pos = self.text_edit.toPlainText().__len__()
            found = doc.find(self.last_keyword, end_pos, QTextDocument.FindBackward)
        if not found.isNull():
            self.text_edit.setTextCursor(found)

    def clear_highlight(self):
        self.highlighter.set_keywords([])

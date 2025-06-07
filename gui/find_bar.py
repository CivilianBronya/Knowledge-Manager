from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal


class FindBar(QWidget):
    search_triggered = pyqtSignal(str)
    next_triggered = pyqtSignal()
    prev_triggered = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("查找内容...")
        self.search_input.returnPressed.connect(self.emit_search)

        self.next_btn = QPushButton("下一个")
        self.prev_btn = QPushButton("上一个")
        self.close_btn = QPushButton("关闭")

        self.next_btn.clicked.connect(self.next_triggered)
        self.prev_btn.clicked.connect(self.prev_triggered)
        self.close_btn.clicked.connect(self.closed)
        self.close_btn.clicked.connect(self.hide)

        layout.addWidget(self.search_input)
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.next_btn)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def emit_search(self):
        keyword = self.search_input.text().strip()
        if keyword:
            self.search_triggered.emit(keyword)

    def setFocus(self):
        self.search_input.setFocus()

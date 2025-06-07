from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal

class SearchBar(QWidget):
    # 文本变化信号，外部可连接
    text_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("搜索:")
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("请输入搜索关键词")

        layout.addWidget(label)
        layout.addWidget(self.edit)

        self.edit.textChanged.connect(self.text_changed.emit)

    def get_text(self):
        return self.edit.text()

    def set_text(self, text):
        self.edit.setText(text)

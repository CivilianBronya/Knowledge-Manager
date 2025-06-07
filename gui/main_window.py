import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QSplitter, QPushButton, QMessageBox, QInputDialog,
    QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from gui.editor_widget import EditorWidget
from gui.preview_widget import PreviewWidget
from gui.search_bar import SearchBar
from core.note_manager import NoteManager
from core.search_engine import SearchEngine
import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.APP_TITLE)
        self.setGeometry(200, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.set_window_icon()
        self.load_stylesheet()

        self.note_manager = NoteManager()
        self.current_note = None

        self.init_ui()
        self.load_notes()

    def set_window_icon(self):
        if os.path.exists(config.ICON_PATH):
            self.setWindowIcon(QIcon(config.ICON_PATH))

    def load_stylesheet(self):
        if os.path.exists(config.STYLE_PATH):
            with open(config.STYLE_PATH, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)

        self.search_bar = SearchBar()
        self.search_bar.text_changed.connect(self.filter_notes)

        # 标签区
        self.tag_list = QListWidget()
        self.tag_list.setSelectionMode(QListWidget.MultiSelection)
        self.tag_list.itemSelectionChanged.connect(self.filter_notes_by_tags)

        self.add_tag_btn = QPushButton("添加标签")
        self.add_tag_btn.clicked.connect(self.add_tag)

        self.remove_tag_btn = QPushButton("删除标签")
        self.remove_tag_btn.clicked.connect(self.remove_tag)

        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.on_note_selected)

        self.new_btn = QPushButton("新建笔记")
        self.new_btn.clicked.connect(self.create_note)

        self.delete_btn = QPushButton("删除笔记")
        self.delete_btn.clicked.connect(self.delete_note)

        self.save_btn = QPushButton("保存笔记")
        self.save_btn.clicked.connect(self.save_note)

        # 左侧布局添加控件
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(QLabel("标签列表"))
        left_layout.addWidget(self.tag_list)
        left_layout.addWidget(self.add_tag_btn)
        left_layout.addWidget(self.remove_tag_btn)
        left_layout.addWidget(QLabel("笔记列表"))
        left_layout.addWidget(self.note_list)
        left_layout.addWidget(self.new_btn)
        left_layout.addWidget(self.delete_btn)
        left_layout.addWidget(self.save_btn)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)

        self.editor = EditorWidget()
        self.preview = PreviewWidget()
        self.editor.text_edit.textChanged.connect(self.update_preview)

        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.preview)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_container)
        splitter.addWidget(right_container)
        splitter.setSizes([400, 1200])

        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)

    def load_notes(self):
        self.note_list.clear()
        notes = self.note_manager.list_notes()
        self.note_list.addItems(notes)

    def on_note_selected(self, item):
        title = item.text()
        content = self.note_manager.get_note(title)
        self.current_note = title
        self.editor.set_text(content)
        self.update_preview()
        self.refresh_tags()

    def create_note(self):
        existing = set(self.note_manager.list_notes())
        title, ok = QInputDialog.getText(self, "新建笔记", "请输入笔记标题:")

        if not ok:
            return

        title = title.strip()
        if not title:
            base_name = "新建笔记"
            idx = 1
            new_name = base_name
            while new_name in existing:
                new_name = f"{base_name} {idx}"
                idx += 1
            title = new_name
        else:
            if title in existing:
                QMessageBox.warning(self, "重名警告", f"笔记《{title}》已存在，请使用其他标题。")
                return

        self.note_manager.save_note(title, "# 新笔记\n")
        self.note_manager.set_tags(title, [])  # 初始化空标签
        self.load_notes()

        items = self.note_list.findItems(title, Qt.MatchExactly)
        if items:
            self.note_list.setCurrentItem(items[0])
            self.on_note_selected(items[0])

    def delete_note(self):
        if not self.current_note:
            QMessageBox.warning(self, "删除笔记", "请先选择一个笔记")
            return
        confirm = QMessageBox.question(self, "删除笔记", f"确认删除笔记：{self.current_note}？",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.note_manager.delete_note(self.current_note)
            self.current_note = None
            self.load_notes()
            self.editor.clear()
            self.preview.clear()
            self.tag_list.clear()

    def save_note(self):
        if not self.current_note:
            QMessageBox.warning(self, "保存笔记", "请先选择一个笔记")
            return
        content = self.editor.get_text()
        self.note_manager.save_note(self.current_note, content)
        QMessageBox.information(self, "保存成功", f"笔记《{self.current_note}》已保存")

    def update_preview(self):
        text = self.editor.get_text()
        self.preview.render_markdown(text)

    def filter_notes(self, text):
        all_notes = self.note_manager.list_notes()
        notes_content = {title: self.note_manager.get_note(title) for title in all_notes}
        engine = SearchEngine(notes_content)
        filtered = engine.search_by_title(text)
        self.note_list.clear()
        self.note_list.addItems(filtered)

    def filter_notes_by_tags(self):
        selected_tags = [item.text() for item in self.tag_list.selectedItems()]
        if not selected_tags:
            self.load_notes()
            return

        filtered = []
        for title in self.note_manager.list_notes():
            tags = self.note_manager.get_tags(title)
            if all(tag in tags for tag in selected_tags):
                filtered.append(title)

        self.note_list.clear()
        self.note_list.addItems(filtered)

    def refresh_tags(self):
        self.tag_list.clear()
        if not self.current_note:
            return
        tags = self.note_manager.get_tags(self.current_note)
        self.tag_list.addItems(tags)

    def add_tag(self):
        if not self.current_note:
            QMessageBox.warning(self, "添加标签", "请先选择一个笔记")
            return
        tag, ok = QInputDialog.getText(self, "添加标签", "请输入新标签：")
        if ok and tag:
            current_tags = self.note_manager.get_tags(self.current_note)
            if tag not in current_tags:
                current_tags.append(tag)
                self.note_manager.set_tags(self.current_note, current_tags)
                self.refresh_tags()

    def remove_tag(self):
        if not self.current_note:
            QMessageBox.warning(self, "删除标签", "请先选择一个笔记")
            return
        selected_items = self.tag_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "删除标签", "请先选择要删除的标签")
            return
        tags = self.note_manager.get_tags(self.current_note)
        for item in selected_items:
            tag = item.text()
            if tag in tags:
                tags.remove(tag)
        self.note_manager.set_tags(self.current_note, tags)
        self.refresh_tags()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            self.editor.show_find_bar()

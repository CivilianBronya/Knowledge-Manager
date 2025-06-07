import os
import json
from config import NOTES_DIR

class FileStorage:
    def __init__(self):
        os.makedirs(NOTES_DIR, exist_ok=True)

    def _get_note_path(self, title):
        return os.path.join(NOTES_DIR, f"{title}.md")

    def _get_meta_path(self, title):
        return os.path.join(NOTES_DIR, f"{title}.json")

    def get_all_notes(self):
        """返回所有笔记标题（去掉.md后缀）"""
        titles = []
        for filename in os.listdir(NOTES_DIR):
            if filename.endswith(".md"):
                titles.append(filename[:-3])
        return sorted(titles)

    def load_note_content(self, title):
        path = self._get_note_path(title)
        if not os.path.exists(path):
            return ""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def save_note_content(self, title, content):
        path = self._get_note_path(title)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def delete_note(self, title):
        content_path = self._get_note_path(title)
        meta_path = self._get_meta_path(title)
        if os.path.exists(content_path):
            os.remove(content_path)
        if os.path.exists(meta_path):
            os.remove(meta_path)

    def load_note_metadata(self, title):
        path = self._get_meta_path(title)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_note_metadata(self, title, metadata):
        path = self._get_meta_path(title)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

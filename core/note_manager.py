from core.file_storage import FileStorage

class NoteManager:
    def __init__(self):
        self.storage = FileStorage()

    def list_notes(self):
        """列出所有笔记标题"""
        return self.storage.get_all_notes()

    def get_note(self, title):
        """获取指定笔记内容"""
        return self.storage.load_note_content(title)

    def save_note(self, title, content):
        """保存或更新笔记"""
        self.storage.save_note_content(title, content)

    def delete_note(self, title):
        """删除笔记"""
        self.storage.delete_note(title)

    def get_tags(self, title):
        """获取某个笔记的标签列表"""
        metadata = self.storage.load_note_metadata(title)
        return metadata.get("tags", [])

    def set_tags(self, title, tags):
        """设置某个笔记的标签列表"""
        metadata = self.storage.load_note_metadata(title)
        metadata["tags"] = tags
        self.storage.save_note_metadata(title, metadata)

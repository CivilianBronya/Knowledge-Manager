class SearchEngine:
    def __init__(self, notes):
        """
        notes: dict，格式 {title: content, ...}
        """
        self.notes = notes

    def search_by_title(self, keyword):
        """
        按标题搜索，返回匹配标题列表
        """
        keyword = keyword.strip().lower()
        if not keyword:
            return list(self.notes.keys())
        return [title for title in self.notes if keyword in title.lower()]

    def search_by_content(self, keyword):
        """
        按内容搜索，返回匹配标题列表
        """
        keyword = keyword.strip().lower()
        if not keyword:
            return list(self.notes.keys())
        return [title for title, content in self.notes.items() if keyword in content.lower()]

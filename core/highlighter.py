from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtCore import Qt, QRegularExpression

class KeywordHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.keywords = []

        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("#ffff99"))
        self.highlight_format.setForeground(Qt.black)

    def set_keywords(self, keywords):
        """设置需要高亮的关键词"""
        self.keywords = keywords
        self.rehighlight()

    def highlightBlock(self, text):
        if not self.keywords:
            return

        for keyword in self.keywords:
            if not keyword:
                continue
            # 忽略大小写匹配
            pattern = QRegularExpression(keyword, QRegularExpression.CaseInsensitiveOption)
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, self.highlight_format)

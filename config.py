import os

APP_TITLE = "知识管理系统"
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
ICON_PATH = os.path.join(ASSETS_DIR, 'icon.png')
STYLE_PATH = os.path.join(ASSETS_DIR, 'style.qss')

NOTES_DIR = os.path.join(BASE_DIR, 'data', 'notes')

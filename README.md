# 知识管理系统（基于 PyQt5 的 Markdown 笔记应用）

> 作者：星丶白羽莲  
> 时间：2025年6月  
> 技术栈：Python3, PyQt5, Markdown  
> 项目目录：data/notes/  

---

## 🧠 项目简介

本项目是一个轻量、简洁、可扩展的 Markdown 笔记管理工具，主要面向个人知识管理与毕业设计演示使用。通过图形化界面实现笔记的创建、编辑、保存、预览、标签分类和搜索等功能，支持笔记内容的实时 Markdown 渲染与标签化组织，提升了内容管理的效率和可读性。

兼易用性和可扩展性，本项目基础功能全部完善!

---

## 📌 主要功能

### ✅ 核心功能模块：

- 📁 **笔记管理：** 创建、编辑、删除、保存笔记内容（`.md` 文件）
- 🔍 **搜索支持：** 支持标题搜索和实时筛选笔记
- 🏷️ **标签系统：** 每篇笔记支持打多个标签，便于分类整理和过滤查看
- 🧾 **双栏结构：** 左栏笔记列表与标签过滤，右栏为 Markdown 编辑器 + 预览视图
- ♻️ **数据持久化：** 所有笔记与标签信息均本地保存于 `data/notes/` 文件夹中
- 🎨 **自定义样式：** 可通过 QSS 文件自定义 UI 风格（如 `style.qss`）

---

## 🧱 模块结构说明
project_root/
│
├── main.py # 程序入口
├── config.py # 全局配置项（窗口大小、资源路径等）
├── data/
│ └── notes/ # 所有笔记存储在此目录（.md 与 .json 元数据）
│
├── core/
│ ├── note_manager.py # 提供对外接口：增删改查、标签管理
│ ├── file_storage.py # 读写本地文件与标签元数据（.md 和 .json）
│ ├── search_engine.py # 简单搜索引擎，用于标题或内容过滤
│ └── highlighter.py # 查询文字，高亮显示
│
├── gui/
│ ├── main_window.py # 主窗口 UI 布局
│ ├── editor_widget.py # Markdown 文本编辑区
│ ├── preview_widget.py # Markdown 渲染区域
│ ├── find_bar.py # 文字高亮匹配控件
│ └── search_bar.py # 搜索栏控件
│
└── extensions/
└── dictionary_helper.py # 预留的扩展功能模块（目前为空）

---

## 🧪 如何运行

确保系统已安装 Python 3.7+ 和 PyQt5：

```bash
pip install PyQt5 markdown

python main.py


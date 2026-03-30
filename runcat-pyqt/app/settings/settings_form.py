#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Settings form module
"""

import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class Translator:
    """Language translator"""
    
    def __init__(self):
        self.translations = {
            "English": {
                "Runner": "Runner",
                "Theme": "Theme",
                "Speed Based On": "Speed Based On",
                "FPS Max Limit": "FPS Max Limit",
                "Launch at startup": "Launch at startup",
                "Manage Runners": "Manage Runners",
                "Language": "Language",
                "Information": "Information",
                "Exit": "Exit",
                "CPU": "CPU",
                "Memory": "Memory",
                "Network": "Network",
                "System": "System",
                "Light": "Light",
                "Dark": "Dark",
                "FPS30": "30 FPS",
                "FPS40": "40 FPS",
                "FPS50": "50 FPS",
                "FPS60": "60 FPS",
                "English": "English",
                "中文": "中文",
                "Version 1.0.0": "Version 1.0.0",
                "Open Repository": "Open Repository",
                "Custom Runners": "Custom Runners",
                "Import GIF": "Import GIF",
                "Remove": "Remove",
                "Close": "Close",
                "Success": "Success",
                "Error": "Error",
                "Confirm": "Confirm",
                "Successfully imported runner: {}": "Successfully imported runner: {}",
                "Failed to import runner. Please check the GIF file.": "Failed to import runner. Please check the GIF file.",
                "Built-in runners cannot be removed.": "Built-in runners cannot be removed.",
                "Are you sure you want to remove runner '{}'?": "Are you sure you want to remove runner '{}'?",
                "Successfully removed runner: {}": "Successfully removed runner: {}",
                "Failed to remove runner.": "Failed to remove runner.",
                "Settings": "Settings",
                "GIF files (*.gif)": "GIF files (*.gif)",
                "[Built-in] {}": "[Built-in] {}",
                "[内置] {}": "[Built-in] {}"
            },
            "中文": {
                "Runner": "角色",
                "Theme": "主题",
                "Speed Based On": "速度基于",
                "FPS Max Limit": "最大 FPS 限制",
                "Launch at startup": "开机自启动",
                "Manage Runners": "管理角色",
                "Language": "语言",
                "Information": "关于",
                "Exit": "退出",
                "CPU": "CPU",
                "Memory": "内存",
                "Network": "网络",
                "System": "系统",
                "Light": "浅色",
                "Dark": "深色",
                "FPS30": "30 FPS",
                "FPS40": "40 FPS",
                "FPS50": "50 FPS",
                "FPS60": "60 FPS",
                "English": "English",
                "中文": "中文",
                "Version 1.0.0": "版本 1.0.0",
                "Open Repository": "打开仓库",
                "Custom Runners": "自定义角色",
                "Import GIF": "导入 GIF",
                "Remove": "删除",
                "Close": "关闭",
                "Success": "成功",
                "Error": "错误",
                "Confirm": "确认",
                "Successfully imported runner: {}": "成功导入角色: {}",
                "Failed to import runner. Please check the GIF file.": "导入角色失败，请检查GIF文件。",
                "Built-in runners cannot be removed.": "内置角色不能删除。",
                "Are you sure you want to remove runner '{}'?": "确定要删除角色 '{}' 吗？",
                "Successfully removed runner: {}": "成功删除角色: {}",
                "Failed to remove runner.": "删除角色失败。",
                "Settings": "设置",
                "GIF files (*.gif)": "GIF文件 (*.gif)",
                "[Built-in] {}": "[内置] {}",
                "[内置] {}": "[Built-in] {}"
        },
        "中文繁体": {
            "Runner": "角色",
            "Theme": "主題",
            "Speed Based On": "速度基於",
            "FPS Max Limit": "最大 FPS 限制",
            "Launch at startup": "開機自啟動",
            "Manage Runners": "管理角色",
            "Language": "語言",
            "Information": "關於",
            "Exit": "退出",
            "CPU": "CPU",
            "Memory": "記憶體",
            "Network": "網路",
            "System": "系統",
            "Light": "淺色",
            "Dark": "深色",
            "FPS30": "30 FPS",
            "FPS40": "40 FPS",
            "FPS50": "50 FPS",
            "FPS60": "60 FPS",
            "English": "English",
            "中文": "简体中文",
            "中文繁体": "繁體中文",
            "Version 1.0.0": "版本 1.0.0",
            "Open Repository": "打開倉庫",
            "Custom Runners": "自定義角色",
            "Import GIF": "匯入 GIF",
            "Remove": "刪除",
            "Close": "關閉",
            "Success": "成功",
            "Error": "錯誤",
            "Confirm": "確認",
            "Successfully imported runner: {}": "成功匯入角色: {}",
            "Failed to import runner. Please check the GIF file.": "匯入角色失敗，請檢查GIF檔案。",
            "Built-in runners cannot be removed.": "內建角色不能刪除。",
            "Are you sure you want to remove runner '{}'?": "確定要刪除角色 '{}' 嗎？",
            "Successfully removed runner: {}": "成功刪除角色: {}",
            "Failed to remove runner.": "刪除角色失敗。",
            "Settings": "設定",
            "GIF files (*.gif)": "GIF檔案 (*.gif)",
            "[Built-in] {}": "[內建] {}",
            "[内置] {}": "[Built-in] {}"
        }
    }
    
    def translate(self, text, language):
        """Translate text to specified language"""
        if language in self.translations:
            if text in self.translations[language]:
                return self.translations[language][text]
        return text


class SettingsForm(QDialog):
    """Settings form"""
    
    def __init__(self, language="English", theme=None, parent=None):
        super().__init__(parent)
        
        # Initialize translator
        self.translator = Translator()
        self.language = language
        self.theme = theme
        
        # Set window title
        self.setWindowTitle(self.translator.translate("Manage Runners", self.language))
        self.setGeometry(100, 100, 400, 300)
        self.setModal(True)
        
        # Set window icon
        from PyQt5.QtGui import QIcon, QPixmap
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "icons", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize custom runner manager
        from app.animation.custom_runner import CustomRunnerManager
        self.custom_runner_manager = CustomRunnerManager()
        self.custom_runner_manager.load_custom_runners()
        
        self.init_ui()
        
        # Apply CSS styles without background colors to respect theme
        self.setStyleSheet("""
            /* 全局基础圆角 */
            QWidget {
                font-family: Microsoft YaHei, Segoe UI, sans-serif;
            }
            
            /* 主窗口/卡片圆角 */
            QMainWindow, QWidget#centralWidget, QFrame#card {
                border-radius: 12px;
            }
            
            /* 按钮标准圆角 */
            QPushButton {
                border-radius: 8px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                border-radius: 8px;
            }
            QPushButton:pressed {
                border-radius: 8px;
            }
            
            /* 输入框、文本框 */
            QLineEdit, QTextEdit, QPlainTextEdit {
                border-radius: 8px;
                padding: 4px 8px;
            }
            
            /* 组合框、下拉框 */
            QComboBox {
                border-radius: 8px;
                padding: 4px 8px;
            }
            QComboBox QAbstractItemView {
                border-radius: 8px;
            }
            
            /* 复选框、单选框 */
            QCheckBox, QRadioButton {
                spacing: 8px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                border-radius: 4px;
            }
            
            /* 进度条 */
            QProgressBar {
                border-radius: 8px;
            }
            QProgressBar::chunk {
                border-radius: 8px;
            }
            
            /* 滑块 */
            QSlider::handle {
                border-radius: 8px;
            }
            
            /* 菜单、右键菜单（托盘菜单也会更圆润） */
            QMenu {
                border-radius: 8px;
                padding: 6px 0;
            }
            QMenu::item {
                border-radius: 6px;
                padding: 6px 16px;
            }
            QMenu::item:selected {
                border-radius: 6px;
            }
            
            /* 分组框 */
            QGroupBox {
                border-radius: 10px;
                margin-top: 16px;
            }
            
            /* 滚动条 */
            QScrollBar:vertical {
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                border-radius: 4px;
            }
            
            /* 列表框 */
            QListWidget {
                border-radius: 8px;
            }
        """)
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Custom runners section
        runners_layout = QVBoxLayout()
        runners_label = QLabel(self.translator.translate("Custom Runners", self.language))
        # Set font size for label
        font = runners_label.font()
        font.setPointSize(12)
        runners_label.setFont(font)
        runners_layout.addWidget(runners_label)
        
        self.runners_list = QListWidget()
        self.runners_list.setSelectionMode(QListWidget.SingleSelection)
        # Set font size for list items
        font = self.runners_list.font()
        font.setPointSize(11)
        self.runners_list.setFont(font)
        runners_layout.addWidget(self.runners_list)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.import_button = QPushButton(self.translator.translate("Import GIF", self.language))
        # Set font size for button
        font = self.import_button.font()
        font.setPointSize(11)
        self.import_button.setFont(font)
        self.import_button.clicked.connect(self.import_gif)
        buttons_layout.addWidget(self.import_button)
        
        self.remove_button = QPushButton(self.translator.translate("Remove", self.language))
        # Set font size for button
        font = self.remove_button.font()
        font.setPointSize(11)
        self.remove_button.setFont(font)
        self.remove_button.clicked.connect(self.remove_runner)
        buttons_layout.addWidget(self.remove_button)
        
        runners_layout.addLayout(buttons_layout)
        main_layout.addLayout(runners_layout)
        
        # Close button
        close_button = QPushButton(self.translator.translate("Close", self.language))
        # Set font size for button
        font = close_button.font()
        font.setPointSize(11)
        close_button.setFont(font)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)
        
        self.setLayout(main_layout)
        self.update_runners_list()
    
    def update_runners_list(self):
        """Update runners list"""
        self.runners_list.clear()
        
        # Add built-in runners
        from app.animation.runner import RunnerManager
        from PyQt5.QtWidgets import QListWidgetItem
        runner_manager = RunnerManager()
        builtin_runners = runner_manager.get_runner_names()
        for runner in builtin_runners:
            item_text = self.translator.translate("[Built-in] {}", self.language).format(runner)
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, "builtin")
            self.runners_list.addItem(item)
        
        # Add custom runners
        custom_runners = self.custom_runner_manager.get_custom_runner_names()
        for runner in custom_runners:
            item = QListWidgetItem(runner)
            item.setData(Qt.UserRole, "custom")
            self.runners_list.addItem(item)
    
    def import_gif(self):
        """Import GIF file"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter(self.translator.translate("GIF files (*.gif)", self.language))
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        if file_dialog.exec_() == QFileDialog.Accepted:
            gif_path = file_dialog.selectedFiles()[0]
            runner_name = os.path.splitext(os.path.basename(gif_path))[0]
            
            if self.custom_runner_manager.import_gif(gif_path, runner_name):
                QMessageBox.information(self, 
                    self.translator.translate("Success", self.language), 
                    self.translator.translate("Successfully imported runner: {}", self.language).format(runner_name)
                )
                self.update_runners_list()
            else:
                QMessageBox.warning(self, 
                    self.translator.translate("Error", self.language), 
                    self.translator.translate("Failed to import runner. Please check the GIF file.", self.language)
                )
    
    def remove_runner(self):
        """Remove selected runner"""
        selected_items = self.runners_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            runner_type = item.data(Qt.UserRole)
            runner_name = item.text()
            
            if runner_type == "builtin":
                QMessageBox.warning(self, 
                    self.translator.translate("Error", self.language), 
                    self.translator.translate("Built-in runners cannot be removed.", self.language)
                )
                return
            
            # For custom runners, remove the [Built-in] prefix if present
            if runner_name.startswith("[内置] "):
                runner_name = runner_name[len("[内置] "):]
            elif runner_name.startswith("[Built-in] "):
                runner_name = runner_name[len("[Built-in] "):]
            
            if QMessageBox.question(self, 
                self.translator.translate("Confirm", self.language), 
                self.translator.translate("Are you sure you want to remove runner '{}'?", self.language).format(runner_name)
            ) == QMessageBox.Yes:
                if self.custom_runner_manager.remove_custom_runner(runner_name):
                    QMessageBox.information(self, 
                        self.translator.translate("Success", self.language), 
                        self.translator.translate("Successfully removed runner: {}", self.language).format(runner_name)
                    )
                    self.update_runners_list()
                else:
                    QMessageBox.warning(self, 
                        self.translator.translate("Error", self.language), 
                        self.translator.translate("Failed to remove runner.", self.language)
                    )

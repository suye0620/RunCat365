#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Settings form module
"""

import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QComboBox, QGroupBox, QSplitter, QWidget
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
                "[内置] {}": "[Built-in] {}",
                "Groups": "Groups",
                "Create Group": "Create Group",
                "Delete Group": "Delete Group",
                "Add to Group": "Add to Group",
                "Remove from Group": "Remove from Group",
                "Action Type": "Action Type",
                "Work": "Work",
                "Rest": "Rest",
                "Group:": "Group:",
                "Action:": "Action:",
                "Enter group name:": "Enter group name:",
                "Are you sure you want to delete group '{}'?": "Are you sure you want to delete group '{}'?",
                "Please select a runner first": "Please select a runner first",
                "Please select a group first": "Please select a group first",
                "Cannot remove built-in runner from group": "Cannot remove built-in runner from group"
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
                "[内置] {}": "[内置] {}",
                "Groups": "分组",
                "Create Group": "创建分组",
                "Delete Group": "删除分组",
                "Add to Group": "添加到分组",
                "Remove from Group": "从分组移除",
                "Action Type": "动作类型",
                "Work": "工作",
                "Rest": "休息",
                "Group:": "分组：",
                "Action:": "动作：",
                "Enter group name:": "输入分组名称：",
                "Are you sure you want to delete group '{}'?": "确定要删除分组 '{}' 吗？",
                "Please select a runner first": "请先选择一个角色",
                "Please select a group first": "请先选择一个分组",
                "Cannot remove built-in runner from group": "无法从分组中移除内置角色"
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
                "中文": "簡體中文",
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
                "GIF files (*.gif)": "GIF檔 (*.gif)",
                "[Built-in] {}": "[內建] {}",
                "[内置] {}": "[內建] {}",
                "Groups": "分組",
                "Create Group": "創建分組",
                "Delete Group": "刪除分組",
                "Add to Group": "添加到分組",
                "Remove from Group": "從分組移除",
                "Action Type": "動作類型",
                "Work": "工作",
                "Rest": "休息",
                "Group:": "分組：",
                "Action:": "動作：",
                "Enter group name:": "輸入分組名稱：",
                "Are you sure you want to delete group '{}'?": "確定要刪除分組 '{}' 嗎？",
                "Please select a runner first": "請先選擇一個角色",
                "Please select a group first": "請先選擇一個分組",
                "Cannot remove built-in runner from group": "無法從分組中移除內建角色"
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
        self.setGeometry(100, 100, 600, 500)
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
        
        # Initialize work mode manager and runner metadata manager
        from app.work_mode.work_mode_manager import WorkModeManager
        from app.work_mode.runner_metadata import RunnerMetadataManager
        self.work_mode_manager = WorkModeManager()
        self.metadata_manager = RunnerMetadataManager()
        
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
                background-color: rgba(66, 133, 244, 0.1);
            }
            QPushButton:pressed {
                border-radius: 8px;
                background-color: rgba(66, 133, 244, 0.2);
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
                background-color: rgba(66, 133, 244, 0.2);
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
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)
        
        # Left section: Runners list
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        runners_label = QLabel(self.translator.translate("Custom Runners", self.language))
        font = runners_label.font()
        font.setPointSize(12)
        runners_label.setFont(font)
        left_layout.addWidget(runners_label)
        
        self.runners_list = QListWidget()
        self.runners_list.setSelectionMode(QListWidget.SingleSelection)
        font = self.runners_list.font()
        font.setPointSize(11)
        self.runners_list.setFont(font)
        self.runners_list.selectionModel().selectionChanged.connect(self._on_runner_selection_changed)
        left_layout.addWidget(self.runners_list)
        
        # Buttons for import/remove
        buttons_layout = QHBoxLayout()
        self.import_button = QPushButton(self.translator.translate("Import GIF", self.language))
        font = self.import_button.font()
        font.setPointSize(11)
        self.import_button.setFont(font)
        self.import_button.clicked.connect(self.import_gif)
        buttons_layout.addWidget(self.import_button)
        
        self.remove_button = QPushButton(self.translator.translate("Remove", self.language))
        font = self.remove_button.font()
        font.setPointSize(11)
        self.remove_button.setFont(font)
        self.remove_button.clicked.connect(self.remove_runner)
        buttons_layout.addWidget(self.remove_button)
        
        left_layout.addLayout(buttons_layout)
        left_widget.setLayout(left_layout)
        
        splitter.addWidget(left_widget)
        
        # Right section: Group management
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        groups_label = QLabel(self.translator.translate("Groups", self.language))
        font = groups_label.font()
        font.setPointSize(12)
        groups_label.setFont(font)
        right_layout.addWidget(groups_label)
        
        self.groups_list = QListWidget()
        self.groups_list.setSelectionMode(QListWidget.SingleSelection)
        font = self.groups_list.font()
        font.setPointSize(11)
        self.groups_list.setFont(font)
        self.groups_list.selectionModel().selectionChanged.connect(self._on_group_selection_changed)
        right_layout.addWidget(self.groups_list)
        
        # Group info and action type
        group_info_layout = QHBoxLayout()
        
        # Action type selection
        action_layout = QVBoxLayout()
        action_label = QLabel(self.translator.translate("Action Type", self.language))
        action_layout.addWidget(action_label)
        
        self.action_combo = QComboBox()
        self.action_combo.addItem(self.translator.translate("Work", self.language), "work")
        self.action_combo.addItem(self.translator.translate("Rest", self.language), "rest")
        action_layout.addWidget(self.action_combo)
        
        group_info_layout.addLayout(action_layout)
        right_layout.addLayout(group_info_layout)
        
        # Group buttons
        group_buttons_layout = QHBoxLayout()
        self.create_group_button = QPushButton(self.translator.translate("Create Group", self.language))
        font = self.create_group_button.font()
        font.setPointSize(11)
        self.create_group_button.setFont(font)
        self.create_group_button.clicked.connect(self._create_group)
        group_buttons_layout.addWidget(self.create_group_button)
        
        self.delete_group_button = QPushButton(self.translator.translate("Delete Group", self.language))
        font = self.delete_group_button.font()
        font.setPointSize(11)
        self.delete_group_button.setFont(font)
        self.delete_group_button.clicked.connect(self._delete_group)
        group_buttons_layout.addWidget(self.delete_group_button)
        
        right_layout.addLayout(group_buttons_layout)
        
        # Runner to group buttons
        runner_group_buttons_layout = QHBoxLayout()
        self.add_to_group_button = QPushButton(self.translator.translate("Add to Group", self.language))
        font = self.add_to_group_button.font()
        font.setPointSize(11)
        self.add_to_group_button.setFont(font)
        self.add_to_group_button.clicked.connect(self._add_selected_runner_to_group)
        runner_group_buttons_layout.addWidget(self.add_to_group_button)
        
        self.remove_from_group_button = QPushButton(self.translator.translate("Remove from Group", self.language))
        font = self.remove_from_group_button.font()
        font.setPointSize(11)
        self.remove_from_group_button.setFont(font)
        self.remove_from_group_button.clicked.connect(self._remove_selected_runner_from_group)
        runner_group_buttons_layout.addWidget(self.remove_from_group_button)
        
        right_layout.addLayout(runner_group_buttons_layout)
        
        # Add close button to right layout
        right_layout.addStretch()
        close_button = QPushButton(self.translator.translate("Close", self.language))
        font = close_button.font()
        font.setPointSize(11)
        close_button.setFont(font)
        close_button.clicked.connect(self.close)
        right_layout.addWidget(close_button)
        
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)
        
        # Set splitter sizes (left wider than right)
        splitter.setSizes([350, 250])
        
        main_layout.addWidget(splitter)
        
        self.setLayout(main_layout)
        self.update_runners_list()
        self.update_groups_list()
    
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
            item.setData(Qt.UserRole, ("builtin", runner))
            # Check if this runner is in any group and show info
            metadata = self.metadata_manager.get_runner_metadata(runner)
            if metadata.get("group_id"):
                group_info = f" (Group: {metadata['group_id']}, Action: {metadata.get('action_type', 'N/A')})"
                item_text += group_info
                item.setText(item_text)
            self.runners_list.addItem(item)
        
        # Add custom runners
        custom_runners = self.custom_runner_manager.get_custom_runner_names()
        for runner in custom_runners:
            item = QListWidgetItem(runner)
            item.setData(Qt.UserRole, ("custom", runner))
            # Check if this runner is in any group and show info
            metadata = self.metadata_manager.get_runner_metadata(runner)
            if metadata.get("group_id"):
                group_info = f" (Group: {metadata['group_id']}, Action: {metadata.get('action_type', 'N/A')})"
                item.setText(runner + group_info)
            self.runners_list.addItem(item)
    
    def update_groups_list(self):
        """Update groups list"""
        self.groups_list.clear()
        from PyQt5.QtWidgets import QListWidgetItem
        
        # Get all created groups
        all_groups = self.metadata_manager.get_all_groups()
        all_metadata = self.metadata_manager.get_all_runners_metadata()
        
        for group_id in all_groups:
            # Count runners in this group
            runner_count = sum(1 for m in all_metadata.values() if m.get("group_id") == group_id)
            item_text = f"{group_id} ({runner_count} runners)"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, group_id)
            self.groups_list.addItem(item)
    
    def _on_runner_selection_changed(self):
        """Called when runner selection changes"""
        selected_items = self.runners_list.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        runner_type, runner_name = item.data(Qt.UserRole)
        
        # Check if this runner is already in a group
        metadata = self.metadata_manager.get_runner_metadata(runner_name)
        if metadata.get("group_id"):
            # Select the group
            group_id = metadata["group_id"]
            groups = self.metadata_manager.get_all_runners_metadata()
            group_ids = set(m.get("group_id") for m in groups.values() if m.get("group_id"))
            group_list = list(group_ids)
            if group_id in group_list:
                index = group_list.index(group_id)
                self.groups_list.setCurrentRow(index)
            # Set current action type
            action_type = metadata.get("action_type", "work")
            index = self.action_combo.findData(action_type)
            if index >= 0:
                self.action_combo.setCurrentIndex(index)
    
    def _on_group_selection_changed(self):
        """Called when group selection changes"""
        pass
    
    def _get_all_groups(self):
        """Get all created groups"""
        return self.metadata_manager.get_all_groups()

    def _create_group(self):
        """Create a new group"""
        from PyQt5.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, 
            self.translator.translate("Create Group", self.language),
            self.translator.translate("Enter group name:", self.language)
        )
        if ok and text.strip():
            group_id = text.strip()
            # Check if group already exists
            all_groups = self._get_all_groups()
            if group_id in all_groups:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, 
                    self.translator.translate("Information", self.language),
                    self.translator.translate("Group '{}' already exists!", self.language).format(group_id)
                )
                return
            # Create empty group
            self.metadata_manager.create_group(group_id)
            # Refresh list
            self.update_groups_list()
    
    def _delete_group(self):
        """Delete selected group"""
        selected_items = self.groups_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, 
                self.translator.translate("Information", self.language),
                self.translator.translate("Please select a group first", self.language)
            )
            return
        
        item = selected_items[0]
        group_id = item.data(Qt.UserRole)
        
        result = QMessageBox.question(self,
            self.translator.translate("Confirm", self.language),
            self.translator.translate("Are you sure you want to delete group '{}'?", self.language).format(group_id)
        )
        if result == QMessageBox.Yes:
            # Remove all runners from this group
            all_metadata = self.metadata_manager.get_all_runners_metadata()
            for runner_name, metadata in all_metadata.items():
                if metadata.get("group_id") == group_id:
                    self.metadata_manager.clear_runner_group(runner_name)
            # Delete the group itself
            self.metadata_manager.delete_group(group_id)
            self.update_groups_list()
            self.update_runners_list()
    
    def _add_selected_runner_to_group(self):
        """Add selected runner to selected group"""
        runner_selected = self.runners_list.selectedItems()
        group_selected = self.groups_list.selectedItems()
        
        if not runner_selected:
            QMessageBox.information(self, 
                self.translator.translate("Information", self.language),
                self.translator.translate("Please select a runner first", self.language)
            )
            return
        
        if not group_selected:
            QMessageBox.information(self, 
                self.translator.translate("Information", self.language),
                self.translator.translate("Please select a group first", self.language)
            )
            return
        
        runner_item = runner_selected[0]
        runner_type, runner_name = runner_item.data(Qt.UserRole)
        group_item = group_selected[0]
        group_id = group_item.data(Qt.UserRole)
        action_type = self.action_combo.currentData()
        
        # Set runner metadata
        metadata = self.metadata_manager.get_runner_metadata(runner_name)
        metadata["group_id"] = group_id
        metadata["action_type"] = action_type
        metadata["is_custom"] = (runner_type == "custom")
        metadata["enabled_modes"] = ["Normal", "Work"]
        self.metadata_manager.set_runner_metadata(runner_name, metadata)
        
        self.update_runners_list()
        self.update_groups_list()
    
    def _remove_selected_runner_from_group(self):
        """Remove selected runner from its current group"""
        runner_selected = self.runners_list.selectedItems()
        
        if not runner_selected:
            QMessageBox.information(self, 
                self.translator.translate("Information", self.language),
                self.translator.translate("Please select a runner first", self.language)
            )
            return
        
        runner_item = runner_selected[0]
        runner_type, runner_name = runner_item.data(Qt.UserRole)
        
        metadata = self.metadata_manager.get_runner_metadata(runner_name)
        if not metadata.get("group_id"):
            QMessageBox.information(self, 
                self.translator.translate("Information", self.language),
                self.translator.translate("Runner is not in any group", self.language)
            )
            return
        
        self.metadata_manager.clear_runner_group(runner_name)
        self.update_runners_list()
        self.update_groups_list()
    
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
            runner_type, runner_name = item.data(Qt.UserRole)
            
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

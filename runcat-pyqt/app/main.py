#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunCat365 PyQt implementation
Main entry point
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QStyleFactory, QStyledItemDelegate
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, QRect, QSize, QCoreApplication, QTranslator

from app.monitor.cpu import CPUMonitor
from app.monitor.memory import MemoryMonitor
from app.monitor.network import NetworkMonitor
from app.animation.runner import RunnerManager
from app.animation.custom_runner import CustomRunnerManager
from app.animation.theme import ThemeManager
from app.settings.settings_manager import SettingsManager
from app.settings.settings_form import SettingsForm

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
                "中文": "Chinese",
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
                "Failed to remove runner.": "Failed to remove runner."
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
                "Failed to remove runner.": "删除角色失败。"
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
                "English": "英文",
                "中文": "簡體中文",
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
                "Failed to remove runner.": "刪除角色失敗。"
            }
        }
    
    def translate(self, text, language):
        """Translate text to specified language"""
        if language in self.translations:
            if text in self.translations[language]:
                return self.translations[language][text]
        return text





class RunCatApp:
    """Main RunCat application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Apply Fusion style
        self.app.setStyle(QStyleFactory.create("Fusion"))
        
        # Apply custom CSS for rounded UI and hover effects
        css = """
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
        /* 确保子菜单也有圆角 */
        QMenu QMenu {
            border-radius: 8px;
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
        """
        self.app.setStyleSheet(css)
        
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.runner_manager = RunnerManager()
        # Write debug info to file
        with open("debug.log", "a") as f:
            f.write(f"Runner manager initialized with runners: {self.runner_manager.get_runner_names()}\n")
        self.custom_runner_manager = CustomRunnerManager()
        self.theme_manager = ThemeManager()
        
        # Initialize translator
        self.translator = Translator()
        
        # Load settings
        self._load_settings()
        
        # Initialize monitors
        self.cpu_monitor = CPUMonitor()
        self.memory_monitor = MemoryMonitor()
        self.network_monitor = NetworkMonitor()
        
        # Create system tray icon
        self.tray = QSystemTrayIcon()
        
        # Set icon
        self.tray.setIcon(self._get_icon())
        self.tray.setToolTip("RunCat365")
        
        # Create context menu with parent
        self.menu = QMenu(None)
        self._setup_menu()
        
        # Set context menu for tray icon
        self.tray.setContextMenu(self.menu)
        
        # Apply Fusion style to menu to ensure theme consistency
        self.menu.setStyle(QStyleFactory.create("Fusion"))
        
        # Ensure menu uses the application's palette
        self.menu.setPalette(self.app.palette())
        
        # Check if system tray is available
        if not QSystemTrayIcon.isSystemTrayAvailable():
            # System tray not available, create a simple window
            from PyQt5.QtWidgets import QMainWindow, QLabel
            self.window = QMainWindow()
            self.window.setWindowTitle("RunCat365")
            self.window.setGeometry(100, 100, 200, 100)
            self.window.setCentralWidget(QLabel("System tray not available. Please check your system settings."))
            self.window.show()
        
        # Add tray icon clicked event
        self.tray.activated.connect(self._tray_activated)
        
        # Animation variables
        self.current_frame = 0
        self.frames = []
        
        # Show tray icon
        self.tray.show()
        
        # Load frames after tray icon is shown
        self._load_frames()
        
        # Setup timers
        self.animate_timer = QTimer()
        self.animate_timer.timeout.connect(self._advance_frame)
        self.animate_timer.start(200)
        
        self.fetch_timer = QTimer()
        self.fetch_timer.timeout.connect(self._fetch_system_info)
        self.fetch_timer.start(5000)  # 5000毫秒 = 5秒
    
    def _load_settings(self):
        """Load settings"""
        # Load runner
        runner = self.settings_manager.get_runner()
        self.runner_manager.set_current_runner(runner)
        
        # Load theme
        theme = self.settings_manager.get_theme()
        self.theme_manager.set_theme(theme)
        # Apply theme
        self.theme_manager.apply_theme(self.app)
        
        # Load speed source
        self.speed_source = self.settings_manager.get_speed_source()
        
        # Load FPS limit
        self.fps_max_limit = self.settings_manager.get_fps_max_limit()
        
        # Load launch at startup
        self.launch_at_startup = self.settings_manager.get_launch_at_startup()
        
        # Load language
        self.language = self.settings_manager.get_language()
    
    def _setup_menu(self):
        """Setup context menu"""
        # Clear existing menu
        self.menu.clear()
        
        # Runner selection
        self.runner_menu = QMenu(self.translator.translate("Runner", self.language))
        self._setup_runner_menu()
        self.menu.addMenu(self.runner_menu)
        
        # Theme selection
        self.theme_menu = QMenu(self.translator.translate("Theme", self.language))
        self._setup_theme_menu()
        self.menu.addMenu(self.theme_menu)
        
        # Speed source
        self.speed_menu = QMenu(self.translator.translate("Speed Based On", self.language))
        self._setup_speed_menu()
        self.menu.addMenu(self.speed_menu)
        
        # FPS limit
        self.fps_menu = QMenu(self.translator.translate("FPS Max Limit", self.language))
        self._setup_fps_menu()
        self.menu.addMenu(self.fps_menu)
        
        # Add separator
        self.menu.addSeparator()
        
        # Launch at startup
        self.startup_action = QAction(self.translator.translate("Launch at startup", self.language))
        self.startup_action.setCheckable(True)
        self.startup_action.setChecked(self.launch_at_startup)
        self.startup_action.triggered.connect(self._toggle_startup)
        self.menu.addAction(self.startup_action)
        
        # Manage runners
        self.manage_runners_action = QAction(self.translator.translate("Manage Runners", self.language))
        self.manage_runners_action.triggered.connect(self._open_settings)
        self.menu.addAction(self.manage_runners_action)
        
        # Add separator
        self.menu.addSeparator()
        
        # Language
        self.language_menu = QMenu(self.translator.translate("Language", self.language))
        self._setup_language_menu()
        self.menu.addMenu(self.language_menu)
        
        # Information
        self.info_menu = QMenu(self.translator.translate("Information", self.language))
        self._setup_info_menu()
        self.menu.addMenu(self.info_menu)
        
        # Add separator
        self.menu.addSeparator()
        
        # Exit
        self.exit_action = QAction(self.translator.translate("Exit", self.language))
        self.exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(self.exit_action)
    
    def _setup_runner_menu(self):
        """Setup runner menu"""
        # Clear existing items
        self.runner_menu.clear()
        
        # Add built-in runners
        runners = self.runner_manager.get_runner_names()
        
        # Debug: Check runners list
        with open("debug.log", "a") as f:
            f.write(f"Available runners: {runners}\n")
        
        # Add built-in runners one by one
        for i, runner_name in enumerate(runners):
            # Get runner icon (first frame)
            runner = self.runner_manager.get_runner(runner_name)
            runner.load_frames(self.theme_manager.get_theme())
            frames = runner.get_frames()
            icon = frames[0] if frames else self._get_icon()
            
            action = QAction(icon, runner_name, self.runner_menu)
            action.setCheckable(True)
            action.setChecked(runner_name == self.runner_manager.current_runner)
            # Use partial to avoid lambda closure issue
            from functools import partial
            action.triggered.connect(partial(self._select_runner, runner_name))
            self.runner_menu.addAction(action)
            
            # Debug: Check action added
            with open("debug.log", "a") as f:
                f.write(f"Added runner {i}: {runner_name}\n")
        
        # Add custom runners
        self.custom_runner_manager.load_custom_runners()
        custom_runners = self.custom_runner_manager.get_custom_runner_names()
        
        # Debug: Check custom runners list
        with open("debug.log", "a") as f:
            f.write(f"Available custom runners: {custom_runners}\n")
        
        if custom_runners:
            self.runner_menu.addSeparator()
            
            # Add custom runners one by one
            for i, runner_name in enumerate(custom_runners):
                # Get custom runner icon (first frame)
                custom_runner = self.custom_runner_manager.get_custom_runner(runner_name)
                if custom_runner:
                    custom_runner.load_frames(self.theme_manager.get_theme())
                    frames = custom_runner.get_frames()
                    icon = frames[0] if frames else self._get_icon()
                else:
                    icon = self._get_icon()
                
                action = QAction(icon, runner_name, self.runner_menu)
                action.setCheckable(True)
                action.setChecked(runner_name == self.runner_manager.current_runner)
                from functools import partial
                action.triggered.connect(partial(self._select_runner, runner_name))
                self.runner_menu.addAction(action)
                
                # Debug: Check custom action added
                with open("debug.log", "a") as f:
                    f.write(f"Added custom runner {i}: {runner_name}\n")
        
        # Debug: Check how many actions are in the runner menu
        with open("debug.log", "a") as f:
            f.write(f"Runner menu actions: {len(self.runner_menu.actions())}\n")
    
    def _setup_theme_menu(self):
        """Setup theme menu"""
        # Clear existing items
        self.theme_menu.clear()
        
        # Add theme options
        theme_names = self.theme_manager.get_theme_names()
        
        # Add theme actions one by one
        for theme_name in theme_names:
            translated_theme_name = self.translator.translate(theme_name, self.language)
            action = QAction(translated_theme_name, self.theme_menu)
            action.setCheckable(True)
            action.setChecked(theme_name == self.theme_manager.get_theme().theme_name)
            # Use partial to avoid lambda closure issue
            from functools import partial
            action.triggered.connect(partial(self._select_theme, theme_name))
            self.theme_menu.addAction(action)
    
    def _setup_speed_menu(self):
        """Setup speed menu"""
        # Clear existing items
        self.speed_menu.clear()
        
        # Add speed source options
        speed_sources = ["CPU", "Memory", "Network"]
        
        # Add speed source actions one by one
        for source in speed_sources:
            translated_source = self.translator.translate(source, self.language)
            action = QAction(translated_source, self.speed_menu)
            action.setCheckable(True)
            action.setChecked(source == self.speed_source)
            # Use partial to avoid lambda closure issue
            from functools import partial
            action.triggered.connect(partial(self._select_speed_source, source))
            self.speed_menu.addAction(action)
    
    def _setup_fps_menu(self):
        """Setup FPS menu"""
        # Clear existing items
        self.fps_menu.clear()
        
        # Add FPS options
        fps_options = ["FPS30", "FPS40", "FPS50", "FPS60"]
        
        # Add FPS actions one by one
        for fps in fps_options:
            translated_fps = self.translator.translate(fps, self.language)
            action = QAction(translated_fps, self.fps_menu)
            action.setCheckable(True)
            action.setChecked(fps == self.fps_max_limit)
            # Use partial to avoid lambda closure issue
            from functools import partial
            action.triggered.connect(partial(self._select_fps_limit, fps))
            self.fps_menu.addAction(action)
    
    def _setup_info_menu(self):
        """Setup info menu"""
        # Clear existing items
        self.info_menu.clear()
        
        # Add version info
        version_action = QAction(self.translator.translate("Version 1.0.0", self.language), self.info_menu)
        version_action.setEnabled(False)
        self.info_menu.addAction(version_action)
        
        # Add repository link
        repo_action = QAction(self.translator.translate("Open Repository", self.language), self.info_menu)
        repo_action.triggered.connect(self._open_repository)
        self.info_menu.addAction(repo_action)
    
    def _setup_language_menu(self):
        """Setup language menu"""
        # Clear existing items
        self.language_menu.clear()
        
        # Add language options
        languages = ["English", "中文", "中文繁体"]
        
        # Add language actions one by one
        for language in languages:
            translated_language = self.translator.translate(language, self.language)
            action = QAction(translated_language, self.language_menu)
            action.setCheckable(True)
            action.setChecked(language == self.language)  # Use current language setting
            from functools import partial
            action.triggered.connect(partial(self._select_language, language))
            self.language_menu.addAction(action)
    
    def _select_language(self, language):
        """Select language"""
        # Update language setting
        self.settings_manager.set_language(language)
        # Update self.language variable
        self.language = language
        # Update entire menu to reflect the language change
        self._setup_menu()
        # Here you would typically update all UI elements with the new language
        # For now, we'll just log the change
        with open("debug.log", "a") as f:
            f.write(f"Language changed to: {language}\n")
    
    def _select_runner(self, runner_name):
        """Select runner"""
        self.runner_manager.set_current_runner(runner_name)
        self.settings_manager.set_runner(runner_name)
        # Reset current frame to 0 when switching runners
        self.current_frame = 0
        self._load_frames()
        # Update only the runner menu to update the checked state
        self._setup_runner_menu()
    
    def _select_theme(self, theme_name):
        """Select theme"""
        self.theme_manager.set_theme(theme_name)
        self.theme_manager.apply_theme(self.app)
        self.settings_manager.set_theme(theme_name)
        self._load_frames()
        # Recreate the menu to ensure theme is applied correctly
        self._setup_menu()
        # Reapply style and palette to menu
        self.menu.setStyle(QStyleFactory.create("Fusion"))
        self.menu.setPalette(self.app.palette())
    

    
    def _select_speed_source(self, source):
        """Select speed source"""
        self.speed_source = source
        self.settings_manager.set_speed_source(source)
        # Update only the speed menu to update the checked state
        self._setup_speed_menu()
    
    def _select_fps_limit(self, fps):
        """Select FPS limit"""
        self.fps_max_limit = fps
        self.settings_manager.set_fps_max_limit(fps)
        # Update only the FPS menu to update the checked state
        self._setup_fps_menu()
    
    def _toggle_startup(self, checked):
        """Toggle launch at startup"""
        self.launch_at_startup = checked
        self.settings_manager.set_launch_at_startup(checked)
    
    def _open_settings(self):
        """Open settings form"""
        settings_form = SettingsForm(language=self.language, theme=self.theme_manager.get_theme())
        settings_form.exec_()
        # Reload custom runners
        self._setup_menu()
    
    def _open_repository(self):
        """Open repository"""
        import webbrowser
        webbrowser.open("https://github.com/Kyome22/RunCat365.git")
    
    def _tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.Trigger:
            # Tray icon clicked, do nothing
            pass
    
    def _get_icon(self):
        """Get default icon"""
        # Create a simple icon if no resource available
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.white)
        return QIcon(pixmap)
    
    def _load_frames(self):
        """Load animation frames"""
        # First check if it's a custom runner
        self.custom_runner_manager.load_custom_runners()
        custom_runner = self.custom_runner_manager.get_custom_runner(self.runner_manager.current_runner)
        
        # Debug: Check current runner and custom runner
        with open("debug.log", "a") as f:
            f.write(f"Current runner: {self.runner_manager.current_runner}\n")
            f.write(f"Custom runner found: {custom_runner is not None}\n")
        
        if custom_runner:
            custom_runner.load_frames(self.theme_manager.get_theme())
            self.frames = custom_runner.get_frames()
            # Debug: Check custom runner frames
            with open("debug.log", "a") as f:
                f.write(f"Custom runner frames count: {len(self.frames)}\n")
        else:
            # If not a custom runner, load built-in runner
            current_runner = self.runner_manager.get_current_runner()
            if current_runner:
                current_runner.load_frames(self.theme_manager.get_theme())
                self.frames = current_runner.get_frames()
                # Debug: Check built-in runner frames
                with open("debug.log", "a") as f:
                    f.write(f"Built-in runner frames count: {len(self.frames)}\n")
        
        # If no frames loaded, create a default frame
        if not self.frames:
            pixmap = QPixmap(32, 32)
            self.frames = [QIcon(pixmap)]
        
        # Update tray icon immediately with the first frame
        if self.frames:
            self.tray.setIcon(self.frames[0])
    
    def _advance_frame(self):
        """Advance animation frame"""
        if self.frames:
            # Check if we're at the last frame
            is_last_frame = (self.current_frame == len(self.frames) - 1)
            
            # Advance to next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            # Use setIcon directly without any delay
            self.tray.setIcon(self.frames[self.current_frame])
            
            # If we were at the last frame, prepare for the next cycle
            if is_last_frame:
                # Stop the animation timer temporarily
                self.animate_timer.stop()
                
                # Calculate new interval based on current system load
                load = 0
                if self.speed_source == "CPU":
                    load = self.cpu_monitor.get_usage()
                elif self.speed_source == "Memory":
                    load = self.memory_monitor.get_usage()
                elif self.speed_source == "Network":
                    load = max(self.network_monitor.get_speed_sent(), self.network_monitor.get_speed_recv()) / 1024 / 1024  # MB/s
                
                # Calculate interval based on load and FPS limit
                fps = int(self.fps_max_limit.replace("FPS", ""))
                speed = max(1.0, (load / 5.0) * (fps / 40.0))
                interval = int(500.0 / speed)
                
                # Update animation timer interval
                self.animate_timer.setInterval(interval)
                
                # Restart the animation timer
                self.animate_timer.start()
    
    def _fetch_system_info(self):
        """Fetch system information"""
        # Update monitors
        self.cpu_monitor.update()
        self.memory_monitor.update()
        self.network_monitor.update()
        
        # Update system tray tooltip
        tooltip = ""
        if self.speed_source == "CPU":
            tooltip = self.cpu_monitor.get_description()
        elif self.speed_source == "Memory":
            tooltip = self.memory_monitor.get_description()
        elif self.speed_source == "Network":
            tooltip = self.network_monitor.get_description()
        
        self.tray.setToolTip(f"RunCat365 - {tooltip}")
        
        # System load is now calculated in _advance_frame method
        # to ensure smooth transition between frames
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = RunCatApp()
    app.run()

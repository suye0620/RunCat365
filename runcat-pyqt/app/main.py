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
from PyQt5.QtCore import Qt, QTimer, QRect, QSize, QCoreApplication, QTranslator, QObject

from app.monitor.cpu import CPUMonitor
from app.monitor.memory import MemoryMonitor
from app.monitor.network import NetworkMonitor
from app.animation.runner import RunnerManager
from app.animation.custom_runner import CustomRunnerManager
from app.animation.theme import ThemeManager
from app.settings.settings_manager import SettingsManager
from app.settings.settings_form import SettingsForm
from app.floating.floating_ball import FloatingBall
from app.widgets.system_info_tooltip import SystemInfoTooltip
from app.work_mode.work_mode_manager import WorkModeManager

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
                "Failed to remove runner.": "Failed to remove runner.",
                "Adjust Opacity": "Adjust Opacity",
                "Opacity": "Opacity",
                "OK": "OK",
                "Size": "Size",
                "Mode": "Mode",
                "Normal": "Normal",
                "Work": "Work",
                "Pomodoro": "Pomodoro",
                "Resting": "Resting",
                "Working": "Working",
                "Cancel Work": "Cancel Work",
                "Start Pomodoro": "Start Pomodoro",
                "Do you want to start a pomodoro work session?": "Do you want to start a pomodoro work session?",
                "Pomodoro finished! Time to rest.": "Pomodoro finished! Time to rest.",
                "No Work mode configuration": "No Work mode configuration",
                "Please go to Manage Runners to configure groups for Work mode.": "Please go to Manage Runners to configure groups for Work mode.",
                "No runners are configured in groups! Please go to Manage Runners and assign runners to groups first.": "No runners are configured in groups! Please go to Manage Runners and assign runners to groups first.",
                "Paused": "Paused",
                "Start": "Start",
                "Pause": "Pause",
                "Abort": "Abort",
                "Ready": "Ready",
                "Working": "Working",
                "Resting": "Resting"
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
                "Adjust Opacity": "调整透明度",
                "Opacity": "透明度",
                "OK": "确定",
                "Size": "大小",
                "Mode": "模式",
                "Normal": "常规",
                "Work": "工作",
                "Pomodoro": "番茄钟",
                "Resting": "休息中",
                "Working": "工作中",
                "Cancel Work": "取消工作",
                "Start Pomodoro": "开始番茄钟",
                "Do you want to start a pomodoro work session?": "需要进入番茄工作时间吗？",
                "Pomodoro finished! Time to rest.": "番茄钟结束！该休息了。",
                "No Work mode configuration": "无工作模式配置",
                "Please go to Manage Runners to configure groups for Work mode.": "请先前往管理角色，为工作模式配置分组。",
                "No runners are configured in groups! Please go to Manage Runners and assign runners to groups first.": "没有任何角色被配置到分组中！请先前往管理角色，将角色分配到分组。",
                "Paused": "已暂停",
                "Start": "开始",
                "Pause": "暂停",
                "Abort": "中止",
                "Ready": "准备开始",
                "Working": "工作中",
                "Resting": "休息中"
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
                "Failed to remove runner.": "刪除角色失敗。",
                "Adjust Opacity": "調整透明度",
                "Opacity": "透明度",
                "OK": "確定",
                "Size": "大小",
                "Mode": "模式",
                "Normal": "常規",
                "Work": "工作",
                "Pomodoro": "番茄鐘",
                "Resting": "休息中",
                "Working": "工作中",
                "Cancel Work": "取消工作",
                "Start Pomodoro": "開始番茄鐘",
                "Do you want to start a pomodoro work session?": "需要進入番茄工作時間嗎？",
                "Pomodoro finished! Time to rest.": "番茄鐘結束！該休息了。",
                "No Work mode configuration": "無工作模式配置",
                "Please go to Manage Runners to configure groups for Work mode.": "請先前往管理角色，為工作模式配置分組。",
                "No runners are configured in groups! Please go to Manage Runners and assign runners to groups first.": "沒有任何角色被配置到分組中！請先前往管理角色，將角色分配到分組。",
                "Paused": "已暫停",
                "Start": "開始",
                "Pause": "暫停",
                "Abort": "中止",
                "Ready": "準備開始",
                "Working": "工作中",
                "Resting": "休息中"
            }
        }
    
    def translate(self, text, language):
        """Translate text to specified language"""
        if language in self.translations:
            if text in self.translations[language]:
                return self.translations[language][text]
        return text





class RunCatApp(QObject):
    """Main RunCat application class"""
    
    def __init__(self):
        super().__init__()
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
        self.work_mode_manager = WorkModeManager()

        # Initialize translator
        self.translator = Translator()
        
        # Load settings
        self._load_settings()
        
        # Initialize monitors
        self.cpu_monitor = CPUMonitor()
        self.memory_monitor = MemoryMonitor()
        self.network_monitor = NetworkMonitor()
        
        # Create system info tooltip
        self.system_info_tooltip = SystemInfoTooltip()
        self.system_info_tooltip.set_monitors(self.cpu_monitor, self.memory_monitor, self.network_monitor)
        self.system_info_tooltip.set_work_mode_manager(self.work_mode_manager)
        self.system_info_tooltip.set_callbacks(
            self._start_pomodoro_confirm,
            self._toggle_pomodoro_pause,
            self._cancel_pomodoro
        )
        # Set initial theme
        current_theme = self.theme_manager.get_theme()
        is_dark = False
        if current_theme.theme_name == "Dark":
            is_dark = True
        elif current_theme.theme_name == "System":
            is_dark = current_theme.is_system_dark()
        self.system_info_tooltip.set_theme(is_dark)
        
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
        
        # Add event filter for tray icon hover events
        self.tray.installEventFilter(self)
        # Timer for tray hover
        self.tray_hover_timer = QTimer(self)
        self.tray_hover_timer.setSingleShot(True)
        self.tray_hover_timer.timeout.connect(self._show_tray_tooltip)
        # Variable to track if tooltip is shown for tray
        self.tray_tooltip_shown = False
        
        # Animation variables
        self.current_frame = 0
        self.frames = []
        
        # Initialize floating ball
        self.floating_ball = FloatingBall(self.runner_manager, self.theme_manager, self.floating_ball_opacity, int(self.floating_ball_size))
        # Set tooltip for floating ball
        self.floating_ball.set_tooltip(self.system_info_tooltip)
        if self.floating_ball_enabled:
            self.floating_ball.show()
        
        # Show tray icon
        self.tray.show()
        
        # Load frames after tray icon is shown
        self._load_frames()
        
        # Resume work mode state from saved configuration
        if self.work_mode_manager.is_work_mode():
            self.work_mode_manager.resume_from_save()
            # Connect signals (only once)
            try:
                self.work_mode_manager.pomodoro_tick.connect(self._update_pomodoro_menu)
                self.work_mode_manager.pomodoro_finished.connect(self._on_pomodoro_finished)
            except TypeError:
                # Already connected
                pass
            # Switch to correct runner based on current state
            if self.work_mode_manager.is_working():
                self._switch_to_work()
            else:
                self._switch_to_rest()
        
        # Update tooltip mode based on current mode
        self.system_info_tooltip.set_mode(self.current_mode)
        
        # Setup timers
        self.animate_timer = QTimer()
        self.animate_timer.timeout.connect(self._advance_frame)
        self.animate_timer.start(200)
        
        # Timer for updating animation speed (every 5 seconds)
        self.speed_update_timer = QTimer()
        self.speed_update_timer.timeout.connect(self._update_animation_speed)
        self.speed_update_timer.start(5000)  # 5000毫秒 = 5秒
        
        # Timer for updating system info (real-time)
        self.fetch_timer = QTimer()
        self.fetch_timer.timeout.connect(self._fetch_system_info)
        self.fetch_timer.start(500)  # 500毫秒 = 0.5秒 (更实时)
    
    def _load_settings(self):
        """Load settings"""
        # Load runner
        runner = self.settings_manager.get_runner()
        self.normal_saved_runner = runner
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
        
        # Load floating ball settings
        self.floating_ball_enabled = self.settings_manager.get_floating_ball_enabled()
        self.floating_ball_opacity = self.settings_manager.get_floating_ball_opacity()
        self.floating_ball_size = self.settings_manager.get_floating_ball_size()
        
        # Load current mode
        self.current_mode = self.settings_manager.get_current_mode()
    
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
        
        # Mode selection
        self.mode_menu = QMenu(self.translator.translate("Mode", self.language))
        self._setup_mode_menu()
        self.menu.addMenu(self.mode_menu)
        
        # Floating Ball
        self.floating_ball_menu = QMenu(self.translator.translate("Floating Ball", self.language))
        self._setup_floating_ball_menu()
        self.menu.addMenu(self.floating_ball_menu)
        
        # Pomodoro status (only shown in Work mode)
        self.pomodoro_status_action = None
        self.pomodoro_cancel_action = None
        self.pomodoro_start_action = None
        if self.work_mode_manager.is_work_mode():
            self.menu.addSeparator()
            self._setup_pomodoro_status_menu()
        
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
    
    def _setup_floating_ball_menu(self):
        """Setup floating ball menu"""
        # Clear existing items
        self.floating_ball_menu.clear()
        
        # Add show/hide action
        show_hide_action = QAction(self.translator.translate("Show", self.language) if not self.floating_ball_enabled else self.translator.translate("Hide", self.language), self.floating_ball_menu)
        show_hide_action.setCheckable(True)
        show_hide_action.setChecked(self.floating_ball_enabled)
        show_hide_action.triggered.connect(self._toggle_floating_ball)
        self.floating_ball_menu.addAction(show_hide_action)
        
        # Add opacity adjustment action
        from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QWidgetAction
        
        # Opacity slider
        opacity_widget = QWidget()
        opacity_layout = QHBoxLayout()
        opacity_layout.setContentsMargins(10, 5, 10, 5)
        
        opacity_label = QLabel(self.translator.translate("Opacity", self.language))
        opacity_layout.addWidget(opacity_label)
        
        opacity_slider = QSlider(Qt.Horizontal)
        opacity_slider.setRange(10, 100)
        opacity_slider.setValue(int(self.floating_ball_opacity * 100))
        opacity_slider.setFixedWidth(100)
        # 确保滑块有足够的高度和样式，避免被覆盖
        opacity_slider.setMinimumHeight(20)
        opacity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #cccccc;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3366cc;
                border: 1px solid #3366cc;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
        """)
        opacity_slider.valueChanged.connect(self._adjust_floating_ball_opacity)
        opacity_layout.addWidget(opacity_slider)
        
        # Add opacity value label
        opacity_value_label = QLabel(f"{int(self.floating_ball_opacity * 100)}%")
        opacity_value_label.setFixedWidth(40)
        opacity_layout.addWidget(opacity_value_label)
        
        # Update value label when slider changes
        def update_opacity_label(value):
            opacity_value_label.setText(f"{value}%")
        
        opacity_slider.valueChanged.connect(update_opacity_label)
        
        opacity_widget.setLayout(opacity_layout)
        
        opacity_action = QWidgetAction(self.floating_ball_menu)
        opacity_action.setDefaultWidget(opacity_widget)
        self.floating_ball_menu.addAction(opacity_action)
        
        # Add size adjustment action
        size_widget = QWidget()
        size_layout = QHBoxLayout()
        size_layout.setContentsMargins(10, 5, 10, 5)
        
        size_label = QLabel(self.translator.translate("Size", self.language))
        size_layout.addWidget(size_label)
        
        size_slider = QSlider(Qt.Horizontal)
        size_slider.setRange(0, 2)  # 0: S(32px), 1: M(64px), 2: L(96px)
        
        # Check if current runner has multiple sizes available
        current_runner = self.runner_manager.get_current_runner()
        has_multiple_sizes = False
        available_sizes = []
        
        if current_runner:
            # Check if 64x64 and 96x96 exist
            # For built-in runners: only 32x32 available -> always False
            # For custom runners: check directories
            from app.animation.custom_runner import CustomRunner
            if isinstance(current_runner, CustomRunner):
                # Custom runner: check if size directories exist
                runner_folder = current_runner.folder_path
                if os.path.exists(os.path.join(runner_folder, "64x64")) and os.path.exists(os.path.join(runner_folder, "96x96")):
                    has_multiple_sizes = True
                    available_sizes = [32, 64, 96]
                elif os.path.exists(os.path.join(runner_folder, "64x64")):
                    has_multiple_sizes = True
                    available_sizes = [32, 64]
                else:
                    available_sizes = [32]
            else:
                # Built-in runner: only 32x32 available
                available_sizes = [32]
        else:
            available_sizes = [32]
        
        # Map current size to slider value, disable slider if only one size
        size_map = {32: 0, 64: 1, 96: 2}
        size_labels = {32: "S", 64: "M", 96: "L"}
        current_size_value = size_map.get(self.floating_ball_size, 2)  # Default to 96px
        size_slider.setValue(current_size_value)
        size_slider.setEnabled(has_multiple_sizes)
        size_slider.setFixedWidth(100)
        size_slider.setMinimumHeight(20)
        size_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #cccccc;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3366cc;
                border: 1px solid #3366cc;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::disabled:horizontal {
                background: #eeeeee;
            }
            QSlider::handle:disabled:horizontal {
                background: #aaaaaa;
                border: 1px solid #aaaaaa;
            }
        """)
        # Add size value label (show S/M/L instead of pixels)
        current_label = size_labels.get(self.floating_ball_size, size_labels.get(available_sizes[-1], "S"))
        size_value_label = QLabel(current_label)
        size_value_label.setFixedWidth(40)
        size_layout.addWidget(size_value_label)
        
        # Update size when slider changes
        def update_floating_ball_size(value):
            size_options = [32, 64, 96]
            if len(available_sizes) == 1:
                # Only one size available, keep current size
                new_size = available_sizes[0]
                size_value_label.setText(size_labels.get(new_size, "S"))
                return
            elif len(available_sizes) == 2:
                # Only 32 and 64 available
                available_options = [32, 64]
                if value >= len(available_options):
                    value = len(available_options) - 1
                new_size = available_options[value]
            else:
                # All three sizes available
                new_size = size_options[value]
            
            self.floating_ball.set_size(new_size)
            self.floating_ball_size = new_size
            self.settings_manager.set_floating_ball_size(new_size)
            size_value_label.setText(size_labels.get(new_size, "S"))
        
        size_slider.valueChanged.connect(update_floating_ball_size)
        size_layout.addWidget(size_slider)
        size_layout.addWidget(size_value_label)
        
        size_widget.setLayout(size_layout)
        
        size_action = QWidgetAction(self.floating_ball_menu)
        size_action.setDefaultWidget(size_widget)
        self.floating_ball_menu.addAction(size_action)
    
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
    
    def _toggle_floating_ball(self, checked):
        """Toggle floating ball visibility"""
        self.floating_ball_enabled = checked
        self.settings_manager.set_floating_ball_enabled(checked)
        if checked:
            self.floating_ball.show()
        else:
            self.floating_ball.hide()
        # Update the menu
        self._setup_floating_ball_menu()
    
    def _adjust_floating_ball_opacity(self, value):
        """Adjust floating ball opacity"""
        opacity = value / 100.0
        self.floating_ball_opacity = opacity
        self.settings_manager.set_floating_ball_opacity(opacity)
        self.floating_ball.set_opacity(opacity)
    
    def _setup_mode_menu(self):
        """Setup mode selection menu"""
        # Normal mode
        normal_action = QAction(self.translator.translate("Normal", self.language), self.mode_menu)
        normal_action.setCheckable(True)
        normal_action.setChecked(self.current_mode == "Normal")
        from functools import partial
        normal_action.triggered.connect(partial(self._select_mode, "Normal"))
        self.mode_menu.addAction(normal_action)
        
        # Work mode
        work_action = QAction(self.translator.translate("Work", self.language), self.mode_menu)
        work_action.setCheckable(True)
        work_action.setChecked(self.current_mode == "Work")
        work_action.triggered.connect(partial(self._select_mode, "Work"))
        self.mode_menu.addAction(work_action)
    
    def _setup_pomodoro_status_menu(self):
        """Setup pomodoro status menu items"""
        if self.work_mode_manager.is_working():
            status_text = self.translator.translate("Pomodoro", self.language) + ": " + \
                         self.translator.translate("Working", self.language) + \
                         " (" + self.work_mode_manager.get_remaining_formatted() + ")"
            self.pomodoro_status_action = QAction(status_text, self.menu)
            self.pomodoro_status_action.setEnabled(False)
            self.menu.addAction(self.pomodoro_status_action)
            
            self.pomodoro_cancel_action = QAction(self.translator.translate("Cancel Work", self.language), self.menu)
            self.pomodoro_cancel_action.triggered.connect(self._cancel_pomodoro)
            self.menu.addAction(self.pomodoro_cancel_action)
        else:
            status_text = self.translator.translate("Pomodoro", self.language) + ": " + \
                         self.translator.translate("Resting", self.language)
            self.pomodoro_status_action = QAction(status_text, self.menu)
            self.pomodoro_status_action.setEnabled(False)
            self.menu.addAction(self.pomodoro_status_action)
            
            self.pomodoro_start_action = QAction(self.translator.translate("Start Pomodoro", self.language), self.menu)
            self.pomodoro_start_action.triggered.connect(self._start_pomodoro_confirm)
            self.menu.addAction(self.pomodoro_start_action)
    
    def _select_mode(self, mode):
        """Select mode"""
        self.current_mode = mode
        self.settings_manager.set_current_mode(mode)
        self.work_mode_manager.set_current_mode(mode)
        
        if mode == "Normal":
            # Switch back to saved normal runner
            if self.runner_manager.current_runner != self.normal_saved_runner:
                self.runner_manager.set_current_runner(self.normal_saved_runner)
                self.settings_manager.set_runner(self.normal_saved_runner)
                self._load_frames()
                self.floating_ball.update_frames()
        elif mode == "Work":
            # Check if there is any configuration
            if not self.work_mode_manager.has_any_configuration():
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(None,
                    self.translator.translate("No Work mode configuration", self.language),
                    self.translator.translate("Please go to Manage Runners to configure groups for Work mode.", self.language)
                )
                # Revert back to Normal mode since we can't switch to Work
                self.current_mode = "Normal"
                self.settings_manager.set_current_mode("Normal")
                self.work_mode_manager.set_current_mode("Normal")
                # Rebuild menu immediately to correct the checked state
                self._setup_menu()
                return
            
            # Save current normal runner before switching
            self.normal_saved_runner = self.settings_manager.get_runner()
            # Ask user to start pomodoro
            self._start_pomodoro_confirm()
        
        # Update tooltip mode based on current mode
        self.system_info_tooltip.set_mode(self.current_mode)
        
        # Rebuild entire menu to show/hide pomodoro status
        self._setup_menu()
    
    def _start_pomodoro_confirm(self):
        """Ask user to confirm starting pomodoro"""
        from PyQt5.QtWidgets import QMessageBox
        
        if not self.work_mode_manager.has_any_configuration():
            QMessageBox.warning(None,
                self.translator.translate("Pomodoro", self.language),
                self.translator.translate("No runners are configured in groups! Please go to Manage Runners and assign runners to groups first.", self.language)
            )
            return
            
        result = QMessageBox.question(None,
            self.translator.translate("Pomodoro", self.language),
            self.translator.translate("Do you want to start a pomodoro work session?", self.language)
        )
        if result == QMessageBox.Yes:
            self._start_pomodoro()
        else:
            # Switch to rest mode
            self._switch_to_rest()
    
    def _start_pomodoro(self):
        """Start pomodoro"""
        self.work_mode_manager.start_pomodoro()
        self._switch_to_work()
        
        # Connect signals
        self.work_mode_manager.pomodoro_tick.connect(self._update_pomodoro_menu)
        self.work_mode_manager.pomodoro_finished.connect(self._on_pomodoro_finished)
    
    def _cancel_pomodoro(self):
        """Cancel current pomodoro"""
        self.work_mode_manager.stop_pomodoro()
        self._switch_to_rest()
        self._setup_menu()
    
    def _on_pomodoro_finished(self):
        """Called when pomodoro finishes"""
        self._switch_to_rest()
        self._setup_menu()
        # Show system notification
        self.work_mode_manager.show_system_notification(
            self.translator.translate("Pomodoro", self.language),
            self.translator.translate("Pomodoro finished! Time to rest.", self.language)
        )
    
    def _update_pomodoro_menu(self):
        """Update pomodoro menu display every second"""
        if self.work_mode_manager.is_work_mode() and self.pomodoro_status_action:
            # Only update the status text, don't rebuild entire menu
            if self.work_mode_manager.is_working():
                if self.work_mode_manager.is_paused():
                    status_text = self.translator.translate("Pomodoro", self.language) + ": " + \
                                 self.translator.translate("Paused", self.language) + \
                                 " (" + self.work_mode_manager.get_remaining_formatted() + ")"
                else:
                    status_text = self.translator.translate("Pomodoro", self.language) + ": " + \
                                 self.translator.translate("Working", self.language) + \
                                 " (" + self.work_mode_manager.get_remaining_formatted() + ")"
                self.pomodoro_status_action.setText(status_text)

    def _toggle_pomodoro_pause(self):
        """Toggle pause/resume for current pomodoro"""
        if self.work_mode_manager.is_paused():
            # Resume
            self.work_mode_manager.resume_pomodoro()
            self.pomodoro_dialog.set_working_state(True, self.work_mode_manager.get_remaining_seconds(), False)
        else:
            # Pause
            self.work_mode_manager.pause_pomodoro()
            self.pomodoro_dialog.set_working_state(True, self.work_mode_manager.get_remaining_seconds(), True)
        self._setup_menu()
    
    def _switch_to_work(self):
        """Switch to work runner"""
        runner_info = self.work_mode_manager.get_random_runner_by_action_type("work")
        if runner_info:
            self._switch_work_mode_runner(runner_info["runner_name"])
    
    def _switch_to_rest(self):
        """Switch to rest runner"""
        runner_info = self.work_mode_manager.get_random_runner_by_action_type("rest")
        if runner_info:
            self._switch_work_mode_runner(runner_info["runner_name"])
    
    def _switch_work_mode_runner(self, runner_name):
        """Switch runner in Work mode"""
        # Update current runner
        self.runner_manager.set_current_runner(runner_name)
        self.settings_manager.set_runner(runner_name)
        self._load_frames()
        self.floating_ball.update_frames()
    
    def eventFilter(self, obj, event):
        """Event filter for tray icon hover events"""
        if obj == self.tray:
            if event.type() == event.Enter:
                # Mouse entered tray icon, start timer to show tooltip
                self.tray_hover_timer.start(500)  # 500ms delay
            elif event.type() == event.Leave:
                # Mouse left tray icon, hide tooltip if shown
                self.tray_hover_timer.stop()
                if self.tray_tooltip_shown:
                    self.system_info_tooltip.hide()
                    self.tray_tooltip_shown = False
        return super().eventFilter(obj, event)
    
    def _show_tray_tooltip(self):
        """Show system info tooltip near tray icon"""
        # Get tray icon geometry
        tray_geometry = self.tray.geometry()
        if tray_geometry.isValid():
            # Create a temporary widget to represent the tray icon position
            from PyQt5.QtWidgets import QWidget
            temp_widget = QWidget()
            temp_widget.setGeometry(tray_geometry)
            # Show tooltip near the temporary widget
            self.system_info_tooltip.show_near_widget(temp_widget)
            self.tray_tooltip_shown = True
    
    def _select_runner(self, runner_name):
        """Select runner"""
        self.runner_manager.set_current_runner(runner_name)
        self.settings_manager.set_runner(runner_name)
        # Reset current frame to 0 when switching runners
        self.current_frame = 0
        self._load_frames()
        # Update floating ball frames
        self.floating_ball.update_frames()
        # Update only the runner menu to update the checked state
        self._setup_runner_menu()
        # Update floating ball menu to reflect available sizes for current runner
        self._setup_floating_ball_menu()
    
    def _select_theme(self, theme_name):
        """Select theme"""
        self.theme_manager.set_theme(theme_name)
        self.theme_manager.apply_theme(self.app)
        # Update system info tooltip theme
        current_theme = self.theme_manager.get_theme()
        is_dark = False
        if current_theme.theme_name == "Dark":
            is_dark = True
        elif current_theme.theme_name == "System":
            is_dark = current_theme.is_system_dark()
        self.system_info_tooltip.set_theme(is_dark)
        self.settings_manager.set_theme(theme_name)
        self._load_frames()
        # Update floating ball frames
        self.floating_ball.update_frames()
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
        """Load animation frames for tray icon (always 32x32)"""
        # First check if it's a custom runner
        self.custom_runner_manager.load_custom_runners()
        custom_runner = self.custom_runner_manager.get_custom_runner(self.runner_manager.current_runner)
        
        # Debug: Check current runner and custom runner
        with open("debug.log", "a") as f:
            f.write(f"Current runner: {self.runner_manager.current_runner}\n")
            f.write(f"Custom runner found: {custom_runner is not None}\n")
        
        # Tray icon always uses 32x32
        tray_size = (32, 32)
        if custom_runner:
            custom_runner.load_frames(self.theme_manager.get_theme(), tray_size)
            self.frames = custom_runner.get_frames()
            # Debug: Check custom runner frames
            with open("debug.log", "a") as f:
                f.write(f"Custom runner frames count: {len(self.frames)}\n")
        else:
            # If not a custom runner, load built-in runner
            current_runner = self.runner_manager.get_current_runner()
            if current_runner:
                current_runner.load_frames(self.theme_manager.get_theme(), tray_size)
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
            # Advance to next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            # Use setIcon directly without any delay
            self.tray.setIcon(self.frames[self.current_frame])
    
    def _update_animation_speed(self):
        """Update animation speed based on system load (every 2 seconds)"""
        # Update monitors first to get current system load
        self.cpu_monitor.update()
        self.memory_monitor.update()
        self.network_monitor.update()
        
        # Calculate system load based on selected speed source
        load = 0
        if self.speed_source == "CPU":
            load = self.cpu_monitor.get_usage()
        elif self.speed_source == "Memory":
            load = self.memory_monitor.get_usage()
        elif self.speed_source == "Network":
            load = max(self.network_monitor.get_speed_sent(), self.network_monitor.get_speed_recv()) / 1024 / 1024  # MB/s
        
        # Calculate new interval based on load and FPS limit
        fps = int(self.fps_max_limit.replace("FPS", ""))
        speed = max(1.0, (load / 5.0) * (fps / 40.0))
        interval = int(500.0 / speed)
        
        # Update animation timer interval only for tray icon
        # Floating ball keeps fixed speed (200ms)
        self.animate_timer.setInterval(interval)
    
    def _fetch_system_info(self):
        """Fetch system information"""
        # Update monitors
        self.cpu_monitor.update()
        self.memory_monitor.update()
        self.network_monitor.update()
        
        # Update system tray tooltip with all system info
        cpu_usage = self.cpu_monitor.get_usage()
        memory_usage = self.memory_monitor.get_usage()
        speed_sent = self.network_monitor.get_speed_sent() / 1024  # KB/s
        speed_recv = self.network_monitor.get_speed_recv() / 1024  # KB/s
        total_speed = speed_sent + speed_recv
        
        tooltip = f"CPU: {cpu_usage:.1f}% \nMemory: {memory_usage:.1f}% \nNetwork: {total_speed:.1f} KB/s"
        self.tray.setToolTip(f"RunCat365 \n{tooltip}")
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    print("Starting RunCat365...")
    app = RunCatApp()
    print("RunCat365 started successfully!")
    app.run()

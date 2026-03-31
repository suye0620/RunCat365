#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System information tooltip module
Shows system info in Normal mode, shows pomodoro info in Work mode
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class SystemInfoTooltip(QWidget):
    """System information tooltip widget
    Shows system info in Normal mode, shows pomodoro info in Work mode
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set window properties
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # System monitors
        self.cpu_monitor = None
        self.memory_monitor = None
        self.network_monitor = None
        
        # Work mode manager for pomodoro
        self.work_mode_manager = None
        
        # Toggle callback for pomodoro pause/resume
        self.on_toggle_pause = None
        self.on_abort_pomodoro = None
        self.on_start_pomodoro = None
        
        # Current mode
        self.current_mode = "Normal"
        
        # Initialize UI
        self.init_ui()
        
        # Update timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_info)
        self.update_timer.start(500)
        
        # Hide initially
        self.hide()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # Title
        self.title_label = QLabel("System Info")
        font = QFont()
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        # System info container (CPU, Memory, Network)
        self.system_container = QVBoxLayout()
        self.system_container.setSpacing(5)
        
        # CPU info
        self.cpu_label = QLabel("CPU: 0%")
        self.system_container.addWidget(self.cpu_label)
        
        # Memory info
        self.memory_label = QLabel("Memory: 0%")
        self.system_container.addWidget(self.memory_label)
        
        # Network info
        self.network_label = QLabel("Network: 0 KB/s")
        self.system_container.addWidget(self.network_label)
        
        self.system_widget = QWidget()
        self.system_widget.setLayout(self.system_container)
        main_layout.addWidget(self.system_widget)
        
        # Pomodoro container
        self.pomodoro_container = QVBoxLayout()
        self.pomodoro_container.setSpacing(8)
        
        # Status
        self.pomodoro_status_label = QLabel("Ready")
        font_status = self.pomodoro_status_label.font()
        font_status.setPointSize(12)
        self.pomodoro_status_label.setFont(font_status)
        self.pomodoro_status_label.setAlignment(Qt.AlignCenter)
        self.pomodoro_container.addWidget(self.pomodoro_status_label)
        
        # Countdown
        self.pomodoro_countdown_label = QLabel("30:00")
        font_count = self.pomodoro_countdown_label.font()
        font_count.setPointSize(20)
        font_count.setBold(True)
        self.pomodoro_countdown_label.setFont(font_count)
        self.pomodoro_countdown_label.setAlignment(Qt.AlignCenter)
        self.pomodoro_container.addWidget(self.pomodoro_countdown_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.pomodoro_start_button = QPushButton("Start")
        self.pomodoro_start_button.clicked.connect(self._on_start_clicked)
        button_layout.addWidget(self.pomodoro_start_button)
        
        self.pomodoro_pause_button = QPushButton("Pause")
        self.pomodoro_pause_button.clicked.connect(self._on_pause_clicked)
        button_layout.addWidget(self.pomodoro_pause_button)
        
        self.pomodoro_abort_button = QPushButton("Abort")
        self.pomodoro_abort_button.clicked.connect(self._on_abort_clicked)
        button_layout.addWidget(self.pomodoro_abort_button)
        
        self.pomodoro_container.addLayout(button_layout)
        
        self.pomodoro_widget = QWidget()
        self.pomodoro_widget.setLayout(self.pomodoro_container)
        main_layout.addWidget(self.pomodoro_widget)
        
        # Set layout
        self.setLayout(main_layout)
        
        # Set style
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            QLabel {
                font-family: Microsoft YaHei, Segoe UI, sans-serif;
                font-size: 12px;
                color: black;
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton {
                font-family: Microsoft YaHei, Segoe UI, sans-serif;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#pause_button {
                background-color: #ff9800;
            }
            QPushButton#pause_button:hover {
                background-color: #e68a00;
            }
            QPushButton#pause_button:pressed {
                background-color: #cc7a00;
            }
            QPushButton#abort_button {
                background-color: #f44336;
            }
            QPushButton#abort_button:hover {
                background-color: #da190b;
            }
            QPushButton#abort_button:pressed {
                background-color: #d32f2f;
            }
        """)
        
        self.pomodoro_pause_button.setObjectName("pause_button")
        self.pomodoro_abort_button.setObjectName("abort_button")
        
        # Initially hide pomodoro
        self._update_visibility()
    
    def set_monitors(self, cpu_monitor, memory_monitor, network_monitor):
        """Set system monitors"""
        self.cpu_monitor = cpu_monitor
        self.memory_monitor = memory_monitor
        self.network_monitor = network_monitor
    
    def set_work_mode_manager(self, work_mode_manager):
        """Set work mode manager for pomodoro"""
        self.work_mode_manager = work_mode_manager
    
    def set_callbacks(self, on_start_pomodoro, on_toggle_pause, on_abort_pomodoro):
        """Set callback for pomodoro controls"""
        self.on_start_pomodoro = on_start_pomodoro
        self.on_toggle_pause = on_toggle_pause
        self.on_abort_pomodoro = on_abort_pomodoro
    
    def set_mode(self, mode):
        """Set current mode: Normal or Work"""
        self.current_mode = mode
        self._update_visibility()
        self.update_info()
    
    def _update_visibility(self):
        """Update visibility based on mode"""
        # Hide/show entire containers
        self.system_widget.setVisible(self.current_mode == "Normal")
        self.pomodoro_widget.setVisible(self.current_mode == "Work")
    
    def update_info(self):
        """Update information based on current mode"""
        if self.current_mode == "Normal":
            self._update_system_info()
        else:
            self._update_pomodoro_info()
        
        # Force repaint to ensure the UI updates immediately
        if self.isVisible():
            self.repaint()
    
    def _update_system_info(self):
        """Update system information"""
        if self.cpu_monitor:
            # Update CPU usage first
            self.cpu_monitor.update()
            cpu_usage = self.cpu_monitor.get_usage()
            self.cpu_label.setText(f"CPU: {cpu_usage:.1f}%")
        
        if self.memory_monitor:
            # Update memory usage first
            self.memory_monitor.update()
            memory_usage = self.memory_monitor.get_usage()
            self.memory_label.setText(f"Memory: {memory_usage:.1f}%")
        
        if self.network_monitor:
            # Update network usage first
            self.network_monitor.update()
            speed_sent = self.network_monitor.get_speed_sent() / 1024
            speed_recv = self.network_monitor.get_speed_recv() / 1024
            total_speed = speed_sent + speed_recv
            self.network_label.setText(f"Network: {total_speed:.1f} KB/s")
        
        self.title_label.setText("System Info")
    
    def _update_pomodoro_info(self):
        """Update pomodoro information"""
        if not self.work_mode_manager:
            return
        
        # Get current language from main app
        import sys
        from PyQt5.QtWidgets import QApplication
        main_window = QApplication.activeWindow()
        if main_window and hasattr(main_window, 'translator') and hasattr(main_window, 'language'):
            translator = main_window.translator
            language = main_window.language
        else:
            translator = None
            language = "English"
        
        def tr(key):
            if translator:
                return translator.translate(key, language)
            return key
        
        self.title_label.setText(f"🍅 {tr('Pomodoro')}")
        
        if self.work_mode_manager.is_working():
            if self.work_mode_manager.is_paused():
                self.pomodoro_status_label.setText(tr("Paused"))
                self.pomodoro_pause_button.setText(tr("Start") if tr("Start") != "Start" else "Resume")
                self.pomodoro_pause_button.setEnabled(True)
                self.pomodoro_start_button.setEnabled(False)
                self.pomodoro_abort_button.setEnabled(True)
            else:
                self.pomodoro_status_label.setText(tr("Working"))
                self.pomodoro_pause_button.setText(tr("Pause"))
                self.pomodoro_pause_button.setEnabled(True)
                self.pomodoro_start_button.setEnabled(False)
                self.pomodoro_abort_button.setEnabled(True)
            remaining = self.work_mode_manager.get_remaining_seconds()
            minutes = remaining // 60
            seconds = remaining % 60
            self.pomodoro_countdown_label.setText(f"{minutes}:{seconds:02d}")
            self.pomodoro_countdown_label.show()
        else:
            self.pomodoro_status_label.setText(tr("Resting"))
            self.pomodoro_pause_button.setText(tr("Pause"))
            self.pomodoro_pause_button.setEnabled(False)
            self.pomodoro_start_button.setText(tr("Start"))
            self.pomodoro_start_button.setEnabled(True)
            self.pomodoro_abort_button.setText(tr("Abort"))
            self.pomodoro_abort_button.setEnabled(False)
            self.pomodoro_countdown_label.setText("30:00")
            self.pomodoro_countdown_label.show()
    
    def _on_start_clicked(self):
        """Handle start pomodoro button click"""
        if self.on_start_pomodoro:
            self.on_start_pomodoro()
    
    def _on_pause_clicked(self):
        """Handle pause/resume button click"""
        if self.on_toggle_pause:
            self.on_toggle_pause()
            self._update_pomodoro_info()
    
    def _on_abort_clicked(self):
        """Handle abort button click"""
        if self.on_abort_pomodoro:
            self.on_abort_pomodoro()
            self._update_pomodoro_info()
    
    def set_theme(self, is_dark):
        """Set theme"""
        if is_dark:
            # Dark theme
            self.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border: none;
                    padding: 5px;
                }
                QLabel {
                    font-family: Microsoft YaHei, Segoe UI, sans-serif;
                    font-size: 12px;
                    color: #ffffff;
                    background-color: rgba(40, 40, 40, 0.95);
                    border: 1px solid #555;
                    border-radius: 8px;
                    padding: 5px;
                }
                QPushButton {
                    font-family: Microsoft YaHei, Segoe UI, sans-serif;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
                QPushButton#pause_button {
                    background-color: #ff9800;
                }
                QPushButton#pause_button:hover {
                    background-color: #e68a00;
                }
                QPushButton#pause_button:pressed {
                    background-color: #cc7a00;
                }
                QPushButton#abort_button {
                    background-color: #f44336;
                }
                QPushButton#abort_button:hover {
                    background-color: #da190b;
                }
                QPushButton#abort_button:pressed {
                    background-color: #d32f2f;
                }
            """)
        else:
            # Light theme
            self.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border: none;
                    padding: 5px;
                }
                QLabel {
                    font-family: Microsoft YaHei, Segoe UI, sans-serif;
                    font-size: 12px;
                    color: #000000;
                    background-color: rgba(255, 255, 255, 0.9);
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 5px;
                }
                QPushButton {
                    font-family: Microsoft YaHei, Segoe UI, sans-serif;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
                QPushButton#pause_button {
                    background-color: #ff9800;
                }
                QPushButton#pause_button:hover {
                    background-color: #e68a00;
                }
                QPushButton#pause_button:pressed {
                    background-color: #cc7a00;
                }
                QPushButton#abort_button {
                    background-color: #f44336;
                }
                QPushButton#abort_button:hover {
                    background-color: #da190b;
                }
                QPushButton#abort_button:pressed {
                    background-color: #d32f2f;
                }
            """)
    
    def show_near_widget(self, widget):
        """Show tooltip near the specified widget"""
        if widget:
            # Get widget position and size
            widget_pos = widget.mapToGlobal(widget.rect().topLeft())
            widget_width = widget.width()
            widget_height = widget.height()
            
            # Get screen geometry
            from PyQt5.QtWidgets import QApplication
            screen = QApplication.screens()[0] if QApplication.screens() else None
            if screen:
                screen_geometry = screen.availableGeometry()
            
            # Calculate tooltip position (above the widget, centered)
            x = widget_pos.x() + (widget_width - self.width()) // 2
            y = widget_pos.y() - self.height() - 10
            
            # Calculate boundaries and clamp position
            if screen:
                max_x = screen_geometry.width() - self.width()
                max_y = screen_geometry.height() - self.height()
                
                # Clamp position to screen boundaries
                x = max(0, min(x, max_x))
                y = max(0, min(y, max_y))
            
            # Move tooltip
            self.move(x, y)
        
        # Update info and show
        self.update_info()
        self.show()

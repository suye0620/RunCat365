#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System information tooltip module
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class SystemInfoTooltip(QWidget):
    """System information tooltip widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set window properties
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # Set transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # System monitors
        self.cpu_monitor = None
        self.memory_monitor = None
        self.network_monitor = None
        
        # Initialize UI
        self.init_ui()
        
        # Update timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_info)
        self.update_timer.start(500)  # 0.5秒更新一次 (与主程序同步)
        
        # Hide initially
        self.hide()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        self.title_label = QLabel("System Info")
        font = QFont()
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        # CPU info
        self.cpu_label = QLabel("CPU: 0%")
        main_layout.addWidget(self.cpu_label)
        
        # Memory info
        self.memory_label = QLabel("Memory: 0%")
        main_layout.addWidget(self.memory_label)
        
        # Network info
        self.network_label = QLabel("Network: 0 KB/s")
        main_layout.addWidget(self.network_label)
        
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
        """)
    
    def set_monitors(self, cpu_monitor, memory_monitor, network_monitor):
        """Set system monitors"""
        self.cpu_monitor = cpu_monitor
        self.memory_monitor = memory_monitor
        self.network_monitor = network_monitor
    
    def update_info(self):
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
            speed_sent = self.network_monitor.get_speed_sent() / 1024  # KB/s
            speed_recv = self.network_monitor.get_speed_recv() / 1024  # KB/s
            total_speed = speed_sent + speed_recv
            self.network_label.setText(f"Network: {total_speed:.1f} KB/s")
        
        # Force repaint to ensure the UI updates immediately
        if self.isVisible():
            self.repaint()
    
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

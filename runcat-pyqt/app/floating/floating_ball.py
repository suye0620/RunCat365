#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Floating ball module
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QPen


class FloatingBall(QWidget):
    """Floating ball widget"""
    
    def __init__(self, runner_manager, theme_manager, opacity=0.8, size=96):
        super().__init__()
        
        self.runner_manager = runner_manager
        self.theme_manager = theme_manager
        self.opacity = opacity
        self.ball_size = size  # Size in pixels (96, 64, or 32)
        
        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_Hover, True)  # Enable hover events
        self.setFixedSize(self.ball_size, self.ball_size)
        self.setWindowOpacity(opacity)
        self.setMouseTracking(True)  # Enable mouse tracking
        
        # Animation variables
        self.current_frame = 0
        self.frames = []
        
        # Mouse dragging variables
        self.dragging = False
        self.drag_start_pos = QPoint()
        
        # Animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._advance_frame)
        self.animation_timer.start(200)
        
        # Load initial frames
        self.update_frames()
        
        # Set initial position (bottom-right corner of the screen, at 2/3 height)
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.screens()[0] if QApplication.screens() else None
        if screen:
            screen_geometry = screen.availableGeometry()
            x = screen_geometry.width() - self.width() - 20  # 离右侧边界20像素
            # 垂直方向上处于靠下的三分点处 (2/3高度)
            y = screen_geometry.height() * 2 // 3
            self.move(x, y)
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move event"""
        if self.dragging:
            # Calculate new position
            new_pos = event.globalPos() - self.drag_start_pos
            
            # Get screen geometry
            from PyQt5.QtWidgets import QApplication
            screen = QApplication.screens()[0] if QApplication.screens() else None
            if screen:
                screen_geometry = screen.availableGeometry()
                
                # Calculate boundaries
                max_x = screen_geometry.width() - self.width()
                max_y = screen_geometry.height() - self.height()
                
                # Clamp position to screen boundaries
                new_x = max(0, min(new_pos.x(), max_x))
                new_y = max(0, min(new_pos.y(), max_y))
                
                # Move to clamped position
                self.move(new_x, new_y)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release event"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def enterEvent(self, event):
        """Handle mouse enter event"""
        # Show system info tooltip
        if hasattr(self, 'tooltip') and self.tooltip:
            # Show tooltip near the floating ball
            self.tooltip.show_near_widget(self)
        event.accept()
    
    def leaveEvent(self, event):
        """Handle mouse leave event"""
        # Hide system info tooltip
        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.hide()
        event.accept()
    
    def set_tooltip(self, tooltip):
        """Set system info tooltip"""
        self.tooltip = tooltip
    
    def paintEvent(self, event):
        """Paint the widget"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.frames and self.current_frame < len(self.frames):
            icon = self.frames[self.current_frame]
            pixmap = icon.pixmap(self.size())
            painter.drawPixmap(0, 0, pixmap)
        else:
            # Draw a default circle if no frames are available
            painter.setPen(Qt.black)
            painter.setBrush(Qt.red)
            painter.drawEllipse(10, 10, self.width() - 20, self.height() - 20)
    
    def _advance_frame(self):
        """Advance animation frame"""
        if self.frames:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.update()
    
    def update_frames(self):
        """Update animation frames"""
        try:
            # Get current runner
            current_runner = self.runner_manager.get_current_runner()
            if current_runner:
                # Load frames with current size
                current_runner.load_frames(self.theme_manager.get_theme(), (self.ball_size, self.ball_size))
                self.frames = current_runner.get_frames()
        except Exception as e:
            # Handle any errors to prevent crash
            print(f"Error loading frames: {e}")
        
        # Reset current frame
        self.current_frame = 0
    
    def set_opacity(self, opacity):
        """Set opacity"""
        self.opacity = opacity
        self.setWindowOpacity(opacity)
    
    def get_opacity(self):
        """Get opacity"""
        return self.opacity
    
    def set_size(self, size):
        """Set floating ball size"""
        self.ball_size = size
        self.setFixedSize(self.ball_size, self.ball_size)
        self.update_frames()  # Update frames with new size
    
    def set_animation_speed(self, interval):
        """Set animation speed interval (in milliseconds)"""
        self.animation_timer.setInterval(interval)

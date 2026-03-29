#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Endless game module
"""

import random
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect


class EndlessGameForm(QMainWindow):
    """Endless game form"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Endless Game")
        self.setGeometry(100, 100, 800, 400)
        
        self.init_game()
        self.init_ui()
    
    def init_game(self):
        """Initialize game variables"""
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.cat_y = 200
        self.cat_velocity = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.obstacles = []
        self.obstacle_speed = 5
        self.obstacle_spawn_rate = 2000  # milliseconds
        self.last_obstacle_time = 0
        
        # Game timer
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(30)
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.score_label = QLabel(f"Score: {self.score}")
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)
        
        self.instruction_label = QLabel("Press Space to start")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction_label)
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Space:
            if not self.game_active:
                self.start_game()
            else:
                self.jump()
    
    def start_game(self):
        """Start the game"""
        self.game_active = True
        self.score = 0
        self.cat_y = 200
        self.cat_velocity = 0
        self.obstacles = []
        self.instruction_label.setText("Press Space to jump")
    
    def jump(self):
        """Make the cat jump"""
        if self.cat_y >= 200:  # Only jump if on ground
            self.cat_velocity = self.jump_power
    
    def game_loop(self):
        """Game loop"""
        if not self.game_active:
            return
        
        # Update cat position
        self.cat_velocity += self.gravity
        self.cat_y += self.cat_velocity
        
        # Keep cat on ground
        if self.cat_y >= 200:
            self.cat_y = 200
            self.cat_velocity = 0
        
        # Spawn obstacles
        current_time = QTimer.currentTime().msecsSinceStartOfDay()
        if current_time - self.last_obstacle_time > self.obstacle_spawn_rate:
            self.spawn_obstacle()
            self.last_obstacle_time = current_time
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle['x'] -= self.obstacle_speed
            if obstacle['x'] < -50:
                self.obstacles.remove(obstacle)
                self.score += 1
                self.score_label.setText(f"Score: {self.score}")
        
        # Check collision
        if self.check_collision():
            self.game_over()
        
        # Repaint
        self.update()
    
    def spawn_obstacle(self):
        """Spawn a new obstacle"""
        obstacle = {
            'x': 800,
            'y': 200,
            'width': 30,
            'height': 50
        }
        self.obstacles.append(obstacle)
    
    def check_collision(self):
        """Check for collision"""
        cat_rect = QRect(100, self.cat_y, 50, 50)
        for obstacle in self.obstacles:
            obstacle_rect = QRect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
            if cat_rect.intersects(obstacle_rect):
                return True
        return False
    
    def game_over(self):
        """Game over"""
        self.game_active = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.instruction_label.setText(f"Game Over! Score: {self.score} High Score: {self.high_score}\nPress Space to restart")
    
    def paintEvent(self, event):
        """Paint event"""
        painter = QPainter(self)
        
        # Draw ground
        painter.setBrush(QColor(100, 200, 100))
        painter.drawRect(0, 250, self.width(), self.height() - 250)
        
        # Draw cat
        painter.setBrush(QColor(255, 100, 100))
        painter.drawRect(100, self.cat_y, 50, 50)
        
        # Draw obstacles
        painter.setBrush(QColor(100, 100, 255))
        for obstacle in self.obstacles:
            painter.drawRect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])

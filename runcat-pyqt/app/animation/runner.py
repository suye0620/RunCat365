#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Runner animation module
"""

import os
from PyQt5.QtGui import QIcon, QPixmap


class Runner:
    """Runner base class"""
    
    def __init__(self, name, frame_count):
        self.name = name
        self.frame_count = frame_count
        self.frames = []
    
    def load_frames(self, theme):
        """Load animation frames"""
        pass
    
    def get_frames(self):
        """Get animation frames"""
        return self.frames
    
    def get_name(self):
        """Get runner name"""
        return self.name
    
    def get_frame_count(self):
        """Get frame count"""
        return self.frame_count


class BuiltinRunner(Runner):
    """Built-in runner"""
    
    def __init__(self, name, frame_count):
        super().__init__(name, frame_count)
    
    def load_frames(self, theme):
        """Load animation frames from resources"""
        self.frames = []
        resource_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "runners", self.name.lower())
        
        for i in range(self.frame_count):
            frame_path = os.path.join(resource_path, f"{self.name.lower()}_{i}.png")
            if os.path.exists(frame_path):
                pixmap = QPixmap(frame_path)
                # Apply theme if needed
                self.frames.append(QIcon(pixmap))
        
        # If no frames loaded, create a default frame
        if not self.frames:
            pixmap = QPixmap(32, 32)
            self.frames = [QIcon(pixmap)]


class RunnerManager:
    """Runner manager"""
    
    def __init__(self):
        self.runners = {
            "Cat": BuiltinRunner("Cat", 5),
            "Parrot": BuiltinRunner("Parrot", 10),
            "Horse": BuiltinRunner("Horse", 5)
        }
        self.current_runner = "Cat"
    
    def get_runner(self, name):
        """Get runner by name"""
        return self.runners.get(name)
    
    def get_current_runner(self):
        """Get current runner"""
        # First try to get built-in runner
        runner = self.get_runner(self.current_runner)
        if runner:
            return runner
        
        # If not found, try to get custom runner
        try:
            from app.animation.custom_runner import CustomRunnerManager
            custom_runner_manager = CustomRunnerManager()
            custom_runner_manager.load_custom_runners()
            return custom_runner_manager.get_custom_runner(self.current_runner)
        except:
            return None
    
    def set_current_runner(self, name):
        """Set current runner"""
        # Allow setting custom runners as well
        self.current_runner = name
    
    def get_runner_names(self):
        """Get all runner names"""
        return list(self.runners.keys())
    
    def add_custom_runner(self, name, frame_count):
        """Add custom runner"""
        # Implementation will be added later
        pass

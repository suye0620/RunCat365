#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom runner module
"""

import os
from PIL import Image
from PyQt5.QtGui import QIcon, QPixmap, QImage


class CustomRunner:
    """Custom runner class"""
    
    def __init__(self, name, frame_count, folder_path):
        self.name = name
        self.frame_count = frame_count
        self.folder_path = folder_path
        self.frames = []
    
    def load_frames(self, theme):
        """Load animation frames"""
        self.frames = []
        
        for i in range(self.frame_count):
            frame_path = os.path.join(self.folder_path, f"{self.name}_{i}.png")
            if os.path.exists(frame_path):
                pixmap = QPixmap(frame_path)
                # Apply theme if needed
                self.frames.append(QIcon(pixmap))
        
        # If no frames loaded, create a default frame
        if not self.frames:
            pixmap = QPixmap(32, 32)
            self.frames = [QIcon(pixmap)]
    
    def get_frames(self):
        """Get animation frames"""
        return self.frames
    
    def get_name(self):
        """Get runner name"""
        return self.name
    
    def get_frame_count(self):
        """Get frame count"""
        return self.frame_count


class CustomRunnerManager:
    """Custom runner manager"""
    
    def __init__(self):
        self.custom_runners = {}
        self.custom_runners_folder = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "custom_runners")
        os.makedirs(self.custom_runners_folder, exist_ok=True)
    
    def load_custom_runners(self):
        """Load custom runners from directory"""
        self.custom_runners = {}
        
        if not os.path.exists(self.custom_runners_folder):
            return
        
        for runner_folder in os.listdir(self.custom_runners_folder):
            folder_path = os.path.join(self.custom_runners_folder, runner_folder)
            if os.path.isdir(folder_path):
                frame_count = self._count_frames(folder_path, runner_folder)
                if frame_count > 0:
                    self.custom_runners[runner_folder] = CustomRunner(runner_folder, frame_count, folder_path)
    
    def _count_frames(self, folder_path, runner_name):
        """Count frames in a runner folder"""
        count = 0
        while os.path.exists(os.path.join(folder_path, f"{runner_name}_{count}.png")):
            count += 1
        return count
    
    def import_gif(self, gif_path, runner_name):
        """Import GIF and extract frames"""
        try:
            # Create runner folder
            runner_folder = os.path.join(self.custom_runners_folder, runner_name)
            os.makedirs(runner_folder, exist_ok=True)
            
            # Open GIF and extract frames
            with Image.open(gif_path) as gif:
                frame_count = gif.n_frames
                
                for i in range(frame_count):
                    gif.seek(i)
                    # Resize to 32x32
                    frame = gif.resize((32, 32), Image.LANCZOS)
                    frame_path = os.path.join(runner_folder, f"{runner_name}_{i}.png")
                    frame.save(frame_path, "PNG")
            
            # Add to custom runners
            self.custom_runners[runner_name] = CustomRunner(runner_name, frame_count, runner_folder)
            return True
        except Exception:
            return False
    
    def remove_custom_runner(self, runner_name):
        """Remove custom runner"""
        if runner_name in self.custom_runners:
            runner = self.custom_runners[runner_name]
            # Delete folder
            import shutil
            if os.path.exists(runner.folder_path):
                shutil.rmtree(runner.folder_path)
            # Remove from dictionary
            del self.custom_runners[runner_name]
            return True
        return False
    
    def get_custom_runner(self, name):
        """Get custom runner by name"""
        return self.custom_runners.get(name)
    
    def get_custom_runner_names(self):
        """Get all custom runner names"""
        return list(self.custom_runners.keys())
    
    def get_all_runners(self):
        """Get all custom runners"""
        return list(self.custom_runners.values())

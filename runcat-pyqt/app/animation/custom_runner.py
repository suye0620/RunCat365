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
    
    def load_frames(self, theme, size=None):
        """Load animation frames"""
        self.frames = []
        
        if not size:
            size = (32, 32)
        
        size_folder = f"{size[0]}x{size[1]}"
        size_dir = os.path.join(self.folder_path, size_folder)
        
        # Check if new directory structure exists
        if os.path.exists(size_dir):
            # New structure: {runner_folder}/{size}/frame_{i}.png
            for i in range(self.frame_count):
                frame_path = os.path.join(size_dir, f"frame_{i}.png")
                if os.path.exists(frame_path):
                    pixmap = QPixmap(frame_path)
                    self.frames.append(QIcon(pixmap))
        else:
            # Old structure: all in one folder with size in filename
            for i in range(self.frame_count):
                frame_path = os.path.join(self.folder_path, f"{self.name}_{i}_{size[0]}x{size[1]}.png")
                if os.path.exists(frame_path):
                    pixmap = QPixmap(frame_path)
                    self.frames.append(QIcon(pixmap))
        
        # If no frames loaded, create a default frame
        if not self.frames:
            pixmap = QPixmap(size[0], size[1])
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
        
        # Migrate old file structure to new structure
        migrated = self.migrate_old_files()
        
        for runner_folder in os.listdir(self.custom_runners_folder):
            folder_path = os.path.join(self.custom_runners_folder, runner_folder)
            if os.path.isdir(folder_path):
                frame_count = self._count_frames(folder_path, runner_folder)
                if frame_count > 0:
                    self.custom_runners[runner_folder] = CustomRunner(runner_folder, frame_count, folder_path)
    
    def _count_frames(self, folder_path, runner_name):
        """Count frames in a runner folder"""
        # Check for new directory structure: {folder_path}/32x32/frame_{i}.png
        size_32_dir = os.path.join(folder_path, "32x32")
        if os.path.exists(size_32_dir):
            count = 0
            while os.path.exists(os.path.join(size_32_dir, f"frame_{count}.png")):
                count += 1
            return count
        
        # Check for old multi-size format: {runner_name}_{i}_{size}x{size}.png
        # Count unique frame indices from filenames
        frame_indices = set()
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                # Match patterns like: name_0_32x32.png or name_0.png
                parts = filename.split('_')
                if len(parts) >= 2:
                    try:
                        frame_idx = int(parts[1]) if len(parts) == 4 else int(parts[-1].split('.')[0])
                        frame_indices.add(frame_idx)
                    except ValueError:
                        continue
        
        if frame_indices:
            return len(frame_indices)
        
        # Check for old single-size format: {runner_name}_{count}.png
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
            
            # Create size subdirectories
            sizes = [(32, 32), (64, 64), (96, 96)]
            for size in sizes:
                size_folder = os.path.join(runner_folder, f"{size[0]}x{size[1]}")
                os.makedirs(size_folder, exist_ok=True)
            
            # Open GIF and extract frames
            with Image.open(gif_path) as gif:
                frame_count = gif.n_frames
                
                for i in range(frame_count):
                    gif.seek(i)
                    # Generate different sizes
                    for size in sizes:
                        frame = gif.resize(size, Image.LANCZOS)
                        size_folder = f"{size[0]}x{size[1]}"
                        frame_path = os.path.join(runner_folder, size_folder, f"frame_{i}.png")
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
    
    def migrate_old_files(self):
        """Migrate old file structure to new directory structure
        Old: {runner_folder}/{name}_{i}_{size}x{size}.png
        New: {runner_folder}/{size}/frame_{i}.png
        """
        migrated_count = 0
        
        if not os.path.exists(self.custom_runners_folder):
            return migrated_count
        
        for runner_folder_name in os.listdir(self.custom_runners_folder):
            runner_folder = os.path.join(self.custom_runners_folder, runner_folder_name)
            if not os.path.isdir(runner_folder):
                continue
            
            # Check if already migrated (has 32x32, 64x64, 96x96 folders)
            size_folders = ['32x32', '64x64', '96x96']
            has_size_folders = all(os.path.exists(os.path.join(runner_folder, f)) for f in size_folders)
            if has_size_folders:
                continue  # Already migrated
            
            # Find all PNG files matching old pattern
            migrated_this_runner = False
            for filename in os.listdir(runner_folder):
                if not filename.endswith('.png'):
                    continue
                
                # Parse filename: {name}_{i}_{size}x{size}.png
                parts = filename.split('_')
                if len(parts) != 4:
                    continue  # Not matching old multi-size pattern
                
                try:
                    frame_idx = int(parts[1])
                    size_part = parts[3].replace('.png', '')
                    width, height = map(int, size_part.split('x'))
                    
                    # Create size folder
                    size_folder = os.path.join(runner_folder, f"{width}x{height}")
                    os.makedirs(size_folder, exist_ok=True)
                    
                    # Move file to new location
                    old_path = os.path.join(runner_folder, filename)
                    new_path = os.path.join(size_folder, f"frame_{frame_idx}.png")
                    
                    if os.path.exists(old_path) and not os.path.exists(new_path):
                        import shutil
                        shutil.move(old_path, new_path)
                        migrated_this_runner = True
                    
                except (ValueError, IndexError):
                    continue
            
            # Handle old single-size format: {name}_{i}.png
            if not migrated_this_runner:
                # Check if it's the old single-size format
                single_size_files = []
                for filename in os.listdir(runner_folder):
                    if filename.endswith('.png') and filename.startswith(runner_folder_name + '_'):
                        parts = filename.split('.')[0].split('_')
                        if len(parts) == 2:
                            try:
                                int(parts[1])
                                single_size_files.append(filename)
                            except ValueError:
                                continue
                
                if single_size_files:
                    # This is old single-size, need to generate all three sizes
                    # We'll skip auto-migration for this case, user can re-import
                    continue
            
            if migrated_this_runner:
                migrated_count += 1
        
        return migrated_count

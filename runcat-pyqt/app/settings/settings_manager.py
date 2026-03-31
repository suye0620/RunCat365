#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Settings manager module
"""

import os
import json


class SettingsManager:
    """Settings manager"""
    
    def __init__(self):
        self.settings_file = os.path.join(os.path.dirname(__file__), "..", "..", "settings.json")
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Load settings from file"""
        default_settings = {
            "runner": "Cat",
            "theme": "System",
            "speed_source": "CPU",
            "fps_max_limit": "FPS40",
            "launch_at_startup": False,
            "language": "English",
            "floating_ball_enabled": True,
            "floating_ball_opacity": 0.8,
            "floating_ball_size": 96,
            "current_mode": "Normal"
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return default_settings
        return default_settings
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def get_setting(self, key, default=None):
        """Get setting by key"""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """Set setting by key"""
        self.settings[key] = value
        return self._save_settings()
    
    def get_runner(self):
        """Get current runner"""
        return self.get_setting("runner", "Cat")
    
    def set_runner(self, runner):
        """Set current runner"""
        return self.set_setting("runner", runner)
    
    def get_theme(self):
        """Get current theme"""
        return self.get_setting("theme", "System")
    
    def set_theme(self, theme):
        """Set current theme"""
        return self.set_setting("theme", theme)
    
    def get_speed_source(self):
        """Get current speed source"""
        return self.get_setting("speed_source", "CPU")
    
    def set_speed_source(self, speed_source):
        """Set current speed source"""
        return self.set_setting("speed_source", speed_source)
    
    def get_fps_max_limit(self):
        """Get current FPS max limit"""
        return self.get_setting("fps_max_limit", "FPS40")
    
    def set_fps_max_limit(self, fps_max_limit):
        """Set current FPS max limit"""
        return self.set_setting("fps_max_limit", fps_max_limit)
    
    def get_launch_at_startup(self):
        """Get launch at startup setting"""
        return self.get_setting("launch_at_startup", False)
    
    def set_launch_at_startup(self, launch_at_startup):
        """Set launch at startup setting"""
        return self.set_setting("launch_at_startup", launch_at_startup)
    
    def get_language(self):
        """Get current language"""
        return self.get_setting("language", "English")
    
    def set_language(self, language):
        """Set current language"""
        return self.set_setting("language", language)
    
    def get_floating_ball_enabled(self):
        """Get floating ball enabled status"""
        return self.get_setting("floating_ball_enabled", True)
    
    def set_floating_ball_enabled(self, enabled):
        """Set floating ball enabled status"""
        return self.set_setting("floating_ball_enabled", enabled)
    
    def get_floating_ball_opacity(self):
        """Get floating ball opacity"""
        return self.get_setting("floating_ball_opacity", 0.8)
    
    def set_floating_ball_opacity(self, opacity):
        """Set floating ball opacity"""
        return self.set_setting("floating_ball_opacity", opacity)
    
    def get_floating_ball_size(self):
        """Get floating ball size"""
        return self.get_setting("floating_ball_size", 96)
    
    def set_floating_ball_size(self, size):
        """Set floating ball size"""
        return self.set_setting("floating_ball_size", size)
    
    def get_current_mode(self):
        """Get current mode"""
        return self.get_setting("current_mode", "Normal")
    
    def set_current_mode(self, mode):
        """Set current mode"""
        return self.set_setting("current_mode", mode)

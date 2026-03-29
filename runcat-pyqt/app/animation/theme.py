#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Theme management module
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette


class Theme:
    """Theme class"""
    
    SYSTEM = "System"
    LIGHT = "Light"
    DARK = "Dark"
    
    def __init__(self, theme_name):
        self.theme_name = theme_name
    
    def get_color(self):
        """Get theme color"""
        if self.theme_name == self.DARK:
            return QColor(255, 255, 255)  # White for dark theme
        else:
            return QColor(0, 0, 0)  # Black for light theme
    
    def is_dark(self):
        """Check if theme is dark"""
        return self.theme_name == self.DARK
    
    def is_system_dark(self):
        """Check if system is in dark mode"""
        if sys.platform == 'darwin':  # macOS
            import subprocess
            try:
                result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                      capture_output=True, text=True)
                return result.stdout.strip() == 'Dark'
            except:
                return False
        elif sys.platform == 'win32':  # Windows
            try:
                import ctypes
                # For Windows 10/11, use Registry to check theme
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize') as key:
                    value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                    return value == 0
            except:
                try:
                    # Fallback method
                    return ctypes.windll.user32.GetWindowTheme() != 0
                except:
                    return False
        return False
    
    def apply(self, app):
        """Apply theme to application"""
        # Determine if we should use dark theme
        use_dark = False
        if self.theme_name == self.DARK:
            use_dark = True
        elif self.theme_name == self.SYSTEM:
            use_dark = self.is_system_dark()
        
        if use_dark:
            # Dark theme (adjusted for better visibility of black icons)
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(60, 60, 60))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(40, 40, 40))
            palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(70, 70, 70))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            # For checkboxes and radio buttons in dark mode
            palette.setColor(QPalette.Active, QPalette.Button, QColor(42, 130, 218))
            palette.setColor(QPalette.Active, QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.Active, QPalette.HighlightedText, Qt.white)
            app.setPalette(palette)
        else:
            # Light theme
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
            app.setPalette(palette)


class ThemeManager:
    """Theme manager"""
    
    def __init__(self):
        self.current_theme = Theme(Theme.SYSTEM)
    
    def set_theme(self, theme_name):
        """Set current theme"""
        self.current_theme = Theme(theme_name)
    
    def get_theme(self):
        """Get current theme"""
        return self.current_theme
    
    def get_theme_names(self):
        """Get all theme names"""
        return [Theme.SYSTEM, Theme.LIGHT, Theme.DARK]
    
    def apply_theme(self, app):
        """Apply theme to application"""
        self.current_theme.apply(app)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for system tray submenu functionality
"""

import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class TestTraySubMenuApp:
    """Test tray submenu application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Create system tray icon
        self.tray = QSystemTrayIcon()
        
        # Create a simple icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.red)
        self.tray.setIcon(QIcon(pixmap))
        self.tray.setToolTip("Test Tray Submenu")
        
        # Create main menu
        self.menu = QMenu()
        
        # Create runner submenu
        self.runner_menu = QMenu("Runner")
        
        # Add runner actions
        runners = ["Cat", "Parrot", "Horse"]
        for runner in runners:
            action = QAction(runner)
            action.setCheckable(True)
            action.setChecked(runner == "Cat")
            action.triggered.connect(lambda checked, name=runner: self.on_runner_selected(name))
            self.runner_menu.addAction(action)
        
        # Add runner menu to main menu
        self.menu.addMenu(self.runner_menu)
        
        # Add exit action
        exit_action = QAction("Exit")
        exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(exit_action)
        
        # Set context menu
        self.tray.setContextMenu(self.menu)
        
        # Show tray icon
        self.tray.show()
        
        print("Test tray app started. Check system tray.")
        print(f"Main menu has {len(self.menu.actions())} actions")
        print(f"Runner menu has {len(self.runner_menu.actions())} actions")
    
    def on_runner_selected(self, runner_name):
        """Handle runner selection"""
        print(f"Runner selected: {runner_name}")
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = TestTraySubMenuApp()
    app.run()

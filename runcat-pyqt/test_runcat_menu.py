#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for RunCat365 menu functionality
"""

import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class TestRunCatMenu:
    """Test RunCat365 menu functionality"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Create system tray icon
        self.tray = QSystemTrayIcon()
        
        # Create a simple icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.red)
        self.tray.setIcon(QIcon(pixmap))
        self.tray.setToolTip("RunCat365")
        
        # Create main menu
        self.menu = QMenu()
        
        # Setup menu
        self._setup_menu()
        
        # Set context menu
        self.tray.setContextMenu(self.menu)
        
        # Show tray icon
        self.tray.show()
        
        print("RunCat365 menu test started. Check system tray.")
        print(f"Main menu has {len(self.menu.actions())} actions")
    
    def _setup_menu(self):
        """Setup context menu"""
        # Clear existing menu
        self.menu.clear()
        
        # Runner selection - create runner menu directly
        self.runner_menu = QMenu("Runner")
        
        # Add built-in runners
        runners = ["Cat", "Parrot", "Horse"]
        
        # Add actions one by one
        for runner_name in runners:
            action = QAction(runner_name)
            action.setCheckable(True)
            action.setChecked(runner_name == "Cat")
            action.triggered.connect(lambda checked, name=runner_name: self._select_runner(name))
            self.runner_menu.addAction(action)
        
        # Add runner menu to main menu
        self.menu.addMenu(self.runner_menu)
        
        print(f"Runner menu has {len(self.runner_menu.actions())} actions")
        
        # Exit
        exit_action = QAction("Exit")
        exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(exit_action)
    

    
    def _select_runner(self, runner_name):
        """Select runner"""
        print(f"Runner selected: {runner_name}")
        # Update check state
        for action in self.runner_menu.actions():
            action.setChecked(action.text() == runner_name)
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = TestRunCatMenu()
    app.run()

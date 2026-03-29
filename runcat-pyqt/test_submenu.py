#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for submenu functionality
"""

import sys
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QMainWindow, QPushButton


class TestSubMenuApp:
    """Test submenu application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle("Test Submenu")
        self.window.setGeometry(100, 100, 400, 300)
        
        # Create a button to show menu
        button = QPushButton("Show Menu", self.window)
        button.setGeometry(150, 100, 100, 50)
        button.clicked.connect(self.show_menu)
        
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
        
        print(f"Main menu has {len(self.menu.actions())} actions")
        print(f"Runner menu has {len(self.runner_menu.actions())} actions")
        
        self.window.show()
    
    def show_menu(self):
        """Show the menu"""
        print("Showing menu...")
        self.menu.exec_(self.window.mapToGlobal(self.window.rect().center()))
    
    def on_runner_selected(self, runner_name):
        """Handle runner selection"""
        print(f"Runner selected: {runner_name}")
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = TestSubMenuApp()
    app.run()

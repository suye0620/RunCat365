#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Minimal test script for system tray with submenu
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


def main():
    """Main function"""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Create system tray icon
    tray = QSystemTrayIcon()
    
    # Create a simple icon
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.red)
    tray.setIcon(QIcon(pixmap))
    tray.setToolTip("Test Tray")
    
    # Create main menu
    menu = QMenu()
    
    # Create runner submenu
    runner_menu = QMenu("Runner")
    
    # Add runner actions
    runners = ["Cat", "Parrot", "Horse"]
    
    # Create actions list
    actions = []
    for runner_name in runners:
        action = QAction(runner_name)
        action.setCheckable(True)
        action.setChecked(runner_name == "Cat")
        actions.append(action)
    
    # Add all actions at once
    runner_menu.addActions(actions)
    
    # Add runner menu to main menu
    menu.addMenu(runner_menu)
    
    # Add exit action
    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)
    
    # Set context menu
    tray.setContextMenu(menu)
    
    # Show tray icon
    tray.show()
    
    print("System tray icon created. Check system tray.")
    print(f"Main menu has {len(menu.actions())} actions")
    print(f"Runner menu has {len(runner_menu.actions())} actions")
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

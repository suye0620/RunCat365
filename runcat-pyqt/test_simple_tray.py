#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple test script for system tray with submenu
"""

import sys
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
    
    # Add actions one by one
    action1 = QAction("Cat")
    action1.setCheckable(True)
    action1.setChecked(True)
    runner_menu.addAction(action1)
    
    action2 = QAction("Parrot")
    action2.setCheckable(True)
    action2.setChecked(False)
    runner_menu.addAction(action2)
    
    action3 = QAction("Horse")
    action3.setCheckable(True)
    action3.setChecked(False)
    runner_menu.addAction(action3)
    
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

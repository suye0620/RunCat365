#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for system tray menu click events
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class TestMenuApp:
    """Test menu application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Create system tray icon
        self.tray = QSystemTrayIcon()
        
        # Create a simple icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.red)
        self.tray.setIcon(QIcon(pixmap))
        self.tray.setToolTip("Test Menu App")
        
        # Create context menu
        self.menu = QMenu()
        
        # Test action 1
        action1 = QAction("Test Action 1")
        action1.triggered.connect(lambda: self.on_action_clicked("Action 1"))
        self.menu.addAction(action1)
        
        # Test action 2
        action2 = QAction("Test Action 2")
        action2.triggered.connect(lambda: self.on_action_clicked("Action 2"))
        self.menu.addAction(action2)
        
        # Exit action
        exit_action = QAction("Exit")
        exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(exit_action)
        
        # Add tray icon clicked event
        self.tray.activated.connect(self.on_tray_activated)
        
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        
        print("Test menu app started. Check system tray.")
        print(f"System tray available: {QSystemTrayIcon.isSystemTrayAvailable()}")
        print(f"Tray icon visible: {self.tray.isVisible()}")
    
    def on_action_clicked(self, action_name):
        """Handle action clicked"""
        print(f"{action_name} clicked!")
    
    def on_tray_activated(self, reason):
        """Handle tray activated"""
        print(f"Tray activated with reason: {reason}")
        if reason == QSystemTrayIcon.Trigger:
            print("Tray icon clicked")
        elif reason == QSystemTrayIcon.Context:
            print("Context menu requested")
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = TestMenuApp()
    app.run()

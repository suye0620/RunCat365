#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for system tray menu
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class TestTrayApp:
    """Test tray application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Create system tray icon
        self.tray = QSystemTrayIcon()
        
        # Create a simple icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.red)
        self.tray.setIcon(QIcon(pixmap))
        self.tray.setToolTip("Test Tray App")
        
        # Create context menu
        self.menu = QMenu()
        
        # Test action
        test_action = QAction("Test Action")
        test_action.triggered.connect(self.on_test_action)
        self.menu.addAction(test_action)
        
        # Exit action
        exit_action = QAction("Exit")
        exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(exit_action)
        
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        
        print("Test tray app started. Check system tray.")
    
    def on_test_action(self):
        """Handle test action"""
        print("Test action clicked!")
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = TestTrayApp()
    app.run()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for debugging
"""

import sys
import os

print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Python path:", sys.path)

# Test PyQt import
try:
    from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
    from PyQt5.QtGui import QIcon, QPixmap
    from PyQt5.QtCore import Qt
    print("PyQt5 imported successfully")
except Exception as e:
    print("Error importing PyQt5:", e)

print("Test completed")

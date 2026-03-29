#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to find menu bug
"""

import sys
from PyQt5.QtWidgets import QApplication, QMenu, QAction


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Create main menu
    menu = QMenu()
    
    # Create runner submenu
    runner_menu = QMenu("Runner")
    
    # Add runner actions
    runners = ["Cat", "Parrot", "Horse"]
    
    print(f"Adding {len(runners)} runners")
    
    # Create actions list
    actions = []
    for runner in runners:
        action = QAction(runner)
        action.setCheckable(True)
        action.setChecked(runner == "Cat")
        print(f"Created action: {action.text()}")
        actions.append(action)
    
    # Add all actions at once
    runner_menu.addActions(actions)
    print(f"Added {len(actions)} actions")
    
    # Add runner menu to main menu
    menu.addMenu(runner_menu)
    
    print(f"Runner menu actions: {runner_menu.actions()}")
    print(f"Runner menu action count: {len(runner_menu.actions())}")
    
    # Check each action
    for i, action in enumerate(runner_menu.actions()):
        print(f"Action {i}: {action.text()}")
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

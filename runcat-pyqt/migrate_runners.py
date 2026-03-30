#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Migration script to convert old runner file structure to new directory structure
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from animation.custom_runner import CustomRunnerManager

def main():
    print("Starting migration of custom runners...")
    manager = CustomRunnerManager()
    migrated = manager.migrate_old_files()
    print(f"Migration completed. Migrated {migrated} runners.")
    
    # Check the result
    manager.load_custom_runners()
    runners = manager.get_custom_runner_names()
    print(f"\nLoaded {len(runners)} custom runners:")
    for name in runners:
        runner = manager.get_custom_runner(name)
        print(f"  - {name}: {runner.get_frame_count()} frames")

if __name__ == "__main__":
    main()

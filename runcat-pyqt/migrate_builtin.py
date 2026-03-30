#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Migrate built-in runners to new directory structure
"""

import os
import shutil

resources_dir = os.path.join(os.path.dirname(__file__), 'resources', 'runners')

built_in_runners = ['cat', 'horse', 'parrot']

for runner_name in built_in_runners:
    runner_folder = os.path.join(resources_dir, runner_name)
    
    # Create 32x32 directory
    size_folder = os.path.join(runner_folder, '32x32')
    os.makedirs(size_folder, exist_ok=True)
    
    # Move all existing files to 32x32, rename to frame_i.png
    for filename in os.listdir(runner_folder):
        if filename == '32x32':
            continue
        if not filename.endswith('.png'):
            continue
        
        # Parse filename: name_i.png
        parts = filename.split('.')[0].split('_')
        if len(parts) == 2:
            try:
                frame_idx = int(parts[1])
                old_path = os.path.join(runner_folder, filename)
                new_path = os.path.join(size_folder, f'frame_{frame_idx}.png')
                if not os.path.exists(new_path):
                    shutil.move(old_path, new_path)
                    print(f"Migrated {runner_name}: {filename} -> 32x32/frame_{frame_idx}.png")
            except ValueError:
                continue

print("\nMigration completed!")

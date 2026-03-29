#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Check if RunCat365 is running
"""

import os
import psutil


def check_process():
    """Check if RunCat365 is running"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'python' in cmdline[0] and 'app\main.py' in ' '.join(cmdline):
                print(f"RunCat365 is running with PID: {proc.info['pid']}")
                print(f"Command line: {' '.join(cmdline)}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("RunCat365 is not running")
    return False


if __name__ == "__main__":
    check_process()

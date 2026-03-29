#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CPU monitoring module
"""

import psutil


class CPUMonitor:
    """CPU usage monitor"""
    
    def __init__(self):
        self.cpu_percent = 0.0
    
    def update(self):
        """Update CPU usage data"""
        try:
            self.cpu_percent = psutil.cpu_percent(interval=0.1)
        except Exception:
            self.cpu_percent = 0.0
    
    def get_usage(self):
        """Get current CPU usage"""
        return self.cpu_percent
    
    def get_description(self):
        """Get CPU usage description"""
        return f"CPU: {self.cpu_percent:.1f}%"
    
    def generate_indicator(self):
        """Generate system tray indicator"""
        return [f"CPU: {self.cpu_percent:.1f}%"]

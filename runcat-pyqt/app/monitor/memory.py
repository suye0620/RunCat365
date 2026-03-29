#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Memory monitoring module
"""

import psutil


class MemoryMonitor:
    """Memory usage monitor"""
    
    def __init__(self):
        self.memory_percent = 0.0
        self.total_memory = 0
        self.used_memory = 0
    
    def update(self):
        """Update memory usage data"""
        try:
            memory = psutil.virtual_memory()
            self.memory_percent = memory.percent
            self.total_memory = memory.total
            self.used_memory = memory.used
        except Exception:
            self.memory_percent = 0.0
            self.total_memory = 0
            self.used_memory = 0
    
    def get_usage(self):
        """Get current memory usage"""
        return self.memory_percent
    
    def get_description(self):
        """Get memory usage description"""
        return f"Memory: {self.memory_percent:.1f}%"
    
    def generate_indicator(self):
        """Generate system tray indicator"""
        return [f"Memory: {self.memory_percent:.1f}%"]
    
    def get_memory_load(self):
        """Get memory load for animation speed"""
        return self.memory_percent

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Network monitoring module
"""

import psutil


class NetworkMonitor:
    """Network usage monitor"""
    
    def __init__(self):
        self.bytes_sent = 0
        self.bytes_recv = 0
        self.prev_bytes_sent = 0
        self.prev_bytes_recv = 0
        self.speed_sent = 0
        self.speed_recv = 0
    
    def update(self):
        """Update network usage data"""
        try:
            net_io = psutil.net_io_counters()
            self.bytes_sent = net_io.bytes_sent
            self.bytes_recv = net_io.bytes_recv
            
            # Calculate speed (bytes per second)
            if self.prev_bytes_sent > 0:
                self.speed_sent = self.bytes_sent - self.prev_bytes_sent
            if self.prev_bytes_recv > 0:
                self.speed_recv = self.bytes_recv - self.prev_bytes_recv
            
            self.prev_bytes_sent = self.bytes_sent
            self.prev_bytes_recv = self.bytes_recv
        except Exception:
            pass
    
    def get_speed_sent(self):
        """Get current upload speed"""
        return self.speed_sent
    
    def get_speed_recv(self):
        """Get current download speed"""
        return self.speed_recv
    
    def get_usage(self):
        """Get network usage for animation speed"""
        # Calculate network usage as a percentage of max speed
        # For simplicity, we'll use a scaled value based on current speed
        # This is a placeholder - in a real implementation, you would calculate based on network interface speed
        max_speed = 100 * 1024 * 1024  # 100 Mbps
        total_speed = self.speed_sent + self.speed_recv
        usage = (total_speed / max_speed) * 100
        return min(usage, 100)  # Cap at 100%
    
    def get_description(self):
        """Get network usage description"""
        return f"Network: {self._format_bytes(self.speed_sent)}/s ↑ {self._format_bytes(self.speed_recv)}/s ↓"
    
    def generate_indicator(self):
        """Generate system tray indicator"""
        return [
            f"Sent: {self._format_bytes(self.speed_sent)}/s",
            f"Received: {self._format_bytes(self.speed_recv)}/s"
        ]
    
    def _format_bytes(self, bytes_value):
        """Format bytes to human-readable string"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"

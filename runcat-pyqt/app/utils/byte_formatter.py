#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Byte formatter utility
"""


def format_bytes(bytes_value):
    """Format bytes to human-readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"

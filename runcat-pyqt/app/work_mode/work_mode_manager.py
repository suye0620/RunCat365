#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Work mode and pomodoro timer manager
"""

import os
import json
import random
from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class WorkModeManager(QObject):
    """Work mode and pomodoro timer manager"""

    pomodoro_tick = pyqtSignal()
    pomodoro_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.config_file = os.path.join(os.path.dirname(__file__), "..", "..", "work_mode_config.json")
        self.config = self._load_config()

        self._is_working = False
        self._remaining_seconds = 0
        self._timer = None

    def _load_config(self):
        """Load configuration from file"""
        default_config = {
            "current_mode": "Normal",
            "pomodoro": {
                "work_duration": 1800,
                "is_working": False,
                "remaining_seconds": 0
            }
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return default_config
        return default_config

    def _save_config(self):
        """Save configuration to file"""
        try:
            self.config["pomodoro"]["is_working"] = self._is_working
            self.config["pomodoro"]["remaining_seconds"] = self._remaining_seconds
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_current_mode(self):
        """Get current mode"""
        return self.config.get("current_mode", "Normal")

    def set_current_mode(self, mode):
        """Set current mode"""
        self.config["current_mode"] = mode
        return self._save_config()

    def is_work_mode(self):
        """Check if current mode is Work"""
        return self.get_current_mode() == "Work"

    def get_work_duration(self):
        """Get work duration in seconds"""
        return self.config["pomodoro"].get("work_duration", 1800)
    
    def has_any_configuration(self):
        """Check if there is any group configured"""
        from .runner_metadata import RunnerMetadataManager
        metadata_manager = RunnerMetadataManager()
        # Check if any group has been created
        groups = metadata_manager.get_all_groups()
        return len(groups) > 0
    
    def get_random_runner_by_action_type(self, action_type):
        """Get a random runner by action type from all groups"""
        from .runner_metadata import RunnerMetadataManager
        metadata_manager = RunnerMetadataManager()
        
        candidates = []
        all_metadata = metadata_manager.get_all_runners_metadata()
        
        for runner_name, metadata in all_metadata.items():
            if metadata.get("action_type") == action_type and metadata.get("group_id") is not None:
                candidates.append(runner_name)
        
        if not candidates:
            return None
        
        return {
            "runner_name": random.choice(candidates),
            "is_custom": metadata_manager.get_runner_metadata(candidates[0]).get("is_custom", False)
        }

    def is_working(self):
        """Check if currently in working state"""
        return self._is_working

    def get_remaining_seconds(self):
        """Get remaining seconds in current pomodoro"""
        return self._remaining_seconds

    def get_remaining_formatted(self):
        """Get remaining time formatted as MM:SS"""
        remaining = self._remaining_seconds
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{minutes}:{seconds:02d}"

    def start_pomodoro(self):
        """Start a new pomodoro"""
        self._is_working = True
        self._remaining_seconds = self.get_work_duration()

        if not self._timer:
            self._timer = QTimer(self)
            self._timer.timeout.connect(self._on_tick)
            self._timer.start(1000)
        else:
            self._timer.start()

        self._save_config()

    def pause_pomodoro(self):
        """Pause current pomodoro"""
        if self._timer and self._timer.isActive():
            self._timer.stop()
        self._save_config()

    def resume_pomodoro(self):
        """Resume paused pomodoro"""
        if self._timer:
            self._timer.start(1000)
        else:
            self._timer = QTimer(self)
            self._timer.timeout.connect(self._on_tick)
            self._timer.start(1000)
        self._save_config()

    def is_paused(self):
        """Check if pomodoro is paused"""
        if self._is_working and self._timer and not self._timer.isActive():
            return True
        return False

    def stop_pomodoro(self):
        """Stop current pomodoro"""
        self._is_working = False
        self._remaining_seconds = 0

        if self._timer:
            self._timer.stop()

        self._save_config()

    def _on_tick(self):
        """Called every second"""
        if self._is_working and self._remaining_seconds > 0:
            self._remaining_seconds -= 1
            self.pomodoro_tick.emit()

            if self._remaining_seconds <= 0:
                self._is_working = False
                self._timer.stop()
                self._save_config()
                self.pomodoro_finished.emit()

    def resume_from_save(self):
        """Resume state from saved configuration"""
        pomo = self.config.get("pomodoro", {})
        self._is_working = pomo.get("is_working", False)
        self._remaining_seconds = pomo.get("remaining_seconds", 0)

        if self._is_working and self._remaining_seconds > 0:
            if not self._timer:
                self._timer = QTimer(self)
                self._timer.timeout.connect(self._on_tick)
            self._timer.start(1000)

    def show_system_notification(self, title, message):
        """Show system native notification"""
        import platform
        system = platform.system()

        if system == "Windows":
            self._show_windows_notification(title, message)
        elif system == "Darwin":
            self._show_macos_notification(title, message)

    def _show_windows_notification(self, title, message):
        """Show notification on Windows using winrt to display in Action Center"""
        try:
            # Use Windows Runtime (WinRT) for modern notifications that show in Action Center
            import winrt
            from winrt.windows.ui.notifications import ToastNotificationManager, ToastNotification
            from winrt.windows.data.xml.dom import XmlDocument

            # Create toast XML
            toast_xml = f"""
            <toast>
                <visual>
                    <binding template='ToastGeneric'>
                        <text>{title}</text>
                        <text>{message}</text>
                    </binding>
                </visual>
            </toast>
            """

            xml_doc = XmlDocument()
            xml_doc.load_xml(toast_xml)
            toast = ToastNotification(xml_doc)
            
            # Get toast notifier and show
            notifier = ToastNotificationManager.get_default().create_toast_notifier()
            notifier.show(toast)
        except ImportError:
            # If winrt is not available, fall back to simpler notification via MessageBox
            try:
                from ctypes import windll
                windll.user32.MessageBoxW(0, message.encode('utf-16'), title.encode('utf-16'), 0)
            except Exception:
                pass
        except Exception:
            pass

    def _show_macos_notification(self, title, message):
        """Show notification on macOS using pyobjc"""
        try:
            import Foundation
            import UserNotifications
            from PyObjCTools import AppHelper

            center = UserNotifications.UNUserNotificationCenter.currentNotificationCenter()

            content = UserNotifications.UNMutableNotificationContent()
            content.setTitle(title)
            content.setBody(message)
            content.setSound(UserNotifications.UNNotificationSound.defaultSound())

            trigger = UserNotifications.UNTimeIntervalNotificationTrigger.triggerWithTimeIntervalRepeats_(1, False)
            request = UserNotifications.UNNotificationRequest.requestWithIdentifierContentTrigger_("pomodoro_finished", content, trigger)

            center.addNotificationRequestWithCompletionHandler_(request, None)
        except Exception:
            pass

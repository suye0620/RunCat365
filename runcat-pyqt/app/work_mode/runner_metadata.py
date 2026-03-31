#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Runner metadata manager
Stores runner metadata including group, action type, and enabled modes
"""

import os
import json


class RunnerMetadataManager:
    """Manages metadata for all runners"""
    
    def __init__(self):
        self.metadata_file = os.path.join(os.path.dirname(__file__), "..", "..", "runner_metadata.json")
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        """Load metadata from file"""
        default_metadata = {
            "runners": {},
            "groups": []
        }
        
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return default_metadata
        return default_metadata
    
    def _save_metadata(self):
        """Save metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def get_runner_metadata(self, runner_name):
        """Get metadata for a specific runner"""
        return self.metadata["runners"].get(runner_name, {
            "enabled_modes": ["Normal"],  # Default to Normal only
            "group_id": None,
            "action_type": None,
            "is_custom": False
        })
    
    def set_runner_metadata(self, runner_name, metadata):
        """Set metadata for a specific runner"""
        self.metadata["runners"][runner_name] = metadata
        return self._save_metadata()
    
    def update_runner_group(self, runner_name, group_id):
        """Update runner's group assignment"""
        metadata = self.get_runner_metadata(runner_name)
        metadata["group_id"] = group_id
        self.metadata["runners"][runner_name] = metadata
        return self._save_metadata()
    
    def update_runner_action_type(self, runner_name, action_type):
        """Update runner's action type"""
        metadata = self.get_runner_metadata(runner_name)
        metadata["action_type"] = action_type
        self.metadata["runners"][runner_name] = metadata
        return self._save_metadata()
    
    def update_runner_enabled_modes(self, runner_name, enabled_modes):
        """Update runner's enabled modes"""
        metadata = self.get_runner_metadata(runner_name)
        metadata["enabled_modes"] = enabled_modes
        self.metadata["runners"][runner_name] = metadata
        return self._save_metadata()
    
    def get_runners_by_group(self, group_id):
        """Get all runners in a group"""
        runners = []
        for runner_name, metadata in self.metadata["runners"].items():
            if metadata.get("group_id") == group_id:
                runners.append({
                    "runner_name": runner_name,
                    "metadata": metadata
                })
        return runners
    
    def get_runners_by_action_type(self, group_id, action_type):
        """Get all runners in a group with specific action type"""
        runners = self.get_runners_by_group(group_id)
        return [r for r in runners if r["metadata"].get("action_type") == action_type]
    
    def get_all_runners_metadata(self):
        """Get all runners metadata"""
        return self.metadata["runners"]
    
    def remove_runner_metadata(self, runner_name):
        """Remove metadata for a runner"""
        if runner_name in self.metadata["runners"]:
            del self.metadata["runners"][runner_name]
            return self._save_metadata()
        return False
    
    def clear_runner_group(self, runner_name):
        """Clear runner's group assignment"""
        metadata = self.get_runner_metadata(runner_name)
        metadata["group_id"] = None
        metadata["action_type"] = None
        self.metadata["runners"][runner_name] = metadata
        return self._save_metadata()
    
    def get_all_groups(self):
        """Get all created groups"""
        return self.metadata.get("groups", [])
    
    def create_group(self, group_id):
        """Create a new empty group"""
        if "groups" not in self.metadata:
            self.metadata["groups"] = []
        if group_id not in self.metadata["groups"]:
            self.metadata["groups"].append(group_id)
            self._save_metadata()
    
    def delete_group(self, group_id):
        """Delete a group"""
        if "groups" in self.metadata and group_id in self.metadata["groups"]:
            self.metadata["groups"].remove(group_id)
            self._save_metadata()

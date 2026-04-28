# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
from datetime import datetime


class UpdateAgent:
    def generate_update(self, actions, alerts, device_states):
        # Create a structured update containing the current system state
        update = {
            # Timestamp of when the update was generated
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            # List of approved actions from the policy agent
            "actions": actions,

            # Any alerts triggered by the system
            "alerts": alerts,

            # Current status of all smart home devices
            "device_states": device_states,
        }

        # Return the update as a dictionary (machine-readable format)
        return update

    def format_message(self, update):
        # Convert the structured update into a human-readable message
        message = f"System update at {update['time']}:\n\n"

        # Add approved actions to the message
        message += "Approved actions:\n"
        for action in update["actions"]:
            message += f"- {action}\n"

        # Add device states to the message
        message += "\nDevice states:\n"
        for device, status in update["device_states"].items():
            message += f"- {device}: {status}\n"

        # Include alerts only if any exist
        if update["alerts"]:
            message += "\nAlerts:\n"
            for alert in update["alerts"]:
                message += f"- {alert}\n"

        # Return the final formatted message
        return message
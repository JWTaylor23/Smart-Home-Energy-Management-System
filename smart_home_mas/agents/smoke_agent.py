# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
class SmokeAgent:
    def __init__(self):
        # Initial state of the smoke alarm (default is OFF)
        self.status = "OFF"

    def act(self, actions):
        # Check if the policy agent has approved turning on the smoke alarm
        if "SMOKE_ALARM_ON" in actions:
            # Activate the smoke alarm if smoke is detected
            self.status = "ON"
        else:
            # Keep the smoke alarm off if no action is required
            self.status = "OFF"

        # Return the current status of the smoke alarm
        return self.status
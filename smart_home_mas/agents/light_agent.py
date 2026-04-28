# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""

class LightAgent:
    def __init__(self):
        # Initial state of the lighting system (default is OFF)
        self.status = "OFF"

    def act(self, actions):
        # Check if the policy agent has approved turning the lights on
        if "LIGHT_ON" in actions:
            self.status = "ON"

        # Check if the policy agent has approved turning the lights off
        elif "LIGHT_OFF" in actions:
            self.status = "OFF"

        # Return the current status of the lights
        return self.status
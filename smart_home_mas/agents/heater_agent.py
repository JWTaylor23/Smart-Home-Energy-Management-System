# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
class HeaterAgent:
    def __init__(self):
        # Initial state of the heater (default is OFF)
        self.status = "OFF"

    def act(self, actions):
        # Check if the policy agent has approved turning the heater on
        if "HEATER_ON" in actions:
            self.status = "ON"

        # Check if the policy agent has approved turning the heater off
        elif "HEATER_OFF" in actions:
            self.status = "OFF"

        # Return the current status of the heater
        return self.status
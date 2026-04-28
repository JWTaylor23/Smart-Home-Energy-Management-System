# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
class ACAgent:
    def __init__(self):
        # Initial state of the air conditioning unit (default is OFF)
        self.status = "OFF"

    def act(self, actions):
        # Check if the policy agent has approved turning the AC on
        if "AC_ON" in actions:
            self.status = "ON"

        # Check if the policy agent has approved turning the AC off
        elif "AC_OFF" in actions:
            self.status = "OFF"

        # Return the current status of the AC unit
        return self.status
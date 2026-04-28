# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
class FridgeAgent:
    def __init__(self):
        # Initial fridge state (assumed to be operating normally)
        self.status = "NORMAL"

    def act(self, actions):
        # Check if the policy agent has triggered a fridge safety alert
        if "FRIDGE_ALERT" in actions:
            # Set status to ALERT if temperature exceeds safe limits
            self.status = "ALERT"
        else:
            # Maintain NORMAL status if no issues are detected
            self.status = "NORMAL"

        # Return the current fridge status
        return self.status
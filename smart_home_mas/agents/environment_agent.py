# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""

class EnvironmentAgent:
    def read_environment(self, brightness, room_temp, fridge_temp, smoke):
        # Collect and structure environmental sensor data
        return {
            # Current ambient light level
            "brightness": brightness,

            # Current room temperature (°C)
            "room_temp": room_temp,

            # Current fridge temperature (°C)
            "fridge_temp": fridge_temp,

            # Smoke detection value (0 = safe, 1 = detected)
            "smoke": smoke,
        }
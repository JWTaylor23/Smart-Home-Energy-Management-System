# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
class PolicyAgent:
    def __init__(self):
        # Threshold values that define safe and optimal conditions
        self.min_room_temp = 18          # Minimum comfortable room temperature (°C)
        self.max_room_temp = 26          # Maximum comfortable room temperature (°C)
        self.min_brightness = 35         # Minimum brightness level before lights are needed
        self.max_fridge_temp = 5         # Maximum safe fridge temperature (°C)
        self.smoke_threshold = 1         # Smoke detection threshold

    def validate(self, environment_status):
        # Lists to store approved actions and system alerts
        approved_actions = []
        alerts = []

        # --- Smoke detection (highest priority safety rule) ---
        if environment_status["smoke"] >= self.smoke_threshold:
            approved_actions.append("SMOKE_ALARM_ON")
            alerts.append("Danger: Smoke detected. Alarm activated.")

        # --- Lighting control ---
        if environment_status["brightness"] < self.min_brightness:
            # Turn lights on if brightness is too low
            approved_actions.append("LIGHT_ON")
        else:
            # Turn lights off if brightness is sufficient
            approved_actions.append("LIGHT_OFF")

        # --- Temperature regulation (mutually exclusive actions) ---
        if environment_status["room_temp"] > self.max_room_temp:
            # Too hot → activate cooling and disable heating
            approved_actions.append("AC_ON")
            approved_actions.append("HEATER_OFF")
        elif environment_status["room_temp"] < self.min_room_temp:
            # Too cold → activate heating and disable cooling
            approved_actions.append("HEATER_ON")
            approved_actions.append("AC_OFF")
        else:
            # Within optimal range → turn both systems off
            approved_actions.append("AC_OFF")
            approved_actions.append("HEATER_OFF")

        # --- Fridge safety monitoring ---
        if environment_status["fridge_temp"] > self.max_fridge_temp:
            # Trigger alert if fridge temperature exceeds safe limit
            approved_actions.append("FRIDGE_ALERT")
            alerts.append("Warning: Fridge temperature is above safe level.")

        # Return validated actions and any generated alerts
        return approved_actions, alerts
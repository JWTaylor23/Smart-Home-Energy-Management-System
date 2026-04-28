# -*- coding: utf-8 -*-

"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
import pandas as pd


class EnergyAgent:
    def __init__(self, file_path):
        self.file_path = file_path

        if file_path.endswith(".csv"):
            self.data = pd.read_csv(file_path)
        else:
            self.data = pd.read_excel(file_path)

        # Remove any non-numeric columns if needed
        self.data = self.data.select_dtypes(include=["number"])

    def get_latest_energy_status(self):
        # Flatten all values into one series
        values = self.data.values.flatten()

        # Remove NaN values
        values = values[~pd.isnull(values)]

        latest_value = values[-1]
        average_value = values.mean()

        return {
            "timestamp": "Latest Entry",
            "total_kwh": round(float(latest_value), 4),
            "average_kwh": round(float(average_value), 4),
            "light_kwh": 0,
            "ac_kwh": 0,
            "heater_kwh": 0,
            "light_status": "N/A",
            "ac_status": "N/A",
            "heater_status": "N/A",
        }
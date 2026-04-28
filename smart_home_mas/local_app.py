# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""
import tkinter as tk
import os
import glob
from datetime import datetime

# Import all smart home agents
from agents.energy_agent import EnergyAgent
from agents.environment_agent import EnvironmentAgent
from agents.policy_agent import PolicyAgent
from agents.light_agent import LightAgent
from agents.ac_agent import ACAgent
from agents.heater_agent import HeaterAgent
from agents.fridge_agent import FridgeAgent
from agents.smoke_agent import SmokeAgent
from agents.llm_agent import LLMAgent


# Locate the project directory and data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")

# Search for either Excel or CSV data files inside the data folder
DATA_FILES = (
  glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
)

# Stop the program if no data file is found
if not DATA_FILES:
    raise FileNotFoundError("No .xlsx or .csv file found inside the data folder.")

# Use the first available data file
DATA_PATH = DATA_FILES[0]



class SmartHomeDashboard:
    def __init__(self, root):
        # Main dashboard window setup
        self.cost_label = None
        self.root = root
        self.root.title("Smart Home Energy Dashboard")
        self.root.geometry("520x760")
        self.root.configure(bg="white")

        # Core system agents
        self.energy_agent = EnergyAgent(DATA_PATH)
        self.environment_agent = EnvironmentAgent()
        self.policy_agent = PolicyAgent()

        # LLM is disabled here, so the system uses fallback/advisory logic
        self.llm_agent = LLMAgent(use_llm=False)

        # Device control agents
        self.light_agent = LightAgent()
        self.ac_agent = ACAgent()
        self.heater_agent = HeaterAgent()
        self.fridge_agent = FridgeAgent()
        self.smoke_agent = SmokeAgent()

        # Simulated sensor starting values
        self.brightness_value = 30
        self.room_temp_value = 22
        self.fridge_temp_value = 4
        self.smoke_value = 0

        # Build and start the live dashboard
        self.build_dashboard()
        self.update_dashboard()

    def section(self, title):
        # Creates a reusable labelled frame for each dashboard section
        frame = tk.LabelFrame(
            self.root,
            text=title,
            bg="white",
            fg="black",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=8,
            bd=1,
            relief="solid"
        )
        frame.pack(fill="x", padx=20, pady=4)
        return frame

    def add_label(self, parent, text, row, col):
        # Creates a reusable label inside a selected frame
        label = tk.Label(
            parent,
            text=text,
            bg="white",
            fg="black",
            anchor="w",
            font=("Arial", 9)
        )
        label.grid(row=row, column=col, sticky="w", padx=8, pady=5)
        return label

    def build_dashboard(self):
        # Main dashboard title
        title = tk.Label(
            self.root,
            text="SMART HOME ENERGY DASHBOARD",
            bg="white",
            fg="black",
            font=("Arial", 15, "bold")
        )
        title.pack(pady=12)

        # Energy information section
        energy_frame = self.section("")
        self.energy_usage_label = self.add_label(energy_frame, "", 0, 0)
        self.status_label = self.add_label(energy_frame, "", 0, 1)
        self.cost_label = self.add_label(energy_frame, "", 1, 0)
        self.mode_label = self.add_label(energy_frame, "Mode: Auto", 1, 1)

        # Environmental readings section
        env_frame = self.section("ENVIRONMENT")
        self.room_temp_label = self.add_label(env_frame, "", 0, 0)
        self.brightness_label = self.add_label(env_frame, "", 0, 1)
        self.smoke_label = self.add_label(env_frame, "", 0, 2)
        self.fridge_temp_label = self.add_label(env_frame, "", 1, 0)
        self.time_label = self.add_label(env_frame, "", 1, 1)

        # Device status section
        device_frame = self.section("DEVICE STATUS")
        self.light_label = self.add_label(device_frame, "", 0, 0)
        self.light_mode_label = self.add_label(device_frame, "Mode: Auto", 0, 1)

        self.ac_label = self.add_label(device_frame, "", 1, 0)
        self.ac_mode_label = self.add_label(device_frame, "Mode: Auto", 1, 1)

        self.heater_label = self.add_label(device_frame, "", 2, 0)
        self.heater_mode_label = self.add_label(device_frame, "Mode: Auto", 2, 1)

        self.fridge_label = self.add_label(device_frame, "", 3, 0)
        self.fridge_mode_label = self.add_label(device_frame, "Mode: Auto", 3, 1)

        self.smoke_alarm_label = self.add_label(device_frame, "", 4, 0)
        self.smoke_monitor_label = self.add_label(device_frame, "Status: Monitoring", 4, 1)

        # LLM recommendation display section
        llm_frame = self.section("LLM RECOMMENDATION")
        self.llm_text = tk.Text(
            llm_frame,
            height=4,
            wrap="word",
            bg="white",
            fg="black",
            font=("Arial", 9),
            bd=0
        )
        self.llm_text.pack(fill="x")

        # Alerts and notifications section
        alert_frame = self.section("ALERTS / NOTIFICATIONS")
        self.alert_text = tk.Text(
            alert_frame,
            height=5,
            wrap="word",
            bg="white",
            fg="black",
            font=("Arial", 9),
            bd=0
        )
        self.alert_text.pack(fill="x")

        # Static action options shown on the interface
        actions_frame = self.section("ACTIONS")
        self.add_label(actions_frame, "View History", 0, 0)
        self.add_label(actions_frame, "Acknowledge Alert", 0, 1)
        self.add_label(actions_frame, "Manual Override", 0, 2)

    def simulate_sensor_changes(self):
        # Simulates changing brightness values
        self.brightness_value -= 1
        if self.brightness_value < 20:
            self.brightness_value = 45

        # Simulates changing room temperature values
        self.room_temp_value += 1
        if self.room_temp_value > 28:
            self.room_temp_value = 21

        # Keeps fridge temperature and smoke values stable
        self.fridge_temp_value = 4
        self.smoke_value = 0

    def update_dashboard(self):
        # Update simulated sensor readings
        self.simulate_sensor_changes()

        # Get latest household energy usage from the data file
        energy_status = self.energy_agent.get_latest_energy_status()

        # Read environmental conditions from simulated sensors
        environment_status = self.environment_agent.read_environment(
            brightness=self.brightness_value,
            room_temp=self.room_temp_value,
            fridge_temp=self.fridge_temp_value,
            smoke=self.smoke_value
        )

        # Policy agent validates actions before devices are controlled
        approved_actions, alerts = self.policy_agent.validate(environment_status)

        # Each device agent acts only on approved actions
        device_states = {
            "Light": self.light_agent.act(approved_actions),
            "AC Unit": self.ac_agent.act(approved_actions),
            "Heater": self.heater_agent.act(approved_actions),
            "Fridge": self.fridge_agent.act(approved_actions),
            "Smoke Alarm": self.smoke_agent.act(approved_actions),
        }

        # LLM/fallback agent generates an energy recommendation
        llm_recommendation = self.llm_agent.generate_recommendation(
            energy_status,
            environment_status
        )

        # Estimate energy cost using a fixed electricity rate
        cost = round(energy_status["total_kwh"] * 0.28, 2)

        # Convert raw sensor values into readable dashboard text
        brightness_text = "Low" if environment_status["brightness"] < 35 else "Normal"
        smoke_text = "Safe" if environment_status["smoke"] == 0 else "Detected"
        status_text = "Normal" if not alerts else "Alert"

        # Update energy and environment labels
        self.energy_usage_label.config(
            text=f"Current Energy Usage: {energy_status['total_kwh']} kWh"
        )
        self.status_label.config(text=f"Status: {status_text}")
        self.cost_label.config(text=f"Today’s Cost Estimate: £{cost}")
        self.room_temp_label.config(text=f"Room Temp: {environment_status['room_temp']}°C")
        self.brightness_label.config(text=f"Brightness: {brightness_text}")
        self.smoke_label.config(text=f"Smoke: {smoke_text}")
        self.fridge_temp_label.config(text=f"Fridge Temp: {environment_status['fridge_temp']}°C")
        self.time_label.config(text=f"Time: {datetime.now().strftime('%H:%M')}")

        # Update device status labels
        self.light_label.config(text=f"Lights      [{device_states['Light']}]")
        self.ac_label.config(text=f"AC Unit     [{device_states['AC Unit']}]")
        self.heater_label.config(text=f"Heater      [{device_states['Heater']}]")
        self.fridge_label.config(text=f"Fridge      [{device_states['Fridge']}]")
        self.smoke_alarm_label.config(text=f"Smoke Alarm [{device_states['Smoke Alarm']}]")

        # Refresh LLM recommendation text
        self.llm_text.delete("1.0", tk.END)
        self.llm_text.insert(tk.END, llm_recommendation)

        # Refresh alert text
        self.alert_text.delete("1.0", tk.END)

        if alerts:
            for alert in alerts:
                self.alert_text.insert(tk.END, f"• {alert}\n")
        else:
            self.alert_text.insert(tk.END, "• No critical alerts\n")

        # Add additional system notifications
        self.alert_text.insert(tk.END, "• Fridge operating within safe temperature range\n")

        if energy_status["total_kwh"] > energy_status["average_kwh"]:
            self.alert_text.insert(tk.END, "• Energy consumption slightly above average\n")
        else:
            self.alert_text.insert(tk.END, "• Energy consumption within normal range\n")

        # Automatically refresh the dashboard every 20 seconds
        self.root.after(20000, self.update_dashboard)

    def short_recommendation(self, actions):
        # Returns a short human-readable recommendation based on approved actions
        if "SMOKE_ALARM_ON" in actions:
            return "Activate smoke alarm immediately."
        if "AC_ON" in actions:
            return "Turn on AC to regulate high room temperature."
        if "HEATER_ON" in actions:
            return "Turn on heater to maintain comfort."
        if "LIGHT_ON" in actions:
            return "Turn lights on because brightness is low."
        return "Keep current settings to reduce unnecessary energy use."

    def short_explanation(self, environment, actions):
        # Explains why a specific device action was selected
        if "SMOKE_ALARM_ON" in actions:
            return "Smoke was detected, so the safety system activated the alarm."
        if "AC_ON" in actions:
            return "Room temperature is above the threshold, so cooling is required."
        if "HEATER_ON" in actions:
            return "Room temperature is below the threshold, so heating is required."
        if "LIGHT_ON" in actions:
            return "Natural light is low, so lighting is required automatically."
        return "All readings are within safe and efficient operating limits."


# Program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeDashboard(root)
    root.mainloop()
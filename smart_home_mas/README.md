# Smart Home Energy Management System

## Overview
This is a smart home energy management system built using a multi-agent architecture. The system monitors environmental conditions, evaluates energy usage, and controls devices such as lighting, heating, air conditioning, fridge monitoring, and smoke detection.

The system combines rule-based agents with an optional Large Language Model (LLM) to provide intelligent recommendations while maintaining safe and controlled device execution. The LLM is currently disabled by default (`use_llm=False`) due to processing speed and hardware limitations.

---

## Features
- Multi-agent system design
- Real-time dashboard using Tkinter
- Energy monitoring from CSV data
- Environmental sensing including temperature, brightness, smoke, and fridge temperature
- Automated device control for lights, AC, heater, fridge, and smoke alarm
- Policy-based validation for safety and efficiency
- Optional LLM-based recommendations with fallback mode

---

## System Architecture

### Agents
- **EnvironmentAgent** – Collects sensor data
- **EnergyAgent** – Processes energy consumption data
- **PolicyAgent** – Validates actions based on rules
- **Device Agents** – Execute approved actions:
  - LightAgent
  - ACAgent
  - HeaterAgent
  - FridgeAgent
  - SmokeAgent
- **LLMAgent** – Generates advisory recommendations
- **UpdateAgent** – Formats system updates

### Design Principle
The system separates:
- **Perception** – EnvironmentAgent
- **Decision-making** – PolicyAgent
- **Execution** – Device agents
- **Advisory intelligence** – LLMAgent

This ensures safe and modular operation. The LLM operates as an advisory layer rather than a direct control mechanism, ensuring all actions are validated through deterministic policy rules for safety and reliability.

---

## Installation

### Requirements
- Python 3.9+

### Install dependencies
```bash
pip install pandas transformers torch
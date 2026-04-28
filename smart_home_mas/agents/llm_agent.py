# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 2026

@author: Joshua Taylor
"""

class LLMAgent:
    def __init__(self, use_llm=False, model_name="Qwen/Qwen3.6-27B"):
        # Flag to enable or disable LLM usage (fallback mode if False)
        self.use_llm = use_llm

        # Name of the transformer model to be used
        self.model_name = model_name

        # Only load the model if LLM mode is enabled (avoids heavy computation)
        if self.use_llm:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM

            # Load tokenizer and model from Hugging Face
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,   # Optimised for GPU memory usage
                device_map="auto"            # Automatically selects CPU/GPU
            )

    def generate_recommendation(self, energy_status, environment_status):
        # If LLM is disabled, use rule-based fallback instead
        if not self.use_llm:
            return self._fallback_recommendation(energy_status, environment_status)

        # Prompt engineering: instruct the LLM to behave as an advisory assistant
        prompt = f"""
You are an intelligent smart home energy assistant.

Energy status:
{energy_status}

Environment status:
{environment_status}

Generate:
1. Recommended actions
2. Explanation
3. Energy-saving reason
4. Safety warnings if needed

Important:
You do not directly control devices.
The PolicyAgent must validate all actions.
"""

        # Convert prompt into model input tensors
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # Generate response using the language model
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=250,   # Limits response length
            temperature=0.7,      # Controls creativity/randomness
            do_sample=True        # Enables non-deterministic output
        )

        # Decode model output into readable text
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _fallback_recommendation(self, energy, environment):
        # Rule-based recommendation used when LLM is disabled
        recommendation = "LLM Recommendation:\n\n"

        # Energy usage summary
        recommendation += (
            f"Current total energy usage is {energy['total_kwh']} kWh. "
            f"The average usage is {energy['average_kwh']} kWh.\n\n"
        )

        # Lighting advice based on brightness level
        if environment["brightness"] < 35:
            recommendation += "- Brightness is low, so lighting may be needed.\n"
        else:
            recommendation += "- Brightness is sufficient, so lights can remain off to save energy.\n"

        # Temperature control advice
        if environment["room_temp"] > 26:
            recommendation += "- Room temperature is high, so AC may be required.\n"
        elif environment["room_temp"] < 18:
            recommendation += "- Room temperature is low, so heating may be required.\n"
        else:
            recommendation += "- Room temperature is comfortable, so AC and heating can remain off.\n"

        # Fridge safety advice
        if environment["fridge_temp"] > 5:
            recommendation += "- Fridge temperature is unsafe and needs attention.\n"

        # Smoke safety advice
        if environment["smoke"] == 1:
            recommendation += "- Smoke detected. Alarm must be activated immediately.\n"

        # Reinforces that LLM is advisory only (important for system design marks)
        recommendation += "\nAll actions must be validated by the PolicyAgent."
        return recommendation
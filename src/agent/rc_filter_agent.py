# RC Filter Agent - Uses QwQ-32B model to design RC bandpass filters
# This agent connects to DashScope API to generate design parameters for the filter

from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv
import math

class RCFilterAgent:
    def __init__(self, api_key=None):
        """
        Initialize the RC filter design agent with an API key for QwQ-32B.
        
        Args:
            api_key (str): API key for DashScope compatible with OpenAI interface
        """
        load_dotenv()
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as DASHSCOPE_API_KEY environment variable")
        
        # Initialize OpenAI client with DashScope compatible endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
    
    def design_bandpass_filter(self, center_freq, bandwidth):
        """
        Design an RC bandpass filter using QwQ-32B to calculate component values.
        
        Args:
            center_freq (float): Target center frequency in Hz
            bandwidth (float): Target bandwidth in Hz
            
        Returns:
            dict: Component values and design parameters
        """
        prompt = f"""
        Design a passive RC bandpass filter with the following specifications:
        - Center frequency: {center_freq} Hz
        - Bandwidth: {bandwidth} Hz
        
        Please calculate the optimal component values (resistors in ohms and capacitors in farads).
        Provide the exact mathematical calculations and formulas used to determine these values.
        Return only the final component values in a valid JSON format with keys: R1, R2, C1, C2, etc.
        """
        
        try:
            # Create chat completion request
            completion = self.client.chat.completions.create(
                model="qwq-32b",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=True,  # QwQ model only supports streaming output
            )
            
            reasoning_content = ""
            answer_content = ""
            is_answering = False
            
            for chunk in completion:
                if not chunk.choices:
                    continue
                    
                delta = chunk.choices[0].delta
                
                # Collect reasoning content
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    reasoning_content += delta.reasoning_content
                    print(delta.reasoning_content, end="")
                else:
                    # Collect answer content
                    if delta.content:
                        answer_content += delta.content
                        print(delta.content, end="")
            
            print("Design reasoning process:")
            # print(reasoning_content)
            
            # Extract JSON from the answer
            # Look for JSON pattern in the response
            json_match = re.search(r'```(?:json)?\s*({[\s\S]*?})\s*```', answer_content)
            if json_match:
                json_str = json_match.group(1)
                component_values = json.loads(json_str)
                return component_values
            
            # Try direct JSON parsing if no code block found
            try:
                component_values = json.loads(answer_content.strip())
                return component_values
            except:
                pass
                
            # Extract key-value pairs if JSON parsing fails
            component_values = {}
            patterns = [
                r'R1\s*[=:]\s*([\d.e+-]+)', 
                r'R2\s*[=:]\s*([\d.e+-]+)',
                r'C1\s*[=:]\s*([\d.e+-]+)',
                r'C2\s*[=:]\s*([\d.e+-]+)'
            ]
            
            for i, pattern in enumerate(patterns):
                match = re.search(pattern, answer_content)
                if match:
                    key = f"R{i//2+1}" if i < 2 else f"C{i-1}"
                    component_values[key] = float(match.group(1))
            
            if component_values:
                return component_values
            else:
                print("Failed to parse component values from LLM response")
                print(f"Raw response: {answer_content}")
                return self._manual_design_calculation(center_freq, bandwidth)
                
        except Exception as e:
            print(f"Error calling QwQ-32B API: {e}")
            # Fallback to manual calculation
            return self._manual_design_calculation(center_freq, bandwidth)
    
    def _manual_design_calculation(self, center_freq, bandwidth):
        """
        Fallback method to calculate component values if LLM fails.
        
        Args:
            center_freq (float): Target center frequency in Hz
            bandwidth (float): Target bandwidth in Hz
            
        Returns:
            dict: Component values
        """
        # For an RC bandpass filter:
        # We can use a high-pass RC followed by a low-pass RC
        # Center frequency: f_c = 1/(2π√(R1*R2*C1*C2))
        # Bandwidth: BW = f_h - f_l
        
        # Starting with standard values
        C1 = 0.1e-6  # 0.1 μF
        C2 = 0.1e-6  # 0.1 μF
        
        # Calculate R1 and R2 for desired center_freq and bandwidth
        
        # For simplicity, let's make R1 = R2 = R
        # Then f_c = 1/(2πRC)
        R = 1 / (2 * math.pi * center_freq * math.sqrt(C1 * C2))
        
        # Adjust values to get desired bandwidth
        Q_factor = center_freq / bandwidth
        R1 = R
        R2 = R * Q_factor
        
        return {
            "R1": R1,
            "R2": R2,
            "C1": C1, 
            "C2": C2
        }
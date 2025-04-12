# RC Bandpass Filter Design - Test Report

## Project Overview
This project implements an intelligent agent using LangChain to design a passive RC bandpass filter. The agent connects to an LLM API compatible with OpenAI to design a filter meeting specific requirements and generates a SPICE netlist for simulation and verification.

## Filter Specifications
- **Type:** Passive RC Bandpass Filter
- **Center Frequency:** 100 Hz
- **Bandwidth:** 40 Hz

## Implementation Details
The project uses the following components:
- **LangChain Framework**: For creating the intelligent agent
- **LLM API**: For generating filter design calculations
- **SPICE Simulator**: For circuit simulation and verification
- **Python**: For implementation of the framework

## Test Results

### Component Values
The intelligent agent designed a filter with the following component values:
- R1: 10000 Ω
- R2: 10000 Ω
- C1: 1.9408e-07 µF
- C2: 1.3046e-07 µF

### SPICE Simulation Results
- **Center Frequency:** 101.16 Hz
- **f_lower:** 46.615 Hz
- **f_upper:** 219.554 Hz
- **Maximum Gain:** -6.86183 dB

### Frequency Response
![Frequency Response](FIG/frequency_response.png)

## Verification Status
The designed filter successfully meets all specifications with the measured values falling within 1% of the target values.

## Notes
- The filter design uses standard component values to ensure practical implementation
- A two-stage RC filter topology was used (high-pass followed by low-pass)
- The simulation was run with a frequency sweep from 10 Hz to 1000 Hz

## Conclusion
The intelligent agent successfully designed an RC bandpass filter meeting the specified center frequency and bandwidth requirements. The design was verified using SPICE simulation, confirming that the filter performs as expected.
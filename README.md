# Intelligent Agent RC Filter Optimization

This project implements an intelligent agent framework using the Langchain library to optimize the design of a passive bandpass RC filter. The filter is designed to have a center frequency of 100Hz and a bandwidth of 40Hz.

|  Name  | Student Number |
| :----: | :------------: |
| 郑志宇 |  24112020118   |

## Project Structure

```
intelligent-agent-rc-filter
├── src
│   ├── main.py                # Entry point of the application
│   ├── agent
│   │   ├── __init__.py        # Package initializer for agent
│   │   └── rc_filter_agent.py  # Contains RCFilterAgent class for optimization
│   └── spice
│       ├── __init__.py        # Package initializer for spice
│       └── netlist_generator.py # Generates SPICE netlist for the filter
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── .env                        # openai LLM API Key
└── test_report.md              # Results of the tests conducted
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/shifengzhicheng/intelligent-agent-rc-filter.git
   cd intelligent-agent-rc-filter
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

First input your API key into the .env file.

To run the intelligent agent framework and optimize the RC filter, execute the following command:

```
python src/main.py
```

## SPICE Netlist

The project includes a SPICE netlist for a passive bandpass filter with the specified parameters. The netlist is generated based on the optimized RC values and can be simulated to verify the filter's performance.

## Testing

Unit tests are provided to ensure the functionality of the `RCFilterAgent` class and the simulation verification process. To run the tests, use:

```
pytest src/tests
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
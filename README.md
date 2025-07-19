# Multi-Tool Agent

A Python-based intelligent agent built with Google's Agent Development Kit (ADK) that provides weather and time information for cities. This project demonstrates how to create a multi-tool agent that can handle multiple types of queries through a single interface.

## Features

- **Weather Information**: Get current weather reports for supported cities
- **Time Information**: Retrieve current time in different timezones
- **Multi-Tool Architecture**: Single agent with multiple specialized tools
- **Error Handling**: Graceful handling of unsupported cities and edge cases
- **Extensible Design**: Easy to add new tools and capabilities

## Supported Cities

Currently, the agent supports the following cities:
- **New York**: Weather and timezone information

## Project Structure

```
adk1/
├── app/
│   └── multi_tool_agent/
│       ├── __init__.py
│       └── agent.py
├── README.md
└── .gitignore
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd adk1
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install google-adk
   ```

## Usage

### Basic Usage

The agent is configured with two main tools:

1. **Weather Tool** (`get_weather`): Retrieves weather information for supported cities
2. **Time Tool** (`get_current_time`): Gets current time in specified timezones

### Example Queries

The agent can handle natural language queries such as:
- "What's the weather in New York?"
- "What time is it in New York?"
- "Tell me about the weather and time in New York"

### Agent Configuration

The agent is configured with:
- **Model**: `gemini-2.0-flash`
- **Name**: `weather_time_agent`
- **Description**: Agent to answer questions about the time and weather in a city
- **Instruction**: Helpful agent for weather and time queries

## API Reference

### `get_weather(city: str) -> dict`

Retrieves weather information for a specified city.

**Parameters:**
- `city` (str): The name of the city

**Returns:**
- `dict`: Status and weather report or error message

**Example Response:**
```python
{
    "status": "success",
    "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)."
}
```

### `get_current_time(city: str) -> dict`

Returns the current time in a specified city.

**Parameters:**
- `city` (str): The name of the city

**Returns:**
- `dict`: Status and time report or error message

**Example Response:**
```python
{
    "status": "success", 
    "report": "The current time in New York is 2024-01-15 14:30:25 EST-0500"
}
```

## Development

### Adding New Cities

To add support for new cities:

1. Update the `get_weather` function to include the new city
2. Update the `get_current_time` function with the appropriate timezone identifier
3. Test the new functionality

### Adding New Tools

To add new tools to the agent:

1. Create a new function with appropriate docstrings
2. Add the function to the `tools` list in the `root_agent` configuration
3. Update the agent's description and instruction if needed

## Error Handling

The agent includes comprehensive error handling:
- Unsupported cities return appropriate error messages
- Invalid inputs are handled gracefully
- All functions return consistent response formats

## Dependencies

- `google-adk`: Google's Agent Development Kit
- `datetime`: Python's datetime module for time handling
- `zoneinfo`: Timezone information handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please open an issue in the repository.

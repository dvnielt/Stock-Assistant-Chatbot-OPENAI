# Stock Analysis Chatbot Assistant

A Flask-based chatbot that provides real-time stock market analysis and information using OpenAI's GPT-4 and various financial analysis tools.

## Features

- Real-time stock price checking
- Technical analysis indicators:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
- Stock price visualization
- Natural language processing for company name to ticker symbol conversion
- Interactive chat interface

## Prerequisites

- Python 3.x
- OpenAI API key
- Flask
- yfinance
- pandas
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create an `API_KEY.txt` file in the root directory and add your OpenAI API key:
```bash
echo "your-api-key-here" > API_KEY.txt
```

## Project Structure

```
├── main.py                 # Main Flask application
├── stock_functions.py      # Stock analysis functions
├── requirements.txt        # Project dependencies
├── API_KEY.txt            # OpenAI API key
├── static/
│   ├── styles.css         # CSS styling
│   └── stock.png          # Generated stock charts
└── templates/
    └── index.html         # Frontend chat interface
```

## Usage

1. Start the Flask server:
```bash
python main.py
```

2. Open a web browser and navigate to:
```
http://localhost:5000
```

3. Example queries:
- "What's Apple's current stock price?"
- "Show me Tesla's stock chart"
- "Calculate the 20-day SMA for Microsoft"
- "What's the RSI for Amazon?"
- "Tell me the MACD values for Google"

## Function Descriptions

- `get_stock_price`: Retrieves current stock price
- `calculate_SMA`: Calculates Simple Moving Average
- `calculate_EMA`: Calculates Exponential Moving Average
- `calculate_RSI`: Calculates Relative Strength Index
- `calculate_MACD`: Calculates MACD indicator
- `plot_stock_price`: Generates stock price visualization

## Customization

- Modify `styles.css` to change the appearance
- Update `index.html` to customize the frontend
- Add new functions in `stock_functions.py` for additional analysis

## Dependencies

- Flask
- OpenAI
- pandas
- matplotlib
- yfinance

## Error Handling

The chatbot includes error handling for:
- Invalid stock tickers
- API failures
- Data retrieval issues
- Invalid user inputs

## Security

- API key is stored separately in `API_KEY.txt`
- Basic error handling and input validation
- Frontend security measures

## Acknowledgments

- OpenAI for GPT-4 API
- yfinance for stock data
- Flask framework
- Contributors and testers

## Notes

- Ensure your OpenAI API key has sufficient credits
- Stock data is provided by Yahoo Finance
- Charts are generated in real-time

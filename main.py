from flask import Flask, render_template, request, jsonify
import json
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from stock_functions import * 

app = Flask(__name__)

client = OpenAI(api_key=open('API_KEY.txt', 'r').read())

functions = [
    {
        'type': 'function',
        'function': {
            'name': 'get_stock_price',
            'description': 'Gets the latest stock price given the ticker symbol of a company.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'The stocker ticker symbol for a company (e.g., AAPL for Apple).'
                    }
                },
                'required': ['ticker']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'calculate_SMA',
            'description': 'Calculate the simple moving average for a given stock ticker and a window.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)'
                    },
                    'window': {
                        'type': 'integer',
                        'description': 'The timeframe to consider when calculating the SMA'
                    }
                },
                'required': ['ticker', 'window']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'calculate_EMA',
            'description': 'Calculate the exponential moving average for a given stock ticker and a window.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)'
                    },
                    'window': {
                        'type': 'integer',
                        'description': 'The timeframe to consider when calculating the EMA'
                    }
                },
                'required': ['ticker', 'window']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'calculate_RSI',
            'description': 'Calculate the RSI for a given stock ticker.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)'
                    }
                },
                'required': ['ticker']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'calculate_MACD',
            'description': 'Calculate the MACD for a given stock ticker.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)'
                    }
                },
                'required': ['ticker']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'plot_stock_price',
            'description': 'Plot the stock price for the last year given the ticker symbol of a company.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)'
                    }
                },
                'required': ['ticker']
            }
        }
    }
]

available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.json['question']
        messages = [{'role': 'user', 'content': user_input}]

        # Always use tools for every request to allow the model to decide
        response = client.chat.completions.create(
            model='gpt-4-0125-preview',
            messages=messages,
            tools=functions,
            tool_choice='auto'
        )

        response_message = response.choices[0].message

        # Handle function calls
        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                args_dict = {'ticker': function_args.get('ticker')}
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}

            function_to_call = available_functions[function_name]
            function_response = function_to_call(**args_dict)

            if function_name == 'plot_stock_price':
                return jsonify({
                    'answer': 'Here is the stock price chart:',
                    'chart': 'static/stock.png'
                })

            # Update messages with the assistant's response and tool output
            messages.append({
                'role': 'assistant',
                'content': None,
                'tool_calls': [{'id': tool_call.id, 'type': 'function', 'function': {'name': function_name, 'arguments': tool_call.function.arguments}}]
            })
            messages.append({
                'role': 'tool',
                'tool_call_id': tool_call.id,
                'name': function_name,
                'content': str(function_response)
            })
            
            # Get final response
            second_response = client.chat.completions.create(
                model='gpt-4-0125-preview',
                messages=messages
            )
            return jsonify({
                'answer': second_response.choices[0].message.content
            })

        # Return regular chat response if no tool was called
        return jsonify({
            'answer': response_message.content
        })
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'answer': "I apologize, but I encountered an error. Could you please rephrase your question?"
        })

if __name__ == '__main__':
    app.run(debug=True)
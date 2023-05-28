# Market Data App
The python script uses the streamlit library to create a web application for extracting financial data from Polygon API and from internally stored historical data in CSV format.The application provides different data retrieval functionalities for stocks, options, and the Indian market.

Here's an overview of the functions in the code:

- Aggregates(ticker, start_date, end_date): Fetches aggregate bars (minute-level data) for a stock over a given date range.
- DailyOpenclose(ticker, date): Retrieves the open, close, and after-hours prices of an options contract on a specific date.
- PreviousClose(ticker): Gets the previous day's open, high, low, and close (OHLC) prices for a specified stock ticker.
- Quotes(ticker): Fetches quotes for a stock ticker symbol in a given time range.
- SnapshotOption(underlying, ticker): Retrieves the snapshot data for an options contract on a specific underlying asset.
- SnapshotStock(ticker): Fetches the most up-to-date market data for a single traded stock ticker.

Please note that the code requires an API key from Polygon to access the data. Make sure to replace the api_key variable with your own API key to use the code successfully.

** Disclaimer:

The GitHub repository, including the data and CSV files provided, is intended for educational purposes and to showcase a portfolio project. The information and materials presented are not guaranteed to be accurate, complete, or up-to-date. They are provided "as is" without any warranties or representations, express or implied.

Additionally, please note that any references or mentions of external facilities, services, or products within the repository are for demonstration purposes only and should not be considered as endorsements or recommendations. The repository owner and contributors do not assume any responsibility or liability for the accuracy, reliability, or suitability of any third-party facilities, services, or products mentioned.

Users are encouraged to exercise their own discretion, conduct thorough research, and seek professional advice when making decisions based on the information and materials provided in this repository. The repository owner and contributors shall not be held responsible for any losses, damages, or consequences arising from the use or misuse of the repository's contents. **

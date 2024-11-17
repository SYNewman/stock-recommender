Plan for the classes in the app_logic folder

1. Stock Class
The Stock class represents a single stock and holds data as well as methods for processing it. This refactoring will encapsulate your existing logic for stock-specific data handling.

Attributes:

- ticker (str): The stock’s ticker symbol.
- price_history (pd.DataFrame): Stores historical price data (e.g., open, high, low, close).
- indicators (dict): Stores calculated indicators for the stock (e.g., RSI, SMA values, Bollinger Bands).
- recommendation (str or dict): Holds the latest recommendation for the stock (e.g., “Buy,” “Sell,” “Hold”) based on strategies.

Methods:

- __init__(self, ticker): Initializes a Stock instance with a ticker symbol.
- fetch_data(self): Imports stock data from yfinance. Can replace any current standalone function.
- update_price_history(self): Updates the price history based on new data.
- calculate_rsi(self, period=14): Calculates the RSI indicator. Refactor any existing RSI logic into this method.
- calculate_sma(self, period): Calculates the SMA for a given period. Integrate existing SMA calculation logic here.
- calculate_bollinger_bands(self, period=20, std_dev=2): Calculates Bollinger Bands. Refactor your Bollinger Bands function here.
- add_indicator(self, name, value): Adds a calculated indicator to the indicators dictionary.
- get_recommendation(self): Returns the latest recommendation, based on applied strategies.

2. Strategy Class
The Strategy class provides a framework for different trading strategies. Subclasses will define specific trading strategies.

Attributes:

- name (str): Name of the strategy (e.g., “Moving Average Strategy”).
- parameters (dict): Strategy-specific parameters, such as periods for SMA or thresholds for RSI.
- signal (str or dict): Last generated signal for the strategy (e.g., “Buy,” “Sell,” or any strategy-specific output).

Methods:

- __init__(self, name, parameters): Initializes a strategy with a name and any required parameters.
- apply(self, stock: Stock): Applies the strategy to a given Stock instance and returns a recommendation or signal. This is an abstract method to be overridden by subclasses.

Example Subclasses:

- MovingAverageStrategy(Strategy):
  - apply(self, stock): Implements the moving average crossover logic, taking short_period and long_period parameters to generate a recommendation.
- RSIStrategy(Strategy):
  - apply(self, stock): Implements RSI logic to generate a recommendation based on threshold values like overbought/oversold.
- BollingerBandsStrategy(Strategy):
  - apply(self, stock): Applies Bollinger Bands logic to generate a buy or sell signal based on upper/lower band crossings.
- Each strategy will use the existing calculation methods from Stock for indicators like SMA, RSI, or Bollinger Bands and apply its specific logic to generate a recommendation.

3. TradingSystem Class
This class orchestrates the overall process by managing stocks and applying strategies to them. It serves as the main control class, calling on methods in Stock and Strategy.

Attributes:

- stocks (list of Stock objects): Holds all Stock objects to be analyzed.
- strategies (list of Strategy objects): Holds all strategies that can be applied to stocks.
- recommendations (dict): Stores the recommendations generated for each stock.

Methods:

- __init__(self, stocks, strategies): Initializes the trading system with a list of stocks and strategies.
- add_stock(self, stock: Stock): Adds a new stock to the list of stocks.
- add_strategy(self, strategy: Strategy): Adds a new strategy to the list of strategies.
- update_all_data(self): Calls each stock’s fetch_data or update_price_history method to refresh data.
- run_strategies(self): Iterates over each stock and applies each strategy, storing results in recommendations.
- generate_recommendations(self): Processes and aggregates signals from all strategies to make a final recommendation for each stock.

from abc import ABC, abstractmethod

from strategies.moving_averages import Moving_Average_Strategy
from strategies.rsi import RSI_Strategy
from strategies.bollinger_bands import Bollinger_Bands_Strategy

class Strategy(ABC):
    def __init__(self, strategy, stats):
        self.strategy = ""
        self.stats = {}
        self.signal = ""
        
    @abstractmethod
    def apply_strategy(self, stock: Stock):
        pass
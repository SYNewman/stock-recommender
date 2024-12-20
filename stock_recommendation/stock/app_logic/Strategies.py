from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, strategy, stats, price):
        self.strategy = ""
        self.stats = []
        self.signal = ""
        
    @abstractmethod
    def generate_signal(self):
        pass
    
    @abstractmethod
    def apply_strategy(self):
        pass
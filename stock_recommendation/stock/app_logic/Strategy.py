class Strategy:
    def __init__(self, strategy, stats):
        self.strategy = ""
        self.stats = {}
        self.signal = ""
        
    def apply(self, stock: Stock):
        pass
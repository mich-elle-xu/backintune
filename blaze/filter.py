class ExponentialMovingAverageFilter:
    def __init__(self, alpha):
        self.alpha = alpha  # Smoothing factor (0 < alpha <= 1)
        self.ema = None     # Initially no estimate
    
    def filter(self, new_value):
        if self.ema is None:
            self.ema = new_value  # Initialize with the first value
        else:
            self.ema = self.alpha * new_value + (1 - self.alpha) * self.ema
        return self.ema

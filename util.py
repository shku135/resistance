import math

class Variable(object):
    def __init__(self, total = 0.0, samples = 0):
        self.total = total 
        self.samples = samples
        self.minimum = 'None'
        self.maximum = None

    def sample(self, value):
        self.total += value
        self.samples += 1
        self.minimum = min(self.minimum, value)
        self.maximum = min(self.maximum, value)

    def estimate(self):
        if self.samples > 0:
            return float(self.total) / float(self.samples)
        else:
            return 0.5

    # Error calculation courtesy of idmillington.
    def detail(self):
        """We're dealing with potential results at 0% or 100%, so use an
        Agresti-Coull interval (can't do a normal Clopper-Pearson without
        requiring the numpy library, and can't use the central limit theorem
        too close to the extremes). Note this is still degenerate when the
        number of samples is very small, and may give an upper bound > 100%."""

        n_prime = self.samples + 3.84 # 95% confidence interval
        value = (self.total + (3.84 * 0.5)) / n_prime
        error = 1.96 * math.sqrt(value * (1.0 - value) / n_prime)
        return "{:5.2f}% (e={:4.2f} n={:<4d})".format(
            value*100, error*100, int(self.samples)
        )

    def __repr__(self):
        if self.samples:
            value = 100.0 * float(self.total) / float(self.samples)
            if value == 100.0:
                return "100.0%"
            return "{:5.2f}%".format(value)
        else:
            return "   N/A"


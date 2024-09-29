from enum import Enum

class Granularity(Enum):
    HOURLY = 'hourly'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    @classmethod
    def list(cls):
        """Returns a list of granularity values."""
        return [g.value for g in cls]

    def resample_rule(self):
        """Return the resampling rule for Pandas."""
        if self == Granularity.HOURLY:
            return 'H'
        elif self == Granularity.DAILY:
            return 'D'
        elif self == Granularity.WEEKLY:
            return 'W'
        elif self == Granularity.MONTHLY:
            return 'M'
        else:
            raise ValueError(f"Unsupported granularity: {self.value}")

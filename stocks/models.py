from django.db import models

from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    avg_returns = models.FloatField()
    avg_close = models.FloatField()
    data = models.JSONField()

    def __str__(self):
        return f"{self.symbol} from {self.start_date} to {self.end_date}"


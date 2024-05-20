from django.contrib import admin
from .models import StockData

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'start_date', 'end_date', 'avg_returns', 'avg_close')
    search_fields = ('symbol',)
    list_filter = ('symbol', 'start_date', 'end_date')

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import StockData
from .serializers import StockDataSerializer
import yfinance as yf

class StockDataViewSet(viewsets.ModelViewSet):
    queryset = StockData.objects.all()
    serializer_class = StockDataSerializer

    def create(self, request, *args, **kwargs):
        symbol = request.data.get('symbol')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        stock_data = self.download_stock_data(symbol, start_date, end_date)
        avg_returns = stock_data['Pct Chg'].mean().round(2)
        avg_close = stock_data['Close'].mean().round(2)
        data = stock_data.to_json()

        stock_entry = StockData.objects.create(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            avg_returns=avg_returns,
            avg_close=avg_close,
            data=data
        )
        serializer = self.get_serializer(stock_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        symbol = request.data.get('symbol', instance.symbol)
        start_date = request.data.get('start_date', instance.start_date)
        end_date = request.data.get('end_date', instance.end_date)

        stock_data = self.download_stock_data(symbol, start_date, end_date)
        avg_returns = stock_data['Pct Chg'].mean().round(2)
        avg_close = stock_data['Close'].mean().round(2)
        data = stock_data.to_json()

        instance.symbol = symbol
        instance.start_date = start_date
        instance.end_date = end_date
        instance.avg_returns = avg_returns
        instance.avg_close = avg_close
        instance.data = data
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def download_stock_data(self, symbol, start_date, end_date):
        stock = yf.download(symbol, start=start_date, end=end_date)
        if stock.empty:
            raise ValueError(f"No data found for symbol: {symbol}")
        stock['Pct Chg'] = stock['Adj Close'].pct_change()
        return stock
    
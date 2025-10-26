# tests/test_csv_loader.py
import pytest
from oadl.stock import Stock
from oadl.stock_diccionario import StockDiccionario
from oadl.stock_pandas import StockPandas

@pytest.mark.parametrize("stock_cls", [StockDiccionario, StockPandas])
def test_stock_init(stock_cls):
    stock = stock_cls('tests/data/stock.json')
    assert isinstance(stock, Stock)
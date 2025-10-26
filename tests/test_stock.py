# tests/test_csv_loader.py
import pytest
from oadl.stock import Stock
from oadl.stock_diccionario import StockDiccionario
from oadl.stock_pandas import StockPandas

@pytest.mark.parametrize("stock_cls", [StockDiccionario, StockPandas])
def test_init(stock_cls):
    stock = stock_cls('tests/data/stock.json')
    assert isinstance(stock, Stock)

@pytest.mark.parametrize("stock_cls", [StockDiccionario, StockPandas])
def test_quantity(stock_cls):
    stock = stock_cls('tests/data/stock.json')
    # get_quantity
    assert stock.get_quantity('') == 0
    assert stock.get_quantity('1U0KF6M5H964WNX') == 10
    # get_quantity_by_rack
    assert stock.get_quantity_by_rack('', '1U0KF6M5H964WNX') == 0
    assert stock.get_quantity_by_rack('Rack_00001', '1U0KF6M5H964WNX') == 5
    assert stock.get_quantity_by_rack('Rack_00361', '1U0KF6M5H964WNX') == 3
    assert stock.get_quantity_by_rack('Rack_01049', '1U0KF6M5H964WNX') == 2
    # get_quantity_by_rack_face
    assert stock.get_quantity_by_rack_face('Rack_00001', 'Cara_1', '1U0KF6M5H964WNX') == 5
    assert stock.get_quantity_by_rack_face('Rack_00001', 'Cara_2', '1U0KF6M5H964WNX') == 0
    assert stock.get_quantity_by_rack_face('Rack_00361', 'Cara_3', '1U0KF6M5H964WNX') == 3
    assert stock.get_quantity_by_rack_face('Rack_01049', 'Cara_3', '1U0KF6M5H964WNX') == 2

@pytest.mark.parametrize("stock_cls", [StockDiccionario, StockPandas])
def test_set_quantity(stock_cls):
    stock = stock_cls('tests/data/stock.json')
    # Negative
    with pytest.raises(ValueError):
        stock.set_quantity('Rack_00001', 'Cara_1', '1U0KF6M5H964WNX', -1)
    # Existent item
    stock.set_quantity('Rack_00001', 'Cara_1', '1U0KF6M5H964WNX', 1)
    assert stock.get_quantity_by_rack_face('Rack_00001', 'Cara_1', '1U0KF6M5H964WNX') == 1
    # Non-existent item
    stock.set_quantity('Rack_Test', 'Face_Test', 'Item_Test', 1)
    assert stock.get_quantity_by_rack_face('Rack_Test', 'Face_Test', 'Item_Test') == 1

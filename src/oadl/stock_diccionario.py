from collections import defaultdict
import json
from oadl.stock import Stock

class StockDiccionario(Stock):
    """Raw dictionary implementation"""
    def __init__(self, file_path):
        self.stock_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        with open(file_path, 'r') as f:
            racks_data = json.load(f)
            
        for rack_name, faces in racks_data.items():
            for face_name, inventory in faces.items():
                for item in inventory:
                    self.stock_data[rack_name][face_name][item["Inventory ID"]] += item["Cantidad"]

    def get_quantity_by_rack(self, rack, item_id):
        return sum(inventory[item_id] for face, inventory in self.stock_data[rack].items())

    def get_quantity_by_rack_face(self, rack, face, item_id):
        return self.stock_data[rack][face][item_id]

    def get_quantity(self, item_id):
        return sum(inventory[item_id] for rack, faces in self.stock_data.items() for face, inventory in faces.items())

    def set_quantity(self, rack, face, item_id, quantity):
        if quantity < 0:
            raise ValueError('Item quantity cannot be negative')
        else:
            self.stock_data[rack][face][item_id] = quantity
    
    def rack_empty(self, rack):
        return sum(quantity for face, inventory in self.stock_data[rack].items() for item_id, quantity in inventory.items()) == 0
    
    def rack_face_empty(self, rack, face):
        return sum(quantity for item_id, quantity in self.stock_data[rack][face].items()) == 0

    def get_racks(self):
        return list(rack for rack in self.stock_data.keys() if not self.rack_empty(rack))

    def get_racks_of_item(self, item_id):
        racks_with_item = []
        for rack, faces in self.stock_data.items():
            for face, inventory in faces.items():
                if inventory[item_id] > 0:
                    racks_with_item.append(rack)
                    break # Move to the next rack once item is found
        return racks_with_item

    def get_racks_and_faces_of_item(self, item_id):
        racks_and_faces_with_item = []
        for rack, faces in self.stock_data.items():
            for face, inventory in faces.items():
                if inventory[item_id] > 0:
                    racks_and_faces_with_item.append((rack, face))
        return racks_and_faces_with_item

    def get_items_by_rack(self, rack):
        items_in_rack = set()
        for face, inventory in self.stock_data[rack].items():
            items_in_rack.update(item_id for item_id in inventory if inventory[item_id] > 0)
        return list(items_in_rack)

    def get_items_by_rack_face(self, rack, face):
        inventory = self.stock_data[rack][face]
        return [item_id for item_id in inventory if inventory[item_id] > 0]

    def get_items_and_quantities(self, rack, face):
        inventory = self.stock_data[rack][face]
        return [(item_id, quantity) for item_id, quantity in inventory.items() if quantity > 0]
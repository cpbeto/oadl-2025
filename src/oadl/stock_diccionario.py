from oadl.stock import Stock
import json

class StockDiccionario(Stock):
    """Raw dictionary implementation"""
    def __init__(self, file_path):
        self.stock_data = {}

        with open(file_path, 'r') as f:
            racks_data = json.load(f)
        for rack_name, faces in racks_data.items():
            for face_name, items in faces.items():
                for item in items:
                    if item["Cantidad"] > 0: # Only store items with quantity > 0
                        if rack_name not in self.stock_data:
                            self.stock_data[rack_name] = {}
                        if face_name not in self.stock_data[rack_name]:
                            self.stock_data[rack_name][face_name] = {}
                        if item["Inventory ID"] not in self.stock_data[rack_name][face_name]:
                            self.stock_data[rack_name][face_name][item["Inventory ID"]] = item["Cantidad"]
                        else:
                            self.stock_data[rack_name][face_name][item["Inventory ID"]] += item["Cantidad"]

    def get_quantity_by_rack(self, rack, item_id):
        quantity = 0
        for face, items in self.stock_data[rack].items():
            if item_id in items:
                quantity += items[item_id]
        return quantity

    def get_quantity_by_rack_face(self, rack, face, item_id):
        return self.stock_data[rack][face].get(item_id, 0)

    def get_quantity(self, item_id):
        quantity = 0
        for rack, faces in self.stock_data.items():
            for face, items in faces.items():
                if item_id in items:
                    quantity += items[item_id]
        return quantity

    def set_quantity(self, rack, face, item_id, quantity):
        if quantity < 0:
            raise ValueError('Item quantity cannot be negative')
        elif quantity == 0:
            # Cuando la cantidad es 0 lo borramos del stock
            if rack in self.stock_data and face in self.stock_data[rack] and item_id in self.stock_data[rack][face]:
                del self.stock_data[rack][face][item_id]
            # Optional: Clean up empty faces or racks
            if not self.stock_data[rack][face]:
                del self.stock_data[rack][face]
            if not self.stock_data[rack]:
                del self.stock_data[rack]
        else:
            self.stock_data[rack][face][item_id] = quantity

    def get_racks(self):
        return list(self.stock_data.keys())

    def get_racks_of_item(self, item_id):
        racks_with_item = []
        for rack, faces in self.stock_data.items():
            for face, items in faces.items():
                if item_id in items:
                    racks_with_item.append(rack)
                    break # Move to the next rack once item is found
        return racks_with_item

    def get_racks_and_faces_of_item(self, item_id):
        racks_and_faces_with_item = []
        for rack, faces in self.stock_data.items():
            for face, items in faces.items():
                if item_id in items:
                    racks_and_faces_with_item.append((rack, face))
        return racks_and_faces_with_item

    def get_items_by_rack(self, rack):
        items_in_rack = set()
        if rack in self.stock_data:
            for face, items in self.stock_data[rack].items():
                items_in_rack.update(items.keys())
        return list(items_in_rack)

    def get_items_by_rack_face(self, rack, face):
        if rack in self.stock_data and face in self.stock_data[rack]:
            return list(self.stock_data[rack][face].keys())
        return []

    def get_items_and_quantities(self, rack, face):
        if rack in self.stock_data and face in self.stock_data[rack]:
            return list(self.stock_data[rack][face].items())
        return []
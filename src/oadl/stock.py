class Stock:
    """Defines the interface for the stock module"""
    def __init__(self, file_path):
        pass

    def get_quantity_by_rack(self, rack, item_id):
        pass

    def get_quantity_by_rack_face(self, rack, face, item_id):
        pass

    def get_quantity(self, item_id):
        pass

    def set_quantity(self, rack, face, item_id, quantity):
        pass

    def get_racks(self):
        pass

    def get_racks_of_item(self, item_id):
        pass

    def get_racks_and_faces_of_item(self, item_id):
        pass

    def get_items_by_rack(self, rack):
        pass

    def get_items_by_rack_face(self, rack, face):
        pass

    def get_items_and_quantities(self, rack, face):
        pass
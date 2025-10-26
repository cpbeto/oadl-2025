import pandas as pd
from oadl.stock import Stock

class StockPandas(Stock):
    def __init__(self, file_path):
        # Leer JSON y formatear
        df = pd\
            .read_json(file_path, orient='index')\
            .stack()\
            .reset_index()
        df.columns = ['Rack', 'Face', 'JSON']

        # Expandir lista de inventario [ {}, {}, ... ] a filas
        df_exploded = df.explode(column='JSON', ignore_index=True)

        # Normalizar inventario { 'Inventory ID', 'Cantidad', ... } a columnas
        df_normalized = pd.json_normalize(df_exploded['JSON'])

        # Concatenar dataframes
        df = pd.concat([df_exploded, df_normalized], axis=1)

        # Eliminar columnas innecesarias
        # A los fines de este sistema el nivel y posición no se utilizan
        df = df.drop(columns=['JSON', 'Nivel', 'Posicion'])

        # Agregación
        df = df.groupby(['Rack', 'Face', 'Inventory ID'], as_index=False).sum()

        # Sort
        self.df = df.sort_index()

    def get_quantity_by_rack(self, rack, item_id):
        return self.df[(self.df['Rack'] == rack) & (self.df['Inventory ID'] == item_id)]['Cantidad'].sum()

    def get_quantity_by_rack_face(self, rack, face, item_id):
        return self.df[(self.df['Rack'] == rack) & (self.df['Face'] == face) & (self.df['Inventory ID'] == item_id)]['Cantidad'].sum()

    def get_quantity(self, item_id):
        return self.df[self.df['Inventory ID'] == item_id]['Cantidad'].sum()

    def set_quantity(self, rack, face, item_id, quantity):
        if quantity < 0:
            raise ValueError('Item quantity cannot be negative')
        elif quantity == 0:
            self.df = self.df.drop(self.df.index[(self.df['Rack'] == rack) & (self.df['Face'] == face) & (self.df['Inventory ID'] == item_id)])
        else:
            exists = ((self.df['Rack'] == rack) & (self.df['Face'] == face) & (self.df['Inventory ID'] == item_id)).any()
            if exists:
                self.df.loc[(self.df['Rack'] == rack) & (self.df['Face'] == face) & (self.df['Inventory ID'] == item_id), 'Cantidad'] = quantity
            else:
                self.df = self.df.append(
                    {'Rack': rack, 'Face': face, 'Inventory ID': item_id, 'Cantidad': quantity},
                    ignore_index=True
                )

    def get_racks(self, item_id):
        return self.df[self.df['Inventory ID'] == item_id]['Rack'].unique().tolist()

    def get_racks_and_faces(self, item_id):
        return self.df[self.df['Inventory ID'] == item_id][['Rack', 'Face']].apply(tuple, axis=1).unique().tolist()

    def get_items(self, rack, face):
        return self.df[(self.df['Rack'] == rack) & (self.df['Face'] == face)]['Inventory ID'].unique().tolist()

    def get_items_and_quantities(self, rack, face):
        return self.df[(self.df['Rack'] == rack) & (self.df['Face'] == face)][['Inventory ID', 'Cantidad']].apply(tuple, axis=1).unique().tolist()
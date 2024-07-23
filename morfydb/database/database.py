from ..table import Table
from ..orm import MorfyBase

class MorfyDB:
    def __init__(self) -> None:
        self.tables:list[Table] = []
        
    def set_table(self, model:MorfyBase):
        table = Table(model)
        self.tables.append(table)
        return table
    
    def insert_table(self, model:MorfyBase, values:list|dict):
        model = model() if callable(model) else model
        index = [func_t.name for func_t in self.tables].index(model._get_name())
        table = self.tables[index]
        return table.insert(values)
    
    def select_table(self, model:MorfyBase):
        model = model() if callable(model) else model
        index = [func_t.name for func_t in self.tables].index(model._get_name())
        table = self.tables[index]
        return table.select()
    
    def update_table(self, model:MorfyBase, ID:int, values:list|dict):
        model = model() if callable(model) else model
        index = [func_t.name for func_t in self.tables].index(model._get_name())
        table = self.tables[index]
        return table.update(ID, values)
    
    def delete_table(self, model:MorfyBase, *ID:int):
        model = model() if callable(model) else model
        index = [func_t.name for func_t in self.tables].index(model._get_name())
        table = self.tables[index]
        return table.delete(*ID)
    
    def append_table(self, model:MorfyBase, model_to:MorfyBase|Table, none:bool=False):
        model = model() if callable(model) else model
        index = [func_t.name for func_t in self.tables].index(model._get_name())
        table = self.tables[index]
        return table.append(model_to() if callable(model_to) else model_to, none=none)
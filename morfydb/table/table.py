from .. import pd, np

from ..orm import MorfyBase, Column
from ..orm import (
    INDEX
)
from ..orm.typing.typing import CheckType, remove_empty_or_all_na_columns, operators
from ..enums.enums import ValueType
from ..errors.errors import ColumnValueError

from types import NoneType


class Table:
    def __init__(self, model:MorfyBase) -> None:
        model = model() if callable(model) else model
        self.columns = model._get_columns()
        self.base = model
        self.name = model._get_name()
        self.model = pd.DataFrame(columns=self.columns)
        self.class_columns = model._get_class_column()
        self.class_columns_alias = [col._alias for col in self.class_columns]
        self.class_columns_default = {col._alias: col._default for col in self.class_columns if col._default is not None}
        self.class_columns_typing = [col._typing for col in self.class_columns]
        
        
        if INDEX in self.class_columns_typing:
            self.__ID = self.class_columns[self.class_columns_typing.index(INDEX)]._alias
            self.model = self.model.set_index(self.__ID)
            self.model.index = self.model.index + self.class_columns[self.class_columns_typing.index(INDEX)]._typing_data.start
            
        
    def insert(self, values:list|dict, none:bool=False):
        lens = len(values)
        if lens != len(self.model.columns):
            raise ColumnValueError("Lengths of values and columns do not match")
        index = len(self.model)
        
        if isinstance(values, list):
            if none:
                for i in range(len(values)):
                    if isinstance(values[i], NoneType):
                        values[i] = ValueType.NONE
            result = {}
            if INDEX in self.class_columns_typing:
                result = {self.__ID:[index + self.class_columns[self.class_columns_typing.index(INDEX)]._typing_data.start]}
            values = [[i] for i in values]
            result.update(dict(zip(self.model.columns, values)))
        elif isinstance(values, dict):
            if none:
                for key, value in values.items():
                    if None in value:
                        tmp = []
                        for i in value:
                            if isinstance(i, NoneType):
                                tmp.append(ValueType.NONE)
                                continue
                            tmp.append(i)
                        values.update({key:tmp})
            result = {}
            if INDEX in self.class_columns_typing:
                result = {self.__ID:list(index + i + self.class_columns[self.class_columns_typing.index(INDEX)]._typing_data.start for i in range(0, len(values[self.model.columns[0]])))}
            result.update(values)
        else:
            raise ValueError("Data type must be dict or list")
        
        result = {key:[self.class_columns_default[key] if row in [None, ValueType.DEFAULT] and key in self.class_columns_default else row for row in value] for key, value in result.items()}
        model = pd.DataFrame(data=result)
        model = CheckType(model, self.base, self.columns.values())
        
        
        if INDEX in self.class_columns_typing:
            model = model.set_index(self.__ID)
        
        model1 = remove_empty_or_all_na_columns(self.model)
        model2 = remove_empty_or_all_na_columns(model)
        if INDEX in self.class_columns_typing:
            self.model = pd.concat([model1, model2])
        else:
            self.model = pd.concat([model1, model2], ignore_index=True)
        return self.model
    
    def update(self, ID:int, values:list|dict):
        if isinstance(values, list):
            for i, col in enumerate(self.model.columns):
                self.model.loc[self.model.index == ID, col] = values[i]
        if isinstance(values, dict):
            for col in self.columns:
                self.model.loc[self.model.index == ID, col] = values[i]
        return self.model
    
    def delete(self, *ID:int):
        for id in ID:
            self.model.drop(self.model.loc[self.model.index == id].index, inplace=True)
        return self.model
    
    def append(self, *models:pd.DataFrame, none:bool=False):
        for model in models:
            if isinstance(model, Table):
                model = model.model
            if none:
                model = model.replace(np.nan, None)
            if INDEX in self.class_columns_typing:
                self.model = pd.concat([self.model, model.astype(self.model.dtypes)], ignore_index=True)
                self.model.index += self.class_columns[self.class_columns_typing.index(INDEX)]._typing_data.start
                self.model.index.name = self.__ID
            else:
                self.model = pd.concat([self.model, model], ignore_index=True)
        return self.model
    
    def select(self,
            *filters:list[str],
            replace= {},
            replace_none:bool = False
        ):
        model = self.model.copy()
        
        if len(replace) != 0:
            for key, value in replace.items():
                model = model.replace(key, value)
        if replace_none:
            model = model.replace(np.nan, None)
        
        if filters:
            for f in filters:
                try:
                    model = model[operators[f[1]](model[f[0]], f[2])]
                except KeyError as e:
                    if e.args[0] == self.__ID:
                        model = model[operators[f[1]](model.index, f[2])]
                    else:
                        raise KeyError(e)
            
        return model
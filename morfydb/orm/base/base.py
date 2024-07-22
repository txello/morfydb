from types import EllipsisType
from typing import Callable, Any

class Column:
    def __init__(self, typing:Callable|EllipsisType = ... ,alias:str|None = None, default:Any|None = None) -> None:
        self._alias = alias
        self._default = default
        self._typing = type(typing)
        self._typing_data = typing if not isinstance(typing, EllipsisType) else None
    
    def _add_alias(self, alias:str):
        self._alias = alias
    
    def __lt__(self,other):
        return [self._alias,'<', other]
    
    def __gt__(self,other):
        return [self._alias,'>', other]
    
    def __eq__(self, other):
        return [self._alias,'==', other]
    
    def __ne__(self, other):
        return [self._alias,'!=', other]
    
    def __le__(self, other):
        return [self._alias,'<=', other]
    
    def __ge__(self, other):
        return [self._alias,'>=', other]
    
    def __repr__(self) -> str:
        return str(self._alias)

class MorfyBase:
    class Config:
        __auto_float__ = False
        __auto_none__ = False
    
    def __init__(self, name:str|None = None) -> None:
        self._name = name if name is not None else self.__class__.__name__
        self._columns = self.__class__.__annotations__
        self._add_value(self._columns)
        
    def _add_value(self, values:dict):
        for key, value in values.items():
            if key not in self.__class__.__dict__:
                if isinstance(value, Column):
                    value._add_alias(alias=key)
                else:
                    value = Column(alias=key)
                setattr(self.__class__,key, value)
            else:
                column = self.__class__.__dict__[key]
                if isinstance(column, Column):
                    column._add_alias(key)
    
    def add_column(self, name:str, typing:type, value:Column|None=None):
        self._columns.update({name:typing})
        self._add_value({name:value})
    
    def settings(self, args:dict|None = None, **kwargs):
        if args is not None:
            for key, value in args.items():
                setattr(self.Config, key, value)
        for key, value in kwargs.items():
            setattr(self.Config, key, value)
        
    def remove_column(self, name:str):
        return self._columns.pop(name)
        
    def _get_columns(self):
        return self._columns
    
    def _get_class_column(self):
        array = [self.__class__.__dict__[key] for key in self.__class__.__annotations__]
        return array
    
    def _get_name(self):
        return self._name
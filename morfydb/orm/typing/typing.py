from ... import pd, np
from ..base.base import MorfyBase
import operator
from types import NoneType, UnionType
from ...enums.enums import ValueType
from typing import get_args, get_origin
from ...errors.errors import ColumnValueError

class CheckType:
    def __new__(self, model:pd.DataFrame, base:MorfyBase, typing:list[type]) -> pd.DataFrame:
        typ = typing
        typ = [get_args(t) if get_origin(t) is UnionType else (t,) for t in typ]
        for col, expected_type in zip(model.columns, typ):
            # Проверяем, если все значения соответствуют ожидаемому типу
            for value in model[col]:
                if value == ValueType.NONE:
                    value = None
                if not isinstance(value, expected_type):
                    self.__check(model, base, value, expected_type, col)
        return model
    
    def __check(model, base:MorfyBase, value, typing:type, column):
        # Если значения не соответствуют ожидаемому типу, проверяем условия для преобразования
        if '__auto_float__' in base.__class__.Config.__dict__ and base.__class__.Config.__auto_float__:
            if float in typing and isinstance(value, (int, float)):
                # Преобразуем колонку в float, если все значения типа int
                model[column] = model[column].astype(float)
                return
        if '__auto_none__' in base.__class__.Config.__dict__ and base.__class__.Config.__auto_none__:
            if isinstance(value, NoneType):
                return
        raise ColumnValueError(f"Data types error: {value} not in {typing}")
    
def remove_empty_or_all_na_columns(df:pd.DataFrame):
    return df.dropna(axis=1, how='all')


class INDEX:
    def __init__(self, start:int=0) -> None:
        self.start = start
        
operators = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge
}
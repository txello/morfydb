from enum import Enum

class ValueType(Enum):
    DEFAULT = 'default'
    """DEFAULT - Значение Column(default="") """
    NONE = None
    """NONE - Замена None"""
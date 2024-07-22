# morfydb - Локальная Pandas БД


## Примеры

### Базовая БД
```python
from morfydb import MorfyDB
from morfydb.orm import MorfyBase

class Books(MorfyBase):
    name:str
    author:str
    price:float
    
db = MorfyDB()

table = db.set_table(Books)

table.insert(['Преступление и наказание', 'Лев Толстой', 2500.0])
table.insert({
    'name':['Евгений Онегин', 'Приключение Тома Сойера'],
    'author':['Александр Пушкин', 'Марк Твен'],
    'price':[2500.0, 2600.0]
})

result = table.select()
print(result)
#                       name            author   price
#0  Преступление и наказание       Лев Толстой  2500.0
#1            Евгений Онегин  Александр Пушкин  2500.0
#2   Приключение Тома Сойера         Марк Твен  2600.0
```

### БД с преднастройками

```python
from morfydb import MorfyDB
from morfydb.orm import MorfyBase, Column, INDEX
from morfydb.enums import ValueType

class Books(MorfyBase):
    ID:int = Column(INDEX(1))
    name:str
    author:str = Column(default='Без автора')
    price:float = Column(default=0)
    count:int|None
    
    class Config:
        __auto_float__ = True
        __auto_none__ = True

db = MorfyDB()

table = db.set_table(Books)

table.insert(['Преступление и наказание', 'Лев Толстой', 2500, ValueType.NONE])
table.insert([ValueType.NONE, ValueType.DEFAULT, 2500, 100])

table.insert({
    'name':['Евгений Онегин', 'Приключение Тома Сойера'],
    'author':['Александр Пушкин', 'Марк Твен'],
    'price':[2500, 2600],
    'count':[100,None]
}, none=True)

result = table.select(
    replace_none=True
)
print(result)

#                        name            author   price           count
#ID
#1   Преступление и наказание       Лев Толстой  2500.0  ValueType.NONE
#2             ValueType.NONE        Без автора  2500.0             100
#3             Евгений Онегин  Александр Пушкин  2500.0             100
#4    Приключение Тома Сойера         Марк Твен  2600.0  ValueType.NONE

result = table.select(
    Books.count == 100
)
print(result)

#              name            author   price count
#ID
#2   ValueType.NONE        Без автора  2500.0   100
#3   Евгений Онегин  Александр Пушкин  2500.0   100
```

### Настраиваемая таблица

```python
from morfydb import MorfyDB
from morfydb.orm import MorfyBase, Column, INDEX
from morfydb.enums import ValueType
from morfydb.filters import ColumnFilter

base = MorfyBase('Books')
base.add_column('ID',int, Column(INDEX(1)))
base.add_column('name',str, Column(default='Без названия'))
base.add_column('author',str, Column(default='Без автора'))
base.add_column('price',float, Column(default=0))
base.add_column('count',int|None)
base.settings(__auto_float__ = True)

db = MorfyDB()

table = db.set_table(base)

table.insert(['Преступление и наказание', 'Лев Толстой', 2500, ValueType.NONE])
table.insert([ValueType.DEFAULT, ValueType.DEFAULT, 2500, 100])

result = table.select(
    ColumnFilter('ID') == 1,
)
print(result)
#                        name       author   price           count
#ID
#1   Преступление и наказание  Лев Толстой  2500.0  ValueType.NONE
```
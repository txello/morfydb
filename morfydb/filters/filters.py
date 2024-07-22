class ColumnFilter:
    def __init__(self) -> None:
        pass
    
    def __init__(self, name:str) -> None:
        self._alias = name
    
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
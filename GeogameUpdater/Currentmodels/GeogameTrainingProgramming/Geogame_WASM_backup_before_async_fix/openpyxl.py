class MockCell:
    def __init__(self):
        self.value = 0

class MockSheet:
    def cell(self, row, column):
        return MockCell()
        
    def __getitem__(self, key):
        return self

class MockWorkbook:
    def __init__(self):
        self.active = MockSheet()
        
    def __getitem__(self, key):
        return MockSheet()
        
    def save(self, *args, **kwargs):
        pass

def load_workbook(*args, **kwargs):
    print("MOCK: load_workbook called")
    return MockWorkbook()

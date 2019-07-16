import json
from src.functions.Snapshot.configSnapshot import splitByApp 

# Tag app-name
def test_splitByApp():
    configSnapshotByApp = splitByApp("test/inputs/Snapshot/ConfigSnapshot1.json")
    a=3
    assert 1 == 1
    
if __name__ == "__main__":
    test_splitByApp()
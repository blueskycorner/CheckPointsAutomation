import json
import os 
print(os.getcwd())
from src.functions.Snapshot.configSnapshot import splitByApp 

# Tag app-name
def test_splitByApp():
    configSnapshotByApp = splitByApp("test/inputs/Snapshot/ConfigSnapshot1.json")
    assert 1 == 1
    
if __name__ == "__main__":
    test_splitByApp()
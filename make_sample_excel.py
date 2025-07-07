import pandas as pd
import os

data = {
    "Part Number": ["BRK-001", "FLT-002", "ENG-003", "BRK-004", "FLT-005"],
    "Description": ["Brake Pad", "Oil Filter", "Spark Plug", "Brake Disc", "Air Filter"],
    "Location": ["Pune", "Mumbai", "Delhi", "Pune", "Chennai"],
    "Quantity": [120, 80, 200, 50, 60],
    "Last Updated": ["2024-07-01", "2024-07-02", "2024-07-01", "2024-07-03", "2024-07-02"]
}

df = pd.DataFrame(data)
os.makedirs('data', exist_ok=True)
df.to_excel("data/sample_inventory.xlsx", index=False)
print("Sample Excel file created at data/sample_inventory.xlsx") 
import pandas as pd
from typing import Dict, Any
from io import BytesIO

def parse_excel(file: BytesIO) -> Dict[str, pd.DataFrame]:
    """
    Parse an Excel file from a BytesIO object, extract all sheets, and return a dictionary of DataFrames.
    Args:
        file (BytesIO): The uploaded Excel file.
    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping sheet names to DataFrames.
    """
    xls = pd.ExcelFile(file)
    sheets = {}
    for sheet_name in xls.sheet_names:
        sheets[sheet_name] = xls.parse(sheet_name)
    return sheets 
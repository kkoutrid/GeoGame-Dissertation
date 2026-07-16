import pandas as pd

# Read CSV file
csv_file_path = 'C:\\Diplomatikh\\diplomatikh\\2023-07-28\\teams_fifa23.csv'
df = pd.read_csv(csv_file_path)

# Save as XLSX file
xlsx_file_path = 'C:\\Diplomatikh\\diplomatikh\\2023-07-28\\teams_fifa23.xlsx'
df.to_excel(xlsx_file_path, index=False)

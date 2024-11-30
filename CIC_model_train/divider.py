import pandas as pd

file_path = 'Raw_Fri_Aft_DDOS.csv'  
df = pd.read_csv(file_path)

total_rows = len(df)
print(f"Total rows in CSV: {total_rows}")

starting_row = int(input("Enter the starting row number (0-based index): "))
num_rows = int(input("Enter the number of rows to select for the first CSV: "))

if starting_row < 0 or starting_row >= total_rows:
    print("Invalid starting row. Please enter a valid row number.")
elif starting_row + num_rows > total_rows:
    print("The number of rows exceeds the total available rows.")
else:
    first_df = df.iloc[starting_row:starting_row + num_rows] 
    second_df = df.drop(first_df.index) 
    
    first_csv_path = 'Test_Fri_Aft_DDOS.csv'
    second_csv_path = 'Train_Fri_Aft_DDOS.csv'

    first_df.to_csv(first_csv_path, index=False)
    second_df.to_csv(second_csv_path, index=False)

    print(f"First CSV with rows from {starting_row} to {starting_row + num_rows - 1} saved as '{first_csv_path}'")
    print(f"Remaining CSV saved as '{second_csv_path}' with {len(second_df)} rows.")

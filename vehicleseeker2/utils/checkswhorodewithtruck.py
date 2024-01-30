import pandas as pd
import glob
import os


def load_and_process_excel_file(file_path):
    # Load the Excel file, skipping initial rows and setting correct headers
    df = pd.read_excel(file_path, header=3)  # Assuming the fourth row contains the headers

    # Rename columns to match the user's naming convention
    df = df.rename(columns={
        'Unnamed: 0': 'Vehicle',
        'Unnamed: 1': 'Route',
        'Unnamed: 2': 'Chauffeur',
        'Unnamed: 3': 'Milieuwerker1',
        'Unnamed: 4': 'Milieuwerker2'
    })

    # Extract date from filename
    base = os.path.basename(file_path)
    base, _ = os.path.splitext(base)
    date = pd.to_datetime(base, format='%d-%m-%Y')

    # Add the date as a new column
    df['Date'] = date

    return df

def search_vehicle(query, df):
    # Filter the DataFrame based on the query
    query_df = df[df.apply(lambda row: row.astype(str).str.contains(query).any(), axis=1)]

    # Return the filtered DataFrame
    return query_df



def load_and_combine_data():
    # Path to the folder containing all the excel files
    folder_path = '/Users/driesminoodt/PycharmProjects/WASTED4/data/shiftreports'

    # Create a list of all .xlsx files in the folder and its subfolders
    file_paths = glob.glob(os.path.join(folder_path, '**/*.xlsx'), recursive=True)

    # Load and process each file, then store the resulting DataFrames in a list
    dataframes = [load_and_process_excel_file(path) for path in file_paths]

    # Concatenate all dataframes into one
    combined_df = pd.concat(dataframes)

    # Cleaning up the DataFrame by keeping only the necessary columns and sorting by date
    columns_to_keep = ['Vehicle', 'Route', 'Chauffeur', 'Milieuwerker1', 'Milieuwerker2', 'Date']
    cleaned_df = combined_df[columns_to_keep]
    cleaned_df = cleaned_df.sort_values(by='Date', ascending=False)

    return cleaned_df


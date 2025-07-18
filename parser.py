import pickle
from pathlib import Path
import pandas as pd


def process_csv_files(base_path):
    """
    Process CSV files from 'control' and 'Amyloidosis' folders and create a DataFrame
    with time series data for each file.

    Args:
        base_path (str): Path to the directory containing the two folders

    Returns:
        pd.DataFrame: DataFrame with processed time series data
    """

    # Define the two folders
    folders = ['control', 'Amyloidosis']

    # List to store all processed data
    all_data = []

    for folder in folders:
        folder_path = Path(base_path) / folder

        if not folder_path.exists():
            print(f"Warning: Folder '{folder}' not found in {base_path}")
            continue

        # Get all CSV files in the folder
        csv_files = list(folder_path.glob('*.csv'))

        print(f"Processing {len(csv_files)} files from '{folder}' folder...")

        for csv_file in csv_files:
            try:
                # Read the CSV file
                df = pd.read_csv(csv_file, sep='\t')  # Using tab separator based on your example

                # Remove the 'measurement' column if it exists (it's always empty)
                if 'measurement' in df.columns:
                    df = df.drop('measurement', axis=1)

                # Extract time series data (all columns except 'samplenr')
                timeseries_columns = [col for col in df.columns if col != 'samplenr']

                # Create a dictionary for this file's data
                file_data = {
                    'filename': csv_file.name,
                    'filepath': str(csv_file),
                    'group': folder,  # 'control' or 'Amyloidosis'
                    'num_samples': len(df),
                }

                # Add each time series as a separate column in the final DataFrame
                for col in timeseries_columns:
                    file_data[f'timeseries_{col}'] = df[col].values.tolist()

                # Also store the sample numbers
                file_data['sample_numbers'] = df['samplenr'].values.tolist()

                all_data.append(file_data)

            except Exception as e:
                print(f"Error processing {csv_file}: {str(e)}")
                continue

    # Create the final DataFrame
    result_df = pd.DataFrame(all_data)

    return result_df


def save_dataframe_as_pickle(df, output_path):
    """
    Save the DataFrame as a pickle file.

    Args:
        df (pd.DataFrame): DataFrame to save
        output_path (str): Path where to save the pickle file
    """
    try:
        with open(output_path, 'wb') as f:
            pickle.dump(df, f)
        print(f"DataFrame saved successfully to {output_path}")
    except Exception as e:
        print(f"Error saving DataFrame: {str(e)}")


def main():
    # Set the base path where your folders are located
    base_path = "."  # Current directory - change this to your actual path

    # Process the CSV files
    print("Starting CSV processing...")
    df = process_csv_files(base_path)

    # Display summary information
    print(f"\nProcessing complete!")
    print(f"Total files processed: {len(df)}")
    print(f"Files by group:")
    if not df.empty:
        print(df['group'].value_counts())

        # Display first few rows info
        print(f"\nDataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        # Show sample of the data
        print(f"\nSample data:")
        print(df[['filename', 'group', 'num_samples']].head())

    # Save as pickle file
    output_file = "timeseries_data.pkl"
    save_dataframe_as_pickle(df, output_file)

    return df


def load_saved_dataframe(pickle_path):
    """
    Load the saved DataFrame from pickle file.

    Args:
        pickle_path (str): Path to the pickle file

    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    try:
        with open(pickle_path, 'rb') as f:
            df = pickle.load(f)
        print(f"DataFrame loaded successfully from {pickle_path}")
        return df
    except Exception as e:
        print(f"Error loading DataFrame: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Process files and create DataFrame
    df = main()


    # Example: How to access the time series data
    if not df.empty:
        print(f"\nExample of accessing time series data:")
        first_file = df.iloc[0]
        print(f"File: {first_file['filename']}")
        print(f"Group: {first_file['group']}")
        print(f"Lead I time series: {first_file['timeseries_I']}")
        print(f"Lead II time series: {first_file['timeseries_II']}")

        # Example: Load the saved DataFrame
        print(f"\nTesting pickle file loading...")
        loaded_df = load_saved_dataframe("timeseries_data.pkl")
        if loaded_df is not None:
            print(f"Loaded DataFrame shape: {loaded_df.shape}")

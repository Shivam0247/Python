import os
import json
import pandas as pd

def read_json_from_directories(directories):
    data = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        data.append(content)
    return data

def calculate_statistics(df):
    df.fillna(0, inplace=True)
    
    # Ensure columns are named correctly and process the data
    df['confirmed_cases'] = df['confirmed_cases'].apply(lambda x: x['total'] if isinstance(x, dict) else 0)
    df['deaths'] = df['deaths'].apply(lambda x: x['total'] if isinstance(x, dict) else 0)
    df['recovered'] = df['recovered'].apply(lambda x: x['total'] if isinstance(x, dict) else 0)
    
    stats = df.groupby('country').agg({
        'confirmed_cases': 'sum',
        'deaths': 'sum',
        'recovered': 'sum'
    }).reset_index()
    
    stats['active_cases'] = stats['confirmed_cases'] - stats['deaths'] - stats['recovered']
    return stats

def get_top_countries(stats, num=5):
    top_confirmed = stats.nlargest(num, 'confirmed_cases')
    lowest_confirmed = stats.nsmallest(num, 'confirmed_cases')
    
    # Debugging: Check if there are any rows in top_confirmed and lowest_confirmed
    print(f"\nTop {num} countries by confirmed cases (Largest):")
    print(top_confirmed)
    print(f"\nTop {num} countries by confirmed cases (Smallest):")
    print(lowest_confirmed)
    
    return top_confirmed, lowest_confirmed

def save_summary_to_json(stats, filename="covid19_summary.json"):
    summary = stats.to_dict(orient='records')
    with open(filename, 'w') as f:
        json.dump(summary, f, indent=4)
    print(f"\nSummary report saved to '{filename}'")

if __name__ == "__main__":
    directories = [
        r"C:\Data\workspace\Advance Python\Practical 4\China", 
        r"C:\Data\workspace\Advance Python\Practical 4\USA",
        r"C:\Data\workspace\Advance Python\Practical 4\Pakistan",
        r"C:\Data\workspace\Advance Python\Practical 4\India",
        r"C:\Data\workspace\Advance Python\Practical 4\Bangkok",
        r"C:\Data\workspace\Advance Python\Practical 4\Russia"
    ]

    # Read JSON data from the specified directories
    data = read_json_from_directories(directories)
    
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Check the DataFrame structure
    print("Initial DataFrame structure:")
    print(df.head())
    
    # Ensure columns are present
    if 'confirmed_cases' in df.columns and 'deaths' in df.columns and 'recovered' in df.columns:
        # Calculate statistics
        stats = calculate_statistics(df)
        
        # Display the statistics
        print("\nStatistics by Country:")
        print(stats)
        
        # Determine top 5 countries with highest and lowest confirmed cases
        top_confirmed, lowest_confirmed = get_top_countries(stats)
        
        # Save the statistics to a CSV file
        stats.to_csv("covid_statistics.csv", index=False)
        print("\nStatistics saved to 'covid_statistics.csv'")
        
        # Save the summary to a JSON file
        save_summary_to_json(stats)
    else:
        print("The required columns are missing from the DataFrame.")

print("ANALYSIS: ")  
print(df.info())      

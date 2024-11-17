import pandas as pd
import os


directories = ['April', 'July', 'June']

all_dataframes = []

# Loop through each directory
for directory in directories:
    
    if os.path.exists(directory):
        
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                
                file_path = os.path.join(directory, filename)
                
                df = pd.read_csv(file_path)
                
                all_dataframes.append(df)
    else:
        print(f"Directory not found: {directory}")

# Concatenate all the dataframes into a single dataframe if not empty
if all_dataframes:
    single_dataframe = pd.concat(all_dataframes, ignore_index=True)
    single_dataframe = single_dataframe.dropna(subset=['ProductID', 'StoreID'])  # Skip null values of ProductID and StoreID


    print("Concatenated DataFrame:")
    print(single_dataframe.head())

    total_sales_by_product = single_dataframe.groupby('ProductID')['Quantity'].sum().reset_index()

 
    print("Total Sales by Product:")
    print(total_sales_by_product.head())


    single_dataframe['Date'] = pd.to_datetime(single_dataframe['Date'], errors='coerce')  # Handle incorrect dates
    single_dataframe['YearMonth'] = single_dataframe['Date'].dt.to_period('M')


    months_count = single_dataframe.groupby('ProductID')['YearMonth'].nunique().reset_index()
    months_count.rename(columns={'YearMonth': 'MonthsCount'}, inplace=True)

    
    total_sales_with_months = total_sales_by_product.merge(months_count, on='ProductID')
    total_sales_with_months['AverageQuantityPerMonth'] = total_sales_with_months['Quantity'] / total_sales_with_months['MonthsCount']

   
    top_5_products = total_sales_with_months.sort_values(by='Quantity', ascending=False).head(5)


    product_names_path = "C:/Data/workspace/Advance Python/Practical 5/product_name.csv" 
    if os.path.exists(product_names_path):
        product_names_df = pd.read_csv(product_names_path)

        print("Product Names DataFrame Columns:")
        print(product_names_df.columns)


        if 'ProductID' in product_names_df.columns and 'productName' in product_names_df.columns:
            # Merge top 5 products with product names
            summary_df = top_5_products.merge(product_names_df, on='ProductID')

            # Select and rename columns for the final summary
            summary_df = summary_df[['ProductID', 'productName', 'Quantity', 'AverageQuantityPerMonth']]
            summary_df.rename(columns={'Quantity': 'TotalQuantitySold', 'productName': 'Product Name'}, inplace=True)

            # Write the summary to a new CSV file
            summary_df.to_csv('sales_summary.csv', index=False)

            # Print the summary DataFrame
            print("Sales Summary:")
            print(summary_df)
        else:
            print(f"Expected columns not found in product names file. Found columns: {product_names_df.columns}")

    else:
        print(f"Product names file not found: {product_names_path}")

else:
    print("No data to process.")


print(summary_df.describe())    

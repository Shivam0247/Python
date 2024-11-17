import pandas as pd

# Initialize a summary list and a dictionary to hold ratings
summary = []
ratings_dict = {}

# Initialize counters
total_reviews_processed = 0
valid_reviews_count = 0
invalid_reviews_count = 0

# Loop to read 5 CSV files
for i in range(1, 6):
    file_name = f"/Users/patelshivam/Documents/PythonLab/Advance Python/Practical 1/Data Sets/file{i}.csv"  # Generate file name
    
    try:
        # Read the CSV file using pandas, skipping bad lines
        df = pd.read_csv(file_name, on_bad_lines='skip')

        # Count total reviews processed
        total_reviews_processed += len(df)

        # Convert 'Review Rating' to numeric, forcing errors to NaN (if any)
        df['Review Rating'] = pd.to_numeric(df['Review Rating'])

        # Calculate average ratings for each product ID
        for index, row in df.iterrows():
            product_id = row['Product ID']
            rating = row['Review Rating']
            
            if pd.isna(rating):  # Skip NaN ratings
                invalid_reviews_count += 1
                continue
            
            valid_reviews_count += 1  # Increment valid review count
            
            if product_id in ratings_dict:
                ratings_dict[product_id]['total_rating'] += rating
                ratings_dict[product_id]['count'] += 1
            else:
                ratings_dict[product_id] = {'total_rating': rating, 'count': 1}

    except FileNotFoundError:
        summary.append(f'Error: {file_name} not found.')
    except Exception as e:
        summary.append(f'An error occurred while reading {file_name}: {e}')

# Calculate average ratings for each product ID
average_ratings = {}
summary.append('Average Ratings for Each Product ID:')
for product_id, data in ratings_dict.items():
    average_rating = data['total_rating'] / data['count']
    average_ratings[product_id] = average_rating
    summary.append(f'Product ID: {product_id}, Average Rating: {average_rating:.2f}')

# Calculate top 3 products by average rating
average_ratings_df = pd.DataFrame(list(average_ratings.items()), columns=['Product ID', 'Average Rating'])

# Sort the DataFrame by 'Average Rating' and get the top 3
top_3_products_df = average_ratings_df.sort_values(by='Average Rating', ascending=False).head(3)

# Convert the DataFrame back to a list of tuples
top_3_products = list(top_3_products_df.itertuples(index=False, name=None))

# Append summary statistics
summary.append('---')
summary.append(f'Total number of reviews processed: {total_reviews_processed}')
summary.append(f'Number of valid reviews: {valid_reviews_count}')
summary.append(f'Number of invalid reviews: {invalid_reviews_count}')
summary.append('Average rating of top 3 products with highest average ratings:')
for product_id, avg_rating in top_3_products:
    summary.append(f'Product ID: {product_id}, Average Rating: {avg_rating:.2f}')

# Write the summary to summary.txt
with open('summary.txt', 'w') as summary_file:
    for line in summary:
        summary_file.write(line + '\n')

print("Summary written to summary.txt")

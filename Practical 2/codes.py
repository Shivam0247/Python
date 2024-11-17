import pandas as pd

# Load trains data
file_path = r'C:\Data\workspace\Advance Python\Practical 2\trains.csv'
df = pd.read_csv(file_path)


print("Trains DataFrame:")
print(df)


print("\nMissing values in Trains DataFrame:")
print(df.isnull().sum())

# Fill missing values
df.fillna({
    'total_seats': 0,  # Assuming 0 for missing total seats
    'price': df['price'].mean()  
}, inplace=True)


file_path2 = r'C:\Data\workspace\Advance Python\Practical 2\passengers.csv'
df2 = pd.read_csv(file_path2)


print("\nPassengers DataFrame:")
print(df2)

# Check for missing values in the passengers DataFrame
print("\nMissing values in Passengers DataFrame:")
print(df2.isnull().sum())

# Fill missing values or drop rows based on your requirement
df2.fillna({
    'passenger_name': 'Unknown', 
    'train_id': 0  
}, inplace=True)

# Initialize total revenue and revenue per train
total_revenue = 0
revenue_per_train = {train_id: 0 for train_id in df['train_id']}

def seat_booking(train_id, requested_seats):
    global total_revenue  
    train = df[df['train_id'] == train_id]

    if not train.empty:
        available_seats = train['total_seats'].values[0]
        price_per_seat = train['price'].values[0]
        
        if available_seats >= requested_seats:
            df.loc[df['train_id'] == train_id, 'total_seats'] -= requested_seats
            booking_revenue = requested_seats * price_per_seat
            total_revenue += booking_revenue
            revenue_per_train[train_id] += booking_revenue
            print(f"\nBooking successful! {requested_seats} seats booked on train ID {train_id}. Revenue: Rs.{booking_revenue}")
        else:
            print(f"\nBooking failed! Only {available_seats} seats available on train ID {train_id}.")
    else:
        print(f"\nBooking failed! Train ID {train_id} does not exist.")

# Example usage
seat_booking(1, 50)
seat_booking(2, 200)
seat_booking(4, 10)
seat_booking(7, 15)

print("REPORT 1")
print("\nAvailable Chart:")
print(df)

print("REPORT 2:")

print("\nTotal Revenue per Train:")
for train_id, revenue in revenue_per_train.items():
    print(f"Train ID {train_id}: Rs{revenue}")

print(f"\nTotal Revenue: Rs.{total_revenue}")

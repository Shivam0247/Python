import logging
import os

# Set up logging configuration
LOG_FILE = "inventory.log"

logging.basicConfig(
    filename=LOG_FILE, 
    filemode="w", 
    format="%(asctime)s - %(levelname)s - %(message)s", 
    level=logging.DEBUG
)

# Simple inventory data structure
inventory = {}

# Function to check log file size
def check_log_file_size():
    try:
        file_size = os.path.getsize(LOG_FILE)
        max_size = 1 * 1024 * 1024  

        if file_size > max_size:
            logging.error("Log file exceeds 1MB.")
            raise Exception("Log file exceeds the maximum allowed size of 1MB.")
    except FileNotFoundError:
        logging.error("Log file not found.")
        raise

# Function to add a new item to the inventory
def add_item(item_name, quantity):
    logging.info(f"Attempting to add item: {item_name} with quantity: {quantity}")
    
    try:
        check_log_file_size()  # Check log file size before proceeding

        if item_name in inventory:
            logging.warning(f"Item {item_name} already exists. Use update_item instead.")
            return "Item already exists. Use update_item instead."
        
        inventory[item_name] = quantity
        logging.debug(f"Item {item_name} added successfully with quantity {quantity}")
        return f"Item {item_name} added successfully."

    except Exception as e:
        logging.error(f"Error adding item: {str(e)}")
        raise

# Function to update the quantity of an existing item
def update_item(item_name, quantity):
    logging.info(f"Attempting to update item: {item_name} with new quantity: {quantity}")
    
    try:
        check_log_file_size()  # Check log file size before proceeding

        if item_name not in inventory:
            logging.warning(f"Item {item_name} does not exist in inventory.")
            return "Item does not exist. Use add_item instead."

        inventory[item_name] += quantity
        logging.debug(f"Item {item_name} updated successfully. New quantity: {inventory[item_name]}")
        return f"Item {item_name} updated successfully."

    except Exception as e:
        logging.error(f"Error updating item: {str(e)}")
        raise

# Function to retrieve the current inventory
def get_inventory():
    logging.info("Fetching current inventory")
    
    try:
        check_log_file_size()  # Check log file size before proceeding

        if not inventory:
            logging.info("Inventory is empty.")
            return "Inventory is currently empty."

        logging.debug(f"Current inventory: {inventory}")
        return inventory

    except Exception as e:
        logging.error(f"Error fetching inventory: {str(e)}")
        raise

# Function to remove an item from the inventory
def remove_item(item_name):
    logging.info(f"Attempting to remove item: {item_name}")
    
    try:
        check_log_file_size()  # Check log file size before proceeding

        if item_name not in inventory:
            logging.warning(f"Item {item_name} does not exist in inventory.")
            return "Item does not exist."

        del inventory[item_name]
        logging.debug(f"Item {item_name} removed successfully.")
        return f"Item {item_name} removed successfully."

    except Exception as e:
        logging.error(f"Error removing item: {str(e)}")
        raise

# Main function to demonstrate the inventory system with logging
def main():
    logging.info("Application started")

    try:
        # Add items to inventory
        print(add_item("Laptop", 10))
        print(add_item("Phone", 15))
        print(add_item("Laptop", 5))  # This should trigger a warning

        # Update item stock
        print(update_item("Phone", 5))
        print(update_item("Tablet", 10))  # This should trigger a warning

        # Retrieve current inventory
        print(get_inventory())

        # Remove an item
        print(remove_item("Laptop"))
        print(remove_item("Camera"))  # This should trigger a warning

        # Fetch final inventory
        print(get_inventory())

    except Exception as e:
        logging.error(f"Application encountered an error: {str(e)}")

    logging.info("Application finished")

if __name__ == "__main__":
    main()

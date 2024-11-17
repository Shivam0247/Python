import logging

logging.basicConfig(
    filename="library.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

library = {}

def add_book(book_title, quantity):
    logging.info(f"Attempting to add book: {book_title} with quantity: {quantity}")
    
    try:
        if book_title in library:
            logging.warning(f"Book {book_title} already exists. Use update_book instead.")
            return "Book already exists. Use update_book instead."
        
        library[book_title] = quantity
        logging.debug(f"Book {book_title} added successfully with quantity {quantity}")
        return f"Book {book_title} added successfully."

    except Exception as e:
        logging.error(f"Error adding book: {str(e)}")
        raise

def update_book(book_title, quantity):
    logging.info(f"Attempting to update book: {book_title} with new quantity: {quantity}")
    
    try:
        if book_title not in library:
            logging.warning(f"Book {book_title} does not exist in library.")
            return "Book does not exist. Use add_book instead."

        library[book_title] += quantity
        logging.debug(f"Book {book_title} updated successfully. New quantity: {library[book_title]}")
        return f"Book {book_title} updated successfully."

    except Exception as e:
        logging.error(f"Error updating book: {str(e)}")
        raise

def get_library():
    logging.info("Fetching current library")
    
    try:
        if not library:
            logging.info("Library is empty.")
            return "Library is currently empty."

        logging.debug(f"Current library: {library}")
        return library

    except Exception as e:
        logging.error(f"Error fetching library: {str(e)}")
        raise

def remove_book(book_title):
    logging.info(f"Attempting to remove book: {book_title}")
    
    try:
        if book_title not in library:
            logging.warning(f"Book {book_title} does not exist in library.")
            return "Book does not exist."

        del library[book_title]
        logging.debug(f"Book {book_title} removed successfully.")
        return f"Book {book_title} removed successfully."

    except Exception as e:
        logging.error(f"Error removing book: {str(e)}")
        raise

def main():
    logging.info("Application started")

    try:
        # Add books to library
        print(add_book("The Great Gatsby", 10))
        print(add_book("1984", 15))
        print(add_book("The Great Gatsby", 5))  

        print(update_book("1984", 5))
        print(update_book("To Kill a Mockingbird", 10))  

        print(get_library())

        # Remove a book
        print(remove_book("The Great Gatsby"))
        print(remove_book("Moby Dick"))  

        # Fetch final library
        print(get_library())

    except Exception as e:
        logging.error(f"Application encountered an error: {str(e)}")

    logging.info("Application finished")

if __name__ == "__main__":
    main()

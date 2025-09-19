import json
import time

def load_books():
    """Reads the books.json file and returns a list of book dictionaries."""
    try:
        with open('books.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    

def save_books(books):
    """Takes a list of book dictionaries and writes it to the books.json file."""
    with open('books.json', 'w') as f:
        json.dump(books, f, indent=2)

def recommend_related_books(target_book, all_books, checked_ids=None):
    """
    Recursively finds related books from the same department.
    """
    if checked_ids is None:
        checked_ids = {target_book['id']}

    recommendations = []
    for book in all_books:
        if (book['department'] == target_book['department'] and 
            book['id'] not in checked_ids):
            
            recommendations.append(book)
            checked_ids.add(book['id'])
            recommendations.extend(recommend_related_books(book, all_books, checked_ids))
            break
    return recommendations
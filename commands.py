import sys
import uuid
from datetime import datetime

from persistence import BookmarkDatabase

persistence = BookmarkDatabase()


class CreateBookmarksTableCommand:
    def execute(self):  
        db.create_table('bookmarks', {
            'id': 'VARCHAR(36) PRIMARY KEY',
            'title': 'VARCHAR(255) NOT NULL',
            'url': 'VARCHAR(255) NOT NULL',
            'notes': 'VARCHAR(500)',
            'date_added': 'VARCHAR(50) NOT NULL',
        })


class AddBookmarkCommand:
    def execute(self, data, timestamp=None):
        data['id'] = str(uuid.uuid4())
        data['date_added'] = timestamp or datetime.utcnow().isoformat()  
        persistence.create(data)
        return True, None  


class ListBookmarksCommand:
    def __init__(self, order_by='date_added'): 
        self.order_by = order_by

    def execute(self, data=None):
        return True, persistence.list(order_by=self.order_by)  


class DeleteBookmarkCommand:
    def execute(self, data):
        persistence.delete(data)
        return True, None


class EditBookmarkCommand:
    def execute(self, data):
        persistence.edit(data['id'], data['update'])
        return True, None


class QuitCommand:
    def execute(self, data=None):
        sys.exit() 
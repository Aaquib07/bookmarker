from abc import ABC, abstractmethod

from database import DatabaseManager


class PersistenceLayer(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError('Persistence Layers must implement a create method')
    
    @abstractmethod
    def list(self, order_by=None):
        raise NotImplementedError('Persistence Layers must implement a list method')

    @abstractmethod
    def edit(self, bookmark_id, bookmark_data):
        raise NotImplementedError('Persistence Layers must implement an edit method')
    
    @abstractmethod
    def delete(self, bookmark_id):
        raise NotImplementedError('Persistence Layers must implement a delete method')


class BookmarkDatabase(PersistenceLayer):
    def __init__(self):
        self.table_name = 'bookmarks'
        self.db = DatabaseManager('bookmark')
        
        self.db.create_table(self.table_name, {
            'id': 'VARCHAR(36) PRIMARY KEY',
            'title': 'VARCHAR(255) NOT NULL',
            'url': 'VARCHAR(255) NOT NULL',
            'notes': 'VARCHAR(500)',
            'date_added': 'VARCHAR(50) NOT NULL',
        })

    def create(self, bookmark_data):
        self.db.add(self.table_name, bookmark_data)
    
    def list(self, order_by=None):
        return self.db.select(self.table_name, order_by=order_by)
    
    def edit(self, bookmark_id, bookmark_data):
        self.db.update(self.table_name, {'id': bookmark_id}, bookmark_data)

    def delete(self, bookmark_id):
        self.db.delete(self.table_name, {'id': bookmark_id})
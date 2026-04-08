# Database initialization module
from .client import db_client, db, users_collection

__all__ = ['db_client', 'db', 'users_collection']

class DatabaseError(Exception):
    """Exception raised when a database-related error occurs"""
    pass

class NoAcquiredConnectionError(DatabaseError):
    """Exception raised when no acquired connection is available to release"""
    def __init__(self):
        super().__init__("No acquired connection to be released")

class CannotExecuteQueryError(DatabaseError):
    """Exception raised when a condition for executing the query fails"""
    pass
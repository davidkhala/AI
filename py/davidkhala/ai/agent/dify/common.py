from enum import Enum


class IndexingStatus(str, Enum):
    WAITING = "waiting"
    PARSING = "parsing"
    SPLITTING = 'splitting'
    INDEXING = "indexing"
    COMPLETED = "completed"
    FAILED = "error"

class IndexingError(Exception):
    """Raised when document indexing fails (indexing_status = 'error')"""
    pass
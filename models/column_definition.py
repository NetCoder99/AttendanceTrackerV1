import enum
from pydantic import BaseModel

class ColumnType(enum.Enum):
    NULL = "NULL"
    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"

class NewColumnDefinition(BaseModel):
    column_name: str
    column_type: ColumnType
    is_primary: bool = False
    is_autoincrement: bool = False
    is_nullable: bool = False

    @classmethod
    def fromSqlAlchemy(cls, column_definition):
        return_rec = NewColumnDefinition.model_construct()
        return_rec.column_name       = column_definition.name
        return_rec.column_type       = column_definition.type
        return_rec.is_primary        = column_definition.primary_key
        return_rec.is_autoincrement  = column_definition.identity
        return_rec.is_nullable       = column_definition.nullable
        return return_rec
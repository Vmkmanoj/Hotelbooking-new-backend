from enum import Enum


class BedType(str, Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    QUEEN = "QUEEN"
    KING = "KING"
    TWIN = "TWIN"
    SOFA_BED = "SOFA_BED"
    BUNK = "BUNK"
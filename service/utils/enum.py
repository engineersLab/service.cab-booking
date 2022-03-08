"""
enums to replace hardcoded values and avoid db calls
"""
DEV_TYPE = {1: "frontend", 2: "backend"}
CAB_TYPE = {"f": 1, "b": 2, "fb": 3}
RESERVED_FOR = {"any": "fb", "frontend": "f", "backend": "b"}

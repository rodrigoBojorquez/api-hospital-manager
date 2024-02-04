from bson import ObjectId as _ObjectId

# VALIDATORS

def check_object_id(val: str) -> str:
    if not _ObjectId.is_valid(val):
        raise ValueError("invalid ObjectId")
    return val
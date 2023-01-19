from typing import Dict
from flask import abort


def is_request_valid(obj: object, data: Dict):
    if not data:
        abort(400, description="No data passed in JSON body")

    invalid_properties = [key for key in data.keys() if key not in obj.__dict__]

    if invalid_properties:
        abort(400, description=f"Invalid property(-ies) in request: {','.join(invalid_properties)}")


def update_instance(obj: object, data: Dict):
    for k, v in data.items():
        setattr(obj, k, v)
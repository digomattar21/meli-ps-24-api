def checkFieldType(param, value, expected_type):
    if isinstance(expected_type, type):
        if not isinstance(value, expected_type):
            return False, f"Parameter {param} is expected to be of type {expected_type.__name__}, but got {type(value).__name__}"
    elif isinstance(expected_type, list):
        if not isinstance(value, list):
            return False, f"Parameter {param} should be a list, but got {type(value).__name__}"
        if not all(isinstance(item, expected_type[0]) for item in value):
            return False, f"All items in parameter {param} should be of type {expected_type[0].__name__}"
    elif isinstance(expected_type, dict):
        if "enum" in expected_type:
            if isinstance(value, list):
                if not all(item in expected_type["enum"] for item in value):
                    return False, f"All elements in parameter {param} must be one of {expected_type['enum']}, but got {value}"
            elif value not in expected_type["enum"]:
                return False, f"Parameter {param} must be one of {expected_type['enum']}, but got {value}"
    return True, None

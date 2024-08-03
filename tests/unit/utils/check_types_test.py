import pytest

from utils.checkTypes import checkFieldType  

def test_check_field_type_with_correct_type():
    result, error = checkFieldType("age", 25, int)
    assert result is True
    assert error is None

def test_check_field_type_with_incorrect_type():
    result, error = checkFieldType("age", "25", int)
    assert result is False
    assert error == "Parameter age is expected to be of type int, but got str"

def test_check_field_type_with_list_correct_type():
    result, error = checkFieldType("numbers", [1, 2, 3], [int])
    assert result is True
    assert error is None

def test_check_field_type_with_list_incorrect_type():
    result, error = checkFieldType("numbers", [1, "two", 3], [int])
    assert result is False
    assert error == "All items in parameter numbers should be of type int"

def test_check_field_type_with_dict_enum_correct():
    result, error = checkFieldType("status", "active", {"enum": ["active", "inactive", "pending"]})
    assert result is True
    assert error is None

def test_check_field_type_with_dict_enum_incorrect():
    result, error = checkFieldType("status", "archived", {"enum": ["active", "inactive", "pending"]})
    assert result is False
    assert error == "Parameter status must be one of ['active', 'inactive', 'pending'], but got archived"

def test_check_field_type_with_list_enum_correct():
    result, error = checkFieldType("roles", ["admin", "user"], {"enum": ["admin", "user", "guest"]})
    assert result is True
    assert error is None

def test_check_field_type_with_list_enum_incorrect():
    result, error = checkFieldType("roles", ["admin", "owner"], {"enum": ["admin", "user", "guest"]})
    assert result is False
    assert error == "All elements in parameter roles must be one of ['admin', 'user', 'guest'], but got ['admin', 'owner']"

if __name__ == "__main__":
    pytest.main()

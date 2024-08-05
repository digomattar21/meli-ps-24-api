from utils.apiMessages import LocalApiCode, error_message

invalid_severity_bodies = [
    (
        {},  # Empty body
        {
            "errors": [error_message(LocalApiCode.emptyRequest, language="portuguese")]
        },  # Invalid
    ),
    (
        {"level": 0},  # Invalid level
        {
            "errors": [
                error_message(LocalApiCode.invalidSeverityLevel, language="portuguese")
            ]
        },
    ),
    (
        {"level": 5},  # Out of range level
        {
            "errors": [
                error_message(LocalApiCode.invalidSeverityLevel, language="portuguese")
            ]
        },
    ),
    (
        {"level": "high"},  # Non-integer level
        {
            "errors": [
                error_message(LocalApiCode.invalidSeverityLevel, language="portuguese")
            ]
        },
    ),
    (
        {"level": None},  # None level
        {
            "errors": [
                error_message(LocalApiCode.invalidSeverityLevel, language="portuguese")
            ]
        },
    ),
]

invalid_category_bodies = [
    (
        {},  # Empty body
        {"errors": [error_message(LocalApiCode.emptyRequest, language="portuguese")]},
    ),
    (
        {"name": ""},  # Empty name
        {
            "errors": [
                error_message(LocalApiCode.invalidCategoryName, language="portuguese")
            ]
        },
    ),
    (
        {"name": None},  # None as name
        {
            "errors": [
                error_message(LocalApiCode.invalidCategoryName, language="portuguese")
            ]
        },
    ),
    (
        {"parent_id": 999},  # No name in json
        {"errors": [error_message(LocalApiCode.invalidJson, language="portuguese")]},
    ),
    (
        {"name": "testandodoooo", "parent_id": 999},  # Non-existent parent_id
        {
            "errors": [
                error_message(LocalApiCode.invalidParentCategory, language="portuguese")
            ]
        },
    ),
    (
        {"name": "Valid Name", "parent_id": "invalid"},  # Invalid parent_id type
        {"errors": ["Parameter parent_id is expected to be of type int, but got str"]},
    ),
]

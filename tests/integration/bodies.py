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

invalid_ticket_bodies = [
    (
        {},  # Empty body
        {"errors": [error_message(LocalApiCode.emptyRequest, language="portuguese")]},
    ),
    (
        {
            "title": "",  # Empty title
            "description": "This is a test ticket",
            "severity_id": 2,
            "category_id": 1,
            "subcategory_id": 6,
        },
        {"errors": [error_message(LocalApiCode.invalidTitle, language="portuguese")]},
    ),
    (
        {
            "title": "Test Ticket",
            "description": "",  # Empty description
            "severity_id": 2,
            "category_id": 1,
            "subcategory_id": 6,
        },
        {
            "errors": [
                error_message(LocalApiCode.invalidDescription, language="portuguese")
            ]
        },
    ),
    (
        {
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "severity_id": 99,  # Invalid severity_id
            "category_id": 1,
            "subcategory_id": 6,
        },
        {"errors": [error_message(LocalApiCode.severityNotFound)]},
    ),
    (
        {
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "severity_id": 2,
            "category_id": 99,  # Invalid category_id
            "subcategory_id": 6,
        },
        {"errors": [error_message(LocalApiCode.categoryNotFound)]},
    ),
    (
        {
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "severity_id": 2,
            "category_id": 1,
            "subcategory_id": 99,  # Invalid subcategory_id
        },
        {"errors": [error_message(LocalApiCode.invalidSubcategory)]},
    ),
    (
        {
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "severity_id": "High",  # Invalid severity_id type
            "category_id": 1,
            "subcategory_id": 6,
        },
        {
            "errors": [
                "Parameter severity_id is expected to be of type int, but got str"
            ]
        },
    ),
]

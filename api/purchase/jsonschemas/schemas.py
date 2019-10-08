ping_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Ping response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status": {"type": "string"}
    },
    "required": ["message", "status"]
}

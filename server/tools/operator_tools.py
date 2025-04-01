def get_operator_tools():
    """Définitions des outils pour manipuler les opérateurs"""
    return [
        {
            "name": "create_operator",
            "description": "Create a new operator in TouchDesigner",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_type": {
                        "type": "string",
                        "description": "Type of operator to create",
                        "enum": ["circle", "box", "noise", "text", "movie", "constant", "null", "feedback"]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the new operator"
                    },
                    "parent_path": {
                        "type": "string",
                        "description": "Path to the parent container (default: /)",
                        "default": "/"
                    },
                    "position": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "X position"},
                            "y": {"type": "number", "description": "Y position"}
                        }
                    }
                },
                "required": ["operator_type"]
            }
        },
        {
            "name": "delete_operator",
            "description": "Delete an operator from the network",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_path": {
                        "type": "string",
                        "description": "Full path to the operator"
                    }
                },
                "required": ["operator_path"]
            }
        },
        {
            "name": "connect_operators",
            "description": "Connect two operators together",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "Path to the source operator"
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "Path to the destination operator"
                    },
                    "output_index": {
                        "type": "integer",
                        "description": "Output index on source (default: 0)",
                        "default": 0
                    },
                    "input_index": {
                        "type": "integer",
                        "description": "Input index on destination (default: 0)",
                        "default": 0
                    }
                },
                "required": ["source_path", "destination_path"]
            }
        },
        # Plus d'outils...
    ]
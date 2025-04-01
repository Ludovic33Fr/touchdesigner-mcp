def get_parameter_tools():
    """Définitions des outils pour manipuler les paramètres"""
    return [
        {
            "name": "set_parameter",
            "description": "Set a parameter value on an operator",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_path": {
                        "type": "string",
                        "description": "Path to the operator"
                    },
                    "parameter_name": {
                        "type": "string",
                        "description": "Name of the parameter to set"
                    },
                    "value": {
                        "type": ["number", "string", "boolean", "array"],
                        "description": "Value to set for the parameter"
                    }
                },
                "required": ["operator_path", "parameter_name", "value"]
            }
        },
        {
            "name": "get_parameter",
            "description": "Get a parameter value from an operator",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_path": {
                        "type": "string",
                        "description": "Path to the operator"
                    },
                    "parameter_name": {
                        "type": "string",
                        "description": "Name of the parameter to get"
                    }
                },
                "required": ["operator_path", "parameter_name"]
            }
        },
        {
            "name": "pulse_parameter",
            "description": "Pulse a parameter on an operator",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_path": {
                        "type": "string",
                        "description": "Path to the operator"
                    },
                    "parameter_name": {
                        "type": "string",
                        "description": "Name of the parameter to pulse"
                    }
                },
                "required": ["operator_path", "parameter_name"]
            }
        },
        {
            "name": "create_parameter",
            "description": "Create a custom parameter on a component",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_path": {
                        "type": "string",
                        "description": "Path to the component operator"
                    },
                    "parameter_name": {
                        "type": "string",
                        "description": "Name for the new parameter"
                    },
                    "parameter_type": {
                        "type": "string",
                        "description": "Type of parameter",
                        "enum": ["float", "int", "string", "menu", "toggle", "pulse", "rgb", "rgba", "uv", "uvw", "xyz", "vector"]
                    },
                    "default_value": {
                        "type": ["number", "string", "boolean", "array"],
                        "description": "Default value for the parameter"
                    },
                    "label": {
                        "type": "string",
                        "description": "Display label for the parameter"
                    },
                    "min": {
                        "type": "number",
                        "description": "Minimum value (for numeric parameters)"
                    },
                    "max": {
                        "type": "number",
                        "description": "Maximum value (for numeric parameters)"
                    },
                    "menu_items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Menu items (for menu parameters)"
                    }
                },
                "required": ["operator_path", "parameter_name", "parameter_type"]
            }
        }
    ]
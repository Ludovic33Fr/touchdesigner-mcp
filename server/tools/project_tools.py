def get_project_tools():
    """Définitions des outils pour gérer les projets TouchDesigner"""
    return [
        {
            "name": "save_project",
            "description": "Save the current TouchDesigner project",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path where to save the project (default: current path)",
                    },
                    "increment": {
                        "type": "boolean",
                        "description": "Whether to increment the filename",
                        "default": False
                    }
                }
            }
        },
        {
            "name": "load_project",
            "description": "Load a TouchDesigner project",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the .toe file to load"
                    }
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "create_container",
            "description": "Create a new container COMP",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the new container"
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
                "required": ["name"]
            }
        },
        {
            "name": "take_screenshot",
            "description": "Take a screenshot of a specific operator or the entire network",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_path": {
                        "type": "string",
                        "description": "Path to the operator (default: current network)",
                        "default": ""
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path where to save the screenshot"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Width of the screenshot in pixels",
                        "default": 1920
                    },
                    "height": {
                        "type": "integer",
                        "description": "Height of the screenshot in pixels",
                        "default": 1080
                    }
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "run_script",
            "description": "Run a Python script in the TouchDesigner context",
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["script"]
            }
        },
        {
            "name": "get_project_info",
            "description": "Get information about the current project",
            "parameters": {
                "type": "object",
                "properties": {
                    "include_operators": {
                        "type": "boolean",
                        "description": "Whether to include operator list",
                        "default": False
                    }
                }
            }
        },
        {
            "name": "export_movie",
            "description": "Export a movie from a TOP operator",
            "parameters": {
                "type": "object",
                "properties": {
                    "operator_path": {
                        "type": "string",
                        "description": "Path to the TOP operator"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path where to save the movie"
                    },
                    "codec": {
                        "type": "string",
                        "description": "Codec to use",
                        "enum": ["H264", "MJPEG", "ProRes", "HAP"],
                        "default": "H264"
                    },
                    "frame_rate": {
                        "type": "number",
                        "description": "Frame rate of the exported movie",
                        "default": 30
                    },
                    "duration": {
                        "type": "number",
                        "description": "Duration in seconds",
                        "default": 10
                    }
                },
                "required": ["operator_path", "file_path"]
            }
        }
    ]
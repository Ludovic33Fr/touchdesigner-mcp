from typing import Any, Dict, List, Optional, Union
import subprocess
import socket
import json
import time
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server for controlling TouchDesigner
mcp = FastMCP("touchdesigner_control")

# Constants
DEFAULT_TOUCHDESIGNER_PATH = r"C:\Program Files\Derivative\TouchDesigner\bin\TouchDesigner.exe"
DEFAULT_PORT = 9980  # Default TouchDesigner Python port

# Global connection state
connection = {
    "td_process": None,
    "td_socket": None,
    "host": "localhost",
    "port": DEFAULT_PORT,
    "connected": False,
    "project_path": None
}

def connect_to_touchdesigner(host="localhost", port=DEFAULT_PORT) -> bool:
    """Establish a connection to TouchDesigner via Python socket."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        connection["td_socket"] = sock
        connection["host"] = host
        connection["port"] = port
        connection["connected"] = True
        return True
    except Exception as e:
        connection["connected"] = False
        return False

def disconnect_from_touchdesigner() -> bool:
    """Close the connection to TouchDesigner."""
    if connection["td_socket"]:
        try:
            connection["td_socket"].close()
        except:
            pass
    connection["td_socket"] = None
    connection["connected"] = False
    return True

def send_python_command(command: str) -> Dict[str, Any]:
    """Send a Python command to TouchDesigner and get the result."""
    if not connection["connected"] or not connection["td_socket"]:
        return {"success": False, "result": None, "error": "Not connected to TouchDesigner"}
    
    try:
        # Prepare the command for proper execution in TouchDesigner
        wrapped_command = f"""
try:
    __td_result = None
    __td_error = None
    __td_result = {command}
except Exception as e:
    __td_error = str(e)

import json
__td_response = {{"result": __td_result, "error": __td_error}}
json.dumps(__td_response)
"""
        connection["td_socket"].sendall(wrapped_command.encode('utf-8'))
        
        # Get response
        data = b""
        while True:
            chunk = connection["td_socket"].recv(4096)
            data += chunk
            if chunk.endswith(b'\n') or not chunk:
                break
        
        # Parse response
        response_str = data.decode('utf-8').strip()
        try:
            response = json.loads(response_str)
            return {"success": response["error"] is None, "result": response["result"], "error": response["error"]}
        except json.JSONDecodeError:
            # If we can't parse JSON, return the raw response
            return {"success": True, "result": response_str, "error": None}
    except Exception as e:
        return {"success": False, "result": None, "error": str(e)}

@mcp.tool()
async def launch_touchdesigner(path: Optional[str] = None, project: Optional[str] = None) -> Dict[str, Any]:
    """Launch TouchDesigner application.
    
    Args:
        path: Path to TouchDesigner executable (optional)
        project: Path to .toe project file to open (optional)
    """
    result = {"success": False, "message": ""}
    
    try:
        # Use provided path or default
        td_path = path if path else DEFAULT_TOUCHDESIGNER_PATH
        
        # Validate path exists
        if not os.path.exists(td_path):
            result["message"] = f"TouchDesigner executable not found at: {td_path}"
            return result
        
        cmd = [td_path]
        
        # Add project if specified
        if project:
            if not os.path.exists(project):
                result["message"] = f"Project file not found at: {project}"
                return result
            cmd.append(project)
            connection["project_path"] = project
        
        # Add Python network interface parameter
        cmd.extend(["-pythonnetport", str(DEFAULT_PORT)])
        
        # Launch TouchDesigner
        connection["td_process"] = subprocess.Popen(cmd)
        
        # Give it time to start up
        time.sleep(5)
        
        # Try to connect
        if connect_to_touchdesigner():
            result["success"] = True
            result["message"] = "TouchDesigner launched successfully and connected via Python port."
        else:
            result["message"] = "TouchDesigner launched, but failed to connect to Python port."
        
        return result
    except Exception as e:
        result["message"] = f"Failed to launch TouchDesigner: {str(e)}"
        return result

@mcp.tool()
async def connect(host: str = "localhost", port: int = DEFAULT_PORT) -> Dict[str, Any]:
    """Connect to a running TouchDesigner instance.
    
    Args:
        host: Hostname or IP address (default: localhost)
        port: Python port (default: 9980)
    """
    result = {"success": False, "message": ""}
    
    # Disconnect if already connected
    if connection["connected"]:
        disconnect_from_touchdesigner()
    
    # Try to connect
    if connect_to_touchdesigner(host, port):
        result["success"] = True
        result["message"] = f"Successfully connected to TouchDesigner at {host}:{port}"
    else:
        result["message"] = f"Failed to connect to TouchDesigner at {host}:{port}"
    
    return result

@mcp.tool()
async def disconnect() -> Dict[str, Any]:
    """Disconnect from TouchDesigner."""
    result = {"success": False, "message": ""}
    
    if connection["connected"]:
        disconnect_from_touchdesigner()
        result["success"] = True
        result["message"] = "Successfully disconnected from TouchDesigner"
    else:
        result["message"] = "Not connected to TouchDesigner"
    
    return result

@mcp.tool()
async def close_touchdesigner() -> Dict[str, Any]:
    """Close the TouchDesigner application."""
    result = {"success": False, "message": ""}
    
    if connection["connected"]:
        # Try to close gracefully first
        command_result = send_python_command("op.quit()")
        disconnect_from_touchdesigner()
        
        # If process was launched by us, make sure it's terminated
        if connection["td_process"]:
            try:
                connection["td_process"].terminate()
                connection["td_process"].wait(timeout=5)
            except:
                try:
                    connection["td_process"].kill()
                except:
                    pass
            connection["td_process"] = None
        
        result["success"] = True
        result["message"] = "TouchDesigner closed successfully"
    else:
        result["message"] = "Not connected to TouchDesigner"
    
    return result

@mcp.tool()
async def execute_python(code: str) -> Dict[str, Any]:
    """Execute arbitrary Python code in TouchDesigner.
    
    Args:
        code: Python code to execute
    """
    result = {"success": False, "message": "", "result": None}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command_result = send_python_command(code)
    result["success"] = command_result["success"]
    result["result"] = command_result["result"]
    
    if not command_result["success"]:
        result["message"] = f"Error executing code: {command_result['error']}"
    else:
        result["message"] = "Code executed successfully"
    
    return result

@mcp.tool()
async def save_project(path: Optional[str] = None) -> Dict[str, Any]:
    """Save the current TouchDesigner project.
    
    Args:
        path: Path to save the project (optional, uses current path if not specified)
    """
    result = {"success": False, "message": ""}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    try:
        if path:
            command = f'op.project.save("{path}")'
        else:
            command = 'op.project.save()'
        
        command_result = send_python_command(command)
        result["success"] = command_result["success"]
        
        if result["success"]:
            result["message"] = f"Project saved successfully"
            if path:
                connection["project_path"] = path
        else:
            result["message"] = f"Failed to save project: {command_result['error']}"
        
        return result
    except Exception as e:
        result["message"] = f"Error saving project: {str(e)}"
        return result

@mcp.tool()
async def create_operator(op_type: str, parent_path: str, name: str) -> Dict[str, Any]:
    """Create a new operator in TouchDesigner.
    
    Args:
        op_type: Operator type (e.g., 'container', 'moviefilein', 'text')
        parent_path: Path to parent operator
        name: Name for the new operator
    """
    result = {"success": False, "message": "", "operator_path": ""}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command = f'op("{parent_path}").create({op_type}, "{name}")'
    command_result = send_python_command(command)
    
    if command_result["success"]:
        result["success"] = True
        result["message"] = f"Operator {name} created successfully"
        result["operator_path"] = f"{parent_path}/{name}"
    else:
        result["message"] = f"Failed to create operator: {command_result['error']}"
    
    return result

@mcp.tool()
async def delete_operator(op_path: str) -> Dict[str, Any]:
    """Delete an operator in TouchDesigner.
    
    Args:
        op_path: Path to the operator to delete
    """
    result = {"success": False, "message": ""}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command = f'op("{op_path}").destroy()'
    command_result = send_python_command(command)
    
    if command_result["success"]:
        result["success"] = True
        result["message"] = f"Operator {op_path} deleted successfully"
    else:
        result["message"] = f"Failed to delete operator: {command_result['error']}"
    
    return result

@mcp.tool()
async def set_parameter(op_path: str, parameter: str, value: Any) -> Dict[str, Any]:
    """Set a parameter value on an operator.
    
    Args:
        op_path: Path to the operator
        parameter: Parameter name
        value: New parameter value
    """
    result = {"success": False, "message": ""}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    # Convert value to proper format based on type
    if isinstance(value, str):
        formatted_value = f'"{value}"'
    elif isinstance(value, (list, tuple)):
        formatted_value = str(value)
    else:
        formatted_value = str(value)
    
    command = f'op("{op_path}").par.{parameter} = {formatted_value}'
    command_result = send_python_command(command)
    
    if command_result["success"]:
        result["success"] = True
        result["message"] = f"Parameter {parameter} set successfully on {op_path}"
    else:
        result["message"] = f"Failed to set parameter: {command_result['error']}"
    
    return result

@mcp.tool()
async def get_parameter(op_path: str, parameter: str) -> Dict[str, Any]:
    """Get a parameter value from an operator.
    
    Args:
        op_path: Path to the operator
        parameter: Parameter name
    """
    result = {"success": False, "message": "", "value": None}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command = f'op("{op_path}").par.{parameter}.eval()'
    command_result = send_python_command(command)
    
    if command_result["success"]:
        result["success"] = True
        result["value"] = command_result["result"]
        result["message"] = f"Parameter {parameter} retrieved successfully from {op_path}"
    else:
        result["message"] = f"Failed to get parameter: {command_result['error']}"
    
    return result

@mcp.tool()
async def list_operators(parent_path: str = "/") -> Dict[str, Any]:
    """List all operators under a specified path.
    
    Args:
        parent_path: Path to the parent operator (default: root)
    """
    result = {"success": False, "message": "", "operators": []}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command = f"""
[{{"name": child.name, 
   "path": child.path,
   "type": child.type,
   "valid": child.valid}} 
 for child in op("{parent_path}").findChildren(depth=1)]
"""
    command_result = send_python_command(command)
    
    if command_result["success"]:
        result["success"] = True
        result["operators"] = command_result["result"]
        result["message"] = f"Listed {len(command_result['result'])} operators under {parent_path}"
    else:
        result["message"] = f"Failed to list operators: {command_result['error']}"
    
    return result

@mcp.tool()
async def cook_operator(op_path: str) -> Dict[str, Any]:
    """Force an operator to cook (update).
    
    Args:
        op_path: Path to the operator
    """
    result = {"success": False, "message": ""}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command = f'op("{op_path}").cook(force=True)'
    command_result = send_python_command(command)
    
    if command_result["success"]:
        result["success"] = True
        result["message"] = f"Operator {op_path} cooked successfully"
    else:
        result["message"] = f"Failed to cook operator: {command_result['error']}"
    
    return result

@mcp.tool()
async def get_operator_info(op_path: str) -> Dict[str, Any]:
    """Get detailed information about an operator.
    
    Args:
        op_path: Path to the operator
    """
    result = {"success": False, "message": "", "info": {}}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command = f"""
operator = op("{op_path}")
if operator.valid:
    {{
        "name": operator.name,
        "path": operator.path,
        "type": operator.type,
        "valid": operator.valid,
        "cooking": operator.cooking,
        "cookTime": operator.cookTime,
        "parameters": [{{
            "name": p.name,
            "value": p.eval(),
            "label": p.label,
            "style": p.style,
            "mode": p.mode
        }} for p in operator.pars],
        "numChildren": len(operator.children),
        "childrenNames": [c.name for c in operator.children]
    }}
else:
    None
"""
    command_result = send_python_command(command)
    
    if command_result["success"] and command_result["result"] is not None:
        result["success"] = True
        result["info"] = command_result["result"]
        result["message"] = f"Retrieved information for {op_path}"
    else:
        result["message"] = f"Failed to get operator info: {command_result['error'] or 'Operator not found'}"
    
    return result

@mcp.tool()
async def export_movie(comp_path: str, output_path: str, settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Export a movie from a TouchDesigner component.
    
    Args:
        comp_path: Path to the component to export
        output_path: Output file path
        settings: Dictionary of export settings (optional)
    """
    result = {"success": False, "message": ""}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    # Use default settings if none provided
    if settings is None:
        settings = {
            "width": 1920,
            "height": 1080,
            "fps": 30,
            "format": "H264",
            "quality": 0.8,
            "duration": 10
        }
    
    # Construct the export code
    command = f"""
movie = op("{comp_path}")
if movie.valid:
    try:
        movie.save(
            "{output_path}",
            width={settings.get('width', 1920)},
            height={settings.get('height', 1080)},
            fps={settings.get('fps', 30)},
            format="{settings.get('format', 'H264')}",
            quality={settings.get('quality', 0.8)},
            exportTime=0,
            exportLength={settings.get('duration', 10)}
        )
        "Success"
    except Exception as e:
        str(e)
else:
    "Invalid component path"
"""
    command_result = send_python_command(command)
    
    if command_result["success"] and command_result["result"] == "Success":
        result["success"] = True
        result["message"] = f"Movie exported successfully to {output_path}"
    else:
        result["message"] = f"Failed to export movie: {command_result['result'] or command_result['error']}"
    
    return result

@mcp.tool()
async def take_screenshot(output_path: str, width: int = 1920, height: int = 1080) -> Dict[str, Any]:
    """Take a screenshot of the current TouchDesigner window.
    
    Args:
        output_path: Output file path
        width: Screenshot width (default: 1920)
        height: Screenshot height (default: 1080)
    """
    result = {"success": False, "message": ""}
    
    if not connection["connected"]:
        result["message"] = "Not connected to TouchDesigner"
        return result
    
    command = f"""
try:
    ui.viewportImage(asImage=True).save("{output_path}", width={width}, height={height})
    "Success"
except Exception as e:
    str(e)
"""
    command_result = send_python_command(command)
    
    if command_result["success"] and command_result["result"] == "Success":
        result["success"] = True
        result["message"] = f"Screenshot saved successfully to {output_path}"
    else:
        result["message"] = f"Failed to take screenshot: {command_result['result'] or command_result['error']}"
    
    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

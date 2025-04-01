from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import logging
from tools import get_all_tools
from td_connector import TouchDesignerConnector

# Configuration du logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Initialiser la connexion TouchDesigner
td_connector = TouchDesignerConnector(host="localhost", port=7001)

@app.route('/mcp/tools', methods=['GET'])
def get_tools():
    """Endpoint pour récupérer tous les outils disponibles"""
    tools = get_all_tools()
    logger.info(f"Returning {len(tools)} tools")
    return jsonify(tools)

@app.route('/mcp/tools/<tool_name>', methods=['GET'])
def get_tool(tool_name):
    """Endpoint pour récupérer un outil spécifique"""
    tools = get_all_tools()
    for tool in tools:
        if tool['name'] == tool_name:
            return jsonify(tool)
    return jsonify({"error": "Tool not found"}), 404

@app.route('/mcp/run', methods=['POST'])
def run_tool():
    """Endpoint pour exécuter un outil"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        tool_name = data.get('tool_name')
        parameters = data.get('parameters', {})
        
        if not tool_name:
            return jsonify({"error": "No tool_name provided"}), 400
        
        logger.info(f"Running tool: {tool_name} with parameters: {parameters}")
        
        # Exécuter l'outil dans TouchDesigner
        result = td_connector.execute_tool(tool_name, parameters)
        
        return jsonify({"result": result})
    
    except Exception as e:
        logger.error(f"Error running tool: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/mcp/status', methods=['GET'])
def get_status():
    """Endpoint pour vérifier l'état de la connexion"""
    if td_connector.is_connected():
        return jsonify({"status": "connected", "message": "Connected to TouchDesigner"})
    else:
        return jsonify({"status": "disconnected", "message": "Not connected to TouchDesigner"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
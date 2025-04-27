from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from tools import get_all_tools
from td_connector import TouchDesignerConnector
from jsonrpcserver import method, dispatch
from jsonrpcserver.response import Response, ErrorResponse

# Configuration du logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Initialiser la connexion TouchDesigner
td_connector = TouchDesignerConnector(host="localhost", port=7001)

# Méthodes MCP via JSON-RPC
@method
def resources_list():
    """Liste des ressources disponibles dans TouchDesigner"""
    tools = get_all_tools()
    resources = [{"id": tool["name"], "name": tool["description"], "type": "tool"} 
                 for tool in tools]
    return Response(resources)

@method
def prompts_list():
    """Liste des prompts disponibles"""
    # À adapter selon vos besoins
    prompts = [
        {"id": "create_object", "name": "Créer un objet dans TouchDesigner"},
        {"id": "modify_parameter", "name": "Modifier un paramètre"}
    ]
    return Response(prompts)

@method
def tools_execute(tool_name, parameters=None):
    """Exécuter un outil dans TouchDesigner"""
    if parameters is None:
        parameters = {}
    
    logger.info(f"Running tool: {tool_name} with parameters: {parameters}")
    
    try:
        # Exécuter l'outil dans TouchDesigner
        result_data = td_connector.execute_tool(tool_name, parameters)
        return Response({"result": result_data})
    except Exception as e:
        logger.error(f"Error running tool: {str(e)}")
        return ErrorResponse(-32000, str(e))

@method
def system_status():
    """Vérifier l'état de la connexion"""
    if td_connector.is_connected():
        return Response({"status": "connected", "message": "Connected to TouchDesigner"})
    else:
        return ErrorResponse(-32001, "Not connected to TouchDesigner")

# Endpoint JSON-RPC principal
@app.route("/", methods=["POST"])
def handle_jsonrpc():
    request_data = request.get_json()
    logger.info(f"Received JSON-RPC request: {request_data}")
    response = dispatch(request_data)
    logger.info(f"Sending JSON-RPC response: {response}")
    return response

# Gardez également vos anciens endpoints REST pour la compatibilité
@app.route('/mcp/tools', methods=['GET'])
def get_tools():
    tools = get_all_tools()
    return jsonify(tools)

@app.route('/mcp/status', methods=['GET'])
def get_status():
    if td_connector.is_connected():
        return jsonify({"status": "connected", "message": "Connected to TouchDesigner"})
    else:
        return jsonify({"status": "disconnected", "message": "Not connected to TouchDesigner"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
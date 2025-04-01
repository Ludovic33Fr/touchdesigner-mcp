import socket
import json
import time
import logging
import threading

logger = logging.getLogger(__name__)

class TouchDesignerConnector:
    def __init__(self, host="localhost", port=7001):
        self.host = host
        self.port = port
        self.connected = False
        self.socket = None
        self.lock = threading.Lock()
        self.connect()
    
    def connect(self):
        """Établir une connexion avec TouchDesigner"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to TouchDesigner at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to TouchDesigner: {str(e)}")
            self.connected = False
            return False
    
    def is_connected(self):
        """Vérifier si la connexion est établie"""
        return self.connected
    
    def reconnect_if_needed(self):
        """Reconnecter si la connexion est perdue"""
        if not self.is_connected():
            logger.info("Attempting to reconnect...")
            return self.connect()
        return True
    
    def send_command(self, command):
        """Envoyer une commande à TouchDesigner"""
        with self.lock:
            try:
                if not self.reconnect_if_needed():
                    return {"error": "Not connected to TouchDesigner"}
                
                # Ajouter un délimiteur de fin de commande
                command_str = json.dumps(command) + "\n"
                self.socket.sendall(command_str.encode('utf-8'))
                
                # Attendre et lire la réponse
                response = ""
                buffer = ""
                while True:
                    buffer = self.socket.recv(4096).decode('utf-8')
                    if not buffer:
                        break
                    response += buffer
                    if "\n" in buffer:  # Le délimiteur de fin a été reçu
                        break
                
                # Analyser la réponse JSON
                try:
                    return json.loads(response.strip())
                except json.JSONDecodeError:
                    return {"raw_response": response.strip()}
            
            except Exception as e:
                logger.error(f"Error sending command: {str(e)}")
                self.connected = False
                return {"error": str(e)}
    
    def execute_tool(self, tool_name, parameters):
        """Exécuter un outil spécifique dans TouchDesigner"""
        command = {
            "action": "execute_tool",
            "tool_name": tool_name,
            "parameters": parameters
        }
        return self.send_command(command)
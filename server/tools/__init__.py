from .operator_tools import get_operator_tools
from .parameter_tools import get_parameter_tools
from .project_tools import get_project_tools

def get_all_tools():
    """Récupérer tous les outils disponibles"""
    tools = []
    
    # Combiner tous les outils des différents modules
    tools.extend(get_operator_tools())
    tools.extend(get_parameter_tools())
    tools.extend(get_project_tools())
    
    return tools
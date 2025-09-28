# Agent with self-defined tools example
# This file demonstrates how to create agents with custom tools

from typing import List, Dict, Any
import json

class CustomTool:
    """Base class for custom tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute the tool - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement execute method")

class CalculatorTool(CustomTool):
    """Calculator tool for basic arithmetic operations"""
    
    def __init__(self):
        super().__init__("calculator", "Perform basic arithmetic calculations")
    
    def execute(self, operation: str, a: float, b: float) -> float:
        """Execute arithmetic operation"""
        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else float('inf')
        }
        
        if operation not in operations:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return operations[operation](a, b)

class AgentWithTools:
    """Agent that can use custom tools"""
    
    def __init__(self):
        self.tools: Dict[str, CustomTool] = {}
        self.register_tool(CalculatorTool())
    
    def register_tool(self, tool: CustomTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    def use_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Use a registered tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        return self.tools[tool_name].execute(*args, **kwargs)

if __name__ == "__main__":
    agent = AgentWithTools()
    result = agent.use_tool("calculator", "add", 5, 3)
    print(f"5 + 3 = {result}")
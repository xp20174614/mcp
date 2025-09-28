# Memory management example for MCP
# This file demonstrates memory handling in MCP applications

from typing import List, Dict, Any
from datetime import datetime

class MemoryManager:
    """Memory manager for storing and retrieving conversation context"""
    
    def __init__(self, max_memory_size: int = 1000):
        self.max_memory_size = max_memory_size
        self.memory: List[Dict[str, Any]] = []
    
    def add_memory(self, content: str, metadata: Dict[str, Any] = None):
        """Add a new memory entry"""
        memory_entry = {
            'timestamp': datetime.now().isoformat(),
            'content': content,
            'metadata': metadata or {}
        }
        
        self.memory.append(memory_entry)
        
        # Trim memory if it exceeds maximum size
        if len(self.memory) > self.max_memory_size:
            self.memory = self.memory[-self.max_memory_size:]
    
    def get_recent_memories(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent memories"""
        return self.memory[-count:]
    
    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search memories by content"""
        results = []
        for memory in self.memory:
            if query.lower() in memory['content'].lower():
                results.append(memory)
        return results
    
    def clear_memory(self):
        """Clear all memories"""
        self.memory.clear()

class ConversationMemory(MemoryManager):
    """Specialized memory for conversation context"""
    
    def __init__(self):
        super().__init__(max_memory_size=50)  # Limit conversation memory
        self.current_session = []
    
    def add_conversation_turn(self, user_input: str, agent_response: str):
        """Add a conversation turn to memory"""
        turn = {
            'user': user_input,
            'agent': agent_response,
            'timestamp': datetime.now().isoformat()
        }
        self.current_session.append(turn)
        
        # Also add to general memory
        self.add_memory(f"User: {user_input}\nAgent: {agent_response}")
    
    def get_conversation_context(self, turns_back: int = 5) -> str:
        """Get recent conversation context as string"""
        recent_turns = self.current_session[-turns_back:]
        context_lines = []
        
        for turn in recent_turns:
            context_lines.append(f"User: {turn['user']}")
            context_lines.append(f"Agent: {turn['agent']}")
        
        return "\n".join(context_lines)

if __name__ == "__main__":
    # Example usage
    memory = ConversationMemory()
    memory.add_conversation_turn("Hello!", "Hi there! How can I help you?")
    memory.add_conversation_turn("What's the weather like?", "I'm an AI and don't have real-time weather data.")
    
    print("Recent conversation:")
    print(memory.get_conversation_context())
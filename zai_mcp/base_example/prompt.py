# Prompt engineering example for MCP
# This file demonstrates prompt management and optimization

from typing import Dict, List, Any
import re

class PromptTemplate:
    """Base class for prompt templates"""
    
    def __init__(self, template: str):
        self.template = template
        self.variables = self._extract_variables(template)
    
    def _extract_variables(self, template: str) -> List[str]:
        """Extract variable names from template"""
        pattern = r'\{([^}]+)\}'
        return re.findall(pattern, template)
    
    def format(self, **kwargs) -> str:
        """Format the template with provided variables"""
        # Check if all required variables are provided
        missing_vars = set(self.variables) - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"Missing variables: {missing_vars}")
        
        return self.template.format(**kwargs)

class PromptManager:
    """Manager for organizing and managing multiple prompts"""
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """Initialize default prompt templates"""
        default_templates = {
            'system_prompt': PromptTemplate(
                "You are a helpful AI assistant. Please provide clear and concise responses to the user's questions."
            ),
            'qa_prompt': PromptTemplate(
                "Question: {question}\n\nContext: {context}\n\nAnswer:"
            ),
            'summarization_prompt': PromptTemplate(
                "Please summarize the following text in {length} words:\n\n{text}"
            ),
            'translation_prompt': PromptTemplate(
                "Translate the following {source_language} text to {target_language}:\n\n{text}"
            )
        }
        
        self.templates.update(default_templates)
    
    def add_template(self, name: str, template: str):
        """Add a new prompt template"""
        self.templates[name] = PromptTemplate(template)
    
    def get_prompt(self, template_name: str, **kwargs) -> str:
        """Get a formatted prompt"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        return self.templates[template_name].format(**kwargs)
    
    def optimize_prompt(self, template_name: str, feedback: str) -> str:
        """Optimize a prompt based on feedback"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Simple optimization: add feedback to the template
        original_template = self.templates[template_name].template
        optimized_template = f"{original_template}\n\nNote: {feedback}"
        
        return optimized_template

class DynamicPromptGenerator:
    """Generate dynamic prompts based on context"""
    
    def __init__(self):
        self.prompt_manager = PromptManager()
    
    def generate_qa_prompt(self, question: str, context: str = "") -> str:
        """Generate a question-answering prompt"""
        return self.prompt_manager.get_prompt(
            'qa_prompt',
            question=question,
            context=context if context else "No additional context provided"
        )
    
    def generate_summary_prompt(self, text: str, length: int = 100) -> str:
        """Generate a summarization prompt"""
        return self.prompt_manager.get_prompt(
            'summarization_prompt',
            text=text,
            length=length
        )

if __name__ == "__main__":
    # Example usage
    prompt_gen = DynamicPromptGenerator()
    
    qa_prompt = prompt_gen.generate_qa_prompt(
        "What is machine learning?",
        "Machine learning is a subset of artificial intelligence."
    )
    print("QA Prompt:")
    print(qa_prompt)
    
    summary_prompt = prompt_gen.generate_summary_prompt(
        "This is a long text that needs to be summarized...",
        50
    )
    print("\nSummary Prompt:")
    print(summary_prompt)
# GLM-4 5B base model fixed example
# This file contains improved and fixed version of GLM-4 model usage

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings
from typing import Optional, Dict, Any

class GLM4BaseFixed:
    """Fixed and improved GLM-4 5B base model example class"""
    
    def __init__(self, model_name: str = "THUDM/glm-4-5b"):
        self.model_name = model_name
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForCausalLM] = None
        self.is_loaded = False
    
    def load_model(self, device: str = "auto", torch_dtype=torch.float16) -> bool:
        """Load the GLM-4 model and tokenizer with error handling"""
        try:
            # Load tokenizer first
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                trust_remote_code=True,
                padding_side="left"
            )
            
            # Load model with appropriate settings
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch_dtype,
                device_map=device,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            # Set model to evaluation mode
            self.model.eval()
            self.is_loaded = True
            
            print(f"✓ Model {self.model_name} loaded successfully")
            print(f"✓ Device: {self.model.device}")
            print(f"✓ Dtype: {self.model.dtype}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            warnings.warn(f"Failed to load model: {e}")
            return False
    
    def generate_text(self, 
                     prompt: str, 
                     max_length: int = 100,
                     temperature: float = 0.7,
                     top_p: float = 0.9,
                     do_sample: bool = True) -> Optional[str]:
        """Generate text using the model with improved error handling"""
        
        if not self.is_loaded:
            print("Model not loaded. Attempting to load...")
            if not self.load_model():
                return None
        
        if not prompt or not prompt.strip():
            print("Warning: Empty prompt provided")
            return ""
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Move inputs to the same device as model
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            # Generate text
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=do_sample,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # Decode the generated text
            generated_text = self.tokenizer.decode(
                outputs[0], 
                skip_special_tokens=True
            )
            
            # Remove the original prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return generated_text
            
        except Exception as e:
            print(f"Error during text generation: {e}")
            return None
    
    def batch_generate(self, prompts: list, **kwargs) -> list:
        """Generate text for multiple prompts"""
        results = []
        
        for i, prompt in enumerate(prompts):
            print(f"Generating for prompt {i+1}/{len(prompts)}...")
            result = self.generate_text(prompt, **kwargs)
            results.append(result)
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_loaded:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.model_name,
            "device": str(self.model.device),
            "dtype": str(self.model.dtype),
            "parameters": sum(p.numel() for p in self.model.parameters()),
            "is_training": self.model.training
        }

class GLM4Chat(GLMFixed):
    """Specialized version for chat applications"""
    
    def __init__(self, model_name: str = "THUDM/glm-4-5b-chat"):
        super().__init__(model_name)
        self.conversation_history = []
    
    def format_chat_prompt(self, message: str, history: list = None) -> str:
        """Format prompt for chat conversation"""
        if history is None:
            history = self.conversation_history
        
        prompt = ""
        for turn in history[-5:]:  # Keep last 5 turns for context
            prompt += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        
        prompt += f"User: {message}\nAssistant:"
        return prompt
    
    def chat(self, message: str) -> str:
        """Generate response for chat message"""
        prompt = self.format_chat_prompt(message)
        response = self.generate_text(prompt, max_length=200)
        
        # Update conversation history
        self.conversation_history.append({
            "user": message,
            "assistant": response or ""
        })
        
        return response or "I'm sorry, I couldn't generate a response."

if __name__ == "__main__":
    # Example usage with improved error handling
    model = GLM4BaseFixed()
    
    # Test model loading
    if model.load_model():
        # Test text generation
        test_prompt = "Explain the concept of machine learning in simple terms:"
        result = model.generate_text(test_prompt)
        
        if result:
            print("Generated text:")
            print(result)
        else:
            print("Failed to generate text")
        
        # Print model info
        print("\nModel information:")
        info = model.get_model_info()
        for key, value in info.items():
            print(f"{key}: {value}")
    else:
        print("Failed to load model")
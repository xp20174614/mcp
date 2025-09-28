# GLM-4 5B base model example
# This file demonstrates basic GLM-4 5B model usage

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class GLM4BaseExample:
    """GLM-4 5B base model example class"""
    
    def __init__(self, model_name="THUDM/glm-4-5b"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
    
    def load_model(self):
        """Load the GLM-4 model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name, 
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            print(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def generate_text(self, prompt, max_length=100):
        """Generate text using the model"""
        if not self.model or not self.tokenizer:
            self.load_model()
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                temperature=0.7,
                do_sample=True
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text

if __name__ == "__main__":
    example = GLM4BaseExample()
    result = example.generate_text("Hello, how are you?")
    print("Generated text:", result)
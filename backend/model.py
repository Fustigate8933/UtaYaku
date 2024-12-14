import litserve as ls
from config import MODEL
from litserve.specs.openai import ChatCompletionRequest, ChatMessage
from transformers import (
    BitsAndBytesConfig,
    AutoModelForCausalLM,
    AutoTokenizer
)
import torch


class Qwen32BInstruct(ls.LitAPI):
    def setup(self, device):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            llm_int8_threshold=6.0,
            llm_int8_skip_modules=["lm_head"]
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL,
            torch_dtype=torch.bfloat16,
            device_map=device,
            quantization_config=quantization_config
        )
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.device = device

    def decode_request(self, request: ChatCompletionRequest, context: dict):
        context["model_args"] = {
            "temperature": request.temperature or 0.7,
            "top_p": request.top_p or 0.9,
            "max_new_tokens": request.max_tokens or 2048
        }
        print(f"Processing input")
        input = self.tokenizer.apply_chat_template(
            request.messages,
            add_generation_prompt=True,
            return_tensors="pt",
            tokenize=True
        )
        return input

    def predict(self, inputs, context: dict):
        model_kwargs = {
            "input_ids": inputs.to(self.device),
            "eos_token_id": self.tokenizer.eos_token_id,
            **context["model_args"]
        }
        
        gen_tokens = self.model.generate(**model_kwargs)
        
        input_length = inputs.shape[1]  # Length of the input prompt
        generated_tokens = gen_tokens[:, input_length:]  # Only the new generated tokens
        
        response = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        yield response


    def encode_response(self, outputs, context:dict):
        for output in outputs:
            if self.tokenizer.eos_token in output:
                output = output.replace(self.tokenizer.eos_token, "")
            yield ChatMessage(role="assistant", content=output)
            break

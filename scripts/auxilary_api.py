"""
Auxilary API
"""
from functools import reduce
from fastapi import Form, FastAPI
from pydantic import BaseModel
# modules should be imported from the root webui
from modules.sd_hijack import model_hijack
from modules import extra_networks
from modules import prompt_parser

from scripts.auth import secure_post

class TokenCountResponse(BaseModel):
    token_count: int
    max_length: int

def add_token_count_api(app : FastAPI):
    @secure_post('/sdapi/v1/count_tokens', response_model=TokenCountResponse)
    def token_count(prompt:str = Form()):
        """
        Returns the token count and max length of the prompt
        example : curl -X POST "http://localhost:7861/sdapi/v1/count_tokens" -H  "accept: application/json" -H  "Content-Type: application/x-www-form-urlencoded" -d "prompt=Hello%20World"
        """
        if not prompt:
            return TokenCountResponse(token_count=0, max_length=0)
        steps = 20 # default steps
        token_count, max_length = calculate_token(prompt, steps)
        return TokenCountResponse(token_count=token_count, max_length=max_length)
        
def calculate_token(text:str, steps:int):
    try:
        text, _ = extra_networks.parse_prompt(text)
        _, prompt_flat_list, _ = prompt_parser.get_multicond_prompt_list([text])
        prompt_schedules = prompt_parser.get_learned_conditioning_prompt_schedules(prompt_flat_list, steps)

    except Exception:
        # a parsing error can happen here during typing, and we don't want to bother the user with
        # messages related to it in console
        prompt_schedules = [[[steps, text]]]

    flat_prompts = reduce(lambda list1, list2: list1+list2, prompt_schedules)
    prompts = [prompt_text for step, prompt_text in flat_prompts]
    token_count, max_length = max([model_hijack.get_prompt_lengths(prompt) for prompt in prompts], key=lambda args: args[0])
    return token_count, max_length
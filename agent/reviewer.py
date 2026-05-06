


import json
import os
from langchain_openai import ChatOpenAI
from config import MODEL_NAME, OPENAI_API_KEY, PROMPTS_DIR
from langchain_core.prompts import ChatPromptTemplate

from schemas.output_schema import FinalOutput



class ReviewerChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.2,
            openai_api_key=OPENAI_API_KEY
        )

    def review(self, task: str, current_output: dict) -> dict:

        prompt_path = os.path.join(PROMPTS_DIR, 'reviewer_prompt.txt')
        system_prompt_path = os.path.join(PROMPTS_DIR, 'reviewer_system_prompt.txt')

        with open(prompt_path, 'r') as f:
            user_prompt_text = f.read()

        with open(system_prompt_path, 'r') as f:
            system_prompt_text = f.read()

        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            ("user", user_prompt_text)
        ])

        chain = prompt | self.llm.with_structured_output(FinalOutput)

        json_str = json.dumps(current_output, indent=2)

        result = chain.invoke({
            "task": task,
            "json_output": json_str
        })

        return result.model_dump()
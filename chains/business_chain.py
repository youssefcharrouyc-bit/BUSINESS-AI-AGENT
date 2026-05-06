

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY, PROMPTS_DIR
from schemas.output_schema import BusinessOverview


class BusinessChain:
    def __init__(self, tone: str = 'professional'):
        self.tone = tone
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.2,
            openai_api_key=OPENAI_API_KEY
        )

    def run(self, business_task: str) -> dict:

        prompt_path = os.path.join(PROMPTS_DIR, 'business_prompt.txt')
        system_prompt_path = os.path.join(PROMPTS_DIR, 'system_prompt.txt')

        with open(prompt_path, 'r') as f:
            user_prompt_text = f.read()

        with open(system_prompt_path, 'r') as f:
            system_prompt_text = f.read()

        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            ("user", user_prompt_text),
        ])

        print('prompt', prompt)

        chain = prompt | self.llm.with_structured_output(BusinessOverview)
        
        print(f"[CHAIN] Running business chain with Tone: {self.tone}")

        enhanced_task = f"{business_task}\n\nPlease write in a {self.tone} tone."
        result = chain.invoke({"business_task": enhanced_task})

        print(f"result: {result}")

        return result
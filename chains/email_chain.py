

import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY, PROMPTS_DIR
from schemas.output_schema import EmailList


class EmailChain:
    def __init__(self, tone: str = 'professional', count: int = 3):
        self.tone = tone
        self.count = count
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.5,
            openai_api_key=OPENAI_API_KEY
        )

    def run(self, business_task: str) -> List[dict]:

        prompt_path = os.path.join(PROMPTS_DIR, 'email_prompt.txt')
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

        chain = prompt | self.llm.with_structured_output(EmailList)
        
        print(f"[CHAIN] Drafting {self.count} Emails in Tone: {self.tone}...")

        enhanced_task = f"{business_task}\n\nWrite {self.count} emails. Use a {self.tone} tone."
        result = chain.invoke({"business_task": enhanced_task})

        return [email.model_dump() for email in result.emails]
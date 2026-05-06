

import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY, PROMPTS_DIR
from schemas.output_schema import TaskList


class TaskChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.2,
            openai_api_key=OPENAI_API_KEY
        )

    def run(self, business_task: str) -> List[dict]:

        prompt_path = os.path.join(PROMPTS_DIR, 'task_prompt.txt')
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

        chain = prompt | self.llm.with_structured_output(TaskList)
        
        print(f"[CHAIN] Breaking down tasks...")

        result = chain.invoke({"business_task": business_task})

        return [task.model_dump() for task in result.tasks]
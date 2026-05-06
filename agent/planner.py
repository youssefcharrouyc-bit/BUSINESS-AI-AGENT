import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY, PROMPTS_DIR

# Planner Schema
from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    steps: list[str] = Field(description="A list of steps to execute the plan.")

class ExecutionPlanner:
    def __init__(self, tone: str = "professional", depth: str = "normal"):
        self.tone = tone
        self.depth = depth

        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.0,
            openai_api_key=OPENAI_API_KEY
        )

    def generate_plan(self, business_task: str) -> dict:

        prompt_path = os.path.join(PROMPTS_DIR, 'planner_prompt.txt')
        system_prompt_path = os.path.join(PROMPTS_DIR, 'system_prompt.txt')

        with open(prompt_path, 'r') as f:
            user_prompt_text = f.read()

        with open(system_prompt_path, 'r') as f:
            system_prompt_text = f.read()

        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            ("user", user_prompt_text)
        ])

        planner_chain = prompt | self.llm.with_structured_output(ExecutionPlan)

        print(f"[PLANNER] Thinking about about with {self.depth} depth...")

        context_enhanced_task = f"{business_task}\n\n[Context: Tone=${self.tone}, Depth={self.depth}]."

        result = planner_chain.invoke({"business_task": context_enhanced_task})

        return result.model_dump()
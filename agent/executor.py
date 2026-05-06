


import asyncio
import time
from agent.planner import ExecutionPlanner
from agent.reviewer import ReviewerChain
from chains.business_chain import BusinessChain
from chains.email_chain import EmailChain
from chains.marketing_chain import MarketingChain
from chains.task_chain import TaskChain
from schemas.output_schema import FinalOutput
from rag.retriever import RAGRetriever

class AgentExecutor:
    def __init__(self, tone: str="professional", depth: int=2):
        self.tone = tone
        self.depth = depth

    async def run_stream(self, business_task: str):

        def create_log(step, message):
            return {
                "type": "log",
                "content": { 
                    "step": step,
                    "message": message,
                    "timestamp": time.time()
                }
            }
        

        # RAG Process Start
        retriever = RAGRetriever()
        yield create_log("RAG", "Starting Retrieval-Augmented Generation process...")
        retrieved_text = await asyncio.to_thread(retriever.retrieve, business_task)

        if retrieved_text:
            yield create_log("RAG", "Relevant documents retrieved successfully.")

            business_task = (
                f"### retrieved_context\n{retrieved_text}\n"
                f"### end_retrieved_context\n\n"                
                f"CORE BUSINESS TASK:{business_task}"
            )
        else:
            yield create_log("RAG", "No relevant documents found. Proceeding without context.")


        # 1.Planning
        planner = ExecutionPlanner(tone=self.tone, depth=self.depth)

        plan = await asyncio.to_thread(planner.generate_plan, business_task)

        steps = plan.get("steps", [])

        yield create_log("PLANNING", f"Decided steps: {steps}")

        # 2. Execution
        final_output_data = {}

        #Business Chain
        if "business_analysis" in steps:
            yield create_log("EXECUTION", "Running Business Chain...")

            chain = BusinessChain(tone=self.tone)
            final_output_data["business_overview"] = await asyncio.to_thread(chain.run, business_task)
        

        #Marketing Chain
        if "marketing_strategy" in steps:
            yield create_log("EXECUTION", "Running Marketing Chain...")

            chain = MarketingChain(tone=self.tone)
            final_output_data["marketing_strategy"] = await asyncio.to_thread(chain.run, business_task)

        #Email Chain
        if "email_campaign" in steps:
            yield create_log("EXECUTION", "Running Email Campaign Chain...")

            count = 3

            chain = EmailChain(tone=self.tone, count=count)
            final_output_data["email_campaigns"] = await asyncio.to_thread(chain.run, business_task)

        #Task Chain
        if "task_breakdown" in steps:
            yield create_log("EXECUTION", "Running Task Breakdown Chain...")

            chain = TaskChain()
            final_output_data["task_breakdown"] = await asyncio.to_thread(chain.run, business_task)

        #Review
        yield create_log("REVIEW", "Reviewing output for quality assurance...")
        reviewer = ReviewerChain()
        reviewed_output = await asyncio.to_thread(reviewer.review, business_task, final_output_data)
        yield create_log("REVIEW", "Review complete. Improvements applied...")

        # 4. Validation
        try:
            final_output_obj = FinalOutput(**reviewed_output)

            validated_data = final_output_obj.model.dump()

            yield create_log("SUCCESS", "Final output validated successfuly.")

            yield {
                "type": "result",
                "content": validated_data
            }

        except Exception as e:
            yield create_log("ERROR", f"Validation failed: {str(e)}")
            raise e
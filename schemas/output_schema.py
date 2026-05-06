


from typing import List

from pydantic import BaseModel, Field


class BusinessOverview(BaseModel):
    summary: str = Field(description="Clear one paragraph business summary.")
    primary_target_audience: str = Field(description="Specific audience description (One primary target)")
    core_pain_point: str = Field(description="Main problem this audience has (One core pain point)")
    unique_value_proposition: str = Field(description="Why this business wins (One clear advantage)")
    not_a_priority: str = Field(description="What should be avoided or deprioritized")
    

class MarketingChannel(BaseModel):
    channel: str = Field(description="Name of the marketing channel")
    priority: str = Field(description="priority level of the channel (1 being highest)")
    why_this_channel: str = Field(description="Specific reason for choosing this channel")


class IgnoredChannel(BaseModel):
    channel: str = Field(description="Name of the ignored marketing channel")
    reason: str = Field(description="Reason for ignoring this channel")

class MarketingStrategy(BaseModel):
    primary_goal: str = Field(description="Main marketing goal")
    core_message: str = Field(description="Key message to communicate")
    channels: list[MarketingChannel] = Field(description="List of 3 marketing channels")
    ignored_channel: IgnoredChannel = Field(description="One marketing channel to avoid and why")

class EmailCampaign(BaseModel):
    email_number: int = Field(description="Email sequence number")
    objective: str = Field(description="Objective of the email")
    subject: str = Field(description="Subject line of the email")
    body:   str = Field(description="Body content of the email")
    call_to_action: str = Field(description="Call to action for the email")

class EmailList(BaseModel):
    emails: list[EmailCampaign] = Field(description="List of 3 email campaigns")
    
class Task(BaseModel):
    task_order : int = Field(description="Order of the task")
    task_name: str = Field(description="Name of the task")
    description: str = Field(description="Description of the task")
    priority: str = Field(description="Priority level of the task")
    why_this_matter: str = Field(description="Reason why this task is important")

class TaskList(BaseModel):
    tasks: list[Task] = Field(description="List of 5 tasks with details")

class FinalOutput(BaseModel):
    business_overview: BusinessOverview
    marketing_strategy: MarketingStrategy
    email_campaign: List[EmailCampaign]
    task_breakdown: List[Task]
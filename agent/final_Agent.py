import os
from dotenv import load_dotenv

load_dotenv("../.env")
from langchain.chat_models import ChatOpenAI
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.llms import OpenAI
from langchain.agents.tools import Tool
from langchain import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain, create_extraction_chain_pydantic
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json
import requests

api_key = os.getenv("OPENAI_API_KEY")
# serper_api_key = os.getenv("SERP_API_KEY")

from typing import Optional, List
from pydantic import BaseModel, Field

class Applicant(BaseModel):
    Name: str
    Contact: str
    Location: str
    University: str
    Degree: str
    Major: str
    Graduation_Year: int
    Skills: list[str]
    Certifications: Optional[list[str]]
    Languages: Optional[list[str]]
    Role: str
    Company: str
    Start_Date: str
    End_Date: str
    Experience: int
    Responsibilities: list[str]
    Achievements: Optional[list[str]]
    Projects: Optional[list[str]]
    LinkedIn_Url: Optional[str]
    Github_Url: Optional[str]
    Hobbies: Optional[list[str]]


from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

from langchain.document_loaders import PyPDFLoader


def analyze_github_profile(profile_url):
    load_dotenv(".env")
    os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
    os.environ["WANDB_PROJECT"] = "Claude"
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    serper_api_key = os.getenv("SERP_API_KEY")

    analyzer = GithubProfileAnalyzer(anthropic_api_key=anthropic_api_key, serper_api_key=serper_api_key)
    return analyzer.analyze(profile_url)


def extract_resume_information(filename):
    # Load PDF
    loader = PyPDFLoader(f"../media/resumes/{filename}")
    # media/resumes/Poojan_vig_resume.pdf
    final = loader.load()
    resume = final[0].page_content
    llm = ChatOpenAI(temperature=0.0)

    pydantic_parser = PydanticOutputParser(pydantic_object=Applicant)
    format_instructions = pydantic_parser.get_format_instructions()

    template_string = """ You are a professional HR that and information extractor that can analyze the resume of the person and extract the contents as given in the instructions below
    Resume: ```{resume}```
    {format_instructions}
    """
    prompt = ChatPromptTemplate.from_template(template=template_string)
    messages = prompt.format_messages(resume=resume, format_instructions=format_instructions)

    output = llm(messages)

    json_out = json.loads(output.content)

    if json_out['Github_Url']:
        analyze_github_profile(json_out['Github_Url'])
    
    




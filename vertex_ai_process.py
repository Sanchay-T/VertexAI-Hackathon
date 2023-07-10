import os
from langchain.document_loaders import DirectoryLoader , PyPDFLoader
from langchain.llms import VertexAI
from langchain import LLMChain
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from IPython.core.display import Markdown
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from account.models import JobPost
import os
from langchain.document_loaders import DirectoryLoader
from langchain.llms import VertexAI
from langchain import LLMChain
from langchain.document_loaders import DirectoryLoader , PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from IPython.core.display import Markdown
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
import json
import pandas as pd



# os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
# os.environ["WANDB_PROJECT"] = "langchain-tracing"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ghc-001-7755ed5582db.json'


directory = "media/resumes/"


final_table = {}

# extract_name_table("resume.pdf")
# final_table.update(output)

# df = pd.DataFrame(final_table)

def dict_to_dataframes(profile_dict):
    dataframes = {}
    
    for key, value in profile_dict.items():
        if isinstance(value, list):
            if value and isinstance(value[0], dict):  # Check if list of dictionaries
                dataframes[key] = pd.DataFrame(value)
            else:
                dataframes[key] = pd.Series(value)  # If list of strings, convert to Series
        else:
            dataframes[key] = value  # If simple value, keep as it is
    
    return dataframes



def extract_name_table(userfilename ):






    name_prompt_template = """
Your task is Entity Recognition , below is the resume of a person you need to extract the name and give the output as JSON only.
For example:

```json
[
    "Name": "John Doe",
]

Resume of the Candidate:

{resume}

"""

    loader1 = PyPDFLoader(f"media/resumes/{userfilename}")
    pages = loader1.load()

    resume = pages[0].page_content

    promp_analysis_table  = PromptTemplate(template=name_prompt_template, input_variables=["resume"])
    llm = VertexAI(model_name="text-bison@001") # select the model
    llm_chain = LLMChain(prompt=promp_analysis_table, llm=llm)
    output = llm_chain.run(resume = resume)
    name = output.split('"')[3]


    process(name)
    
    
    


def process(name):

    directory = "media/resumes/"
    dl = DirectoryLoader(directory, "**/*.pdf")
    docs = dl.load()


    splitter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap=200)
    document_section = splitter.split_documents(docs)

    embeddings = VertexAIEmbeddings()
    db = Chroma.from_documents(document_section, embeddings)

    retriever = db.as_retriever(search_kwargs = dict(k=3))
    



# new flow 
    question = f"Create a table for the resume of {name}"
    docs = retriever.get_relevant_documents(question)

    prompt_template = """
In this task, you'll be analyzing the resume of a job candidate. Your objective is to extract key information from the resume, and evaluate how well the candidate's profile aligns with the requirements of the job.

Here is the candidate's resume:

***

{resume}

***

Your task is to carefully read through the resume and identify key information about the candidate.
For example, if you're examining the resume of a software engineer named John Doe, your output might look like this in JSON format:
The JSON should include the following fields:

```json
[
    "Name": "John Doe",
    "Summary": "Software Engineer with 10 years of experience in developing scalable web applications. Proficient in Java, Python, C++.",
    "Work Experience": "Google Search, Facebook Ads, Uber",
    "Years Of Experience": "10 years",
    "Skills": ["Java", "Python", "C++"],
    "Projects": ["Google Search", "Facebook Ads", "Uber"],
    "Education": "Stanford University",
    "Certifications": ["AWS Certified Solutions Architect - Associate", "Google Cloud Certified Professional Cloud Architect"],
    "Awards and Achievements": ["Google Founders' Award", "ACM Grace Hopper Award"]
]

When you encounter a category for which the resume provides no information, please use None as the value.

"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["resume"])
    llm = VertexAI(model_name="text-bison@001") # select the model
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    resume = "\n\n".join([doc.page_content for doc in docs])
    output= llm_chain.run(resume = resume)
    len(output)

    


    json_string = output.replace('```json\n', '').replace('\n```', '')

# Parse JSON string into a Python dictionary
    output_dict = json.loads(json_string)

# Convert the dictionary into pandas DataFrames
    output_dataframes = dict_to_dataframes(output_dict)

# Initialize a dictionary to hold the flattened data
    flat_data = {}

# Iterate over the output_dataframes dictionary
    for key, value in output_dataframes.items():
        if isinstance(value, pd.DataFrame):  # If the value is a DataFrame
        # Take the first row of the DataFrame and convert it into a dictionary
        # This will lose information if there are multiple rows in the DataFrame
            flat_data[key] = value.iloc[0].to_dict()
        elif isinstance(value, pd.Series):  # If the value is a Series
        # Take the first value of the Series
        # This will lose information if there are multiple values in the Series
            flat_data[key] = value.iloc[0]
        else:  # If the value is a simple data type
            flat_data[key] = value

# Convert the flat_data dictionary into a single-row DataFrame
    flat_df = pd.DataFrame(flat_data, index=[0])

    print(flat_df)




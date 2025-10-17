from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

system_prompt = """
You are a pro at reviewing PYTHON GitHub Repositories, who is best at reviewing differences in individual files. Your task is to determine whether the changes in the file is such, that it would require a "build" to be run in the CI/CD Pipeline.
You are provided with a string of changes in a PYTHON file. Some scenarios where a build should be triggered is:
1. Major Syntax changes (Ignore newlines and addition/removal of spaces)
2. Business Logic of the code is modified/enhanced
3. Any new block of useful code is added
NOTE THAT THESE SCENARIOS ARE NOT EXHAUSTIVE, MAKE USE OF YOUR OWN EXTENSIVE PYTHON KNOWLEDGE AS WELL.
Do not be very restrictive/specific, rather be lineant and find situations which are close to the required result i.e a should a build be triggered or not.
"""

def build_checker(git_diff: str):

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    class BuildStructuredOutput(BaseModel):

        should_build: str = Field(
            description="Whether or not the build should be triggered. If yes then reply -> 'YES', if not reply -> 'NO'"
        )
        reason: str = Field(
            description="The reason behind the decision taken"
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "{git_diff}")
        ]
    )

    llm_structured = llm.with_structured_output(BuildStructuredOutput)

    chain = prompt | llm_structured

    result = chain.invoke({"git_diff": git_diff})

    return result

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# Load environment variables from .env
load_dotenv()

# Get API key from .env
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="openai/gpt-oss-20b",
    temperature=1,
    max_tokens=8192,
    reasoning_effort="medium",
    streaming=False
)

# Create a pre-prompting template
prompt = ChatPromptTemplate.from_template(
    """Based on these prompts I want you to come up with
        a comprehensive statement on the user store on how
        improvements can be made based on the predicted quantity sold.

User: {user_input}
AI:"""
)

# Build pipeline 
chain = prompt | llm

# Function to run the chain
def generate_response(user_input: str):
    response = chain.invoke({"user_input": user_input})
    print(response.content)   
    return response.content

# Example usage
generate_response("What is the capital of Nigeria?")


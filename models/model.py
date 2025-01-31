from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai.models.gemini import GeminiModel
from dotenv import load_dotenv
import os
from typing import List
load_dotenv()

class multi_question(BaseModel):
    question : str
    choice_1 : str
    choice_2 : str
    choice_3 : str
    choice_4 : str
    answer : str

class one_line_question(BaseModel):
    question : str
    answer : str

question_agent = Agent(
    "google-gla:gemini-1.5-flash",
    deps_type=str,
    result_type=List[multi_question],
    system_prompt=(
        """You are an AI that generates educational quizzes based on provided text.  
        Create multiple-choice questions based on the given learning material.  

        Instructions:
        - Each question should test **key concepts** from the text.
        - Provide **four answer choices** (A, B, C, D).
        - Clearly **indicate the correct answer**.
        - Ensure the difficulty level matches the text complexity.
        - If the text is technical, use scenario-based questions."""    
    ),
    model_settings= {
        "temperature":0.7
    }
    
)
oneline_agent = Agent(
    "google-gla:gemini-1.5-flash",
    deps_type=str,
    result_type=List[one_line_question],
    system_prompt=(
        """You are an AI that generates educational quizzes based on provided text.  
        Create one line based on the given learning material.  

        Instructions:
        - Each question should test key concepts from the text.
        - Provide the question
        - Clearly indicate the correct answer in about one line.
        - Ensure the difficulty level matches the text complexity.
        - If the text is technical, use scenario-based questions."""    
    ),
    
    
)


@question_agent.system_prompt
def add_text(ctx : RunContext[str]) -> str:
    return f"The text is {ctx.deps}"


@oneline_agent.system_prompt
def add_text(ctx : RunContext[str]) -> str:
    return f"The text is {ctx.deps}"


text = """Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. It takes place in the chloroplasts of plant cells and primarily involves two stages: the light-dependent reactions and the Calvin cycle. 

In the light-dependent reactions, sunlight is absorbed by chlorophyll, exciting electrons that help generate ATP and NADPH. These energy carriers are then used in the Calvin cycle, where carbon dioxide is fixed into glucose. Oxygen is released as a byproduct of this process.

Photosynthesis is essential for life on Earth as it produces oxygen and forms the base of the food chain. Factors affecting photosynthesis include light intensity, carbon dioxide concentration, and temperature.
"""


# result = question_agent.run_sync("Generate 5 questions", deps=text)
# print(result.all_messages_json())
# print("Multiple Choice Questions")
# for q in result.data:
#     print(f"Q: {q.question}")
#     print(f"A) {q.choice_1}")
#     print(f"B) {q.choice_2}")
#     print(f"C) {q.choice_3}")
#     print(f"D) {q.choice_4}")
#     print(f"Answer: {q.answer}")
#     print("\n")



# one_result = oneline_agent.run_sync("Generate 5 questions", deps=text)

# print("One line Questions : ")

# for q in one_result.data:
#     print(f"Q: {q.question}")
#     print(f"Answer: {q.answer}")
#     print("\n")


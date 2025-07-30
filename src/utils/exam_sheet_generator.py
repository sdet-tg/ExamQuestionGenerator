import os
from google import genai

# Configure your API key
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set your Gemini API key.")

def generate_exam_questions(subject, grade_level, num_questions=10, model_name="gemini-2.5-flash"):
    """
    Generates exam questions relevant to a given subject and grade level using Gemini.

    Args:
        subject (str): The subject for the questions (e.g., "math", "history", "science").
        grade_level (int): The grade level (e.g., 5, 8, 12).
        num_questions (int): The number of questions to generate.
        model_name (str): The Gemini model to use.

    Returns:
        list: A list of generated exam questions.
    """
    client = genai.Client()

    # Craft a clear and specific prompt for Gemini
    prompt = f"""
    Generate {num_questions} exam questions for a Grade {grade_level} {subject} class.
    
    The questions should be challenging but appropriate for the specified grade level.
    Include a mix of question types if applicable (e.g., multiple choice, fill-in-the-blank, short answer).
    For multiple-choice questions, provide 4 options (A, B, C, D) and indicate the correct answer.
    
    Here are some examples of what I'm looking for:

    If subject is 'math' and grade is '5' (multiplication):
    1. What is 12 x 7?
    A) 74
    B) 84
    C) 96
    D) 68
    Correct Answer: B

    2. A baker bakes 15 batches of cookies, with 12 cookies in each batch. How many cookies did the baker bake in total?
    Correct Answer: 180

    If subject is 'science' and grade is '8' (biology):
    1. Which of the following is the powerhouse of the cell?
    A) Nucleus
    B) Mitochondria
    C) Ribosome
    D) Endoplasmic Reticulum
    Correct Answer: B

    2. Explain the process of photosynthesis in your own words.

    Now, generate {num_questions} questions for Grade {grade_level} {subject}.
    """

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        # Split the response into individual questions
        questions = [q.strip() for q in response.text.split('\n\n') if q.strip()]
        
        # Optionally, you might want to filter or format the questions further here
        # For example, to ensure exactly num_questions are returned, or to parse 
        # multiple-choice options into a structured format.
        
        return questions[:num_questions] # Return up to num_questions
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

if __name__ == "__main__":
    print("--- Exam Question Generator ---")

    # Example 1: Grade 5 Math - Multiplications
    print("\n--- Grade 5 Math - Multiplications ---")
    math_questions = generate_exam_questions("math - multiplications", 5)
    for i, q in enumerate(math_questions):
        print(f"Question {i+1}:\n{q}\n")

    # Example 2: Grade 8 Science - Biology
    print("\n--- Grade 8 Science - Biology ---")
    science_questions = generate_exam_questions("science - biology", 8)
    for i, q in enumerate(science_questions):
        print(f"Question {i+1}:\n{q}\n")

    # Example 3: Grade 10 History - World War II
    print("\n--- Grade 10 History - World War II ---")
    history_questions = generate_exam_questions("history - World War II", 10)
    for i, q in enumerate(history_questions):
        print(f"Question {i+1}:\n{q}\n")

    # Example 4: Grade 3 English - Nouns
    print("\n--- Grade 3 English - Nouns ---")
    english_questions = generate_exam_questions("English - nouns", 3)
    for i, q in enumerate(english_questions):
        print(f"Question {i+1}:\n{q}\n")
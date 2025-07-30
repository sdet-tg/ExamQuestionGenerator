import json
from flask import Flask, request, jsonify, render_template
import os
from google import genai
from mistralai import Mistral

app = Flask(__name__)

def generate_exam_questions_gemini(className, topic, grade_level, num_questions=10, difficulty="medium"):
    """
    Generates exam questions relevant to a given subject and grade level using Gemini.

    Args:
        className (str): The subject for the questions (e.g., "math", "history", "science").
        topic (str): The specific topic within the class.
        grade_level (int): The grade level (e.g., 5, 8, 12).
        num_questions (int): The number of questions to generate.
        difficulty (str): The difficulty level of the questions ("easy", "medium", "hard").

    Returns:
        list: A list of generated exam questions.
    """
    API_KEY = os.environ.get("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set your Gemini API key.")

    client = genai.Client()

    # Craft a clear and specific prompt for Gemini
    prompt = f"""
    Generate {num_questions} exam questions for a Grade {grade_level} on {topic} for {className} class.
    
    The questions should be challenging but appropriate for the specified grade level.
    Adjust the difficulty level to "{difficulty}".
    Ensure that the questions are unique and not repetitive.
    Include a mix of question types if applicable (e.g.,fill-in-the-blank, short answer{').' if difficulty =='hard'
        else ', multiple choice). For multiple-choice questions, provide 4 options (A, B, C, D) and indicate the correct answer.'}

    Only return the questions without any additional text or explanation.
    Generate questions in JSON format and each question should include:
    a "question" string,
    a "type" field ("multiple_choice", "short_answer", or "open_ended"),
    if type is "multiple_choice", include an "options" array with 4 choices labeled A) to D),
    a "correct_answer" string.
    Return only the JSON array, do not include any explanations or markdown code block (like ```json).

    Here are some examples of what I'm looking for:

    If class is 'math', topic is 'Division' and grade is '12':
    [{{'question': "When the polynomial P(x) = 2x^4 - 3x^3 + ax^2 - 8x + 1 is divided by (x^2 + 1), the remainder is 3x - 5. What is the value of 'a'?",
    'type': 'short_answer', 'Correct Answer': '-2'}},

    {{'question': "When a polynomial P(x) is divided by (2x + 1), the quotient is (x^2 - 3x + 5) and the remainder is -4. Determine the original polynomial P(x).
    'type': 'short_answer', 'Correct Answer': '2x^3 - 5x^2 + 7x + 1'}},

    If class is 'science', topic is biology and grade is '8':
    [{{'question': "Name the three essential ingredients (reactants) that plants need to perform photosynthesis.
    'type': 'short_answer', 'Correct Answer': 'Carbon dioxide, water, and sunlight (or light energy)'}},

    {{'question': "Describe how a significant decrease in the population of producers (like grass) in an ecosystem
    would likely affect the populations of herbivores and carnivores in that same ecosystem.",
    'type': 'short_answer', 'Correct Answer': "A decrease in producers would lead to a decrease in the food available for herbivores,
    causing their population to decline. Subsequently, with fewer herbivores available as food, the population of carnivores would also likely decrease due to lack of prey."

    Now, generate {num_questions} questions for Grade {grade_level} on {topic} for {className} class.
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

def generate_exam_questions_mistral(className, topic, grade_level, num_questions=10, difficulty="medium"):
    """
    Generates exam questions relevant to a given subject and grade level using Mistral AI.

    Args:
        className (str): The subject for the questions (e.g., "math", "history", "science").
        topic (str): The specific topic within the class.
        grade_level (int): The grade level (e.g., 5, 8, 12).
        num_questions (int): The number of questions to generate.
        difficulty (str): The difficulty level of the questions ("easy", "medium", "hard").

    Returns:
        list: A list of generated exam questions.
    """
    API_KEY = os.environ.get("MISTRAL_API_KEY")
    if not API_KEY:
        raise ValueError("MISTRAL_API_KEY environment variable not set. Please set your Mistral API key.")

    client = mistral.Client()

    # Optimized prompt for Mistral AI
    prompt = f"""
    Create {num_questions} unique exam questions for Grade {grade_level} students studying {topic} in {className}.
    
    Difficulty level: {difficulty}.
    Ensure the questions are diverse and cover various aspects of the topic.
    Include short-answer and open-ended questions where applicable.
    {'Also, include multiple-choice questions with 4 options (A, B, C, D) and clearly specify the correct answer.' if difficulty !='hard' else ''}
    
    Format the output as a JSON array where each question includes:
    - "question": The text of the question.
    - "type": The type of question ("multiple_choice", "short_answer", "open_ended").
    - "options": An array of 4 options (for multiple-choice questions only).
    - "correct_answer": The correct answer (for all question types).
    
    Example:
    [
        {
            "question": "What is 12 x 7?",
            "type": "multiple_choice",
            "options": ["74", "84", "96", "68"],
            "correct_answer": "84"
        },
        {
            "question": "Explain the process of photosynthesis.",
            "type": "open_ended",
            "correct_answer": "Photosynthesis is the process by which green plants use sunlight to synthesize food from carbon dioxide and water."
        }
    ]

    Generate the questions strictly in the specified JSON format without any additional text or explanations.
    """

    try:
        response = client.models.generate_content(model="mistral-1.0", contents=prompt)
        # Parse the response into individual questions
        questions = json.loads(response.text)
        return questions[:num_questions]  # Return up to num_questions
    except Exception as e:
        print(f"Error generating questions with Mistral: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        className = data.get("className", "")
        topic = data.get("topic", "")
        grade = data.get("gradeLevel", 0)
        count = data.get("numQuestions", 0)
        difficulty = data.get("difficulty", "medium")
        platform = data.get("platform", "gemini")
        print(f"Received query for className={className}, topic={topic}, grade={grade}, count={count}, difficulty={difficulty}")
        if platform == "mistral":
            questions = generate_exam_questions_mistral(className, topic, grade, count, difficulty)
        else:
            questions = generate_exam_questions_gemini(className, topic, grade, count, difficulty)
        print(f"Response:\n{questions}")
        try:
            parsed_json = json.loads(questions[0])
        except json.JSONDecodeError as e:
            return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 400
        print(f"Parsed:\n{parsed_json}")
        return parsed_json

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
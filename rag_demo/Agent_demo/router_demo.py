import os
from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


MODEL_NAME = "gemini-3.6-flash"

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# ROUTES
# ============================================================

ROUTES = [
    "KNOWLEDGE",
    "LIVE_DATA",
    "DATABASE",
    "ACTION",
    "UNKNOWN"
]


# ============================================================
# ROUTER
# ============================================================

def route_question(question):

    prompt = f"""
You are an Enterprise AI Router.

Your job is ONLY to classify the user's request.

Choose exactly ONE of these categories:

KNOWLEDGE
Use this when the user is asking for:
- General knowledge
- Documentation
- Concepts
- How something works
- Technical explanations

Example:
"What is OAuth 2.0?"

LIVE_DATA
Use this when the user needs current information
from an operational system or API.

Example:
"What is the current status of OIC integration 10025?"

DATABASE
Use this when the user needs business information
that should be retrieved from a database.

Example:
"Show me the sales amount for customer C100."

ACTION
Use this when the user wants the system to perform
an operation or change something.

Example:
"Restart OIC integration 10025."

UNKNOWN
Use this when the request does not fit the above categories.

IMPORTANT:
Return ONLY ONE category name.

Do not explain your answer.

USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    route = response.text.strip().upper()

    # --------------------------------------------------------
    # Clean possible formatting
    # --------------------------------------------------------

    route = route.replace("`", "")
    route = route.replace("\n", "")
    route = route.strip()

    # --------------------------------------------------------
    # Validate route
    # --------------------------------------------------------

    if route not in ROUTES:
        route = "UNKNOWN"

    return route


# ============================================================
# DISPLAY ROUTING EXPLANATION
# ============================================================

def explain_route(route):

    explanations = {

        "KNOWLEDGE":
            "Send the request to the RAG / Knowledge Agent.",

        "LIVE_DATA":
            "Send the request to an operational API such as OIC.",

        "DATABASE":
            "Send the request to a database / SQL Agent.",

        "ACTION":
            "Send the request to an Action Agent with security and approval checks.",

        "UNKNOWN":
            "The system cannot confidently determine the destination."
    }

    return explanations[route]


# ============================================================
# TEST QUESTIONS
# ============================================================

def run_test_questions():

    test_questions = [

        "What is OAuth 2.0?",

        "What is the current status of OIC integration 10025?",

        "Restart OIC integration 10025.",

        "How does OIC communicate with external applications?",

        "Show me the sales amount for customer C100.",

        "Tell me something interesting about cricket."
    ]

    print("\n==========================================")
    print("       AUTOMATIC ROUTER TEST")
    print("==========================================")

    for number, question in enumerate(
        test_questions,
        start=1
    ):

        print("\n------------------------------------------")
        print(f"TEST CASE {number}")
        print("------------------------------------------")

        print("Question:")
        print(question)

        route = route_question(question)

        print("\nROUTER DECISION:")
        print(route)

        print("\nNEXT DESTINATION:")
        print(explain_route(route))


# ============================================================
# INTERACTIVE MODE
# ============================================================

def interactive_mode():

    print("\n==========================================")
    print("       INTERACTIVE ROUTER TEST")
    print("==========================================")

    print("\nAvailable Routes:")
    print("1. KNOWLEDGE")
    print("2. LIVE_DATA")
    print("3. DATABASE")
    print("4. ACTION")
    print("5. UNKNOWN")

    while True:

        question = input(
            "\nEnter your question: "
        ).strip()

        if not question:
            print("Please enter a question.")
            continue

        if question.lower() in [
            "exit",
            "quit",
            "q"
        ]:
            break

        print("\n------------------------------------------")
        print("ROUTING REQUEST")
        print("------------------------------------------")

        print("USER:")
        print(question)

        route = route_question(question)

        print("\nROUTER:")
        print(route)

        print("\nROUTING ACTION:")
        print(explain_route(route))

        print("------------------------------------------")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    print("\n==========================================")
    print("       ENTERPRISE AI ROUTER")
    print("==========================================")

    print("\nGemini initialized successfully.")

    while True:

        print("\n==========================================")
        print("MENU")
        print("==========================================")

        print("1. Run automatic test")
        print("2. Test your own question")
        print("3. Exit")

        choice = input(
            "\nSelect option: "
        ).strip()

        if choice == "1":

            run_test_questions()

        elif choice == "2":

            interactive_mode()

        elif choice == "3":

            print("\nRouter demo finished.")
            break

        else:

            print("\nInvalid option.")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()
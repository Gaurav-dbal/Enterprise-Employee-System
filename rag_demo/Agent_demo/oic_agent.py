import os
import json
from dotenv import load_dotenv
from google import genai


# ============================================================
# 1. LOAD API KEY
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")


# ============================================================
# 2. INITIALIZE GEMINI
# ============================================================

client = genai.Client(
    api_key=API_KEY
)

MODEL_NAME = "gemini-3.6-flash"


print("==========================================")
print("       OIC AI AGENT - DEMO")
print("==========================================")

print("Gemini initialized successfully.")


# ============================================================
# 3. TOOL 1 - GET INTEGRATION STATUS
# ============================================================

def get_integration_status(integration_id):

    print("\n==========================================")
    print("TOOL: get_integration_status")
    print("==========================================")

    print("Integration ID:", integration_id)

    result = {
        "integration_id": integration_id,
        "status": "FAILED"
    }

    print("\nTOOL RESULT:")
    print(json.dumps(result, indent=2))

    return result


# ============================================================
# 4. TOOL 2 - GET ERROR DETAILS
# ============================================================

def get_error_details(integration_id):

    print("\n==========================================")
    print("TOOL: get_error_details")
    print("==========================================")

    print("Integration ID:", integration_id)

    result = {
        "integration_id": integration_id,
        "error_code": "AUTHENTICATION_FAILURE",
        "message": "OAuth token expired"
    }

    print("\nTOOL RESULT:")
    print(json.dumps(result, indent=2))

    return result


# ============================================================
# 5. TOOL 3 - SEARCH OIC DOCUMENTATION
# ============================================================

def search_oic_docs(query):

    print("\n==========================================")
    print("TOOL: search_oic_docs")
    print("==========================================")

    print("Query:", query)

    documents = [
        {
            "title": "OIC Authentication",
            "content":
                "Authentication is required when an integration "
                "accesses protected APIs."
        },
        {
            "title": "OIC Authorization",
            "content":
                "OAuth 2.0 is commonly used for API authorization."
        },
        {
            "title": "OIC Error Handling",
            "content":
                "When an integration fails, error handling and "
                "monitoring should be used to identify the cause "
                "of the failure."
        },
        {
            "title": "OIC Retry",
            "content":
                "Retry policies can be configured for certain "
                "integration failures."
        }
    ]

    results = []

    query_words = query.lower().split()

    for document in documents:

        score = 0

        for word in query_words:

            if word in document["content"].lower():
                score += 1

        if score > 0:
            results.append(document)

    print("\nTOOL RESULT:")
    print(json.dumps(results, indent=2))

    return {
        "results": results
    }


# ============================================================
# 6. TOOL DEFINITIONS
# ============================================================

get_status_tool = {
    "type": "function",
    "name": "get_integration_status",
    "description":
        "Gets the current status of an OIC integration.",
    "parameters": {
        "type": "object",
        "properties": {
            "integration_id": {
                "type": "string",
                "description":
                    "The OIC integration ID."
            }
        },
        "required": ["integration_id"]
    }
}


get_error_tool = {
    "type": "function",
    "name": "get_error_details",
    "description":
        "Gets error details for a failed OIC integration.",
    "parameters": {
        "type": "object",
        "properties": {
            "integration_id": {
                "type": "string",
                "description":
                    "The OIC integration ID."
            }
        },
        "required": ["integration_id"]
    }
}


search_docs_tool = {
    "type": "function",
    "name": "search_oic_docs",
    "description":
        "Searches OIC documentation for technical guidance.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description":
                    "Technical OIC search query."
            }
        },
        "required": ["query"]
    }
}


TOOLS = [
    get_status_tool,
    get_error_tool,
    search_docs_tool
]


# ============================================================
# 7. TOOL EXECUTION
# ============================================================

def execute_tool(name, arguments):

    if name == "get_integration_status":

        return get_integration_status(
            arguments["integration_id"]
        )

    elif name == "get_error_details":

        return get_error_details(
            arguments["integration_id"]
        )

    elif name == "search_oic_docs":

        return search_oic_docs(
            arguments["query"]
        )

    return {
        "error": "Unknown tool"
    }


# ============================================================
# 8. AGENT
# ============================================================

def run_agent(question):

    print("\n==========================================")
    print("             AGENT START")
    print("==========================================")

    print("\nUSER:")
    print(question)


    # --------------------------------------------------------
    # SYSTEM INSTRUCTION
    # --------------------------------------------------------

    system_instruction = """
You are an enterprise OIC support agent.

Investigate OIC integration problems.

Available tools:

1. get_integration_status
2. get_error_details
3. search_oic_docs

Rules:

- Use the integration status tool when live status is required.
- Use error details when you need to know why an integration failed.
- Use documentation search when technical guidance is required.
- You may call multiple tools.
- After each tool result, decide whether another tool is required.
- Do not invent information.
- Stop when you have enough information.
- Give a concise final answer with the failure reason and recommendation.
"""


    # --------------------------------------------------------
    # FIRST GEMINI CALL
    # --------------------------------------------------------

    interaction = client.interactions.create(

        model=MODEL_NAME,

        input=question,

        system_instruction=system_instruction,

        tools=TOOLS
    )


    # --------------------------------------------------------
    # AGENT LOOP
    # --------------------------------------------------------

    MAX_ITERATIONS = 5


    for iteration in range(MAX_ITERATIONS):

        print("\n==========================================")
        print(
            f"AGENT ITERATION {iteration + 1}"
        )
        print("==========================================")


        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]


        # ====================================================
        # NO TOOL CALL
        # ====================================================

        if not function_calls:

            print("\n==========================================")
            print("             FINAL ANSWER")
            print("==========================================")

            print(
                interaction.output_text
            )

            return


        # ====================================================
        # EXECUTE FUNCTION CALLS
        # ====================================================

        function_results = []


        for call in function_calls:

            print("\n------------------------------------------")
            print("LLM DECIDED TO CALL TOOL")
            print("------------------------------------------")

            print(
                "Tool:",
                call.name
            )

            print(
                "Arguments:",
                call.arguments
            )


            # ----------------------------------------------
            # Execute Python function
            # ----------------------------------------------

            result = execute_tool(
                call.name,
                call.arguments
            )


            # ----------------------------------------------
            # Create function result
            # ----------------------------------------------

            function_results.append({

                "type": "function_result",

                "name": call.name,

                "call_id": call.id,

                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(result)
                    }
                ]
            })


        # ====================================================
        # SEND RESULTS BACK TO GEMINI
        # ====================================================

        print("\n------------------------------------------")
        print("SENDING TOOL RESULT BACK TO GEMINI")
        print("------------------------------------------")


        interaction = client.interactions.create(

            model=MODEL_NAME,

            previous_interaction_id=interaction.id,

            input=function_results,

            tools=TOOLS
        )


    # ========================================================
    # MAX ITERATIONS
    # ========================================================

    print("\n==========================================")
    print("AGENT STOPPED")
    print("==========================================")

    print(
        "Maximum iterations reached."
    )


# ============================================================
# 9. MAIN
# ============================================================

def main():

    print("\n==========================================")
    print("       OIC AGENT LEARNING DEMO")
    print("==========================================")

    question = input(
        "\nEnter your question: "
    )

    run_agent(question)


# ============================================================
# 10. START
# ============================================================

if __name__ == "__main__":
    main()
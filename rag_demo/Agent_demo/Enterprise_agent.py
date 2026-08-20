import os
import json
from datetime import datetime

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
# USER / PERMISSION CONFIGURATION
# ============================================================

CURRENT_USER = {
    "name": "Gaurav",
    "role": "ADMIN",
    "environment": "PRODUCTION"
}


PERMISSIONS = {
    "ADMIN": [
        "get_integration_status",
        "get_error_details",
        "search_oic_docs",
        "restart_integration",
        "delete_integration"
    ],

    "DEVELOPER": [
        "get_integration_status",
        "get_error_details",
        "search_oic_docs"
    ],

    "VIEWER": [
        "get_integration_status",
        "search_oic_docs"
    ]
}


# ============================================================
# HIGH-RISK ACTIONS
# ============================================================

HIGH_RISK_ACTIONS = [
    "restart_integration",
    "delete_integration"
]


# ============================================================
# AGENT STATE
# ============================================================

def create_agent_state(question):

    return {

        "goal": question,

        "route": None,

        "plan": [],

        "completed_steps": [],

        "observations": [],

        "tool_results": [],

        "current_action": None,

        "iteration": 0,

        "status": "STARTED",

        "final_answer": None
    }


# ============================================================
# MEMORY
# ============================================================

MEMORY_FILE = "agent_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):

        return []

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4
        )


def add_memory(question, answer):

    memory = load_memory()

    memory.append({

        "timestamp":
            datetime.now().isoformat(),

        "question":
            question,

        "answer":
            answer
    })

    save_memory(memory)


def show_memory():

    memory = load_memory()

    print("\n==========================================")
    print("              LONG-TERM MEMORY")
    print("==========================================")

    if not memory:

        print("Memory is empty.")

        return

    for index, item in enumerate(
        memory,
        start=1
    ):

        print(f"\nMemory {index}")

        print(
            "Time     :",
            item.get("timestamp")
        )

        print(
            "Question :",
            item.get("question")
        )

        print(
            "Answer   :",
            item.get("answer")
        )


# ============================================================
# ROUTER
# ============================================================

def route_question(question):

    print("\n==========================================")
    print("                 ROUTER")
    print("==========================================")

    prompt = f"""
You are an Enterprise AI Router.

Classify the user's request into exactly ONE category.

KNOWLEDGE
Questions about concepts, documentation,
or how something works.

LIVE_DATA
Questions requiring current information
from an operational system or API.

DATABASE
Questions requiring business information
from a database.

ACTION
Requests asking the system to perform
an operation or change something.

UNKNOWN
Anything that does not fit the categories.

Examples:

"What is OAuth 2.0?"
KNOWLEDGE

"What is the current status of OIC integration 12345?"
LIVE_DATA

"Show me sales for customer C100."
DATABASE

"Restart OIC integration 12345."
ACTION

Return ONLY the category.

USER QUESTION:
{question}
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        route = response.text.strip().upper()

        route = route.replace(
            "`",
            ""
        ).replace(
            "\n",
            ""
        ).strip()

        if route not in ROUTES:

            route = "UNKNOWN"

    except Exception as e:

        print("Router error:", e)

        route = "UNKNOWN"

    print("User Question :", question)
    print("Router Decision:", route)

    return route


# ============================================================
# PLANNER
# ============================================================

def create_plan(question, route):

    print("\n==========================================")
    print("                PLANNER")
    print("==========================================")

    if route == "KNOWLEDGE":

        plan = [
            "search_knowledge",
            "generate_answer"
        ]

    elif route == "LIVE_DATA":

        plan = [
            "get_integration_status",
            "get_error_details",
            "search_oic_docs",
            "generate_answer"
        ]

    elif route == "DATABASE":

        plan = [
            "get_customer_sales",
            "generate_answer"
        ]

    elif route == "ACTION":

        plan = [
            "identify_action",
            "check_guardrail",
            "check_permission",
            "request_human_approval",
            "execute_action",
            "generate_answer"
        ]

    else:

        plan = [
            "generate_answer"
        ]

    print("\nGoal:")
    print(question)

    print("\nGenerated Plan:")

    for number, step in enumerate(
        plan,
        start=1
    ):

        print(
            f"{number}. {step}"
        )

    return plan


# ============================================================
# MOCK OIC TOOLS
# ============================================================

def get_integration_status(
    integration_id
):

    print("\n==========================================")
    print("       TOOL: GET INTEGRATION STATUS")
    print("==========================================")

    print(
        "Integration ID:",
        integration_id
    )

    result = {

        "integration_id":
            integration_id,

        "status":
            "FAILED"
    }

    print("\nTOOL RESULT:")

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    return result


def get_error_details(
    integration_id
):

    print("\n==========================================")
    print("          TOOL: GET ERROR DETAILS")
    print("==========================================")

    print(
        "Integration ID:",
        integration_id
    )

    result = {

        "integration_id":
            integration_id,

        "error_code":
            "AUTHENTICATION_FAILURE",

        "message":
            "OAuth token expired."
    }

    print("\nTOOL RESULT:")

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    return result


def search_oic_docs(query):

    print("\n==========================================")
    print("          TOOL: SEARCH OIC DOCS")
    print("==========================================")

    print(
        "Search Query:",
        query
    )

    result = {

        "documentation":
            "Refresh the OAuth credentials or token and retry the integration."
    }

    print("\nTOOL RESULT:")

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    return result


def get_customer_sales(customer_id):

    print("\n==========================================")
    print("        TOOL: GET CUSTOMER SALES")
    print("==========================================")

    print(
        "Customer:",
        customer_id
    )

    result = {

        "customer_id":
            customer_id,

        "sales":
            1250000
    }

    print("\nTOOL RESULT:")

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    return result


def restart_integration(
    integration_id
):

    print("\n==========================================")
    print("       TOOL: RESTART INTEGRATION")
    print("==========================================")

    print(
        "Integration:",
        integration_id
    )

    result = {

        "integration_id":
            integration_id,

        "action":
            "RESTART",

        "status":
            "SUCCESS"
    }

    print("\nTOOL RESULT:")

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    return result


def delete_integration(
    integration_id
):

    print("\n==========================================")
    print("        TOOL: DELETE INTEGRATION")
    print("==========================================")

    print(
        "Integration:",
        integration_id
    )

    result = {

        "integration_id":
            integration_id,

        "action":
            "DELETE",

        "status":
            "SUCCESS"
    }

    print("\nTOOL RESULT:")

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    return result


# ============================================================
# GUARDRAILS
# ============================================================

def check_guardrail(action):

    print("\n==========================================")
    print("              GUARDRAIL")
    print("==========================================")

    print(
        "Requested Action:",
        action
    )

    if action in HIGH_RISK_ACTIONS:

        print(
            "Risk Level: HIGH"
        )

        print(
            "Decision: HUMAN APPROVAL REQUIRED"
        )

        return {

            "allowed":
                True,

            "high_risk":
                True,

            "reason":
                "High-risk operation."
        }

    print(
        "Risk Level: LOW"
    )

    print(
        "Decision: ALLOW"
    )

    return {

        "allowed":
            True,

        "high_risk":
            False,

        "reason":
            "Low-risk operation."
    }


# ============================================================
# PERMISSION CHECK
# ============================================================

def check_permission(action):

    print("\n==========================================")
    print("           PERMISSION CHECK")
    print("==========================================")

    role = CURRENT_USER["role"]

    print(
        "User:",
        CURRENT_USER["name"]
    )

    print(
        "Role:",
        role
    )

    print(
        "Requested Action:",
        action
    )

    allowed_actions = PERMISSIONS.get(
        role,
        []
    )

    if action in allowed_actions:

        print(
            "Permission: ALLOWED"
        )

        return True

    print(
        "Permission: DENIED"
    )

    return False


# ============================================================
# HUMAN APPROVAL
# ============================================================

def human_approval(action):

    print("\n==========================================")
    print("          HUMAN APPROVAL")
    print("==========================================")

    print(
        "HIGH-RISK ACTION DETECTED"
    )

    print(
        "\nAction:",
        action
    )

    print(
        "User:",
        CURRENT_USER["name"]
    )

    print(
        "Environment:",
        CURRENT_USER["environment"]
    )

    approval = input(
        "\nApprove this action? (y/n): "
    ).strip().lower()

    if approval == "y":

        print(
            "\nHuman Decision: APPROVED"
        )

        return True

    print(
        "\nHuman Decision: REJECTED"
    )

    return False


# ============================================================
# AGENT STATE DISPLAY
# ============================================================

def show_state(state):

    print("\n==========================================")
    print("              AGENT STATE")
    print("==========================================")

    print(
        json.dumps(
            state,
            indent=4
        )
    )


# ============================================================
# EXTRACT ID FROM QUESTION
# ============================================================

def extract_integration_id(question):

    words = question.split()

    for word in words:

        cleaned = (
            word
            .replace(".", "")
            .replace(",", "")
            .replace("?", "")
        )

        if cleaned.isdigit():

            return cleaned

    return "12345"


# ============================================================
# EXTRACT CUSTOMER ID
# ============================================================

def extract_customer_id(question):

    words = question.split()

    for word in words:

        cleaned = (
            word
            .replace(".", "")
            .replace(",", "")
            .replace("?", "")
        )

        if cleaned.upper().startswith("C"):

            return cleaned.upper()

    return "C100"


# ============================================================
# FINAL ANSWER
# ============================================================

def generate_final_answer(
    question,
    state
):

    print("\n==========================================")
    print("            FINAL ANSWER")
    print("==========================================")

    observations = state["observations"]

    if state["route"] == "KNOWLEDGE":

        answer = (
            "OAuth 2.0 is commonly used "
            "for API authorization."
        )

    elif state["route"] == "LIVE_DATA":

        status = None
        error = None
        docs = None

        for item in observations:

            if "status" in item:

                status = item["status"]

            if "error_code" in item:

                error = item["error_code"]

            if "documentation" in item:

                docs = item["documentation"]

        if error:

            answer = (
                f"The integration failed with "
                f"{error}. "
                f"The likely cause is an expired "
                f"OAuth token. "
                f"Recommended action: {docs}"
            )

        elif status:

            answer = (
                f"The integration status is "
                f"{status}."
            )

        else:

            answer = (
                "I don't have enough information."
            )

    elif state["route"] == "DATABASE":

        for item in observations:

            if "sales" in item:

                answer = (
                    f"Customer "
                    f"{item['customer_id']} "
                    f"has sales of "
                    f"{item['sales']}."
                )

                break

        else:

            answer = (
                "No sales information found."
            )

    elif state["route"] == "ACTION":

        for item in observations:

            if item.get("status") == "SUCCESS":

                answer = (
                    f"The requested action "
                    f"{item.get('action')} "
                    f"was completed successfully."
                )

                break

        else:

            answer = (
                "The requested action "
                "was not executed."
            )

    else:

        answer = (
            "I don't have enough information "
            "to answer that request."
        )

    print(answer)

    return answer


# ============================================================
# KNOWLEDGE TOOL
# ============================================================

def search_knowledge(question):

    print("\n==========================================")
    print("          TOOL: KNOWLEDGE SEARCH")
    print("==========================================")

    result = {

        "content":
            "OAuth 2.0 is commonly used for API authorization."
    }

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    return result


# ============================================================
# COMPLETE AGENT
# ============================================================

def run_agent(question):

    print("\n############################################################")
    print("              ENTERPRISE AI AGENT")
    print("############################################################")

    print("\nUSER QUESTION:")
    print(question)

    # --------------------------------------------------------
    # 1. CREATE STATE
    # --------------------------------------------------------

    state = create_agent_state(
        question
    )

    # --------------------------------------------------------
    # 2. ROUTER
    # --------------------------------------------------------

    route = route_question(
        question
    )

    state["route"] = route

    # --------------------------------------------------------
    # 3. PLANNER
    # --------------------------------------------------------

    plan = create_plan(
        question,
        route
    )

    state["plan"] = plan

    # --------------------------------------------------------
    # 4. EXECUTION LOOP
    # --------------------------------------------------------

    for step in plan:

        state["iteration"] += 1

        print("\n############################################################")
        print(
            f"              ITERATION {state['iteration']}"
        )
        print("############################################################")

        print(
            "Current Step:",
            step
        )

        # ====================================================
        # KNOWLEDGE
        # ====================================================

        if step == "search_knowledge":

            result = search_knowledge(
                question
            )

            state["observations"].append(
                result
            )

            state["completed_steps"].append(
                step
            )

            state["tool_results"].append(
                result
            )

        # ====================================================
        # OIC STATUS
        # ====================================================

        elif step == "get_integration_status":

            integration_id = extract_integration_id(
                question
            )

            result = get_integration_status(
                integration_id
            )

            state["observations"].append(
                result
            )

            state["completed_steps"].append(
                step
            )

            state["tool_results"].append(
                result
            )

        # ====================================================
        # ERROR
        # ====================================================

        elif step == "get_error_details":

            integration_id = extract_integration_id(
                question
            )

            result = get_error_details(
                integration_id
            )

            state["observations"].append(
                result
            )

            state["completed_steps"].append(
                step
            )

            state["tool_results"].append(
                result
            )

        # ====================================================
        # DOCUMENTATION
        # ====================================================

        elif step == "search_oic_docs":

            result = search_oic_docs(
                "OIC authentication failure OAuth token"
            )

            state["observations"].append(
                result
            )

            state["completed_steps"].append(
                step
            )

            state["tool_results"].append(
                result
            )

        # ====================================================
        # DATABASE
        # ====================================================

        elif step == "get_customer_sales":

            customer_id = extract_customer_id(
                question
            )

            result = get_customer_sales(
                customer_id
            )

            state["observations"].append(
                result
            )

            state["completed_steps"].append(
                step
            )

            state["tool_results"].append(
                result
            )

        # ====================================================
        # ACTION IDENTIFICATION
        # ====================================================

        elif step == "identify_action":

            question_lower = question.lower()

            if "delete" in question_lower:

                action = "delete_integration"

            elif "restart" in question_lower:

                action = "restart_integration"

            else:

                action = "unknown_action"

            state["current_action"] = action

            print(
                "\nACTION IDENTIFIED:",
                action
            )

            state["completed_steps"].append(
                step
            )

        # ====================================================
        # GUARDRAIL
        # ====================================================

        elif step == "check_guardrail":

            action = state["current_action"]

            result = check_guardrail(
                action
            )

            state["observations"].append(
                result
            )

            if not result["allowed"]:

                state["status"] = "BLOCKED"

                print(
                    "\nAgent stopped by guardrail."
                )

                break

            state["completed_steps"].append(
                step
            )

        # ====================================================
        # PERMISSION
        # ====================================================

        elif step == "check_permission":

            action = state["current_action"]

            allowed = check_permission(
                action
            )

            if not allowed:

                state["status"] = "PERMISSION_DENIED"

                print(
                    "\nAgent stopped by permission system."
                )

                break

            state["completed_steps"].append(
                step
            )

        # ====================================================
        # HUMAN APPROVAL
        # ====================================================

        elif step == "request_human_approval":

            action = state["current_action"]

            approved = human_approval(
                action
            )

            if not approved:

                state["status"] = "HUMAN_REJECTED"

                print(
                    "\nAgent stopped by human."
                )

                break

            state["completed_steps"].append(
                step
            )

        # ====================================================
        # ACTION EXECUTION
        # ====================================================

        elif step == "execute_action":

            action = state["current_action"]

            integration_id = extract_integration_id(
                question
            )

            if action == "restart_integration":

                result = restart_integration(
                    integration_id
                )

            elif action == "delete_integration":

                result = delete_integration(
                    integration_id
                )

            else:

                result = {
                    "status":
                        "FAILED",
                    "reason":
                        "Unknown action"
                }

            state["observations"].append(
                result
            )

            state["tool_results"].append(
                result
            )

            state["completed_steps"].append(
                step
            )

        # ====================================================
        # FINAL ANSWER
        # ====================================================

        elif step == "generate_answer":

            answer = generate_final_answer(
                question,
                state
            )

            state["final_answer"] = answer

            state["status"] = "COMPLETED"

            state["completed_steps"].append(
                step
            )

    # --------------------------------------------------------
    # MEMORY
    # --------------------------------------------------------

    if state["final_answer"]:

        add_memory(
            question,
            state["final_answer"]
        )

    # --------------------------------------------------------
    # FINAL STATE
    # --------------------------------------------------------

    print("\n############################################################")
    print("                 FINAL AGENT STATE")
    print("############################################################")

    show_state(
        state
    )

    return state


# ============================================================
# TEST SCENARIOS
# ============================================================

def run_demo_scenarios():

    scenarios = [

        "What is OAuth 2.0?",

        "What is the current status of OIC integration 12345?",

        "Why did OIC integration 12345 fail?",

        "Show me the sales amount for customer C100.",

        "Restart OIC integration 12345.",

        "Delete OIC integration 12345."
    ]

    for index, question in enumerate(
        scenarios,
        start=1
    ):

        print("\n\n")
        print("############################################################")
        print(
            f"                 SCENARIO {index}"
        )
        print("############################################################")

        run_agent(
            question
        )

        input(
            "\nPress ENTER for next scenario..."
        )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    print("\n==========================================")
    print("       ENTERPRISE AI AGENT")
    print("==========================================")

    print(
        "Gemini initialized successfully."
    )

    while True:

        print("\n==========================================")
        print("                 MENU")
        print("==========================================")

        print("1. Ask Agent")
        print("2. Run all demo scenarios")
        print("3. Show Memory")
        print("4. Test Guardrails")
        print("5. Test Permissions")
        print("6. Exit")

        choice = input(
            "\nSelect option: "
        ).strip()

        # ----------------------------------------------------
        # ASK AGENT
        # ----------------------------------------------------

        if choice == "1":

            question = input(
                "\nEnter your question: "
            ).strip()

            if question:

                run_agent(
                    question
                )

        # ----------------------------------------------------
        # ALL SCENARIOS
        # ----------------------------------------------------

        elif choice == "2":

            run_demo_scenarios()

        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        elif choice == "3":

            show_memory()

        # ----------------------------------------------------
        # GUARDRAILS
        # ----------------------------------------------------

        elif choice == "4":

            print("\n==========================================")
            print("            GUARDRAIL TEST")
            print("==========================================")

            for action in [
                "get_integration_status",
                "restart_integration",
                "delete_integration"
            ]:

                result = check_guardrail(
                    action
                )

                print(
                    "\nResult:",
                    result
                )

        # ----------------------------------------------------
        # PERMISSIONS
        # ----------------------------------------------------

        elif choice == "5":

            print("\n==========================================")
            print("          PERMISSION TEST")
            print("==========================================")

            for role in PERMISSIONS:

                print(
                    f"\nROLE: {role}"
                )

                for action in [
                    "get_integration_status",
                    "restart_integration",
                    "delete_integration"
                ]:

                    allowed = action in PERMISSIONS[
                        role
                    ]

                    print(
                        f"{action:30} "
                        f"{'ALLOWED' if allowed else 'DENIED'}"
                    )

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "6":

            print(
                "\nEnterprise AI Agent finished."
            )

            break

        else:

            print(
                "\nInvalid option."
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
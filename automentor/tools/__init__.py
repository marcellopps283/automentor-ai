from .memory_tool import update_knowledge_node, memory_store
from .calendar_tool import schedule_study_session
from .github_tool import create_github_lab
from .showcase_tool import generate_linkedin_showcase

# List of tools provided to the Gemini model
MENTOR_TOOLS = [
    update_knowledge_node,
    schedule_study_session,
    create_github_lab,
    generate_linkedin_showcase,
]

from .memory_tool import update_knowledge_node, memory_store, MemoryStore
from .calendar_tool import schedule_study_session
from .github_tool import create_github_lab
from .showcase_tool import generate_linkedin_showcase
from .cheat_sheet_tool import generate_study_cheat_sheet

# Registered tools for Gemini 3.5 function calling
MENTOR_TOOLS = [
    update_knowledge_node,
    schedule_study_session,
    create_github_lab,
    generate_linkedin_showcase,
    generate_study_cheat_sheet
]

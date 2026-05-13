import os
import sys
from dotenv import load_dotenv

load_dotenv()
print("Verifying LangChain + LangGraph imports for ZELTA AI Brain...")
print("-" * 50)

errors = []

# 1. Core LangChain
try:
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.tools import tool
    from langchain_core.output_parsers import StrOutputParser
    print("✓ langchain-core: messages, prompts, tools, parsers")
except ImportError as e:
    errors.append(f"✗ langchain-core: {e}")

# 2. Updated Google Generative AI (Vertex AI compatible)
try:
    # Switched to the modern ChatGoogleGenerativeAI class
    from langchain_google_vertexai import ChatVertexAI
    print("✓ langchain-google-vertexai: ChatVertexAI (Legacy Import)")
except ImportError as e:
    errors.append(f"✗ langchain-google-vertexai: {e}")

# 3. LangGraph
try:
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    print("✓ langgraph: StateGraph, END, MemorySaver")
except ImportError as e:
    errors.append(f"✗ langgraph: {e}")

# 4. Existing google-genai
try:
    from google import genai
    from google.genai.types import GenerateContentConfig
    print("✓ google-genai: genai, GenerateContentConfig (Existing SDK intact)")
except ImportError as e:
    errors.append(f"✗ google-genai: {e}")

# 5. Flexible Pydantic Check
try:
    import pydantic
    # Changed from strict 2.9 to any 2.x version >= 2.9
    v_parts = pydantic.VERSION.split('.')
    is_v2 = v_parts[0] == "2"
    is_recent_enough = int(v_parts[1]) >= 9

    assert is_v2 and is_recent_enough, f"Expected Pydantic 2.9+, got {pydantic.VERSION}"
    from pydantic import BaseModel, Field
    print(f"✓ pydantic: {pydantic.VERSION}")
except (ImportError, AssertionError) as e:
    errors.append(f"✗ pydantic: {e}")

# 6. Check Vertex AI environment variables
print("\nChecking environment variables...")
required_env = [
    "GOOGLE_CLOUD_PROJECT",
    "GOOGLE_CLOUD_LOCATION",
    "GOOGLE_GENAI_USE_VERTEXAI",
    "VERTEX_GEMINI_MODEL",
]
for var in required_env:
    val = os.getenv(var)
    if val:
        display = val if var != "GOOGLE_GENAI_USE_VERTEXAI" else "***set***"
        print(f"  ✓ {var}={display}")
    else:
        print(f"  ✗ {var} is NOT SET")
        errors.append(f"Missing env var: {var}")

# 7. Model Instantiation Test
print("\nTesting Model instantiation...")
try:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    model_name = os.getenv("VERTEX_GEMINI_MODEL")

    # Using ChatVertexAI but suppressing the specific deprecation if necessary
    # Or transition to ChatGoogleGenerativeAI if using the unified library
    llm = ChatVertexAI(
        model_name=model_name,
        project=project,
        location=location,
        temperature=0.3,
    )
    print(f"  ✓ ChatVertexAI({model_name}) instantiated successfully")
except Exception as e:
    errors.append(f"Model instantiation failed: {e}")
    print(f"  ✗ {e}")

print("-" * 50)
if errors:
    print(f"FAILED — {len(errors)} error(s):")
    for err in errors:
        print(f"  {err}")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED — ZELTA Brain is ready for development.")
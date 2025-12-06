from app.core.llm_model import get_llm


def test_llm_fallback():
    print("Loading LLM...")
    llm = get_llm()

    print("LLM Loaded:", type(llm).__name__)

    response = llm.invoke("Say hello in one sentence.")
    print("Response:", response)


test_llm_fallback()


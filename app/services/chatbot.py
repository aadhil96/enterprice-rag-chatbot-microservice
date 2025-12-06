#services/chatbot.py
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
# Memory imports
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from typing import Dict, List
from app.core.embedding_model import get_embedding_function
from app.core.llm_model import get_llm
from app.core.vectorstore import get_retriever
from app.core.prompt import qa_prompt


embedding_function = get_embedding_function()
llm = get_llm()
retriver = get_retriever()
chat_prompt = qa_prompt

chat_histories: Dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> ChatMessageHistory:

    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

def get_rag_chain():

    question_answer_chain = create_stuff_documents_chain(llm, chat_prompt)

    rag_chain = create_retrieval_chain(retriver, question_answer_chain)
    
    rag_chain_with_history = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )
    
    return rag_chain_with_history



def clear_session_history(session_id: str):
    if session_id in chat_histories:
        del chat_histories[session_id]


def get_all_sessions():
    return list(chat_histories.keys())
  
  
    
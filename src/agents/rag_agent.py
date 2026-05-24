from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from config import Config

class CitationValidation(BaseModel):
    missing_citations: list[str] = Field(description="Claims that require a scholarly citation but lack one.")
    matched_references: list[str] = Field(description="Existing references verified against known literature.")
    hallucination_warnings: list[str] = Field(description="Sentences that appear to misrepresent academic facts or data.")

class RetrievalValidationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=Config.LLM_MODEL,
            openai_api_key=Config.OPENAI_API_KEY,
            temperature=0.1
        )
        self.structured_llm = self.llm.with_structured_output(CitationValidation)

    def cross_reference_draft(self, draft_text: str, context_documents: list[str] = None) -> CitationValidation:
        """
        Cross-references the manuscript draft against provided context documents
        or vector store references to validate academic integrity.
        """
        # Fallback empty context if none is injected from the vector database layer
        docs_context = "\n---\n".join(context_documents) if context_documents else "No external database context supplied."

        system_prompt = (
            "You are the Retrieval Validation Agent for PAMAS Module 3.\n"
            "Your task is to cross-reference the user's text draft against the provided background context documents.\n"
            "Identify any high-risk factual claims that lack citations, validate current references, "
            "and call out any specific academic hallucinations."
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Background Database Context:\n{context}\n\nManuscript Draft to Validate:\n{text}")
        ])

        chain = prompt | self.structured_llm
        return chain.invoke({"text": draft_text, "context": docs_context})

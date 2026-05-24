from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import json
from config import Config

# Define a structured output schema for validation reports
class VerificationReport(BaseModel):
    coherence_score: float = Field(description="Score from 0.0 to 1.0 indicating logical flow.")
    hallucination_risk: str = Field(description="Risk level: Low, Medium, or High.")
    formatting_compliant: bool = Field(description="True if document structure matches targets.")
    critical_feedback: list[str] = Field(description="Actionable issues that must be fixed.")
    suggestions: list[str] = Field(description="Minor improvements for style or tone.")

class SelfVerificationAgent:
    def __init__(self):
        # Initialize the language model using the configuration settings
        self.llm = ChatOpenAI(
            model=Config.LLM_MODEL, 
            openai_api_key=Config.OPENAI_API_KEY,
            temperature=0.2
        )
        # Bind the Pydantic schema to force structured JSON responses
        self.structured_llm = self.llm.with_structured_output(VerificationReport)
        
    def verify_manuscript(self, draft_text: str, target_format: str = "IEEE") -> VerificationReport:
        """
        Analyzes academic text drafts for structural soundness, 
        logical contradictions, and style guide adherence.
        """
        system_prompt = (
            "You are an expert academic editor and peer-reviewer for PAMAS Module 3.\n"
            "Analyze the submitted text comprehensively. Evaluate its logical flow, check for "
            "obvious factual leaps or hallucinations, and determine if it complies with {format} guidelines."
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Please verify the following manuscript draft:\n\n{text}")
        ])
        
        # Build and invoke the processing pipeline
        chain = prompt | self.structured_llm
        report = chain.invoke({"text": draft_text, "format": target_format})
        return report

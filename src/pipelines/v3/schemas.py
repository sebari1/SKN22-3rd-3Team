from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractionMetadataV3(BaseModel):
    """Schema for LLM extraction in V3 (Clean)."""
    summary: str = Field(description="One sentence summary in professional Korean")
    keywords: List[str] = Field(description="3-5 high-signal keywords")
    intent_tags: List[str] = Field(description="Intent labels (e.g., 'Emergency', 'Daily Care')")

class ExtractionArticleV3(BaseModel):
    """The structured result LLM returns for each article in V3."""
    title_refined: str = Field(description="Refined, search-optimized title")
    metadata: ExtractionMetadataV3
    categories: List[str] = Field(description="Standardized English categories")
    specialists: List[str] = Field(description="Standardized English personas")

class StoredDocumentV3(ExtractionArticleV3):
    """Schema for final storage in MongoDB for V3 (Clean)."""
    uid: str = Field(description="Final unique ID (e.g., v3_00001)")
    text: str = Field(description="The full raw text of the article")
    tokenized_text: str = Field(description="The full text tokenized with custom dictionary")
    embedding: Optional[List[float]] = Field(default=None, description="OpenAI structured embedding")
    source: str = "bemypet_catlab"
    original_url: Optional[str] = None

class BatchResultV3(BaseModel):
    results: List[ExtractionArticleV3]

class BreedStats(BaseModel):
    weight_metric: str = "Unknown"
    life_span: str = "Unknown"
    indoor: Optional[int] = 0
    lap: Optional[int] = 0
    hypoallergenic: Optional[int] = 0
    adaptability: Optional[int] = 0
    affection_level: Optional[int] = 0
    child_friendly: Optional[int] = 0
    dog_friendly: Optional[int] = 0
    energy_level: Optional[int] = 0
    grooming: Optional[int] = 0
    health_issues: Optional[int] = 0
    intelligence: Optional[int] = 0
    shedding_level: Optional[int] = 0
    social_needs: Optional[int] = 0
    stranger_friendly: Optional[int] = 0
    vocalisation: Optional[int] = 0

class StoredBreedV3(BaseModel):
    """Schema for V3 Breed Collection."""
    uid: str = Field(description="Unique ID (e.g., breed_abys)")
    title_refined: str = Field(description="Unified Title field for Retriever compatibility")
    name_ko: str = Field(description="Korean Breed Name")
    name_en: str
    summary: str
    personality_traits: List[str]
    physical_traits: List[str]
    stats: BreedStats
    text: str = Field(description="Full description for RAG context")
    tokenized_text: str = Field(description="Kiwi tokenized text")
    embedding: Optional[List[float]] = None
    source: str = "thecatapi_integrated"
    categories: List[str] = ["Breeds"]
    specialists: List[str] = ["Matchmaker"]

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BasePreprocessor(ABC):
    """Abstract Base Class for Data Preprocessing."""
    @abstractmethod
    def run(self) -> str:
        """
        Executes the preprocessing logic.
        Returns:
            str: Path to the processed output file.
        """
        pass

class BaseEmbedder(ABC):
    """Abstract Base Class for Embedding Generation."""
    @abstractmethod
    async def run(self, input_path: str) -> str:
        """
        Generates embeddings for the input data.
        Args:
            input_path (str): Path to the preprocessed data file.
        Returns:
            str: Path to the embedded data file (pickle).
        """
        pass

class BaseLoader(ABC):
    """Abstract Base Class for Database Loading."""
    @abstractmethod
    async def run(self, input_path: str):
        """
        Loads the embedded data into the database.
        Args:
            input_path (str): Path to the embedded data file.
        """
        pass

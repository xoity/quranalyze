"""
Base visualization interface.

This module provides the abstract base class for all visualization
implementations in the framework.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..core.word import Word
from ..graph.graph_builder import WordGraph
from ..exceptions import VisualizationError


class BaseVisualizer(ABC):
    """
    Abstract base class for all visualizers.
    
    This class defines the interface that all visualization implementations
    must follow, ensuring consistency across different visualization methods.
    """
    
    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the visualizer with configuration options.
        
        Args:
            **kwargs: Configuration options specific to the visualizer
        """
        self.config = kwargs
    
    @abstractmethod
    def visualize_words(
        self,
        words: list[Word],
        title: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Visualize a list of words.
        
        Args:
            words: List of Word objects to visualize
            title: Optional title for the visualization
            **kwargs: Additional visualization options
            
        Returns:
            Visualization object (implementation-specific)
            
        Raises:
            VisualizationError: If visualization fails
        """
        pass
    
    @abstractmethod
    def visualize_graph(
        self,
        graph: WordGraph,
        title: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Visualize a word graph.
        
        Args:
            graph: WordGraph to visualize
            title: Optional title for the visualization
            **kwargs: Additional visualization options
            
        Returns:
            Visualization object (implementation-specific)
            
        Raises:
            VisualizationError: If visualization fails
        """
        pass
    
    @abstractmethod
    def save(self, filepath: str, **kwargs: Any) -> None:
        """
        Save the visualization to a file.
        
        Args:
            filepath: Path to save the visualization
            **kwargs: Format-specific save options
            
        Raises:
            VisualizationError: If saving fails
        """
        pass
    
    @abstractmethod
    def show(self) -> None:
        """
        Display the visualization.
        
        Raises:
            VisualizationError: If display fails
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """
        Close and cleanup the visualization.
        """
        pass


class VisualizationConfig:
    """
    Configuration container for visualization settings.
    
    This class holds common configuration options that can be used
    across different visualizer implementations.
    """
    
    def __init__(
        self,
        figure_size: tuple[int, int] = (12, 8),
        dpi: int = 100,
        point_size: int = 20,
        alpha: float = 0.6,
        color_scheme: str = "viridis",
        show_labels: bool = False,
        font_size: int = 10,
    ) -> None:
        """
        Initialize visualization configuration.
        
        Args:
            figure_size: Size of the figure (width, height)
            dpi: Dots per inch for the figure
            point_size: Size of points in scatter plots
            alpha: Transparency level (0.0 to 1.0)
            color_scheme: Color scheme/colormap name
            show_labels: Whether to show labels on points
            font_size: Font size for labels and text
        """
        self.figure_size = figure_size
        self.dpi = dpi
        self.point_size = point_size
        self.alpha = alpha
        self.color_scheme = color_scheme
        self.show_labels = show_labels
        self.font_size = font_size
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary of configuration options
        """
        return {
            "figure_size": self.figure_size,
            "dpi": self.dpi,
            "point_size": self.point_size,
            "alpha": self.alpha,
            "color_scheme": self.color_scheme,
            "show_labels": self.show_labels,
            "font_size": self.font_size,
        }

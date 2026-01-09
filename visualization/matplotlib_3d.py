"""
Matplotlib 3D visualization implementation.

This module provides 3D visualization capabilities using matplotlib.
"""

from typing import Any, Optional

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from ..config import (
    DEFAULT_ALPHA,
    DEFAULT_DPI,
    DEFAULT_FIGURE_SIZE,
    DEFAULT_POINT_SIZE,
)
from ..core.word import Word
from ..exceptions import VisualizationError
from ..graph.graph_builder import WordGraph
from .base import BaseVisualizer


class Matplotlib3DVisualizer(BaseVisualizer):
    """
    3D visualization using matplotlib.
    
    This visualizer creates 3D scatter plots of words based on their
    positions in the Quran (surah, ayah, position).
    """
    
    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the matplotlib 3D visualizer.
        
        Args:
            **kwargs: Configuration options including:
                - figure_size: Tuple of (width, height)
                - dpi: Dots per inch
                - point_size: Size of scatter points
                - alpha: Transparency level
                - color_scheme: Colormap name
        
        Raises:
            VisualizationError: If matplotlib is not available
        """
        if not MATPLOTLIB_AVAILABLE:
            raise VisualizationError(
                "Matplotlib is not installed. Install it with: pip install matplotlib"
            )
        
        super().__init__(**kwargs)
        
        self.figure_size = kwargs.get("figure_size", DEFAULT_FIGURE_SIZE)
        self.dpi = kwargs.get("dpi", DEFAULT_DPI)
        self.point_size = kwargs.get("point_size", DEFAULT_POINT_SIZE)
        self.alpha = kwargs.get("alpha", DEFAULT_ALPHA)
        self.color_scheme = kwargs.get("color_scheme", "viridis")
        
        self.fig: Optional[Any] = None
        self.ax: Optional[Any] = None
    
    def visualize_words(
        self,
        words: list[Word],
        title: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Visualize words as 3D scatter plot.
        
        The visualization maps:
        - X-axis: Surah number
        - Y-axis: Ayah number
        - Z-axis: Word position within ayah
        - Color: Surah number (for visual distinction)
        
        Args:
            words: List of Word objects to visualize
            title: Optional title for the plot
            **kwargs: Additional options (color_by, etc.)
            
        Returns:
            Matplotlib figure object
            
        Raises:
            VisualizationError: If visualization fails
        """
        if not words:
            raise VisualizationError("Cannot visualize empty word list")
        
        try:
            # Create figure and 3D axis
            self.fig = plt.figure(figsize=self.figure_size, dpi=self.dpi)
            self.ax = self.fig.add_subplot(111, projection='3d')
            
            # Extract coordinates
            x = [w.surah_number for w in words]
            y = [w.ayah_number for w in words]
            z = [w.position for w in words]
            
            # Color by surah number
            colors = [w.surah_number for w in words]
            
            # Create scatter plot
            scatter = self.ax.scatter(
                x, y, z,
                c=colors,
                cmap=self.color_scheme,
                s=self.point_size,
                alpha=self.alpha,
            )
            
            # Labels and title
            self.ax.set_xlabel('Surah Number', fontsize=10)
            self.ax.set_ylabel('Ayah Number', fontsize=10)
            self.ax.set_zlabel('Word Position', fontsize=10)
            
            if title:
                self.ax.set_title(title, fontsize=12)
            else:
                self.ax.set_title(f'3D Word Distribution ({len(words)} words)', fontsize=12)
            
            # Add colorbar
            self.fig.colorbar(scatter, ax=self.ax, label='Surah Number', shrink=0.5)
            
            return self.fig
        except Exception as e:
            raise VisualizationError(f"Failed to visualize words: {e}") from e
    
    def visualize_graph(
        self,
        graph: WordGraph,
        title: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Visualize a word graph in 3D.
        
        This creates a 3D scatter plot of nodes with edges drawn between them.
        
        Args:
            graph: WordGraph to visualize
            title: Optional title for the plot
            **kwargs: Additional options
            
        Returns:
            Matplotlib figure object
            
        Raises:
            VisualizationError: If visualization fails
        """
        if graph.node_count() == 0:
            raise VisualizationError("Cannot visualize empty graph")
        
        try:
            # Create figure and 3D axis
            self.fig = plt.figure(figsize=self.figure_size, dpi=self.dpi)
            self.ax = self.fig.add_subplot(111, projection='3d')
            
            # Plot nodes
            words = list(graph.nodes.keys())
            x = [w.surah_number for w in words]
            y = [w.ayah_number for w in words]
            z = [w.position for w in words]
            colors = [w.surah_number for w in words]
            
            scatter = self.ax.scatter(
                x, y, z,
                c=colors,
                cmap=self.color_scheme,
                s=self.point_size,
                alpha=self.alpha,
            )
            
            # Plot edges
            for word1, word2, weight, _ in graph.edges:
                xs = [word1.surah_number, word2.surah_number]
                ys = [word1.ayah_number, word2.ayah_number]
                zs = [word1.position, word2.position]
                self.ax.plot(xs, ys, zs, 'gray', alpha=0.2, linewidth=0.5)
            
            # Labels and title
            self.ax.set_xlabel('Surah Number', fontsize=10)
            self.ax.set_ylabel('Ayah Number', fontsize=10)
            self.ax.set_zlabel('Word Position', fontsize=10)
            
            if title:
                self.ax.set_title(title, fontsize=12)
            else:
                self.ax.set_title(
                    f'Word Graph ({graph.node_count()} nodes, {graph.edge_count()} edges)',
                    fontsize=12
                )
            
            # Add colorbar
            self.fig.colorbar(scatter, ax=self.ax, label='Surah Number', shrink=0.5)
            
            return self.fig
        except Exception as e:
            raise VisualizationError(f"Failed to visualize graph: {e}") from e
    
    def save(self, filepath: str, **kwargs: Any) -> None:
        """
        Save the visualization to a file.
        
        Args:
            filepath: Path to save the visualization
            **kwargs: Additional save options (format, dpi, etc.)
            
        Raises:
            VisualizationError: If saving fails or no figure exists
        """
        if self.fig is None:
            raise VisualizationError("No figure to save. Create a visualization first.")
        
        try:
            self.fig.savefig(filepath, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to save figure: {e}") from e
    
    def show(self) -> None:
        """
        Display the visualization.
        
        Raises:
            VisualizationError: If no figure exists
        """
        if self.fig is None:
            raise VisualizationError("No figure to show. Create a visualization first.")
        
        try:
            plt.show()
        except Exception as e:
            raise VisualizationError(f"Failed to show figure: {e}") from e
    
    def close(self) -> None:
        """Close and cleanup the visualization."""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None

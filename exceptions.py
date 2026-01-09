"""
Custom exceptions for the quranalyze framework.

This module defines all custom exceptions used throughout the framework
to provide clear error handling and messaging.
"""


class QuranalyzeError(Exception):
    """Base exception for all quranalyze-related errors."""
    pass


class DataLoadError(QuranalyzeError):
    """Raised when data cannot be loaded from the quranjson dataset."""
    pass


class DataValidationError(QuranalyzeError):
    """Raised when loaded data does not match expected structure."""
    pass


class FilterError(QuranalyzeError):
    """Raised when filter operations fail or produce invalid results."""
    pass


class GraphBuildError(QuranalyzeError):
    """Raised when graph construction fails."""
    pass


class VisualizationError(QuranalyzeError):
    """Raised when visualization operations fail."""
    pass


class NormalizationError(QuranalyzeError):
    """Raised when text normalization fails."""
    pass


class TokenizationError(QuranalyzeError):
    """Raised when tokenization fails."""
    pass


class TransliterationError(QuranalyzeError):
    """Raised when transliteration operations fail."""
    pass

# quranalyze Development Guide

## Overview

This document provides guidance for developers working on the quranalyze framework.

## Core Principles

### 1. Observational Analysis Only
- No interpretation of religious meaning
- No thematic conclusions
- Only factual, observable data relationships
- Document all assumptions explicitly

### 2. Data Source Integrity
- quranjson is the **only** data source
- Never accept user-supplied text
- Never fetch external data
- Reject unknown data formats

### 3. Transparency
- All defaults in `config.py`
- Explicit error messages
- Document all transformations
- Type hints everywhere

### 4. Reproducibility
- Deterministic algorithms
- Export capabilities
- Version metadata
- No hidden state

## Code Style

### Type Hints
All functions must have complete type hints:

```python
def process_ayah(ayah: Ayah, normalize: bool = True) -> list[Word]:
    """Process ayah into words."""
    ...
```

### Docstrings
Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
```

### Immutability
Prefer immutable data structures:
- Use `@dataclass(frozen=True)` for data classes
- Use tuples instead of lists for fixed collections
- Document any mutable state

### Error Handling
- Use custom exceptions from `exceptions.py`
- Provide clear error messages
- Include context in exceptions
- Don't suppress errors silently

## Module Guidelines

### Core Module
- Contains fundamental data structures
- All classes should be immutable when possible
- Validate data in `__post_init__`
- Provide clear `__repr__` and `__str__`

### Data Module
- Handle all file I/O
- Validate data structure strictly
- Use context managers for file operations
- Provide clear validation errors

### Linguistics Module
- Current implementations are placeholders
- Future: integrate external tools (AraMorph, MADAMIRA)
- Document unavailable features clearly
- Return `None` for unavailable data

### Graph Module
- Use standard graph terminology
- Provide both node-centric and edge-centric APIs
- Document time/space complexity
- Consider memory for large graphs

### Visualization Module
- Follow BaseVisualizer interface
- Support save and show operations
- Provide sensible defaults
- Handle missing dependencies gracefully

## Testing

### Unit Tests
```python
def test_word_creation():
    """Test Word object creation and validation."""
    word = Word(
        surah_number=1,
        ayah_number=1,
        position=0,
        text="test",
        normalized="test",
        buckwalter="test"
    )
    assert word.location == (1, 1, 0)
```

### Integration Tests
Test complete workflows:
- Load data
- Build corpus
- Apply filters
- Generate outputs

### Edge Cases
Always test:
- Empty inputs
- Invalid data
- Missing files
- Large datasets

## Performance Considerations

### Memory
- Corpus can be large (77,000+ words)
- Consider generators for large operations
- Profile memory usage
- Document memory requirements

### Speed
- Tokenization is O(n) where n = text length
- Graph construction is O(n²) for all-pairs
- Filtering is O(n) for linear scans
- Consider indexing for repeated queries

## Future Enhancements

### Morphological Analysis
Integration points:
- `linguistics/morphology.py` - root/lemma extraction
- Update Word objects with morphological data
- Extend graph relations to use roots/lemmas

### POS Tagging
Integration points:
- `linguistics/pos.py` - tagging implementation
- Train on annotated Quranic corpus
- Consider context-aware tagging

### Advanced Clustering
- Integrate networkx for graph algorithms
- Implement community detection
- Add spectral clustering
- Document algorithm choices

### Audio Synthesis
- Integrate Arabic TTS engine
- Apply tajweed rules
- Handle phonetic edge cases
- Support multiple reciters

## Documentation

### Code Comments
- Explain "why", not "what"
- Document non-obvious decisions
- Reference external resources
- Keep comments up-to-date

### API Documentation
- Complete docstrings
- Usage examples in docstrings
- Link related functions
- Document side effects

### User Documentation
- Clear installation instructions
- Working examples
- Common use cases
- Troubleshooting guide

## Release Checklist

Before releasing a new version:
- [ ] All tests pass
- [ ] Type checking passes (mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `__init__.py`
- [ ] Examples tested
- [ ] README.md reviewed

## Questions?

For questions about development:
1. Check existing documentation
2. Review similar code in the codebase
3. Ensure changes align with core principles
4. Document your decisions

## Philosophy

Remember: This is a research tool, not an interpretation tool. Every feature should:
- Provide observable facts
- Maintain transparency
- Enable reproducibility
- Respect the data source

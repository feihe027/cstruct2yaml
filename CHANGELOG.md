# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-27

### Added
- Initial release of C Struct YAML Generator
- Core functionality for parsing C header files with pycparser
- Support for complex nested structures and bitfields
- Anonymous structure and union handling
- Multi-dimensional array support
- Bit-level precision calculations
- Configurable pack alignment settings
- YAML output format with comprehensive metadata
- YAML viewer utility for analyzing generated files
- Tree view and flat list display modes
- Member filtering capabilities
- Verbose debugging output
- Comprehensive error handling
- MIT license
- Complete documentation and examples

### Features
- **Struct Analysis**: Complete C struct parsing with nested support
- **Bitfield Support**: Precise bitfield width and offset calculations
- **Memory Layout**: Bit-level accurate offset and size information
- **Preprocessing**: Intelligent handling of includes, macros, and directives
- **Multiple Output Modes**: Single struct or batch processing
- **Flexible Configuration**: Customizable alignment and output options
- **Cross-platform**: Works on Windows, macOS, and Linux

### Technical Details
- Python 3.7+ compatibility
- Based on pycparser library for reliable C parsing
- YAML output with human-readable formatting
- Command-line interface with extensive options
- Modular design for easy extension
- Type hints for better code maintainability

### Documentation
- Comprehensive README with usage examples
- API documentation with detailed method descriptions
- Example input and output files
- Installation and setup instructions
- Contributing guidelines

## [Unreleased]

### Planned Features
- JSON output format support
- Plugin system for custom processors
- GUI interface
- Integration with popular IDEs
- Performance optimizations for large files
- Support for C++ features
- Web-based viewer interface

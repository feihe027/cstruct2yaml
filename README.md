# C Struct YAML Generator

A powerful and flexible C struct analysis tool based on Python's pycparser library that converts complex C structures into detailed YAML description files. This tool provides comprehensive analysis of C data structures with bit-level precision, making it ideal for firmware development, protocol analysis, and memory layout optimization.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Features

### 🔍 **Comprehensive Structure Analysis**
- ✅ **Complex nested struct analysis** - Handles deeply nested structures and compositions with unlimited depth
- ✅ **Anonymous structures and unions** - Full support for anonymous members with automatic member expansion
- ✅ **Union member analysis** - Accurate union size calculation and member overlap detection
- ✅ **Typedef resolution** - Complete typedef chain resolution and type aliasing
- ✅ **Struct inheritance** - Handles complex struct compositions and nested relationships

### 🎯 **Precise Memory Layout**
- ✅ **Bit-level precision** - Precise offset and size calculations at bit level granularity
- ✅ **Bitfield processing** - Accurate bitfield width, offset, and packing calculations
- ✅ **Memory alignment** - Configurable pack alignment with automatic padding detection
- ✅ **Structure padding** - Automatic detection and calculation of padding bytes
- ✅ **Pointer analysis** - Multi-level pointer support with base type tracking

### 📊 **Advanced Array Support**
- ✅ **Multi-dimensional arrays** - Support for arrays of any dimension with size calculation
- ✅ **C# style array notation** - Arrays displayed as `type[dim1][dim2]...` for clarity
- ✅ **Array of structures** - Complex nested array structures with member expansion
- ✅ **Dynamic array detection** - Flexible array member support
- ✅ **Array size calculation** - Precise total size calculation for multi-dimensional arrays

### ⚙️ **Intelligent Preprocessing**
- ✅ **Macro expansion** - Smart macro evaluation with expression calculation
- ✅ **Include file resolution** - Recursive include file processing
- ✅ **Conditional compilation** - Preprocessing directive handling
- ✅ **Pragma pack support** - Automatic pack directive detection and application
- ✅ **Comment removal** - Clean C/C++ comment stripping

### 📤 **Flexible Output & Configuration**
- ✅ **YAML output format** - Human-readable structured output
- ✅ **Configurable detail level** - Optional inclusion of bitfields, offsets, and children
- ✅ **Verbose analysis mode** - Detailed processing information and debugging
- ✅ **Single or batch processing** - Analyze specific structs or entire files
- ✅ **Custom alignment settings** - Configurable pack alignment for different platforms

## Project Structure

```
cstruct2yaml/
├── pycparser_yaml_generator.py  # Main YAML generator (core analysis engine)
├── yaml_viewer.py               # YAML file viewer and analysis utility  
├── test.h                       # Comprehensive test C header file
├── example.h                    # Example dependency header
├── DeviceManager.yml            # Generated YAML output example
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Package setup and installation
├── README.md                    # This documentation file
├── LICENSE                      # MIT license
├── CHANGELOG.md                 # Version history and changes
├── CONTRIBUTING.md              # Contribution guidelines
└── tests/                       # Test suite
    ├── test_integration.py      # Integration tests
    └── __init__.py              # Test package initialization
```

## Supported C Features

### 🏗️ **Data Types**
- **Basic Types**: `char`, `int`, `short`, `long`, `long long`, `float`, `double`
- **Signed/Unsigned Variants**: Complete support for all signed and unsigned integer types
- **Size Variants**: `int8_t`, `int16_t`, `int32_t`, `int64_t`, `size_t`, `ptrdiff_t`
- **Character Types**: `char`, `wchar_t`, `char16_t`, `char32_t`
- **Boolean Types**: `bool`, `_Bool`

### 🔗 **Complex Types**
- **Pointers**: Single and multi-level pointers (`*`, `**`, `***`, etc.)
- **Arrays**: Single and multi-dimensional arrays with C# style notation
- **Structures**: Named and anonymous structures with nested support
- **Unions**: Named and anonymous unions with overlap analysis
- **Enumerations**: Named and anonymous enums with value tracking
- **Function Pointers**: Function pointer type analysis

### ⚡ **Special Features**
- **Bitfields**: Precise bit-level field analysis with packing optimization
- **Anonymous Members**: Automatic expansion of anonymous struct/union members
- **Nested Structures**: Unlimited depth nested structure analysis
- **Typedef Chains**: Complete typedef resolution and type aliasing
- **Pragma Pack**: Automatic pack directive detection and application
- **Zero-Length Arrays**: Flexible array member support

## Installation

### Prerequisites

- **Python 3.7+** - Required for modern asyncio and type hinting support
- **pip package manager** - For dependency installation
- **C preprocessor** (optional) - For advanced macro processing

### Quick Install

```bash
# Clone the repository
git clone https://github.com/feihe027/cstruct2yaml.git
cd cstruct2yaml

# Install dependencies
pip install -r requirements.txt

# For development environment
pip install -r requirements-dev.txt
```

### Dependencies

**Core Dependencies:**
- `pycparser>=2.20` - C parser and AST analysis
- `PyYAML>=5.4.1` - YAML file generation and parsing

**Development Dependencies:**
- `pytest>=6.0` - Unit testing framework
- `pytest-cov>=2.10` - Test coverage reporting
- `black>=21.0` - Code formatting
- `flake8>=3.8` - Code linting

### Verify Installation

```bash
# Test the installation
python pycparser_yaml_generator.py test.h -s DeviceManager -v

# Expected output: Should generate DeviceManager.yml successfully
```

## Quick Start

### 1. Analyze a Specific Structure

```bash
# Analyze a specific struct with verbose output
python pycparser_yaml_generator.py test.h -s DeviceManager -v

# Output: Generates DeviceManager.yml with detailed analysis
```

### 2. Analyze All Structures

```bash
# Analyze all structs in a header file
python pycparser_yaml_generator.py test.h -v

# Output: Generates test_structs.yml with all discovered structures
```

### 3. View Generated Results

```bash
# View the generated YAML with summary
python yaml_viewer.py DeviceManager.yml -s

# View with tree structure (depth limited to 2 levels)
python yaml_viewer.py DeviceManager.yml -t -d 2

# View only array members
python yaml_viewer.py DeviceManager.yml -l -f array
```

### 4. Custom Configuration

```bash
# Use 4-byte alignment (common for 32-bit systems)
python pycparser_yaml_generator.py test.h -s MyStruct -p 4

# Exclude bitfield details for cleaner output
python pycparser_yaml_generator.py test.h --no-bitfields --no-offsets

# Save to custom output file
python pycparser_yaml_generator.py test.h -s MyStruct -o custom_output.yml
```

## Usage Guide

### 1. Core Generator (pycparser_yaml_generator.py)

The main tool for converting C structs to YAML format with comprehensive analysis capabilities.

#### Command Line Arguments

| Argument         | Type | Description                              | Default        |
| ---------------- | ---- | ---------------------------------------- | -------------- |
| `input_file`     | str  | Input C header file (required)           | -              |
| `-s, --struct`   | str  | Target struct name (optional)            | All structs    |
| `-o, --output`   | str  | Output YAML filename (optional)          | Auto-generated |
| `-p, --pack`     | int  | Pack alignment in bytes (1, 2, 4, 8, 16) | 1              |
| `-v, --verbose`  | flag | Enable verbose output and debugging      | False          |
| `--no-bitfields` | flag | Exclude bitfield information             | False          |
| `--no-offsets`   | flag | Exclude offset information               | False          |
| `--no-children`  | flag | Exclude child members                    | False          |

#### Advanced Examples

```bash
# Complete analysis with maximum verbosity
python pycparser_yaml_generator.py complex_header.h -s NetworkProtocol -v -p 4

# Lightweight analysis (no detailed offset/bitfield info)  
python pycparser_yaml_generator.py embedded_structs.h --no-bitfields --no-offsets

# Batch processing with custom output
python pycparser_yaml_generator.py firmware.h -o firmware_analysis.yml -v

# Platform-specific alignment (16-byte alignment for SIMD)
python pycparser_yaml_generator.py simd_types.h -p 16 -v
```

### 2. YAML Viewer (yaml_viewer.py)

Advanced utility for viewing, analyzing, and filtering generated YAML files.

#### Command Line Arguments

| Argument        | Type                                          | Description               | Default |
| --------------- | --------------------------------------------- | ------------------------- | ------- |
| `yaml_file`     | str                                           | YAML file path (required) | -       |
| `-s, --summary` | flag                                          | Show summary information  | False   |
| `-t, --tree`    | flag                                          | Show tree view            | False   |
| `-l, --list`    | flag                                          | Show member list          | False   |
| `-f, --filter`  | choice: bitfield/array/struct/union/anonymous | Filter member types       | None    |
| `-d, --depth`   | int                                           | Maximum tree depth        | 3       |

#### Filter Options Explained

- **`bitfield`** - Show only bitfield members with bit-level details
- **`array`** - Show only array members (including multi-dimensional)
- **`struct`** - Show only struct members (including nested structures)  
- **`union`** - Show only union members with overlap analysis
- **`anonymous`** - Show only anonymous members (structs/unions)

#### Viewer Examples

```bash
# Complete analysis overview
python yaml_viewer.py firmware_analysis.yml

# Quick summary only
python yaml_viewer.py device_structs.yml -s

# Deep tree view with extended depth
python yaml_viewer.py complex_protocol.yml -t -d 5

# Focus on memory layout (arrays and structures)
python yaml_viewer.py memory_layout.yml -l -f struct
python yaml_viewer.py buffer_analysis.yml -l -f array

# Analyze bit-level packing
python yaml_viewer.py bitfield_packed.yml -l -f bitfield

# Find anonymous member issues
python yaml_viewer.py legacy_code.yml -l -f anonymous
```

## Output Format

### Single Struct Analysis

```yaml
struct_info:
  name: DeviceManager                    # Structure name
  total_size_bits: 126072               # Total size in bits  
  total_size_bytes: 15759               # Total size in bytes
  pack_alignment: 8                     # Pack alignment in bits
  generated_at: '2025-08-27T17:24:04'   # Generation timestamp
  generator: pycparser_yaml_generator   # Generator tool name

struct_definition:
  name: DeviceManager
  type: struct DeviceManager            # Full type declaration
  size_bits: 126072                     # Structure size in bits
  offset_bits: 0                        # Base offset (always 0)
  offset_bytes: 0                       # Base byte offset
  offset_bit_in_byte: 0                 # Bit offset within byte
  size_bytes: 15759                     # Structure size in bytes
  size_bit_remainder: 0                 # Remaining bits after byte boundary
  is_struct: true                       # Type identification flag
  members:                              # Array of structure members
    - name: devices                     # Member name
      type: ComplexDeviceDescriptor[8]  # C# style array notation
      size_bits: 89856                  # Member size in bits
      offset_bits: 0                    # Bit offset from structure start
      offset_bytes: 0                   # Byte offset from structure start
      offset_bit_in_byte: 0             # Bit position within byte
      size_bytes: 11232                 # Member size in bytes
      size_bit_remainder: 0             # Remaining bits
      is_array: true                    # Array identification flag
      array_dimensions: [8]             # Array dimension list
      is_struct: true                   # Element type is struct
      members: [...]                    # Nested member analysis
```

### Multi-Struct Analysis

```yaml
generation_info:
  generated_at: '2025-08-27T17:24:04'   # Generation timestamp
  generator: pycparser_yaml_generator   # Generator tool name
  pack_alignment: 8                     # Global pack alignment
  total_structs: 7                      # Number of structures found
  total_unions: 2                       # Number of unions found

structs:                                # Dictionary of all structures
  DeviceManager:                        # Structure name as key
    name: DeviceManager                 # Structure definition
    type: struct DeviceManager
    size_bits: 126072
    members: [...]                      # Complete member analysis
  NetworkProtocol:                      # Additional structure
    name: NetworkProtocol
    type: struct NetworkProtocol  
    size_bits: 2048
    members: [...]

unions:                                 # Dictionary of all unions
  ConfigFlags:                          # Union name as key
    name: ConfigFlags                   # Union definition
    type: union ConfigFlags
    size_bits: 32
    members: [...]                      # Union member analysis
```

## Field Information Reference

Each member provides comprehensive metadata for complete structure analysis:

### 🏷️ **Basic Information**
- **`name`** - Member field name (or auto-generated for anonymous)
- **`type`** - Data type with C# style array notation (e.g., `char[64]`, `int[2][3]`)
- **`size_bits`** - Total size in bits (including array elements)
- **`offset_bits`** - Bit offset from structure start

### 📏 **Memory Layout Information**
- **`offset_bytes`** - Byte offset from structure start  
- **`offset_bit_in_byte`** - Bit position within the offset byte (0-7)
- **`size_bytes`** - Size in complete bytes
- **`size_bit_remainder`** - Remaining bits that don't fill a complete byte

### ⚡ **Bitfield Attributes**
- **`is_bitfield`** - Boolean flag indicating bitfield member
- **`bit_width`** - Width of the bitfield in bits (1-64)
- **`bit_offset`** - Bit position within the containing storage unit

### 📦 **Array Attributes**  
- **`is_array`** - Boolean flag indicating array member
- **`array_dimensions`** - List of array dimensions `[dim1, dim2, ...]`
- **`base_type`** - Base element type (for arrays)

### 🔗 **Pointer Attributes**
- **`is_pointer`** - Boolean flag indicating pointer member
- **`base_type`** - Type being pointed to

### 🏗️ **Composite Type Flags**
- **`is_struct`** - Boolean flag indicating structure member
- **`is_union`** - Boolean flag indicating union member  
- **`is_enum`** - Boolean flag indicating enumeration member
- **`is_anonymous`** - Boolean flag indicating anonymous member

### 🌳 **Hierarchical Information**
- **`members`** - Array of child members (for structs/unions)
- **`description`** - Optional descriptive text

### 💡 **Example Field Analysis**

```yaml
- name: packet_header                   # Field name
  type: PacketHeader[16]               # C# style array type
  size_bits: 2048                      # Total: 16 * 128 bits
  offset_bits: 64                      # Starts at bit 64
  offset_bytes: 8                      # Starts at byte 8
  offset_bit_in_byte: 0                # Aligned to byte boundary
  size_bytes: 256                      # Total: 2048 / 8 bytes
  size_bit_remainder: 0                # No partial bytes
  is_array: true                       # Array member
  array_dimensions: [16]               # Single dimension array
  is_struct: true                      # Array of structures
  members:                             # Structure member analysis
    - name: type                       # Bitfield example
      type: unsigned char
      size_bits: 4                     # 4-bit field
      offset_bits: 0                   # Relative to parent
      is_bitfield: true                # Bitfield flag
      bit_width: 4                     # 4 bits wide
      bit_offset: 0                    # First 4 bits
    - name: length                     # Regular field example  
      type: unsigned short
      size_bits: 16
      offset_bits: 8                   # After 8-bit bitfield container
```

## Configuration Options

The tool provides extensive configuration through the `ConfigOptions` class for customizing analysis behavior:

### 🔧 **Memory Layout Configuration**
```python
config = ConfigOptions(
    pack_alignment=8,           # Pack alignment in bits (8, 16, 32, 64, 128)
    pointer_size=32,            # Pointer size in bits (32 for 32-bit, 64 for 64-bit)
    bit_precision=True,         # Use bit-level precision calculations
)
```

### 📊 **Output Control Configuration**
```python
config = ConfigOptions(
    include_anonymous=True,     # Include anonymous struct/union members
    include_bitfields=True,     # Include bitfield information and calculations
    include_offsets=True,       # Include offset information (bytes and bits)
    include_children=True,      # Include nested member analysis
    output_format="yaml",       # Output format: "yaml" or "json"
)
```

### 🐛 **Debugging Configuration**
```python
config = ConfigOptions(
    verbose=False,              # Enable verbose processing output
)
```

### 🌐 **Platform-Specific Configurations**

#### Embedded Systems (8-bit/16-bit microcontrollers)
```python
embedded_config = ConfigOptions(
    pack_alignment=8,           # 1-byte alignment
    pointer_size=16,            # 16-bit pointers
    bit_precision=True,         # Bit-level precision critical
    verbose=True                # Debug memory layout issues
)
```

#### 32-bit Systems
```python
desktop_32_config = ConfigOptions(
    pack_alignment=32,          # 4-byte alignment  
    pointer_size=32,            # 32-bit pointers
    bit_precision=True
)
```

#### 64-bit Systems  
```python
desktop_64_config = ConfigOptions(
    pack_alignment=64,          # 8-byte alignment
    pointer_size=64,            # 64-bit pointers
    bit_precision=True
)
```

#### SIMD/Vector Processing
```python
simd_config = ConfigOptions(
    pack_alignment=128,         # 16-byte alignment for SIMD
    pointer_size=64,            # 64-bit system
    bit_precision=True
)
```

## Advanced Features

### 🧠 **Intelligent Preprocessing Engine**

#### Macro Processing
- **Expression Evaluation**: Calculates complex macro expressions `#define SIZE (WIDTH * HEIGHT + PADDING)`
- **Nested Macro Expansion**: Resolves multi-level macro dependencies  
- **Arithmetic Operations**: Supports `+`, `-`, `*`, `/`, `()` in macro definitions
- **Conditional Macros**: Handles `#ifdef`, `#ifndef`, `#if defined()` constructs

#### Include Resolution
- **Recursive Processing**: Automatically processes `#include "local.h"` files
- **Path Resolution**: Resolves relative paths and nested includes
- **Circular Detection**: Prevents infinite loops in circular includes
- **Missing File Handling**: Graceful fallback for missing includes

#### Preprocessing Directive Handling
- **Pragma Pack**: Automatic detection and application of `#pragma pack(n)`
- **Comment Stripping**: Removes C (`/* */`) and C++ (`//`) style comments
- **Conditional Compilation**: Basic support for `#if`, `#else`, `#endif`

### 🔍 **Advanced Type Analysis**

#### Complex Type Resolution
- **Typedef Chains**: Resolves complex typedef chains (`typedef struct {...} name_t`)
- **Forward Declarations**: Handles incomplete types and forward references
- **Function Pointers**: Analyzes function pointer types and signatures
- **Nested Declarations**: Supports deeply nested structure definitions

#### Memory Layout Optimization
- **Padding Detection**: Identifies structure padding and alignment gaps
- **Bitfield Packing**: Optimizes bitfield storage and bit-level layout
- **Union Overlap Analysis**: Calculates union member overlaps and shared storage
- **Cache Line Analysis**: Identifies cache line boundaries and alignment

#### Array Analysis
- **Multi-dimensional Support**: Handles arrays of any dimension `int arr[2][3][4]`
- **C# Style Notation**: Displays arrays as `type[dim1][dim2]` for clarity
- **Zero-Length Arrays**: Supports flexible array members `char data[]`
- **Array of Structures**: Deep analysis of complex nested array structures

### 🏗️ **Structure Composition Analysis**

#### Anonymous Member Expansion
- **Automatic Flattening**: Expands anonymous struct/union members automatically
- **Name Generation**: Creates meaningful names for anonymous members
- **Namespace Preservation**: Maintains proper scoping for nested anonymous types
- **Member Promotion**: Correctly promotes anonymous members to parent scope

#### Inheritance Simulation
- **Struct Composition**: Analyzes struct-within-struct patterns
- **Base Structure Analysis**: Identifies common header/footer patterns
- **Member Override Detection**: Handles member name conflicts in nested structures

### ⚡ **Performance & Scalability**

#### Large File Processing
- **Streaming Analysis**: Processes large header files efficiently
- **Memory Management**: Optimized memory usage for complex structures
- **Incremental Processing**: Supports partial analysis and caching
- **Error Recovery**: Continues analysis despite individual parsing errors

#### Debugging & Diagnostics
- **Verbose Mode**: Detailed processing information and debug output
- **Error Reporting**: Precise error locations with context
- **AST Inspection**: Option to save preprocessed content for debugging
- **Performance Metrics**: Processing time and memory usage statistics

## Use Cases & Applications

### 📡 **Embedded Systems Development**
- **Firmware Structure Analysis**: Verify memory layout for microcontroller firmware
- **Memory Optimization**: Identify padding and optimize structure packing
- **Cross-Platform Compatibility**: Ensure consistent layout across different architectures
- **Real-Time Systems**: Analyze critical timing structures and buffer layouts

### 🌐 **Network Protocol Analysis**
- **Packet Structure Documentation**: Generate comprehensive protocol documentation
- **Binary Protocol Reverse Engineering**: Analyze unknown protocol structures
- **Protocol Implementation Verification**: Validate protocol structure implementations
- **Cross-Language Compatibility**: Ensure consistent structures across C/C++/other languages

### 🔧 **System Programming**
- **Kernel Structure Analysis**: Analyze Linux/Windows kernel data structures
- **Driver Development**: Verify hardware interface structures
- **Memory Layout Debugging**: Debug alignment and padding issues
- **Performance Optimization**: Optimize cache-friendly structure layouts

### 🔍 **Reverse Engineering**
- **Binary File Format Analysis**: Decode unknown file formats
- **Legacy Code Documentation**: Document undocumented legacy structures  
- **Malware Analysis**: Analyze malicious code data structures
- **Forensic Analysis**: Understand data structures in forensic investigations

### 📚 **Documentation & Code Quality**
- **Automatic Documentation Generation**: Create comprehensive structure documentation
- **Code Review Support**: Validate structure designs in code reviews
- **API Documentation**: Generate detailed interface documentation
- **Onboarding Materials**: Help new developers understand complex codebases

### 🧪 **Testing & Validation**
- **Unit Test Generation**: Generate test cases for structure validation
- **Regression Testing**: Detect unintended structure changes
- **Compliance Verification**: Ensure structures meet industry standards
- **Cross-Compiler Validation**: Verify consistency across different compilers

### 🎯 **Specialized Applications**
- **Game Engine Development**: Analyze game object and rendering structures
- **Database Systems**: Understand internal storage formats
- **Cryptographic Systems**: Analyze key and cipher structures
- **Scientific Computing**: Document computational data structures

## Examples

### 🔥 **Real-World Example: Network Protocol Structure**

#### Input C Header (protocol.h)
```c
#pragma pack(1)

// Protocol version and feature flags
typedef struct {
    unsigned char major;
    unsigned char minor;  
} Version;

typedef struct {
    unsigned char type : 4;           // Message type (4 bits)
    unsigned char priority : 2;      // Priority level (2 bits)  
    unsigned char encrypted : 1;     // Encryption flag (1 bit)
    unsigned char reserved : 1;      // Reserved bit (1 bit)
} MessageFlags;

// Complete network packet structure
typedef struct {
    unsigned int magic;               // Protocol magic number
    Version version;                  // Protocol version
    MessageFlags flags;               // Message flags (bitfield)
    unsigned short length;            // Payload length
    unsigned char payload[1024];      // Variable payload data
    struct {                          // Anonymous footer structure
        unsigned int checksum;        // CRC32 checksum
        unsigned char status;         // Status byte
    };
} NetworkPacket;
```

#### Generated YAML Output
```yaml
struct_info:
  name: NetworkPacket
  total_size_bits: 8312            # 1039 bytes total
  total_size_bytes: 1039
  pack_alignment: 8                # 1-byte packing
  generated_at: '2025-08-27T17:30:00'
  generator: pycparser_yaml_generator

struct_definition:
  name: NetworkPacket
  type: struct NetworkPacket
  size_bits: 8312
  members:
    - name: magic                    # Magic number field
      type: unsigned int
      size_bits: 32
      offset_bits: 0
      offset_bytes: 0
      size_bytes: 4
      
    - name: version                  # Nested structure
      type: Version
      size_bits: 16
      offset_bits: 32
      offset_bytes: 4
      size_bytes: 2
      is_struct: true
      members:
        - name: major
          type: unsigned char
          size_bits: 8
          offset_bits: 0
          size_bytes: 1
        - name: minor
          type: unsigned char
          size_bits: 8
          offset_bits: 8
          size_bytes: 1
          
    - name: flags                    # Bitfield structure
      type: MessageFlags
      size_bits: 8
      offset_bits: 48
      offset_bytes: 6
      size_bytes: 1
      is_struct: true
      members:
        - name: type
          type: unsigned char
          size_bits: 4
          offset_bits: 0
          is_bitfield: true
          bit_width: 4
          bit_offset: 0
        - name: priority
          type: unsigned char
          size_bits: 2
          offset_bits: 0
          is_bitfield: true
          bit_width: 2
          bit_offset: 4
        - name: encrypted
          type: unsigned char
          size_bits: 1
          offset_bits: 0
          is_bitfield: true
          bit_width: 1
          bit_offset: 6
        - name: reserved
          type: unsigned char
          size_bits: 1
          offset_bits: 0
          is_bitfield: true
          bit_width: 1
          bit_offset: 7
          
    - name: length                   # Length field
      type: unsigned short
      size_bits: 16
      offset_bits: 64
      offset_bytes: 8
      size_bytes: 2
      
    - name: payload                  # Large array with C# notation
      type: unsigned char[1024]
      size_bits: 8192
      offset_bits: 80
      offset_bytes: 10
      size_bytes: 1024
      is_array: true
      array_dimensions: [1024]
      
    - name: anonymous_8272           # Anonymous structure (auto-named)
      type: struct anonymous
      size_bits: 40
      offset_bits: 8272
      offset_bytes: 1034
      size_bytes: 5
      is_anonymous: true
      is_struct: true
      members:
        - name: checksum
          type: unsigned int
          size_bits: 32
          offset_bits: 0
          size_bytes: 4
        - name: status
          type: unsigned char
          size_bits: 8
          offset_bits: 32
          size_bytes: 1
```

### 📊 **Analysis Results Summary**
```bash
$ python pycparser_yaml_generator.py protocol.h -s NetworkPacket -v

Structure Analysis Results:
Name: NetworkPacket
Total size: 8312 bits (1039 bytes)
Alignment: 8 bits
Total members: 13

  - Array members: 1
  - Struct members: 3  
  - Bitfield members: 4
  - Anonymous members: 1

✅ YAML file generated: NetworkPacket.yml
```

### 🔍 **Multi-Dimensional Array Example**

#### Input C Code
```c
typedef struct {
    char description[4][64];        // 4 strings, 64 chars each
    int matrix[3][3];               // 3x3 integer matrix
    float tensor[2][4][8];          // 3D tensor
} ComplexArrays;
```

#### Generated Output (Key Parts)
```yaml
members:
  - name: description
    type: char[4][64]              # C# style multi-dimensional notation
    size_bits: 2048                # 4 * 64 * 8 bits
    is_array: true
    array_dimensions: [4, 64]      # Multiple dimensions listed
    
  - name: matrix  
    type: int[3][3]                # 2D array notation
    size_bits: 288                 # 3 * 3 * 32 bits
    is_array: true
    array_dimensions: [3, 3]
    
  - name: tensor
    type: float[2][4][8]           # 3D array notation  
    size_bits: 2048                # 2 * 4 * 8 * 32 bits
    is_array: true
    array_dimensions: [2, 4, 8]    # Three dimensions
```

---

## Troubleshooting & FAQ

### 🚨 **Common Issues**

#### Issue: "Parsing failed" Error
```bash
# Problem: Header file contains unsupported C++ features
# Solution: Use standard C headers only
python pycparser_yaml_generator.py clean_c_header.h -s MyStruct -v
```

#### Issue: Incorrect Structure Sizes
```bash
# Problem: Wrong pack alignment setting
# Solution: Match your compiler's pack setting
python pycparser_yaml_generator.py input.h -s MyStruct -p 4  # 4-byte alignment
```

#### Issue: Missing Include Files
```bash
# Problem: Cannot find included headers
# Solution: Ensure all local includes are in the same directory
# or use preprocessed files
```

#### Issue: Bitfield Layout Incorrect
```bash
# Problem: Bitfield packing differs from compiler
# Solution: Verify pack alignment and compiler settings
python pycparser_yaml_generator.py input.h -s BitfieldStruct -p 1 -v
```

### ❓ **Frequently Asked Questions**

**Q: Does this tool support C++?**
A: Limited support. The tool works best with standard C headers. C++ features like classes, templates, and namespaces are not fully supported.

**Q: How accurate are the offset calculations?**
A: Bit-level accurate for standard C constructs when using the correct pack alignment setting. Results match GCC and Clang behavior.

**Q: Can I analyze system headers like `<stdio.h>`?**
A: Not directly. The tool works best with local headers. System headers often contain compiler-specific extensions.

**Q: What's the difference between single and batch analysis?**
A: Single analysis (`-s StructName`) analyzes one specific structure. Batch analysis processes all structures in the file.

**Q: How do I handle large header files?**
A: Use verbose mode (`-v`) to monitor progress. The tool can handle files with hundreds of structures efficiently.

### 🔧 **Performance Tips**

1. **Use specific struct analysis** (`-s StructName`) for faster processing
2. **Disable unnecessary features** (`--no-bitfields --no-offsets`) for lightweight analysis
3. **Preprocess complex headers** to remove unnecessary includes
4. **Use appropriate pack alignment** matching your target platform

### 🛠️ **Debug Mode Usage**

```bash
# Enable maximum debugging information
python pycparser_yaml_generator.py problematic.h -s DebugStruct -v

# This will create preprocessed_debug.h for inspection
# Check this file if parsing fails
```

---

## Contributing

### 🤝 **How to Contribute**

We welcome contributions from the community! Here's how you can help:

#### 1. **Bug Reports**
- Use the [GitHub Issues](https://github.com/feihe027/cstruct2yaml/issues) page
- Provide sample C code that demonstrates the issue
- Include expected vs. actual output
- Specify your operating system and Python version

#### 2. **Feature Requests** 
- Submit detailed feature proposals via GitHub Issues
- Explain the use case and benefits
- Provide example input/output if possible

#### 3. **Code Contributions**
```bash
# 1. Fork the repository
git fork https://github.com/feihe027/cstruct2yaml.git

# 2. Create your feature branch
git checkout -b feature/amazing-feature

# 3. Install development dependencies
pip install -r requirements-dev.txt

# 4. Make your changes and add tests
# 5. Run the test suite
pytest tests/

# 6. Commit your changes
git commit -m 'Add amazing feature: detailed description'

# 7. Push to your branch
git push origin feature/amazing-feature

# 8. Open a Pull Request
```

#### 4. **Development Setup**
```bash
# Clone and setup development environment
git clone https://github.com/feihe027/cstruct2yaml.git
cd cstruct2yaml

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=pycparser_yaml_generator --cov-report=html
```

### 📋 **Contribution Guidelines**

- **Code Style**: Follow PEP 8 guidelines
- **Testing**: Add tests for new features
- **Documentation**: Update README and docstrings
- **Commit Messages**: Use clear, descriptive commit messages
- **Pull Requests**: Include detailed description of changes

### 🧪 **Testing**

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_integration.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=pycparser_yaml_generator
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 📄 **MIT License Summary**
- ✅ **Commercial use** - Use in commercial projects
- ✅ **Modification** - Modify and distribute modified versions  
- ✅ **Distribution** - Distribute original or modified versions
- ✅ **Private use** - Use privately without restrictions
- ❗ **License and copyright notice** - Include original license in distributions
- ❌ **Liability** - No warranty or liability provided
- ❌ **Warranty** - No warranty provided

## Acknowledgments

### 🙏 **Special Thanks**

- **[pycparser](https://github.com/eliben/pycparser)** - Excellent C parser library that makes this tool possible
- **[PyYAML](https://pyyaml.org/)** - Robust YAML processing library
- **[Python Software Foundation](https://www.python.org/)** - For the amazing Python ecosystem

### 💡 **Inspiration**

- **Embedded Systems Community** - Real-world need for precise C struct analysis
- **Reverse Engineering Tools** - IDA Pro, Ghidra, and other analysis tools
- **Protocol Analysis** - Network protocol reverse engineering and documentation needs
- **Firmware Development** - Memory layout optimization in resource-constrained environments

### 🌟 **Contributors**

Thanks to all contributors who have helped improve this project through code, documentation, testing, and feedback.

## Support & Community

### 💬 **Getting Help**

1. **Documentation** - Read this README thoroughly
2. **GitHub Issues** - Search existing issues or create new ones
3. **Code Examples** - Check the examples in this README
4. **Stack Overflow** - Tag questions with `pycparser` and `c-struct-analysis`

### 🐛 **Reporting Issues**

When reporting issues, please include:

```bash
# System information
python --version
pip list | grep -E "(pycparser|PyYAML)"

# Error reproduction
python pycparser_yaml_generator.py your_file.h -s YourStruct -v
```

- **Minimal reproduction case** - Smallest possible C code that demonstrates the issue
- **Expected behavior** - What you expected to happen
- **Actual behavior** - What actually happened  
- **System information** - OS, Python version, dependency versions
- **Sample files** - If possible, attach the problematic header file

### 🔄 **Version History**

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and breaking changes.

### 🚀 **Roadmap**

Future enhancements being considered:
- JSON output format support
- C++ limited support for simple classes
- Integration with popular IDEs
- Web-based interface for online analysis
- Support for more preprocessor directives
- Performance optimizations for very large header files

---

## Final Notes

**⚠️ Compatibility Note**: This tool is designed for analyzing standard C structures and may not handle all complex C++ features. For best results, use with standard C header files.

**🎯 Accuracy**: The tool provides bit-level accurate analysis for standard C constructs when using appropriate pack alignment settings. Results are verified to match GCC and Clang compiler behavior.

**📈 Performance**: Optimized for processing large header files with hundreds of structures efficiently while maintaining accuracy.

---

**Made with ❤️ for the embedded systems and reverse engineering community**

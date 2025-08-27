# C Struct YAML Generator

A flexible C struct analysis tool based on Python's pycparser library that converts complex C structures into detailed YAML description files.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Features

- ✅ **Complex nested struct analysis** - Handles deeply nested structures and compositions
- ✅ **Precise bitfield processing** - Accurate bitfield width and offset calculations
- ✅ **Anonymous structures and unions** - Full support for anonymous members
- ✅ **Array member analysis** - Multi-dimensional array support
- ✅ **Bit-level precision** - Precise offset and size calculations at bit level
- ✅ **Flexible output formats** - YAML and JSON output support
- ✅ **Configurable alignment** - Customizable pack alignment settings
- ✅ **Detailed member information** - Comprehensive field metadata

## Project Structure

```
ai_parse_structure/
├── pycparser_yaml_generator.py  # Main YAML generator
├── yaml_viewer.py               # YAML file viewer utility
├── test.h                       # Test C header file
├── example.h                    # Example dependency header
├── README.md                    # This file
├── LICENSE                      # MIT license
└── examples/                    # Example outputs
    ├── single_struct.yml        # Single struct output example
    └── all_structs.yml          # Multi-struct output example
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Dependencies

```bash
pip install pycparser pyyaml
```

### Clone Repository

```bash
git clone https://github.com/yourusername/ai_parse_structure.git
cd ai_parse_structure
```

## Quick Start

### Analyze a specific struct

```bash
python pycparser_yaml_generator.py test.h -s MyStruct -v
```

### Analyze all structs in a file

```bash
python pycparser_yaml_generator.py test.h -v
```

### View generated YAML

```bash
python yaml_viewer.py MyStruct.yml
```

## Usage Guide

### 1. pycparser_yaml_generator.py

The main tool for converting C structs to YAML format.

#### Command Line Arguments

| Argument         | Description                     | Default        |
| ---------------- | ------------------------------- | -------------- |
| `input_file`     | Input C header file (required)  | -              |
| `-s, --struct`   | Target struct name (optional)   | All structs    |
| `-o, --output`   | Output YAML filename (optional) | Auto-generated |
| `-p, --pack`     | Pack alignment in bytes         | 1              |
| `-v, --verbose`  | Enable verbose output           | False          |
| `--no-bitfields` | Exclude bitfield information    | False          |
| `--no-offsets`   | Exclude offset information      | False          |
| `--no-children`  | Exclude child members           | False          |

#### Examples

```bash
# Analyze specific struct with verbose output
python pycparser_yaml_generator.py input.h -s DeviceManager -v

# Custom pack alignment (4-byte alignment)
python pycparser_yaml_generator.py input.h -s MyStruct -p 4

# Save to specific output file
python pycparser_yaml_generator.py input.h -s MyStruct -o custom_output.yml

# Analyze without bitfield details
python pycparser_yaml_generator.py input.h --no-bitfields --no-offsets
```

### 2. yaml_viewer.py

A utility for viewing and analyzing generated YAML files.

#### Command Line Arguments

| Argument        | Description               | Default |
| --------------- | ------------------------- | ------- |
| `yaml_file`     | YAML file path (required) | -       |
| `-s, --summary` | Show summary information  | False   |
| `-t, --tree`    | Show tree view            | False   |
| `-l, --list`    | Show member list          | False   |
| `-f, --filter`  | Filter member types       | None    |
| `-d, --depth`   | Maximum tree depth        | 3       |

#### Filter Options

- `bitfield` - Show only bitfield members
- `array` - Show only array members  
- `struct` - Show only struct members
- `union` - Show only union members
- `anonymous` - Show only anonymous members

#### Examples

```bash
# Show all information
python yaml_viewer.py output.yml

# Show only summary
python yaml_viewer.py output.yml -s

# Show tree view with depth limit
python yaml_viewer.py output.yml -t -d 2

# Show filtered member list
python yaml_viewer.py output.yml -l -f bitfield
```

## Output Format

### Single Struct Format

```yaml
struct_info:
  name: DeviceManager
  total_size_bits: 106952
  total_size_bytes: 13369
  pack_alignment: 8
  generated_at: '2025-08-27T12:19:55.490061'
  generator: pycparser_yaml_generator

struct_definition:
  name: DeviceManager
  type: struct DeviceManager
  size_bits: 106952
  offset_bits: 0
  offset_bytes: 0
  offset_bit_in_byte: 0
  size_bytes: 13369
  size_bit_remainder: 0
  members:
    - name: devices
      type: ComplexDeviceDescriptor
      size_bits: 87040
      offset_bits: 0
      offset_bytes: 0
      offset_bit_in_byte: 0
      size_bytes: 10880
      size_bit_remainder: 0
      is_array: true
      array_dimensions: [8]
      is_struct: true
      members: [...]
    # ... more members
```

### Multi-Struct Format

```yaml
generation_info:
  generated_at: '2025-08-27T12:23:52.765523'
  generator: pycparser_yaml_generator
  pack_alignment: 8
  total_structs: 7
  total_unions: 0

structs:
  DeviceManager:
    name: DeviceManager
    type: struct DeviceManager
    size_bits: 106952
    members: [...]
  # ... more structs

unions: {}
```

## Field Information

Each member contains comprehensive metadata:

### Basic Information
- `name` - Member name
- `type` - Data type
- `size_bits` - Size in bits
- `offset_bits` - Offset in bits

### Byte-Level Information
- `offset_bytes` - Byte offset
- `offset_bit_in_byte` - Bit offset within byte
- `size_bytes` - Size in bytes
- `size_bit_remainder` - Remaining bits

### Special Attributes
- `is_bitfield` - Whether it's a bitfield
- `bit_width` - Bitfield width
- `bit_offset` - Bitfield offset
- `is_array` - Whether it's an array
- `array_dimensions` - Array dimensions
- `is_pointer` - Whether it's a pointer
- `is_struct` - Whether it's a struct
- `is_union` - Whether it's a union
- `is_anonymous` - Whether it's anonymous

### Nested Information
- `members` - Child member list (for structs/unions)

## Configuration Options

The tool supports various configuration options through the `ConfigOptions` class:

```python
config = ConfigOptions(
    pack_alignment=8,           # Pack alignment (bits)
    pointer_size=32,            # Pointer size (bits)
    include_anonymous=True,     # Include anonymous members
    include_bitfields=True,     # Include bitfield information
    include_offsets=True,       # Include offset information
    include_children=True,      # Include child members
    bit_precision=True,         # Use bit precision
    verbose=False               # Verbose output
)
```

## Advanced Features

### Preprocessing

The tool intelligently handles:
- Include file resolution
- Macro expansion and evaluation
- Conditional compilation directives
- Pragma pack directives
- Comment removal

### Type Analysis

Supports comprehensive type analysis:
- Basic C types (char, int, float, etc.)
- Pointers and multi-level pointers
- Arrays and multi-dimensional arrays
- Nested structs and unions
- Bitfields with precise calculations
- Anonymous structures and unions
- Function pointers
- Enumerations

### Memory Layout

Provides precise memory layout information:
- Bit-level offset calculations
- Structure padding analysis
- Alignment boundary detection
- Pack directive handling
- Bitfield packing optimization

## Use Cases

- **Documentation Generation** - Create comprehensive struct documentation
- **Memory Layout Analysis** - Understand exact memory usage and alignment
- **Protocol Analysis** - Analyze communication protocol structures
- **Firmware Development** - Verify embedded system data structures
- **Reverse Engineering** - Analyze binary file formats
- **Code Optimization** - Optimize struct layouts for memory efficiency

## Examples

### Example Input (test.h)

```c
#pragma pack(1)

typedef struct {
    unsigned char type : 4;
    unsigned char flags : 4;
    unsigned short length;
    unsigned int data[10];
} PacketHeader;

typedef struct {
    PacketHeader header;
    char payload[256];
    struct {
        unsigned int checksum;
        unsigned char status;
    } footer;
} NetworkPacket;
```

### Example Output

```yaml
struct_info:
  name: NetworkPacket
  total_size_bits: 2400
  total_size_bytes: 300
  pack_alignment: 8

struct_definition:
  name: NetworkPacket
  type: struct NetworkPacket
  size_bits: 2400
  members:
    - name: header
      type: PacketHeader
      size_bits: 368
      offset_bits: 0
      is_struct: true
      members:
        - name: type
          type: unsigned char
          size_bits: 4
          offset_bits: 0
          is_bitfield: true
          bit_width: 4
        - name: flags
          type: unsigned char
          size_bits: 4
          offset_bits: 4
          is_bitfield: true
          bit_width: 4
        # ... more fields
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pycparser](https://github.com/eliben/pycparser) - A complete C parser written in Python
- Inspired by the need for precise C struct analysis in embedded systems development
- Thanks to the open source community for continuous improvements and feedback

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/ai_parse_structure/issues) page
2. Create a new issue with detailed description
3. Include sample C code and expected output when possible

---

**Note**: This tool is designed for analyzing C structures and may not handle all complex C++ features. For best results, use with standard C header files.

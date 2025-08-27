#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C Struct YAML Generator based on pycparser
Supports complex structs, bitfields, anonymous members, nested structures, etc.
Highly flexible and configurable
"""

import os
import sys
import re
import yaml
import argparse
from typing import Dict, List, Tuple, Optional, Any, Set, Union as TypingUnion
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pycparser import c_parser, c_ast, parse_file
from pycparser.c_ast import (
    Typedef, Decl, Struct, Union, Enum as EnumNode, 
    TypeDecl, IdentifierType, PtrDecl, ArrayDecl, 
    Constant, BinaryOp, UnaryOp, FuncDecl
)


@dataclass
class ConfigOptions:
    """Configuration options"""
    pack_alignment: int = 8  # bits, default 1-byte alignment
    pointer_size: int = 32   # bits, pointer size
    include_anonymous: bool = True  # include anonymous members
    include_bitfields: bool = True  # include bitfield information
    include_offsets: bool = True    # include offset information
    include_children: bool = True   # include child members
    output_format: str = "yaml"     # output format: yaml, json
    bit_precision: bool = True      # use bit precision
    verbose: bool = False           # verbose output


@dataclass
class TypeInfo:
    """Type information"""
    name: str
    size_bits: int
    is_signed: bool = True
    is_pointer: bool = False
    is_array: bool = False
    is_struct: bool = False
    is_union: bool = False
    is_enum: bool = False
    is_function: bool = False
    base_type: Optional[str] = None
    array_dimensions: List[int] = field(default_factory=list)
    
    
@dataclass
class FieldInfo:
    """Field information"""
    name: str
    type_info: TypeInfo
    offset_bits: int
    size_bits: int
    bit_width: Optional[int] = None
    bit_offset: Optional[int] = None
    is_anonymous: bool = False
    is_bitfield: bool = False
    children: List['FieldInfo'] = field(default_factory=list)
    description: str = ""
    
    def to_dict(self, config: ConfigOptions) -> Dict[str, Any]:
        """Convert to dictionary"""
        # Generate C# style array type name if it's an array
        type_name = self.type_info.name
        if self.type_info.is_array and self.type_info.array_dimensions:
            # Build C# style array syntax: baseType[dim1][dim2]...
            for dimension in self.type_info.array_dimensions:
                type_name += f"[{dimension}]"
        
        result = {
            'name': self.name,
            'type': type_name,
            'size_bits': self.size_bits
        }
        
        if config.include_offsets:
            result['offset_bits'] = self.offset_bits
            if config.bit_precision:
                result['offset_bytes'] = self.offset_bits // 8
                result['offset_bit_in_byte'] = self.offset_bits % 8
                result['size_bytes'] = self.size_bits // 8
                result['size_bit_remainder'] = self.size_bits % 8
        
        if config.include_bitfields and self.is_bitfield:
            result['is_bitfield'] = True
            result['bit_width'] = self.bit_width
            if self.bit_offset is not None:
                result['bit_offset'] = self.bit_offset
        
        if config.include_anonymous and self.is_anonymous:
            result['is_anonymous'] = True
            
        if self.type_info.is_array:
            result['is_array'] = True
            result['array_dimensions'] = self.type_info.array_dimensions
            
        if self.type_info.is_pointer:
            result['is_pointer'] = True
            result['base_type'] = self.type_info.base_type
            
        if self.type_info.is_struct:
            result['is_struct'] = True
        elif self.type_info.is_union:
            result['is_union'] = True
        elif self.type_info.is_enum:
            result['is_enum'] = True
            
        if self.description:
            result['description'] = self.description
            
        if config.include_children and self.children:
            result['members'] = [child.to_dict(config) for child in self.children]
            
        return result


class PycparserYamlGenerator:
    """YAML generator based on pycparser"""
    
    def __init__(self, config: Optional[ConfigOptions] = None):
        self.config = config or ConfigOptions()
        
        # Basic type size mapping (bits)
        self.basic_types = {
            'void': 0,
            'char': 8, '_Bool': 8, 'bool': 8,
            'signed char': 8, 'unsigned char': 8,
            'short': 16, 'short int': 16, 
            'unsigned short': 16, 'unsigned short int': 16,
            'int': 32, 'signed int': 32, 'unsigned int': 32,
            'long': 32, 'unsigned long': 32,
            'long long': 64, 'unsigned long long': 64,
            'float': 32, 'double': 64, 'long double': 128,
            'size_t': 32, 'ptrdiff_t': 32,
            'wchar_t': 16, 'char16_t': 16, 'char32_t': 32
        }
        
        # Type definition cache
        self.typedefs: Dict[str, Any] = {}
        self.structs: Dict[str, Any] = {}
        self.unions: Dict[str, Any] = {}
        self.enums: Dict[str, Any] = {}
        
        # Parse state
        self.current_offset = 0
        self.current_bit_offset = 0
        
    def parse_file(self, filename: str, target_struct: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Parse C header file"""
        try:
            if self.config.verbose:
                print(f"Parsing file: {filename}")
                
            # Preprocess file
            preprocessed_content = self._preprocess_file(filename)
            
            # Parse AST
            parser = c_parser.CParser()
            ast = parser.parse(preprocessed_content, filename=filename)
            
            if self.config.verbose:
                print("AST parsing successful, starting type definition analysis...")
                
            # Collect all type definitions
            self._collect_types(ast)
            
            if self.config.verbose:
                print(f"Found {len(self.structs)} structs, {len(self.unions)} unions, {len(self.typedefs)} typedefs")
            
            # If target struct specified, analyze only that struct
            if target_struct:
                return self._analyze_target_struct(target_struct)
            else:
                # Analyze all structs
                return self._analyze_all_structs()
                
        except Exception as e:
            print(f"Error parsing file: {e}")
            if self.config.verbose:
                import traceback
                traceback.print_exc()
            return None
    
    def _preprocess_file(self, filename: str) -> str:
        """Preprocess file content"""
        content = self._read_file_recursive(filename)
        
        # Remove comments
        content = self._remove_comments(content)
        
        # Process pragma pack
        self._extract_pragma_pack(content)
        
        # Expand macros first (before removing preprocessing directives)
        content = self._expand_simple_macros(content)
        
        # Remove preprocessing directives but keep necessary defines
        content = self._process_preprocessor_directives(content)
        
        # Final cleanup to ensure no remaining preprocessing directives
        content = self._final_cleanup(content)
        
        if self.config.verbose:
            # Save preprocessed content for debugging
            with open('preprocessed_debug.h', 'w', encoding='utf-8') as f:
                f.write(content)
            print("Preprocessed content saved to preprocessed_debug.h")
        
        return content
    
    def _final_cleanup(self, content: str) -> str:
        """Final cleanup, remove all remaining preprocessing directives"""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            # If it's a preprocessing directive line, skip completely
            if line_stripped.startswith('#'):
                continue
            # Keep all other content
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _read_file_recursive(self, filename: str) -> str:
        """Recursively read file, handling includes"""
        if not os.path.exists(filename):
            return ""
            
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Handle local includes
        base_dir = os.path.dirname(filename)
        include_pattern = r'#include\s*"([^"]+)"'
        
        def replace_include(match):
            include_file = match.group(1)
            include_path = os.path.join(base_dir, include_file)
            if os.path.exists(include_path):
                return self._read_file_recursive(include_path)
            return f"// Include not found: {include_file}\n"
        
        content = re.sub(include_pattern, replace_include, content)
        return content
    
    def _remove_comments(self, content: str) -> str:
        """Remove C-style comments"""
        # Remove multi-line comments first to handle nested // inside /* */
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Then remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        return content
    
    def _extract_pragma_pack(self, content: str) -> None:
        """Extract pragma pack information"""
        pack_pattern = r'#pragma\s+pack\s*\(\s*(\d+)\s*\)'
        matches = re.findall(pack_pattern, content)
        if matches:
            self.config.pack_alignment = int(matches[-1]) * 8  # Convert to bits
            if self.config.verbose:
                print(f"Detected pack alignment: {self.config.pack_alignment} bits")
    
    def _process_preprocessor_directives(self, content: str) -> str:
        """Process preprocessing directives"""
        # First handle conditional compilation
        content = self._process_conditional_compilation(content)
        
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith('#'):
                # Keep numeric macro definitions
                if re.match(r'#define\s+\w+\s+\d+', line_stripped):
                    processed_lines.append(line)
                # Remove other preprocessing directives, including pragma
                elif (line_stripped.startswith('#pragma') or 
                      line_stripped.startswith('#include') or
                      line_stripped.startswith('#ifndef') or
                      line_stripped.startswith('#ifdef') or
                      line_stripped.startswith('#if') or
                      line_stripped.startswith('#else') or
                      line_stripped.startswith('#endif') or
                      line_stripped.startswith('#define') or
                      line_stripped.startswith('#undef')):
                    # Completely remove these directives
                    continue
                else:
                    # Remove other preprocessing directives as well
                    continue
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _process_conditional_compilation(self, content: str) -> str:
        """Process conditional compilation directives like #if, #ifdef, #else, #endif"""
        lines = content.split('\n')
        result_lines = []
        
        # Track conditional compilation state
        condition_stack = []  # Stack of (condition_met, in_else) tuples
        current_condition = True  # Whether current block should be included
        
        # Extract defined macros for ifdef/ifndef evaluation
        defined_macros = set()
        macro_pattern = r'#define\s+(\w+)'
        for line in lines:
            # Use search instead of match to handle lines with leading whitespace
            match = re.search(macro_pattern, line.strip())
            if match:
                macro_name = match.group(1)
                defined_macros.add(macro_name)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            line_stripped = line.strip()
            
            if line_stripped.startswith('#if '):
                # Parse #if condition
                condition_expr = line_stripped[4:].strip()
                condition_met = self._evaluate_condition(condition_expr, defined_macros)
                condition_stack.append((current_condition, False))
                current_condition = current_condition and condition_met
                
            elif line_stripped.startswith('#ifdef '):
                # Check if macro is defined
                macro_name = line_stripped[7:].strip()
                condition_met = macro_name in defined_macros
                condition_stack.append((current_condition, False))
                current_condition = current_condition and condition_met
                
            elif line_stripped.startswith('#ifndef '):
                # Check if macro is NOT defined - but for header guards, assume they should be included
                macro_name = line_stripped[8:].strip()
                # Skip header guard patterns (simple heuristic: macro name ends with _H)
                if macro_name.endswith('_H'):
                    # Assume this is a header guard, skip the #ifndef and include content
                    condition_stack.append((current_condition, False))
                    current_condition = current_condition  # Don't change condition for header guards
                else:
                    condition_met = macro_name not in defined_macros
                    condition_stack.append((current_condition, False))
                    current_condition = current_condition and condition_met
                
            elif line_stripped.startswith('#else'):
                if condition_stack:
                    parent_condition, _ = condition_stack[-1]
                    condition_stack[-1] = (parent_condition, True)
                    # Flip the current condition within the parent scope
                    current_condition = parent_condition and not current_condition
                    
            elif line_stripped.startswith('#elif '):
                # Treat #elif as #else followed by #if
                if condition_stack:
                    parent_condition, in_else = condition_stack[-1]
                    if not in_else:  # Only process #elif if we haven't seen #else yet
                        condition_expr = line_stripped[6:].strip()
                        condition_met = self._evaluate_condition(condition_expr, defined_macros)
                        current_condition = parent_condition and (not current_condition) and condition_met
                        
            elif line_stripped.startswith('#endif'):
                if condition_stack:
                    current_condition, _ = condition_stack.pop()
                    
            else:
                # Regular line - include it if current condition is true
                if current_condition:
                    result_lines.append(line)
            
            i += 1
        
        return '\n'.join(result_lines)
    
    def _evaluate_condition(self, condition: str, defined_macros: set) -> bool:
        """Evaluate a preprocessor condition like '0', '1', 'defined(MACRO)', etc."""
        condition = condition.strip()
        
        # Handle simple numeric conditions
        if condition == '0':
            return False
        elif condition == '1':
            return True
        
        # Handle defined() expressions
        defined_pattern = r'defined\s*\(\s*(\w+)\s*\)'
        condition = re.sub(defined_pattern, 
                          lambda m: '1' if m.group(1) in defined_macros else '0', 
                          condition)
        
        # Replace macro names with 1 if defined, 0 if not
        for macro in defined_macros:
            condition = re.sub(r'\b' + re.escape(macro) + r'\b', '1', condition)
        
        # Replace any remaining unknown identifiers with 0
        condition = re.sub(r'\b[a-zA-Z_]\w*\b', '0', condition)
        
        # Try to evaluate the expression safely
        try:
            # Only allow basic arithmetic and comparison operators
            if re.match(r'^[0-9+\-*/()&|!<>=\s]+$', condition):
                # Replace C-style operators with Python equivalents
                condition = condition.replace('&&', ' and ')
                condition = condition.replace('||', ' or ')
                condition = condition.replace('!', ' not ')
                result = eval(condition)
                return bool(result)
        except:
            pass
        
        # Default to False for complex or unparseable conditions
        return False
    
    def _expand_simple_macros(self, content: str) -> str:
        """Expand simple numeric macros, supporting expression calculation"""
        # Extract macro definitions (including expressions)
        # Use line-by-line processing to avoid cross-line matching
        lines = content.split('\n')
        macros = {}
        
        for line in lines:
            line_stripped = line.strip()
            # Match #define directives
            define_match = re.match(r'#define\s+(\w+)(?:\s+(.*))?$', line_stripped)
            if define_match:
                name = define_match.group(1)
                value = define_match.group(2)
                
                # Handle empty macro definitions (like #define __TAB_RECOVER__)
                if value is None or value.strip() == '':
                    macros[name] = ''  # Empty string for empty macros
                    if self.config.verbose:
                        print(f"Found empty macro definition: {name}")
                    continue
                    
                value = value.strip()
                
                # If it's a simple number
                if value.isdigit():
                    macros[name] = value
                # If it's an expression, try to calculate
                elif re.match(r'^[\d+\-*/().\w\s]+$', value):
                    # First replace known macros
                    for known_macro, known_value in macros.items():
                        if known_value:  # Only replace non-empty macros
                            value = re.sub(r'\b' + re.escape(known_macro) + r'\b', known_value, value)
                    
                    try:
                        # Try to evaluate expression
                        # Remove parentheses and calculate
                        clean_value = value.replace('(', '').replace(')', '')
                        if re.match(r'^[\d+\-*/.\s]+$', clean_value):
                            result = eval(clean_value)
                            macros[name] = str(int(result))
                        else:
                            macros[name] = value
                    except:
                        macros[name] = value
                else:
                    macros[name] = value
                
                if self.config.verbose:
                    print(f"Found macro definition: {name} = {value if value else '(empty)'} -> {macros[name]}")
        
        # Multiple rounds of replacement to ensure nested macros are properly expanded
        # But skip empty macros for expansion (they should remain as empty)
        for _ in range(3):  # Maximum 3 rounds of replacement
            for name, value in macros.items():
                if value:  # Only expand non-empty macros
                    content = re.sub(r'\b' + re.escape(name) + r'\b', value, content)
        
        return content
    
    def _collect_types(self, ast: c_ast.FileAST) -> None:
        """Collect all type definitions"""
        class TypeCollector(c_ast.NodeVisitor):
            def __init__(self, generator):
                self.gen = generator
            
            def visit_Typedef(self, node):
                self.gen._process_typedef(node)
                self.generic_visit(node)
            
            def visit_Struct(self, node):
                if node.name:
                    self.gen.structs[node.name] = node
                self.generic_visit(node)
            
            def visit_Union(self, node):
                if node.name:
                    self.gen.unions[node.name] = node
                self.generic_visit(node)
            
            def visit_Enum(self, node):
                if node.name:
                    self.gen.enums[node.name] = node
                self.generic_visit(node)
        
        collector = TypeCollector(self)
        collector.visit(ast)
    
    def _process_typedef(self, typedef: c_ast.Typedef) -> None:
        """Process typedef definition"""
        name = typedef.name
        self.typedefs[name] = typedef
        
        # If typedef defines a struct or union, add to corresponding collection
        if isinstance(typedef.type, c_ast.TypeDecl):
            if isinstance(typedef.type.type, c_ast.Struct):
                self.structs[name] = typedef.type.type
                if typedef.type.type.name:
                    self.structs[typedef.type.type.name] = typedef.type.type
            elif isinstance(typedef.type.type, c_ast.Union):
                self.unions[name] = typedef.type.type
                if typedef.type.type.name:
                    self.unions[typedef.type.type.name] = typedef.type.type
    
    def _analyze_target_struct(self, target_name: str) -> Optional[Dict[str, Any]]:
        """Analyze specified struct"""
        if target_name not in self.structs:
            print(f"Error: Struct '{target_name}' not found")
            return None
        
        struct_node = self.structs[target_name]
        field_info = self._analyze_struct_node(struct_node, target_name)
        
        return {
            'struct_info': {
                'name': target_name,
                'total_size_bits': field_info.size_bits,
                'total_size_bytes': field_info.size_bits // 8,
                'pack_alignment': self.config.pack_alignment,
                'generated_at': datetime.now().isoformat(),
                'generator': 'pycparser_yaml_generator'
            },
            'struct_definition': field_info.to_dict(self.config)
        }
    
    def _analyze_all_structs(self) -> Dict[str, Any]:
        """Analyze all structs"""
        result = {
            'structs': {},
            'unions': {},
            'generation_info': {
                'generated_at': datetime.now().isoformat(),
                'generator': 'pycparser_yaml_generator',
                'pack_alignment': self.config.pack_alignment,
                'total_structs': len(self.structs),
                'total_unions': len(self.unions)
            }
        }
        
        # Analyze all structs
        for name, struct_node in self.structs.items():
            if self.config.verbose:
                print(f"Analyzing struct: {name}")
            field_info = self._analyze_struct_node(struct_node, name)
            result['structs'][name] = field_info.to_dict(self.config)
        
        # Analyze all unions
        for name, union_node in self.unions.items():
            if self.config.verbose:
                print(f"Analyzing union: {name}")
            field_info = self._analyze_union_node(union_node, name)
            result['unions'][name] = field_info.to_dict(self.config)
        
        return result
    
    def _analyze_struct_node(self, struct_node: c_ast.Struct, name: str) -> FieldInfo:
        """Analyze struct node"""
        self.current_offset = 0
        self.current_bit_offset = 0
        
        children = []
        if struct_node.decls:
            for decl in struct_node.decls:
                field = self._analyze_declaration(decl)
                if field:
                    children.append(field)
        
        total_size = self.current_offset
        # Struct alignment
        alignment = self.config.pack_alignment
        if total_size % alignment != 0:
            total_size = ((total_size // alignment) + 1) * alignment
        
        type_info = TypeInfo(
            name=f"struct {name}",
            size_bits=total_size,
            is_struct=True
        )
        
        return FieldInfo(
            name=name,
            type_info=type_info,
            offset_bits=0,
            size_bits=total_size,
            children=children
        )
    
    def _analyze_union_node(self, union_node: c_ast.Union, name: str) -> FieldInfo:
        """Analyze union node"""
        children = []
        max_size = 0
        
        if union_node.decls:
            for decl in union_node.decls:
                # Union members all start from offset 0
                saved_offset = self.current_offset
                saved_bit_offset = self.current_bit_offset
                self.current_offset = 0
                self.current_bit_offset = 0
                
                field = self._analyze_declaration(decl)
                if field:
                    children.append(field)
                    max_size = max(max_size, field.size_bits)
                
                # Restore offset
                self.current_offset = saved_offset
                self.current_bit_offset = saved_bit_offset
        
        type_info = TypeInfo(
            name=f"union {name}",
            size_bits=max_size,
            is_union=True
        )
        
        return FieldInfo(
            name=name,
            type_info=type_info,
            offset_bits=0,
            size_bits=max_size,
            children=children
        )
    
    def _analyze_declaration(self, decl: c_ast.Decl) -> Optional[FieldInfo]:
        """Analyze declaration"""
        if not decl.type:
            return None
        
        name = decl.name or f"anonymous_{self.current_offset}"
        is_anonymous = not decl.name
        
        # Debug information
        if self.config.verbose and is_anonymous:
            print(f"Analyzing anonymous member: {name}, type: {type(decl.type)}")
            if hasattr(decl.type, 'type'):
                print(f"  Inner type: {type(decl.type.type)}")
        
        # Check bitfield
        is_bitfield = hasattr(decl, 'bitsize') and decl.bitsize is not None
        bit_width = None
        if is_bitfield:
            bit_width = self._get_constant_value(decl.bitsize)
        
        # Analyze type
        type_info, size_bits = self._analyze_type(decl.type)
        
        # Special handling: if it's anonymous and is an inline struct or union definition
        if is_anonymous and isinstance(decl.type, c_ast.TypeDecl):
            if isinstance(decl.type.type, c_ast.Struct):
                # Anonymous struct
                if self.config.verbose:
                    print(f"  Identified as anonymous struct")
                type_info = TypeInfo(
                    name="struct anonymous",
                    size_bits=self._calculate_struct_size(decl.type.type),
                    is_struct=True
                )
                size_bits = type_info.size_bits
            elif isinstance(decl.type.type, c_ast.Union):
                # Anonymous union
                if self.config.verbose:
                    print(f"  Identified as anonymous union")
                type_info = TypeInfo(
                    name="union anonymous", 
                    size_bits=self._calculate_union_size(decl.type.type),
                    is_union=True
                )
                size_bits = type_info.size_bits
        
        # Calculate offset
        field_offset = self.current_offset
        
        if is_bitfield and bit_width is not None:
            # Bitfield processing
            if self.current_bit_offset + bit_width <= self._get_type_alignment(type_info):
                # Can fit in current byte/word
                bit_offset = self.current_bit_offset
                self.current_bit_offset += bit_width
            else:
                # Need to align to next boundary
                alignment = self._get_type_alignment(type_info)
                self.current_offset = ((self.current_offset + alignment - 1) // alignment) * alignment
                field_offset = self.current_offset
                bit_offset = 0
                self.current_bit_offset = bit_width
            
            # Bitfield size is just the bit width
            actual_size = bit_width
        else:
            # Normal field alignment
            alignment = self._get_type_alignment(type_info)
            aligned_offset = ((self.current_offset + alignment - 1) // alignment) * alignment
            field_offset = aligned_offset
            self.current_offset = aligned_offset + size_bits
            self.current_bit_offset = 0
            actual_size = size_bits
            bit_offset = None
        
        # Analyze child members (if it's a struct or union)
        children = []
        
        # 对于数组，分析其元素类型
        if type_info.is_array and type_info.base_type:
            base_type_name = type_info.base_type
            
            # 检查基本类型是否是结构体或联合体
            if base_type_name in self.structs:
                children = self._get_struct_children(self.structs[base_type_name])
            elif base_type_name in self.unions:
                children = self._get_union_children(self.unions[base_type_name])
            elif base_type_name in self.typedefs:
                typedef_node = self.typedefs[base_type_name]
                if isinstance(typedef_node.type, c_ast.TypeDecl):
                    if isinstance(typedef_node.type.type, c_ast.Struct):
                        children = self._get_struct_children(typedef_node.type.type)
                    elif isinstance(typedef_node.type.type, c_ast.Union):
                        children = self._get_union_children(typedef_node.type.type)
            # 对于匿名结构体数组，检查数组类型本身
            elif type_info.is_struct and isinstance(decl.type, c_ast.ArrayDecl) and isinstance(decl.type.type, c_ast.TypeDecl):
                if isinstance(decl.type.type.type, c_ast.Struct):
                    # 匿名结构体数组，直接展开其成员
                    children = self._get_struct_children(decl.type.type.type)
                elif isinstance(decl.type.type.type, c_ast.Union):
                    # 匿名联合体数组，直接展开其成员
                    children = self._get_union_children(decl.type.type.type)
        
        # 如果不是数组，按原来的逻辑处理
        elif type_info.is_struct:
            if type_info.name.startswith('struct '):
                struct_name = type_info.name[7:]  # 移除 "struct " 前缀
                if struct_name in self.structs:
                    children = self._get_struct_children(self.structs[struct_name])
                elif struct_name == "anonymous" and isinstance(decl.type, c_ast.TypeDecl) and isinstance(decl.type.type, c_ast.Struct):
                    # 处理匿名结构体
                    children = self._get_struct_children(decl.type.type)
                elif struct_name == "anonymous" and isinstance(decl.type, c_ast.Struct):
                    # 直接的匿名结构体
                    children = self._get_struct_children(decl.type)
            else:
                # 检查是否是typedef的结构体
                if type_info.name in self.structs:
                    children = self._get_struct_children(self.structs[type_info.name])
                elif type_info.name in self.typedefs:
                    typedef_node = self.typedefs[type_info.name]
                    if isinstance(typedef_node.type, c_ast.TypeDecl) and isinstance(typedef_node.type.type, c_ast.Struct):
                        children = self._get_struct_children(typedef_node.type.type)
        elif type_info.is_union:
            if type_info.name.startswith('union '):
                union_name = type_info.name[6:]  # 移除 "union " 前缀
                if union_name in self.unions:
                    children = self._get_union_children(self.unions[union_name])
                elif union_name == "anonymous" and isinstance(decl.type, c_ast.TypeDecl) and isinstance(decl.type.type, c_ast.Union):
                    # 处理匿名联合体
                    children = self._get_union_children(decl.type.type)
                elif union_name == "anonymous" and isinstance(decl.type, c_ast.Union):
                    # 直接的匿名联合体
                    children = self._get_union_children(decl.type)
            else:
                # 检查是否是typedef的联合体
                if type_info.name in self.unions:
                    children = self._get_union_children(self.unions[type_info.name])
        
        return FieldInfo(
            name=name,
            type_info=type_info,
            offset_bits=field_offset,
            size_bits=actual_size or size_bits,
            bit_width=bit_width,
            bit_offset=bit_offset,
            is_anonymous=is_anonymous,
            is_bitfield=is_bitfield,
            children=children
        )
    
    def _analyze_type(self, type_node) -> Tuple[TypeInfo, int]:
        """分析类型节点"""
        if isinstance(type_node, c_ast.TypeDecl):
            return self._analyze_type_decl(type_node)
        elif isinstance(type_node, c_ast.PtrDecl):
            return self._analyze_ptr_decl(type_node)
        elif isinstance(type_node, c_ast.ArrayDecl):
            return self._analyze_array_decl(type_node)
        elif isinstance(type_node, c_ast.FuncDecl):
            return self._analyze_func_decl(type_node)
        elif isinstance(type_node, c_ast.Struct):
            # 直接的结构体节点（匿名结构体）
            struct_name = type_node.name or "anonymous"
            size_bits = self._calculate_struct_size(type_node)
            return TypeInfo(
                name=f"struct {struct_name}",
                size_bits=size_bits,
                is_struct=True
            ), size_bits
        elif isinstance(type_node, c_ast.Union):
            # 直接的联合体节点（匿名联合体）
            union_name = type_node.name or "anonymous"
            size_bits = self._calculate_union_size(type_node)
            return TypeInfo(
                name=f"union {union_name}",
                size_bits=size_bits,
                is_union=True
            ), size_bits
        else:
            # 未知类型，默认处理
            return TypeInfo(name="unknown", size_bits=32), 32
    
    def _analyze_type_decl(self, type_decl: c_ast.TypeDecl) -> Tuple[TypeInfo, int]:
        """分析类型声明"""
        if isinstance(type_decl.type, c_ast.IdentifierType):
            type_name = ' '.join(type_decl.type.names)
            size_bits = self._get_basic_type_size(type_name)
            is_signed = 'unsigned' not in type_name
            
            # 检查是否是typedef的结构体或联合体
            is_struct = False
            is_union = False
            if type_name in self.typedefs:
                typedef_node = self.typedefs[type_name]
                if isinstance(typedef_node.type, c_ast.TypeDecl):
                    if isinstance(typedef_node.type.type, c_ast.Struct):
                        is_struct = True
                    elif isinstance(typedef_node.type.type, c_ast.Union):
                        is_union = True
            elif type_name in self.structs:
                is_struct = True
            elif type_name in self.unions:
                is_union = True
            
            return TypeInfo(
                name=type_name,
                size_bits=size_bits,
                is_signed=is_signed,
                is_struct=is_struct,
                is_union=is_union
            ), size_bits
            
        elif isinstance(type_decl.type, c_ast.Struct):
            struct_node = type_decl.type
            struct_name = struct_node.name or "anonymous"
            
            if struct_node.decls:
                # 内联结构体定义
                size_bits = self._calculate_struct_size(struct_node)
            elif struct_name in self.structs:
                # 引用已定义的结构体
                size_bits = self._calculate_struct_size(self.structs[struct_name])
            else:
                size_bits = 0
            
            return TypeInfo(
                name=f"struct {struct_name}",
                size_bits=size_bits,
                is_struct=True
            ), size_bits
            
        elif isinstance(type_decl.type, c_ast.Union):
            union_node = type_decl.type
            union_name = union_node.name or "anonymous"
            
            if union_node.decls:
                # 内联联合体定义
                size_bits = self._calculate_union_size(union_node)
            elif union_name in self.unions:
                # 引用已定义的联合体
                size_bits = self._calculate_union_size(self.unions[union_name])
            else:
                size_bits = 0
            
            return TypeInfo(
                name=f"union {union_name}",
                size_bits=size_bits,
                is_union=True
            ), size_bits
            
        elif isinstance(type_decl.type, c_ast.Enum):
            enum_node = type_decl.type
            enum_name = enum_node.name or "anonymous"
            
            return TypeInfo(
                name=f"enum {enum_name}",
                size_bits=32,  # 枚举通常是int大小
                is_enum=True
            ), 32
        
        else:
            return TypeInfo(name="unknown", size_bits=32), 32
    
    def _analyze_ptr_decl(self, ptr_decl: c_ast.PtrDecl) -> Tuple[TypeInfo, int]:
        """分析指针声明"""
        base_type_info, _ = self._analyze_type(ptr_decl.type)
        
        return TypeInfo(
            name=f"{base_type_info.name} *",
            size_bits=self.config.pointer_size,
            is_pointer=True,
            base_type=base_type_info.name
        ), self.config.pointer_size
    
    def _analyze_array_decl(self, array_decl: c_ast.ArrayDecl) -> Tuple[TypeInfo, int]:
        """分析数组声明"""
        element_type_info, element_size = self._analyze_type(array_decl.type)
        
        # 获取当前维度
        array_size = 1
        if array_decl.dim:
            array_size = self._get_constant_value(array_decl.dim)
        
        # 构建维度列表
        dimensions = [array_size]
        
        # 如果元素类型也是数组，合并维度
        if element_type_info.is_array:
            dimensions.extend(element_type_info.array_dimensions)
            total_size = element_size * array_size
        else:
            total_size = element_size * array_size
        
        # 保持元素类型的结构体/联合体标记
        return TypeInfo(
            name=element_type_info.name,
            size_bits=total_size,
            is_array=True,
            base_type=element_type_info.name,
            array_dimensions=dimensions,
            is_struct=element_type_info.is_struct,  # 保持结构体标记
            is_union=element_type_info.is_union,    # 保持联合体标记
            is_enum=element_type_info.is_enum       # 保持枚举标记
        ), total_size
    
    def _analyze_func_decl(self, func_decl: c_ast.FuncDecl) -> Tuple[TypeInfo, int]:
        """分析函数声明"""
        return TypeInfo(
            name="function",
            size_bits=self.config.pointer_size,
            is_function=True
        ), self.config.pointer_size
    
    def _get_basic_type_size(self, type_name: str) -> int:
        """获取基本类型大小"""
        type_name = type_name.strip()
        
        # 检查类型定义
        if type_name in self.typedefs:
            typedef_node = self.typedefs[type_name]
            _, size = self._analyze_type(typedef_node.type)
            return size
        
        # 检查是否是已知的结构体类型
        if type_name in self.structs:
            return self._calculate_struct_size(self.structs[type_name])
        
        # 检查是否是已知的联合体类型
        if type_name in self.unions:
            return self._calculate_union_size(self.unions[type_name])
        
        # 检查基本类型
        if type_name in self.basic_types:
            return self.basic_types[type_name]
        
        # 处理修饰符
        base_type = type_name.replace('signed ', '').replace('unsigned ', '')
        if base_type in self.basic_types:
            return self.basic_types[base_type]
        
        # 默认大小
        return 32
    
    def _get_type_alignment(self, type_info: TypeInfo) -> int:
        """获取类型对齐大小"""
        if type_info.is_pointer:
            return self.config.pointer_size
        elif type_info.size_bits <= 8:
            return 8
        elif type_info.size_bits <= 16:
            return 16
        elif type_info.size_bits <= 32:
            return 32
        elif type_info.size_bits <= 64:
            return 64
        else:
            return min(self.config.pack_alignment, 64)
    
    def _calculate_struct_size(self, struct_node: c_ast.Struct) -> int:
        """计算结构体大小"""
        if not struct_node.decls:
            return 0
        
        # 保存当前状态
        saved_offset = self.current_offset
        saved_bit_offset = self.current_bit_offset
        
        self.current_offset = 0
        self.current_bit_offset = 0
        
        for decl in struct_node.decls:
            self._analyze_declaration(decl)
        
        total_size = self.current_offset
        
        # 结构体对齐
        alignment = self.config.pack_alignment
        if total_size % alignment != 0:
            total_size = ((total_size // alignment) + 1) * alignment
        
        # 恢复状态
        self.current_offset = saved_offset
        self.current_bit_offset = saved_bit_offset
        
        return total_size
    
    def _calculate_union_size(self, union_node: c_ast.Union) -> int:
        """计算联合体大小"""
        if not union_node.decls:
            return 0
        
        max_size = 0
        for decl in union_node.decls:
            if decl.type:
                _, size = self._analyze_type(decl.type)
                max_size = max(max_size, size)
        
        return max_size
    
    def _get_struct_children(self, struct_node: c_ast.Struct) -> List[FieldInfo]:
        """获取结构体子成员"""
        if not struct_node.decls:
            return []
        
        # 保存当前状态
        saved_offset = self.current_offset
        saved_bit_offset = self.current_bit_offset
        
        self.current_offset = 0
        self.current_bit_offset = 0
        
        children = []
        for decl in struct_node.decls:
            field = self._analyze_declaration(decl)
            if field:
                children.append(field)
        
        # 恢复状态
        self.current_offset = saved_offset
        self.current_bit_offset = saved_bit_offset
        
        return children
    
    def _get_union_children(self, union_node: c_ast.Union) -> List[FieldInfo]:
        """获取联合体子成员"""
        if not union_node.decls:
            return []
        
        children = []
        for decl in union_node.decls:
            # 保存当前状态
            saved_offset = self.current_offset
            saved_bit_offset = self.current_bit_offset
            
            self.current_offset = 0
            self.current_bit_offset = 0
            
            field = self._analyze_declaration(decl)
            if field:
                children.append(field)
            
            # 恢复状态
            self.current_offset = saved_offset
            self.current_bit_offset = saved_bit_offset
        
        return children
    
    def _get_constant_value(self, const_node) -> int:
        """获取常量值"""
        if const_node is None:
            return 1
        
        if hasattr(const_node, 'value'):
            try:
                value = const_node.value
                # 处理不同进制
                if value.startswith('0x') or value.startswith('0X'):
                    return int(value, 16)
                elif value.startswith('0') and len(value) > 1 and value.isdigit():
                    return int(value, 8)
                else:
                    return int(value)
            except ValueError:
                return 1
        
        return 1
    
    def save_yaml(self, data: Dict[str, Any], filename: str) -> bool:
        """Save as YAML file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, 
                         allow_unicode=True, indent=2, sort_keys=False)
            
            if self.config.verbose:
                print(f"YAML file saved: {filename}")
            
            return True
        except Exception as e:
            print(f"Error saving YAML file: {e}")
            return False
    
    def print_summary(self, data: Dict[str, Any]) -> None:
        """Print struct analysis summary"""
        if 'struct_info' in data:
            # 单个结构体
            info = data['struct_info']
            print(f"\n结构体分析结果:")
            print(f"名称: {info['name']}")
            print(f"总大小: {info['total_size_bits']} bits ({info['total_size_bytes']} 字节)")
            print(f"对齐: {info['pack_alignment']} bits")
            
            # 统计成员
            def count_members(field_data):
                count = 0
                if 'members' in field_data:
                    count += len(field_data['members'])
                    for member in field_data['members']:
                        count += count_members(member)
                return count
            
            if 'struct_definition' in data:
                member_count = count_members(data['struct_definition'])
                print(f"总成员数: {member_count}")
        
        elif 'generation_info' in data:
            # 多个结构体
            info = data['generation_info']
            print(f"\n批量分析结果:")
            print(f"结构体数量: {info['total_structs']}")
            print(f"联合体数量: {info['total_unions']}")
            print(f"对齐设置: {info['pack_alignment']} bits")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="C Struct YAML Generator based on pycparser")
    parser.add_argument('input_file', help='Input C header file')
    parser.add_argument('-s', '--struct', help='Target struct name (optional)')
    parser.add_argument('-o', '--output', help='Output YAML filename (optional)')
    parser.add_argument('-p', '--pack', type=int, default=1, help='Pack alignment in bytes (default 1)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--no-bitfields', action='store_true', help='Exclude bitfield information')
    parser.add_argument('--no-offsets', action='store_true', help='Exclude offset information')
    parser.add_argument('--no-children', action='store_true', help='Exclude child members')
    
    args = parser.parse_args()
    
    # Create configuration
    config = ConfigOptions(
        pack_alignment=args.pack * 8,  # Convert to bits
        verbose=args.verbose,
        include_bitfields=not args.no_bitfields,
        include_offsets=not args.no_offsets,
        include_children=not args.no_children
    )
    
    # Create generator
    generator = PycparserYamlGenerator(config)
    
    # Parse file
    result = generator.parse_file(args.input_file, args.struct)
    
    if result is None:
        print("Parsing failed")
        return 1
    
    # Print summary
    generator.print_summary(result)
    
    # Save result
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        if args.struct:
            output_file = f"{args.struct}.yml"
        else:
            output_file = f"{base_name}_structs.yml"
    
    if generator.save_yaml(result, output_file):
        print(f"\n✅ YAML file generated: {output_file}")
        return 0
    else:
        print(f"\n❌ YAML file generation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# shigl_cli.py
import sys
import os
from shigl.lexer import Lexer
from shigl.parser import Parser
from shigl.android import AndroidCodeGenerator

def main():
    if len(sys.argv) < 2:
        print("Usage: shigl <file.shigl>")
        sys.exit(1)
    
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        sys.exit(1)
    
    with open(filename, 'r') as f:
        source = f.read()
    
    # Lexer
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    print(f"✅ Tokens: {len(tokens)}")
    
    # Parser
    parser = Parser(tokens)
    program = parser.parse()
    print(f"✅ AST generated")
    
    # Find Android app
    android_app = None
    for stmt in program.statements:
        if hasattr(stmt, 'name') and hasattr(stmt, 'package'):
            android_app = stmt
            break
    
    if android_app:
        generator = AndroidCodeGenerator()
        files = generator.generate(android_app)
        
        # Create output directory
        output_dir = "android_output"
        os.makedirs(output_dir, exist_ok=True)
        
        for name, content in files.items():
            with open(os.path.join(output_dir, name), 'w') as f:
                f.write(content)
            print(f"✅ Generated: {name}")
        
        print(f"\n✅ All files generated in '{output_dir}/'")
    else:
        print("❌ No Android app found in source")

if __name__ == "__main__":
    main()
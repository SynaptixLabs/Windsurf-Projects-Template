#!/usr/bin/env python3
"""
Quick test script for windsurf_generate.py inheritance
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

try:
    from windsurf_generate import get_available_templates
    
    print("🧪 Testing Template Inheritance System")
    print("=" * 40)
    
    templates = get_available_templates()
    
    print("📋 Available Templates:")
    for name, info in templates.items():
        inheritance = f" (extends {info['extends']})" if info['extends'] else ""
        base_marker = " [BASE]" if info['is_base'] else ""
        print(f"  • {name}: {info['description']}{inheritance}{base_marker}")
    
    print("\n✅ Inheritance system loaded successfully!")
    print("\n🚀 Ready to generate projects:")
    print("   python scripts/windsurf_generate.py --template python-modern")
    print("   python scripts/windsurf_generate.py --template python-game-development")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

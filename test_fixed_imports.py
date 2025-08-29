import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Test the fixed relative imports
    from lib.cli import cli
    print('✅ lib.cli imports work!')
    print('✅ Ready to run the application!')
except ImportError as e:
    print(f'❌ Import error: {e}')

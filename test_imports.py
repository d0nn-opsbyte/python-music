import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from lib.helpers import seed_sample_data
    from lib.models import session
    from lib.interactive import interactive_main
    print('✅ All your custom imports work!')
except ImportError as e:
    print(f'❌ Custom import error: {e}')
    print('This might be a file path issue, not a dependency issue')

import sys
from pathlib import Path

"""
Jack Notes, this file sets up the testing enviroment and provides the backend path
to the testing suite without affecting the original application strcture
"""

sys.path.insert(0, str(Path(__file__).parent.parent))
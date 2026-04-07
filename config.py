
from pathlib import Path

# Get the directory where this file is located
BASE_DIR = Path(__file__).parent

# Data folder paths
DATA_DIR = BASE_DIR / "data"
FAQ_PATH = DATA_DIR / "faq.csv"
DB_PATH = DATA_DIR / "products.db"

# Make sure data folder exists
DATA_DIR.mkdir(exist_ok=True)



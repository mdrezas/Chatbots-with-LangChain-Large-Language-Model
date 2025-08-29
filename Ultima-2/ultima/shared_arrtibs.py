from pathlib import Path

PAGE_ICON = "🌱"
APP_NAME = "Ultima-2"
PROJECT_URL = "https://github.com/Ultima-Insights/WaynePracticum"

K = 26
FETCH_K = 26
CHUNK_SIZE = 1536
CHUNK_OVERLAP = 128
TEMPERATURE = 0.25
MAX_TOKENS = 8192
MODEL_N_CTX = 1000
DISTANCE_METRIC = "cos"
MAXIMAL_MARGINAL_RELEVANCE = True

ENABLE_ADVANCED_OPTIONS = False
ENABLE_LOCAL_MODE = False

MODEL_PATH = Path.cwd() / "models"
GPT4ALL_BINARY = "ggml-gpt4all-j-v1.3-groovy.bin"
EMB_INSTRUCTOR_XL = "hkunlp/instructor-xl"

DATA_PATH = Path.cwd() / "data"
DEFAULT_DATA_SOURCE = "https://github.com/Ultima-Insights/WaynePracticum"
MODE_HELP = """
TBD
"""

LOCAL_MODE_DISABLED_HELP = """
Local mode disabled!
"""

AUTHENTICATION_HELP = f"""
TBD
"""

USAGE_HELP = f"""
TBD
"""

OPENAI_HELP = """
TBD
"""

ACTIVELOOP_HELP = """
TBD
"""

UPLOAD_HELP = """
TBD
"""

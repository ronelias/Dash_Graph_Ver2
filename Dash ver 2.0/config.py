from dotenv import load_dotenv
import os

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT")
API_VERSION = "2024-12-01-preview"

# Fail fast if configs are missing
required = {
    "AZURE_API_KEY": AZURE_API_KEY,
    "AZURE_ENDPOINT": AZURE_ENDPOINT,
    "AZURE_DEPLOYMENT": AZURE_DEPLOYMENT,
}

missing = [key for key, value in required.items() if not value]
if missing:
    raise EnvironmentError(f"❌ Missing required environment variables: {', '.join(missing)}")

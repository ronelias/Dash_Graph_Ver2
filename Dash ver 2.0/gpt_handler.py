from openai import AzureOpenAI
from config import AZURE_API_KEY, AZURE_ENDPOINT, AZURE_DEPLOYMENT, API_VERSION
import pandas as pd
import re

client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION,
)

def extract_code_block(content: str) -> str:
    matches = re.findall(r"```(?:python)?(.*?)```", content, re.DOTALL)
    return matches[0].strip() if matches else content.strip()

def generate_code_from_prompt(prompt: str, df: pd.DataFrame) -> str:
    full_prompt = (
        f"You are an expert Python data scientist. Given a pandas DataFrame called df "
        f"with columns: {list(df.columns)}, generate matplotlib code to visualize: \"{prompt}\".\n"
        "The code should:\n"
        "1. Use clear titles and labels.\n"
        "2. Be concise and correct.\n"
        "3. Return only the Python code (no explanations).\n"
    )

    try:
        completion = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes Python visualization code. Return code only."},
                {"role": "user", "content": full_prompt}
            ]
        )
        content = completion.choices[0].message.content
        return extract_code_block(content)
    except Exception as e:
        raise RuntimeError(f"❌ GPT request failed: {e}")

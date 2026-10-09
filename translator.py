import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "translate_prompt.md"


def _resolve_api_key():
    # 读取我们刚才存的钥匙
    api_key = os.getenv("OPEN_ROUTER_KEY")
    if not api_key:
        raise ValueError("没有找到 OPEN_ROUTER_KEY，请检查 .env 文件")
    return api_key

def llm_generate(user_prompt, target_language="Chinese"):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=_resolve_api_key(),
    )

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8").format(
        target_language=target_language
    )
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(llm_generate(sys.argv[1]))
import os
from data.master_syllabus import generate_overview
import anthropic
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む

def generate_book():
    """
    """
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    # 🌸 messages contentの中にあるtextを変数として外に出しました
    with open("AIdocs/講義資料生成AI.md", "r") as f:
        book_prompt = f.read()

    with open("syllabus.yaml", "r") as f:
        syllabus = f.read()

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.5,
        system="",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "入力データ: " + syllabus + "<br>" + "要件定義書: " + book_prompt + "<br> をもとにしてpythonのコードブロックのみ出力"
                    }
                ]
            }
        ]
    )
    return message.content[0].text



code = generate_book()
code = code.replace("```python", "").replace("```", "")
with open("generate_book.py", "w") as f:
    f.write(code)

# codeを実行するコードを追記
# exec(code)




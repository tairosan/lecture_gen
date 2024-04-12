import os
from data.master_syllabus import generate_overview
import anthropic
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む

def generate_lecture_content(lecture_title, lecture_description):
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

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
"text": f"""
次の講義のタイトルに基づいて、講義の内容を生成してください。
講義のタイトル: {lecture_title}
講義の概要: {lecture_description}
上記の内容を学習できる研修資料の作成をお願いします。
- pythonコード    
- md形式



以下は構成例
## 目次（リンクで飛ぶことができるように <a id="introduction"></a> など利用）
## {lecture_title}とは（1000文字程度でわかりやすく）

## 解説
詳細解説と簡単な例題
### タイトル（5つ）
#### 詳細解説（500文字）
#### 例題と解説


                        """
                    }
                ]
            }
        ]
    )

    return message.content[0].text

def generate_quiz_content(lecture_title, lecture_description):
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    # 花屋さんへ: ここから下は、AIに4択問題を作ってもらうための指示を出しているところです。
    # まず、どのAIモデルを使うか指定します。ここでは "claude-3-opus-20240229" というモデルを使います。
    message = client.messages.create(
        model="claude-3-opus-20240229",  # 使用するAIモデルの名前
        max_tokens=4000,  # AIが生成する最大の単語数
        temperature=0.5,  # 生成する文章のランダム性を調整するパラメータ
        system="",  # AIに事前に与える設定（ここでは空欄）
        messages=[  # AIに与える指示やコンテキストを設定
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
次の講義のタイトルと概要に基づいて、4択問題を5つ生成してください。
講義のタイトル: {lecture_title}
講義の概要: {lecture_description}

## 目次（リンクで飛ぶことができるように <a id="introduction"></a> など利用）
                        
## 実践問題
思考力を要する基礎問題
### 課題と解説（5つ）

## 4択問題
    - 4択問題を5つ
    - 回答、解説はトグルにする
    - 解説には引用を載せる
    形式は以下の通り
<details>
<summary>問題1: DALL·E 3 で生成できる画像の最大サイズは？</summary>

- a. 512x512
- b. 1024x1024
- c. 1792x1792
- d. 2048x2048

<details>
<summary>回答と解説</summary>

回答: b. 1024x1024

DALL·E 3 では、1024x1024, 1024x1792, 1792x1024 の3つのサイズから選択できます。最大サイズは 1792x1024 です。
</details>
</details>
                        """
                    }
                ]
            }
        ]
    )

    return message.content[0].text

def generate_lectures(syllabus):
    os.makedirs("output", exist_ok=True)
    total_weeks = len(syllabus)
    
    for week_num, week in enumerate(syllabus, start=1):
        week_dir = f"output/week{week['week']}"
        os.makedirs(week_dir, exist_ok=True)
        
        with open(f"{week_dir}/syllabus.md", "w") as f:
            f.write(f"# Week {week['week']} Syllabus\n\n")
            f.write("## Topics\n")
            for topic in week["topics"]:
                f.write(f"- {topic}\n")
        
        print(f"Week {week['week']}の講義を生成しています...")
        for i, lecture in enumerate(tqdm(week["lectures"], desc=f"Week {week['week']}, Lecture"), start=1):
            with open(f"{week_dir}/lecture{i}.md", "w") as f:
                f.write(f"# {lecture['title']}\n\n")
                lecture_content = generate_lecture_content(lecture["title"], lecture["description"])
                f.write(lecture_content)
            print(f"講義 {i} の生成が完了しました。")
            
            with open(f"{week_dir}/quiz{i}.md", "w") as f:    
                quiz_content = generate_quiz_content(lecture["title"], lecture["description"])
                f.write("# 問題集\n\n")
                f.write(quiz_content)
            print(f"問題集 {i} の生成が完了しました。")
        
        print(f"Week {week['week']} が完了しました。")
        print(f"進捗状況: {week_num}/{total_weeks} 週が完了しました。\n")

    generate_overview()
    print("すべての講義が正常に生成されました!")

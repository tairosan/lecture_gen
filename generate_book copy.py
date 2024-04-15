
import os
import yaml
import anthropic
from lecture_generator import generate_lecture_content
from quiz_generator import generate_quiz_content

def main():
    # syllabusファイルを読み込む
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    # 大項目ごとにディレクトリを作成
    for week in syllabus:
        week_dir = f"book/week{week['week']}"
        os.makedirs(week_dir, exist_ok=True)

        # 中項目ごとにMarkdownファイルを作成
        for lecture in week["lectures"]:
            lecture_file = f"{week_dir}/{lecture['title']}.md"

            # 講義資料を生成
            lecture_content = generate_lecture_content(lecture["title"], lecture["description"])

            # 問題を生成
            quiz_content = generate_quiz_content(lecture["title"], lecture["description"])

            # 講義資料と問題を中項目のファイルに書き込む
            with open(lecture_file, "w") as f:
                f.write(f"# {lecture['title']}\n\n")
                f.write(lecture_content)
                f.write("\n\n")
                f.write(quiz_content)

if __name__ == "__main__":
    main()



import os
import anthropic

def generate_lecture_content(lecture_title, lecture_description):
    # Claude APIのクライアントを初期化
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    # 講義資料生成AIの仕様書を読み込む
    with open("AIdocs/講義資料生成AI.md", "r") as f:
        lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

    # Claude APIを使って講義資料を生成
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
                        "text": lecture_content_prompt
                    }
                ]
            }
        ]
    )

    return message.content[0].text



import os
import anthropic

def generate_quiz_content(lecture_title, lecture_description):
    # Claude APIのクライアントを初期化
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    # 問題生成AIの仕様書を読み込む
    with open("AIdocs/問題生成AI.md", "r") as f:
        quiz_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

    # Claude APIを使って問題を生成
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
                        "text": quiz_content_prompt
                    }
                ]
            }
        ]
    )

    return message.content[0].text

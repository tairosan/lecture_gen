
import os
import yaml
import anthropic
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む

class LectureGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def generate_lecture_content(self, lecture_title, lecture_description):
        with open("ais/講義資料生成AI.md", "r") as f:
            lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
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

        return response.content[0].text.strip()

class QuizGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def generate_quiz_content(self, lecture_title, lecture_description):
        with open("ais/問題生成AI.md", "r") as f:
            quiz_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
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

        return response.content[0].text.strip()

def main():
    # aisディレクトリがなければ作成
    os.makedirs("ais", exist_ok=True)

    # syllabus.yamlを読み込む
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    lecture_generator = LectureGenerator()
    quiz_generator = QuizGenerator()

    # bookディレクトリを作成
    os.makedirs("book", exist_ok=True)

    for week in syllabus:
        week_num = week["week"]
        topics = week["topics"]

        # 週ごとのディレクトリを作成
        week_dir = f"book/week{week_num}"
        os.makedirs(week_dir, exist_ok=True)

        for lecture in week["lectures"]:
            lecture_title = lecture["title"]
            lecture_description = lecture["description"]

            # 講義資料を生成
            lecture_content = lecture_generator.generate_lecture_content(lecture_title, lecture_description)

            # 問題を生成
            quiz_content = quiz_generator.generate_quiz_content(lecture_title, lecture_description)

            # 講義資料と問題をファイルに書き出す
            with open(f"{week_dir}/{lecture_title}.md", "w") as f:
                f.write(f"# {lecture_title}\n\n")
                f.write(f"## 講義資料\n\n{lecture_content}\n\n")
                f.write(f"## 問題\n\n{quiz_content}\n")

if __name__ == "__main__":
    main()


import os
import yaml
from dotenv import load_dotenv
import anthropic
from tqdm import tqdm

load_dotenv()  # .envファイルから環境変数を読み込む

class BookGenerator:
    def __init__(self, syllabus_file):
        self.syllabus_file = syllabus_file
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def generate_book(self):
        # syllabusファイルを読み込む
        with open(self.syllabus_file, "r") as f:
            syllabus = yaml.safe_load(f)

        # aisディレクトリがなければ作成
        os.makedirs("ais", exist_ok=True)

        # 大項目ごとにbookディレクトリ内にディレクトリを作成
        for week in syllabus:
            week_dir = f"book/week{week['week']}"
            os.makedirs(week_dir, exist_ok=True)

            # 中項目ごとにMarkdownファイルを作成
            for lecture in tqdm(week["lectures"], desc=f"Week {week['week']}"):
                lecture_file = f"{week_dir}/{lecture['title']}.md"

                # 講義資料を生成
                lecture_content = self.generate_lecture_content(lecture["title"], lecture["description"])

                # 問題集を生成
                quiz_content = self.generate_quiz_content(lecture["title"], lecture["description"])

                # 講義資料と問題集をファイルに書き込む
                with open(lecture_file, "w") as f:
                    f.write(f"# {lecture['title']}\n\n")
                    f.write(lecture_content)
                    f.write("\n\n")
                    f.write(quiz_content)

    def generate_lecture_content(self, lecture_title, lecture_description):
        # aisディレクトリから講義資料生成AIのドキュメントを読み込む
        with open("ais/講義資料生成AI.md", "r") as f:
            lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        # Claude APIを使って講義資料を生成
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

    def generate_quiz_content(self, lecture_title, lecture_description):
        # aisディレクトリから問題生成AIのドキュメントを読み込む
        with open("ais/問題生成AI.md", "r") as f:
            quiz_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        # Claude APIを使って問題集を生成
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


if __name__ == "__main__":
    generator = BookGenerator("syllabus.yaml")
    generator.generate_book()

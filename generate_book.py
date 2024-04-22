
import os
import yaml
from dotenv import load_dotenv
import anthropic
from tqdm import tqdm

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
    print("📚 書籍生成AIを開始します...")

    # aisディレクトリがなければ作成
    os.makedirs("ais", exist_ok=True)

    # syllabus.yamlを読み込み
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    lecture_generator = LectureGenerator()
    quiz_generator = QuizGenerator()

    for month_data in tqdm(syllabus, desc="📆 月別処理中"):
        month = month_data["month"]
        topics = month_data["topics"]
        lectures = month_data["lectures"]

        # 大項目ディレクトリを作成
        os.makedirs(f"book/{month:02d}", exist_ok=True)

        for lecture in tqdm(lectures, desc=f"📝 {month}月の講義を生成中", leave=False):
            lecture_title = lecture["title"]
            lecture_description = lecture["description"]

            # 講義資料を生成
            lecture_content = lecture_generator.generate_lecture_content(lecture_title, lecture_description)

            # 問題を生成
            quiz_content = quiz_generator.generate_quiz_content(lecture_title, lecture_description)

            # 中項目のMarkdownファイルを作成
            with open(f"book/{month:02d}/{lecture_title}.md", "w") as f:
                f.write(f"# {lecture_title}\n\n")
                f.write(lecture_content)
                f.write("\n\n")
                f.write(quiz_content)

    print("📖 書籍の生成が完了しました！")

if __name__ == "__main__":
    main()


import os
import yaml
import anthropic

# LectureGeneratorクラス
class LectureGenerator:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_lecture_content(self, lecture_title, lecture_description):
        with open("ais/講義資料生成AI.md", "r") as f:
            lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": lecture_content_prompt
                }
            ]
        )
        return message.content

# QuizGeneratorクラス
class QuizGenerator:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_quiz_content(self, lecture_title, lecture_description):
        with open("ais/問題生成AI.md", "r") as f:
            quiz_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": quiz_content_prompt
                }
            ]
        )
        return message.content

# メイン処理
def main():
    # APIキーを環境変数から取得
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # LectureGeneratorとQuizGeneratorのインスタンスを作成
    lecture_generator = LectureGenerator(api_key)
    quiz_generator = QuizGenerator(api_key)

    # syllabus.yamlを読み込む
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    # 大項目ごとにディレクトリを作成し、中項目ごとにファイルを生成
    for week in syllabus:
        week_dir = f"book/week{week['week']}"
        os.makedirs(week_dir, exist_ok=True)

        for topic in week["topics"]:
            topic_file = f"{week_dir}/{topic}.md"

            with open(topic_file, "w") as f:
                f.write(f"# {topic}\n\n")

                for lecture in week["lectures"]:
                    lecture_title = lecture["title"]
                    lecture_description = lecture["description"]

                    # 講義資料を生成
                    lecture_content = lecture_generator.generate_lecture_content(lecture_title, lecture_description)
                    f.write(f"## {lecture_title}\n\n")
                    f.write(lecture_content)
                    f.write("\n\n")

                    # 問題を生成
                    quiz_content = quiz_generator.generate_quiz_content(lecture_title, lecture_description)
                    f.write("## 問題\n\n")
                    f.write(quiz_content)
                    f.write("\n\n")

if __name__ == "__main__":
    main()

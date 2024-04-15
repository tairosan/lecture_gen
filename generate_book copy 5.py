
import os
import yaml
import anthropic
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# aisディレクトリが存在しない場合は作成する
if not os.path.exists("ais"):
    os.makedirs("ais")

# 講義資料生成AIのドキュメントを作成
with open("ais/lecture_generator.md", "w") as f:
    f.write("""
## 📝 講義資料生成AI

講義のタイトルと概要から、講義資料の内容を生成するAI

<details>
<summary>🎯 入力</summary>

- 講義のタイトル (テキスト): {lecture_title}
- 講義の概要 (テキスト): {lecture_description}
</details>

<details>
<summary>📚 出力</summary>

- md形式の研修資料 (テキスト)
</details>

<details>
<summary>🛠️ 処理</summary>

以下の構成で、講義のタイトルと概要から、わかりやすく体系的な講義資料を生成します。学習者が講義内容を効果的に理解し、実践的なスキルを身につけられるような資料を目指します。

1. 📋 目次（リンク付き）
   - 講義資料の各セクションへのリンクを含む目次を作成します。 
   - 目次のリンクをクリックすると、該当セクションにジャンプできます。
    -（例: <a id="introduction"></a>）

2. 📝 {lecture_title}の説明（1000文字程度）
   - 講義のタイトル（{lecture_title}）について、1000文字程度でわかりやすく説明します。
   - 講義の概要や目的、学習内容などを簡潔にまとめます。

3. 🔍 詳細解説（5つのトピック、各500文字）  
   - 講義の内容を5つのトピックに分けて、各トピックを500文字程度で詳しく解説します。
   - トピックごとに、重要なポイントや具体例を交えながら、わかりやすく説明します。

4. ✏️ 各トピックの例題と解説
   - 各トピックについて、理解を深めるための例題を提示します。 
   - 例題の問題文と解答、解説を記載し、学習者が実践的に理解できるようにします。

5. 📚 専門用語の表形式まとめ
   - 講義で登場した専門用語を表形式でまとめます。
   - 用語の意味や説明を簡潔に記載し、学習者が専門用語を整理・理解しやすいようにします。
</details>

<details>
<summary>✅ テスト</summary>

- [ ] 目次にリンクが付いているか（例: <a id="introduction"></a>）
- [ ] {lecture_title}が実際の講義タイトルに置き換えられているか
- [ ] 詳細解説が5つのトピックについて、各500文字程度で説明されているか
- [ ] 各トピックに例題と解説が付いているか 
- [ ] 専門用語が表形式でまとめられているか
</details>
""")

# 問題生成AIのドキュメントを作成
with open("ais/quiz_generator.md", "w") as f:
    f.write("""
## 📝 問題生成AI
講義のタイトルと概要から、問題資料の内容を生成します

<details>
<summary>🎯 入力</summary>

- 講義のタイトル: {lecture_title}
- 講義の概要: {lecture_description}
</details>

<details>
<summary>📝 出力</summary>

- 4択問題を5つ生成
  - 目次（リンクで飛ぶことができるように <a id="introduction"></a> など利用）
  - 実践問題（思考力を要する基礎問題）
    - 課題と解説（5つ）
  - 4択問題
    - 回答、解説はトグルにする
    - 解説には引用を載せる
    - 形式は以下の通り
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
</details>

<details>
<summary>🛠️ 処理</summary>

1. 講義のタイトルと概要から、4択問題を5つ生成
2. 目次を作成（リンク付き）
4. 4択問題を5つ作成
   - 回答と解説はトグルで表示
   - 解説には引用を載せる
5. 実践問題を5つ作成
   - 思考力を要する基礎問題
</details>

<details>
<summary>⚠️ 注意</summary>

- 目次にはリンクを付ける（例: <a id="introduction"></a>）
- 4択問題の選択肢と解説は、講義の内容に即したものにする
- 解説には、講義資料からの引用を含める
</details>
""")

class LectureGenerator:
    def __init__(self):
        # Anthropic APIクライアントを初期化
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
        )

    def generate_lecture_content(self, lecture_title, lecture_description):
        # 講義資料生成AIのドキュメントを読み込む
        with open("ais/lecture_generator.md", "r") as f:
            lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        # Claude APIを使って講義資料を生成
        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            # model="claude-3-opus-20240229",
            max_tokens=200,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": lecture_content_prompt
                }
            ]
        )
        text = message.content[0].text.strip()
        return text

class QuizGenerator:
    def __init__(self):
        # Anthropic APIクライアントを初期化
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
        )

    def generate_quiz_content(self, lecture_title, lecture_description):
        # 問題生成AIのドキュメントを読み込む
        with open("ais/quiz_generator.md", "r") as f:
            quiz_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description)

        # Claude APIを使って問題を生成
        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            # model="claude-3-opus-20240229",
            max_tokens=200,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": quiz_content_prompt
                }
            ]
        )
        text = message.content[0].text.strip()
        return text

def main():
    # syllabus.yamlを読み込む
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    # 講義資料生成AIと問題生成AIのインスタンスを作成
    lecture_generator = LectureGenerator()
    quiz_generator = QuizGenerator()

    # 大項目ごとにディレクトリを作成し、中項目ごとにファイルを生成
    for week in syllabus:
        week_dir = f"book/week{week['week']}"
        os.makedirs(week_dir, exist_ok=True)

        for lecture in week["lectures"]:
            lecture_title = lecture["title"]
            lecture_description = lecture["description"]

            # 講義資料を生成
            lecture_content = lecture_generator.generate_lecture_content(lecture_title, lecture_description)
            print(lecture_content)

            # 問題を生成
            quiz_content = quiz_generator.generate_quiz_content(lecture_title, lecture_description)
            print(quiz_content)

            # 中項目のファイルに講義資料と問題を書き込む
            with open(f"{week_dir}/{lecture_title}.md", "w") as f:
                f.write(lecture_content)
                f.write("\n\n")
                f.write(quiz_content)

if __name__ == "__main__":
    main()

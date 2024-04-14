# 📚 書籍生成AI
講義資料生成AIと問題生成AIを使った書籍生成プログラムの仕様

<details>
<summary>📥 入力</summary>

- カリキュラムのYAMLファイル（`syllabus.yaml`）
  - 各週のタイトルと概要が記載されたYAMLファイル
</details>

<details>
<summary>📤 出力</summary>

- 書籍用のMarkdownファイル（`book.md`）
  - 各週の講義資料と問題集が1つのMarkdownファイルにまとめられる
</details>

<details>
<summary>🛠️ 処理の流れ</summary>

1. `curriculum.yaml`を読み込み、各週のタイトルと概要を取得
2. 各週について以下の処理を繰り返す：
   1. 講義資料生成AIを使って、タイトルと概要から講義資料を生成
   2. 問題生成AIを使って、タイトルと概要から問題集を生成
   3. 生成された講義資料と問題集を`book.md`に追記
3. 完成した`book.md`を出力
</details>

<details>
<!-- <summary>📝 プログラムの構成</summary>

- `main.py`
  - メインの処理を行うPythonスクリプト
  - `curriculum.yaml`の読み込み、AIの呼び出し、`book.md`の生成を行う
- `lecture_generator.py`
  - 講義資料生成AIを呼び出す関数`generate_lecture_content()`を定義
- `quiz_generator.py`
  - 問題生成AIを呼び出す関数`generate_quiz_content()`を定義
- `aidocs/講義資料生成AI.md`
  - 講義資料生成AIのプロンプトが記載されたMarkdownファイル
- `aidocs/quiz_content_prompt.md`
  - 問題生成AIのプロンプトが記載されたMarkdownファイル
</details> -->
<summary>📝 プログラムの構成</summary>

- `main.py`
  - メインの処理を行うPythonスクリプト
  - `curriculum.yaml`の読み込み、AIの呼び出し、`book.md`の生成を行う
- `lecture_generator.py`
  - 講義資料生成AIを呼び出す関数`generate_lecture_content()`を定義
- `quiz_generator.py`
  - 問題生成AIを呼び出す関数`generate_quiz_content()`を定義
- `aidocs/講義資料生成AI.md`
  - 講義資料生成AIのプロンプトが記載されたMarkdownファイル
- `aidocs/quiz_content_prompt.md`
  - 問題生成AIのプロンプトが記載されたMarkdownファイル
</details>

<details>
<summary>🌟 プログラムの特徴</summary>

- 📝 YAMLファイルでカリキュラムの構造を柔軟に定義可能！
- 🤖 講義資料生成AIと問題生成AIの2つのAIを組み合わせて自動生成！
- 📚 生成された資料は1つのMarkdownファイルにまとめて書籍として出力！
</details>




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

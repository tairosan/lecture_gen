# Lecture Generator

Lecture Generatorは、講義シリーズの資料を自動生成するPythonプロジェクトです。マスターシラバスに基づいて、週ごとのシラバスと個々の講義資料をマークダウン形式で生成します。また、講義の全体像をGraphVizを使って視覚化します。

## 必要条件

- Python 3.x
- GraphViz
- PyYAML

## インストール

1. このリポジトリをクローンまたはダウンロードします。

2. 必要なPythonパッケージをインストールします。
   ```
   pip install graphviz pyyaml
   ```

## 使用方法

1. `./transcript.txt` に書きたい書籍の読み上げ文章を書き込みます
2. 以下のコマンドを実行し、読み上げ文章からシラバスを作成します。
   ```
   python 1_transcript_to_syllabus.py
   ```
   このスクリプトは、`./transcript.txt`に書かれた読み上げ文章を読み込み、それをもとにシラバスを生成します。生成されたシラバスは`data/syllabus.yaml`に保存されます。

3. 次に、以下のコマンドを実行し、シラバスから書籍を作成します。
   ```
   python 2_syllabus_to_book.py
   ```
   このスクリプトは、`data/syllabus.yaml`に保存されたシラバスを読み込み、それをもとに書籍の各章や節を生成します。生成された書籍の内容は`output/`ディレクトリ内に保存されます。


4. 生成された資料は `output/` ディレクトリ内の対応する週のサブディレクトリに保存されます。また、講義の全体像を示す画像が `syllabus_graph.png` に生成されます。

## フォルダ構成

```
lecture_generator/
.
├── README.md
├── data
│   ├──  syllabus.yaml
│   ├── __pycache__
│   │   └── master_syllabus.cpython-311.pyc
│   └── master_syllabus.py
├── images
│   ├── course_overview
│   └── course_overview.pdf
├── main.py
├── output
│   ├── week1
│   │   ├── lecture1.md
│   │   ├── lecture2.md
│   │   ├── lecture3.md
│   │   ├── lecture4.md
│   │   ├── lecture5.md
│   │   ├── lecture6.md
│   │   ├── lecture7.md
│   │   ├── quiz1.md
│   │   ├── quiz2.md
│   │   ├── quiz3.md
│   │   ├── quiz4.md
│   │   ├── quiz5.md
│   │   ├── quiz6.md
│   │   ├── quiz7.md
│   │   └── syllabus.md
│   ├── week2
│   │   ├── lecture1.md
│   │   ├── lecture2.md
│   │   ├── lecture3.md
│   │   ├── lecture4.md
│   │   ├── lecture5.md
│   │   ├── lecture6.md
│   │   ├── lecture7.md
│   │   ├── quiz1.md
│   │   ├── quiz2.md
│   │   ├── quiz3.md
│   │   ├── quiz4.md
│   │   ├── quiz5.md
│   │   ├── quiz6.md
│   │   ├── quiz7.md
│   │   └── syllabus.md
├── references
│   ├── cursor.md
│   ├── openinterpreter.md
│   └── promptprogramming.md
├── templates
│   ├── lecture_template.md
│   └── weekly_syllabus_template.md
└── utils
    ├── __pycache__
    │   └── generator.cpython-311.pyc
    └── generator.py

19 directories, 92 files

```

## ライセンス

このプロジェクトは [MIT ライセンス](LICENSE) の下で公開されています。


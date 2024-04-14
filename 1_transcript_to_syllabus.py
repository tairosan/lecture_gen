import yaml
import anthropic
import os
from dotenv import load_dotenv
from graphviz import Digraph  # graphvizモジュールをインポート

load_dotenv()  # .envファイルから環境変数を読み込む

anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")  # 環境変数からAPI keyを取得

def generate_syllabus(transcript):
    """
    文字起こし情報からカリキュラムを作成する関数
    
    Args:
        transcript (str): 文字起こし情報
        
    Returns:
        str: カリキュラム
    """
    client = anthropic.Anthropic(api_key=anthropic.api_key)
    
    prompt = f"""
    以下の文字起こし情報からカリキュラムを作成してください。
    カリキュラムはyaml形式で出力してください。

    
    文字起こし情報:
    {transcript}
    
    - week: 1
     topics:
     - 基礎開発ツール講習
     lectures:
       - title: （複数）
       description: |
    - week: 2
     topics:
     - 
     lectures:
       - title: （複数）
       description: |
         
    """
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    syllabus_yaml = response.content[0].text.strip()
    syllabus_yaml = syllabus_yaml.replace("```yaml", "").replace("```", "")
    return syllabus_yaml

def generate_syllabus_graph():
    """
    syllabusの内容からグラフを生成する関数
    
    Args:
        syllabus (dict): syllabusの内容が入った辞書
        
    Returns:
        None
    """
    client = anthropic.Anthropic(api_key=anthropic.api_key)

    with open("./syllabus.yaml", "r") as file:
        syllabus = file.read()

    prompt = f"""
    syllabus:
    {syllabus}

    上記のシラバスから、
    以下のPythonコードを生成してください。

    # syllabusデータの作成 （型：リスト[dict]）
    # Graphvizを使ってグラフを作成。コメントに'Syllabus Graph'を指定。
    # 週のボックスノードと講義サブボックスの作成
    # syllabusデータの各週について繰り返し処理
    # 週のインデックスを取得
    # 週のトピックを取得し、カンマ区切りの文字列に変換
    # 週のノード名を作成（例: "Week 1\n基礎開発ツール講習"）
    # 週のノードを作成。ボックス形状、塗りつぶし、水色の背景色を指定。
    # 週ごとのサブグラフを作成
    # 講義のタイトルをリストアップし、改行区切りの文字列に変換
    # サブグラフ内に講義一覧のノードを作成。ボックス形状、ラベルに講義一覧を指定。
    # 週のノードと講義一覧のノードを破線で接続
    # 週ボックスノードの下部（south）からエッジを始め、headport='sw'はサブグラフの左下（south-west）にエッジを接続するように指定
    # 隔週ごとの矢印の接続
    # syllabusデータの週の数-1回繰り返し処理
    # 現在の週のデータを取得
    # 次の週のデータを取得
    # 現在の週のノード名を作成
    # 次の週のノード名を作成
    # 現在の週のノードと次の週のノードを矢印で接続
    # グラフの保存と表示
    # グラフを'syllabus_graph.png'という名前で保存し、表示する

    pythonのコードブロックのみ出力。その他説明は書かないこと。
    """
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    code = response.content[0].text.strip()
    
    code = code.replace("```python", "").replace("```", "")
    with open("generate_syllabus_graph.py", "w") as f:
        f.write(code)

    # codeを実行するコードを追記
    exec(code)
    
    
# from generate_syllabus_graph import generate_syllabus_graph

# 使用例
with open("./transcript_cook.txt", "r") as f:
    transcript = f.read()  # transcript.txtファイルから文字起こし情報を読み込む
    syllabus = generate_syllabus(transcript)
    print(syllabus)
    with open("syllabus.txt", "w") as f:
        f.write(syllabus)
    
    os.rename("syllabus.txt", "syllabus.yaml")
    
    # # syllabusをyamlで読み込んで辞書形式に変換
    # syllabus_dict = yaml.safe_load(syllabus)
    
    # syllabusの内容からグラフを生成
    generate_syllabus_graph()

# generate_syllabus_graph()

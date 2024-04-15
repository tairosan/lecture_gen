
import yaml
from graphviz import Digraph

# syllabusデータの作成 （型：リスト[dict]）
with open('syllabus.yaml', 'r') as file:
    syllabus = yaml.safe_load(file)

# Graphvizを使ってグラフを作成。コメントに'Syllabus Graph'を指定。
graph = Digraph(comment='Syllabus Graph')

# 月のボックスノードと講義サブボックスの作成
for month_data in syllabus:
    # 月のインデックスを取得
    month = month_data['month']
    
    # 月のトピックを取得し、カンマ区切りの文字列に変換
    topics = ', '.join(month_data['topics'])
    
    # 月のノード名を作成（例: "Month 1\n武士の歴史と心構え"）
    month_node_name = f"Month {month}\n{topics}"
    
    # 月のノードを作成。ボックス形状、塗りつぶし、水色の背景色を指定。
    graph.node(month_node_name, shape='box', style='filled', fillcolor='lightblue')
    
    # 月ごとのサブグラフを作成
    with graph.subgraph(name=f'cluster_month_{month}') as subgraph:
        # 講義のタイトルをリストアップし、改行区切りの文字列に変換
        lecture_titles = [lecture['title'] for lecture in month_data['lectures']]
        lecture_list = '\n'.join(lecture_titles)
        
        # サブグラフ内に講義一覧のノードを作成。ボックス形状、ラベルに講義一覧を指定。
        subgraph.node(f'lectures_month_{month}', shape='box', label=lecture_list)
        
        # 月のノードと講義一覧のノードを破線で接続
        graph.edge(month_node_name, f'lectures_month_{month}', style='dashed', tailport='s', headport='nw')

# 隔月ごとの矢印の接続
for i in range(len(syllabus) - 1):
    # 現在の月のデータを取得
    current_month_data = syllabus[i]
    current_month = current_month_data['month']
    current_topics = ', '.join(current_month_data['topics'])
    current_month_node_name = f"Month {current_month}\n{current_topics}"
    
    # 次の月のデータを取得
    next_month_data = syllabus[i + 1]
    next_month = next_month_data['month']
    next_topics = ', '.join(next_month_data['topics'])
    next_month_node_name = f"Month {next_month}\n{next_topics}"
    
    # 現在の月のノードと次の月のノードを矢印で接続
    graph.edge(current_month_node_name, next_month_node_name)

# グラフの保存と表示
graph.render('syllabus_graph', format='png', view=True)

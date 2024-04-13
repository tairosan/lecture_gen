
import graphviz

# syllabusデータの作成 （型：リスト[dict]）
syllabus = [{'week': 1, 'topics': ['GPTsを用いたプロンプトプログラミングとドキュメントプログラミング', 'Cursorの基本操作と活用法'], 'lectures': [{'title': 'GPTsの特徴と利用方法', 'description': 'GPTsの概要と書籍作成への活用方法を学ぶ。Chatbot作成の手順を理解し、プロンプトプログラミングとドキュメントプログラミングのデモを通して、効率的な書籍作成を目指す。\n'}, {'title': 'Cursorの概要と主要機能', 'description': 'Cursorの基本操作を習得し、コード編集・生成、オートコンプリート、AIとの対話など、主要機能を活用して生成されたコンテンツを迅速かつ的確に修正できるようになる。\n'}]}, {'week': 2, 'topics': ['テキスト生成AIの概要', 'シェルとOpen Interpreterの活用法'], 'lectures': [{'title': '書籍作成に適したテキスト生成AIの選択', 'description': 'APIとローカルLLMの違いと分類を理解し、主要モデル（GPT-4, Claude, Mistral, Llamaなど）を比較する。特にGPTとClaudeの比較を通して、Claudeの優位性を学び、APIを使った出力方法を習得する。\n'}, {'title': 'シェルとOpen Interpreterの基礎', 'description': 'シェルの基礎（CLI, ファイル操作, シェルスクリプトなど）を学び、Open Interpreterの概要と必要性を理解する。これらのツールを使いこなすことで、書籍作成プロセスを効率化する。\n'}]}, {'week': 3, 'topics': ['Githubを用いたバージョン管理と共同開発', 'Cursorを用いたClaudeによる書籍作成実践'], 'lectures': [{'title': 'Githubの基本とAIモデルのバージョン管理', 'description': 'Githubの基本（リポジトリ, ブランチ, プルリクエストなど）を学び、AIモデルのバージョン管理方法を習得する。チーム開発とコラボレーションを円滑に行い、オープンソース活動に参加する。\n'}, {'title': 'CursorとClaudeを組み合わせた書籍作成', 'description': 'ClaudeのAPIを使った書籍作成方法を学び、Cursorを用いて編集, 構成, フォーマットなどの仕上げを行う。Githubを用いて書籍プロジェクトを管理する方法も習得する。\n'}]}, {'week': 4, 'topics': ['CursorからのGAS開発'], 'lectures': [{'title': 'メーリングリストへの書籍告知', 'description': 'CursorからGASを開発し、メーリングリストに書籍の告知を行う方法を学ぶ。これにより、書籍のプロモーションと販売促進を効果的に行うことができる。\n'}]}]

# Graphvizを使ってグラフを作成。コメントに'Syllabus Graph'を指定。
dot = graphviz.Digraph(comment='Syllabus Graph')

# 週のボックスノードと講義サブボックスの作成
for i, week_data in enumerate(syllabus):
    # 週のインデックスを取得
    week_index = i + 1
    
    # 週のトピックを取得し、カンマ区切りの文字列に変換
    week_topics = ', '.join(week_data['topics'])
    
    # 週のノード名を作成（例: "Week 1\n基礎開発ツール講習"）
    week_node_name = f"Week {week_index}\n{week_topics}"
    
    # 週のノードを作成。ボックス形状、塗りつぶし、水色の背景色を指定。
    dot.node(week_node_name, shape='box', style='filled', fillcolor='lightblue')
    
    # 週ごとのサブグラフを作成
    with dot.subgraph(name=f'cluster_week_{week_index}') as sub:
        # 講義のタイトルをリストアップし、改行区切りの文字列に変換
        lecture_titles = '\n'.join([lecture['title'] for lecture in week_data['lectures']])
        
        # サブグラフ内に講義一覧のノードを作成。ボックス形状、ラベルに講義一覧を指定。
        sub.node(f'lectures_week_{week_index}', shape='box', label=lecture_titles)
        
        # 週のノードと講義一覧のノードを破線で接続
        dot.edge(week_node_name, f'lectures_week_{week_index}', style='dashed', tailport='s', headport='sw')

# 隔週ごとの矢印の接続
for i in range(len(syllabus) - 1):
    # 現在の週のデータを取得
    current_week_data = syllabus[i]
    
    # 次の週のデータを取得
    next_week_data = syllabus[i + 1]
    
    # 現在の週のノード名を作成
    current_week_node_name = f"Week {i + 1}\n{', '.join(current_week_data['topics'])}"
    
    # 次の週のノード名を作成
    next_week_node_name = f"Week {i + 2}\n{', '.join(next_week_data['topics'])}"
    
    # 現在の週のノードと次の週のノードを矢印で接続
    dot.edge(current_week_node_name, next_week_node_name)

# グラフの保存と表示
dot.render('syllabus_graph', view=True)

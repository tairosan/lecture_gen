
from graphviz import Digraph

syllabus = [
    {
        'week': 1, 
        'topics': ['1枚分の文書執筆をAIで自動化しよう'], 
        'lectures': [
            {'title': 'GPTsの基本的な特徴と利用方法について学ぶ。\n', 'description': ''}, 
        ]
    }, 
    {
        'week': 2, 
        'topics': ['文書をAIで修正しよう'], 
        'lectures': [
            {'title': 'Cursorの基本的な操作方法を学ぶ。\n', 'description': ''}, 
        ]
    }, 
    {
        'week': 3, 
        'topics': ['APIで文書執筆を効率化しよう'], 
        'lectures': [
            {'title': 'APIの概要、APIの種類、APIの活用方法を学ぶ。\n', 'description': ''}, 
        ]
    }, 
    {
        'week': 4, 
        'topics': ['AIで書籍を作ろう'], 
        'lectures': [
            {'title': 'CursorとClaudeのAPIを組み合わせて、高品質な書籍を短時間で作成する方法を学ぶ。\n', 'description': ''}, 
        ]
    }, 
    {
        'week': 5, 
        'topics': ['書籍をバージョン管理しよう'], 
        'lectures': [
            {'title': 'Githubの基本的な操作方法を学ぶ。\n', 'description': ''}, 
        ]
    }, 
    {
        'week': 6, 
        'topics': ['メーリングリストへの一斉送信で書籍を売り込もう'], 
        'lectures': [
            {'title': 'CursorとGASを使って、メーリングリストへの一斉送信を行う方法を学ぶ。\n', 'description': ''}, 
        ]
    }
]
g = Digraph('Syllabus Graph', format='png')

for i, week_data in enumerate(syllabus):
    week_index = i + 1
    week_topics = ', '.join(week_data['topics'])
    week_node_name = f"Index {week_index}\n{week_topics}"
    g.node(week_node_name, shape='box', style='filled', fillcolor='lightblue')

    with g.subgraph(name=f'cluster_week_{week_index}') as c:
        lecture_titles = '\n'.join([lecture['title'] for lecture in week_data['lectures']])
        c.node(f'lectures_{week_index}', shape='box', label=lecture_titles)
        g.edge(week_node_name, f'lectures_{week_index}', style='dashed', tailport='s', headport='sw')

for i in range(len(syllabus) - 1):
    current_week = syllabus[i]
    next_week = syllabus[i + 1]
    current_week_node_name = f"Index {i + 1}\n{', '.join(current_week['topics'])}"
    next_week_node_name = f"Index {i + 2}\n{', '.join(next_week['topics'])}"
    g.edge(current_week_node_name, next_week_node_name)

g.render(filename='syllabus_graph', view=True)

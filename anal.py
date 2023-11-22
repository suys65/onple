import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib as mpl


# 한글 폰트 설정
path = 'C:\\Windows\\Fonts\\malgun.ttf' 
font_name = fm.FontProperties(fname=path).get_name()
plt.rc('font', family=font_name)
mpl.rcParams['axes.unicode_minus'] = False  # 마이너스 기호도 올바르게 표시

# 파일 경로 설정
input_pkl_path = 'data\input_data.pkl'
output_pkl_path = 'data\association_rules.pkl'

# input_data.pkl 파일을 불러옴
with open(input_pkl_path, 'rb') as f:
    input_data = pickle.load(f)

input_data = input_data.drop('주문번호', axis=1)  # '주문번호' 열을 삭제
input_data = input_data.fillna(False)  # NaN 값을 False로 채움
input_data = input_data.dropna(how='all')  # 한 행의 모든 값이 NaN일 때 그 행 삭제

# 데이터 프레임은 원핫인코딩 형태여야 함
df = input_data.astype(bool)

# 아이템 집합의 최소 지지도를 0.0001로 설정하고, Apriori 알고리즘을 적용
frequent_itemsets = apriori(df, min_support=0.001, use_colnames=True)

# 신뢰도(confidence)가 0.001 이상인 연관 규칙을 찾음
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.001)

# 향상도(Lift)와 리프트(Leverage) 계산
rules["lift"] = rules["lift"].apply(lambda x : round(x, 2))
rules["leverage"] = rules["leverage"].apply(lambda x : round(x, 2))

rules = rules[rules['leverage'] != 0.00]
rules = rules.sort_values('confidence', ascending=False)

# 전체 거래 횟수 계산
total_transactions = len(df)

# 각 연관 규칙에 대한 구매 횟수를 계산하고, 'joint_purchase_count'라는 새로운 열을 추가
rules['joint_purchase_count'] = round(rules['support'] * total_transactions)

# 결과를 출력
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift', 'leverage', 'joint_purchase_count']])

categories = df.columns

# 'antecedents'로 언급된 카테고리를 추출
antecedents_categories = set(rules['antecedents'].explode().apply(lambda x: list(x)[0]))

# 'antecedents' 카테고리를 'categories'에서 제거
remaining_categories = [category for category in categories if category not in antecedents_categories]
print(remaining_categories)

# Network Graph 그리기
G = nx.DiGraph()

for _, rule in rules.iterrows():
    G.add_edge(list(rule['antecedents'])[0], list(rule['consequents'])[0], 
               weight=rule['confidence'])

# 레이아웃 변경
pos = nx.shell_layout(G)

# 그래프 크기 설정
plt.figure(figsize=(10, 10))

# 노드와 에지의 색깔 변경, 노드의 크기 변경
nx.draw_networkx(G, pos, node_size=500, node_color='skyblue', edge_color='gray', 
                 font_family=font_name, font_size=8, width=[d['weight']*10 for u,v,d in G.edges(data=True)])

# 선 위에 신뢰도를 표시합니다. 신뢰도는 소수점 셋째 자리에서 반올림합니다.
edge_labels = nx.get_edge_attributes(G, 'weight')
edge_labels = {k: '{:.2f}'.format(v) for k, v in edge_labels.items()}

# 각 에지에 대해 신뢰도를 선의 시작지점에 가깝게 표시합니다.
for edge, label in edge_labels.items():
    start, end = pos[edge[0]], pos[edge[1]]
    label_pos = [start[0]*0.8 + end[0]*0.2, start[1]*0.8 + end[1]*0.2]
    plt.text(label_pos[0], label_pos[1], label, va='bottom', ha='right')

plt.show()



# Create empty matrix
matrix = pd.DataFrame(index=categories, columns=categories)

# Fill matrix with confidence values
for _, rule in rules.iterrows():
    antecedent = list(rule['antecedents'])[0]
    consequent = list(rule['consequents'])[0]
    matrix.loc[antecedent, consequent] = rule['confidence']

# NaN 값을 포함하는 모든 행과 열을 삭제합니다.
matrix = matrix.dropna(how='all', axis=1).dropna(how='all', axis=0)

# Draw heatmap
plt.figure(figsize=(10, 10))
sns.heatmap(matrix.fillna(0), cmap='YlGnBu')
plt.show()
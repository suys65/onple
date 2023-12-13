# 필요한 모듈 임포트
import pickle
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# pickle 파일 경로 설정
pkl_path = 'data\input_data.pkl'

# pickle 파일 불러오기
with open(pkl_path, 'rb') as f:
    input = pickle.load(f)

# '주문번호' 열 제거
input = input.drop('주문번호', axis=1)

# 결측값을 False로 채우기
input = input.fillna(False)

# 모든 열이 비어있는 행 제거
input = input.dropna(how='all')

# 데이터프레임 복사 후 타입을 불리언으로 변환
df=input
df = df.astype(bool)

# Apriori 알고리즘을 사용해 빈번한 아이템 집합 찾기 (최소 지지도: 0.00001)
frequent_itemsets = apriori(df, min_support=0.00001, use_colnames=True)

# 연관 규칙 찾기 (최소 지지도: 0.001)
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.001)

# 'confidence' 기준으로 내림차순 정렬
rules = rules.sort_values(by='confidence', ascending=False)

# 연관 규칙 pickle 파일로 저장
pkl_path = 'data\ssociation_rules.pkl'
with open(pkl_path, 'wb') as f:
    pickle.dump(rules, f)

# 결과 출력
print(rules[['antecedents', 'consequents', 'support', 'confidence']])

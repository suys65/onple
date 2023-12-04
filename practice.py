import pickle
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
pkl_path = 'data\input_data.pkl'

with open(pkl_path, 'rb') as f:
    input = pickle.load(f)
input = input.drop('주문번호', axis=1)
#input = input.drop('1+1', axis=1)
input = input.fillna(False)

# 한 행의 모든 값이 nan일 때 그 행 삭제
input = input.dropna(how='all')
#print(input)
# 데이터 프레임은 원핫인코딩 형태여야 합니다.
df=input
df = df.astype(bool)

# 아이템 집합의 최소 지지도를 0.01로 설정하고, Apriori 알고리즘을 적용합니다.
frequent_itemsets = apriori(df, min_support=0.00001, use_colnames=True)

# 신뢰도(confidence)가 0.5 이상인 연관 규칙을 찾습니다.
# rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.2)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.001)
import pickle
import pandas as pd
pkl_path = 'data\ssociation_rules.pkl'  # 여기에 저장하려는 pickle 파일의 경로를 입력하세요
with open(pkl_path, 'wb') as f:
    pickle.dump(rules, f)
# 결과를 출력합니다.
print(rules[['antecedents', 'consequents', 'support', 'confidence']])

import pickle
import pandas as pd
pkl_path = 'data/ssociation_rules.pkl'  # '\\' 대신 '/'를 사용
with open(pkl_path, 'wb') as f:
    pickle.dump(rules, f)
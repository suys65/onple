import pandas as pd

# pickle 파일 로드
df = pd.read_pickle('data\ssociation_rules.pkl')


# DataFrame을 csv 파일로 저장
df.to_csv('data\ssociation_rules.csv', index=False, encoding = 'cp949')

# 필요한 라이브러리 임포트
import pandas as pd
import pickle

# 추천 상품을 찾는 함수 정의
def get_recommendations(item):
    # practice.py에서 만든 연관 규칙 데이터 불러오기
    with open('data\ssociation_rules.pkl', 'rb') as f:
        rules = pd.read_pickle(f)
    
    # 입력된 아이템과 연관된 규칙 찾기
    rules['antecedents_items'] = rules['antecedents'].apply(lambda x: next(iter(x)) if len(x) > 0 else None)
    recommended_category = rules[rules['antecedents_items'] == item]['consequents']

    # 제품 데이터 불러오기
    with open('data\product.pkl', 'rb') as f:
        products = pd.read_pickle(f)

    # 추천 카테고리로 필터링
    recommended_categoryi = recommended_category.apply(lambda x: next(iter(x)) if len(x) > 0 else None)
    category_products = products[products['중 카테고리'] == recommended_categoryi.iloc[0]]
    
    # 카테고리 내에서 주문량이 가장 많은 제품을 추천 상품으로 선택
    recommended_product = category_products.sort_values('주문량', ascending=False).iloc[0]

    # 추천 상품 반환
    return recommended_product


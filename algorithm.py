
import pandas as pd
import pickle

def get_recommendations(item):
    # Load the association rules
    with open('data\ssociation_rules.pkl', 'rb') as f:
        rules = pd.read_pickle(f)
    
    # Find the recommended category
    # 'antecedents' 컬럼의 각 frozenset에서 값 추출
    rules['antecedents_items'] = rules['antecedents'].apply(lambda x: next(iter(x)) if len(x) > 0 else None)

    # 추출한 값으로 비교
    recommended_category = rules[rules['antecedents_items'] == item]['consequents']

    # Load the product data
    with open('data\product.pkl', 'rb') as f:
        products = pd.read_pickle(f)
    recommended_categoryi = recommended_category.apply(lambda x: next(iter(x)) if len(x) > 0 else None)
    print(recommended_categoryi)
    # Filter the products that belong to the recommended category
    category_products = products[products['중 카테고리'] == recommended_categoryi.iloc[0]]
    
    # Find the product with the highest order quantity in the category
    recommended_product = category_products.sort_values('주문량', ascending=False).iloc[0]

    return recommended_product
#print(get_recommendations('인테리어식물'))

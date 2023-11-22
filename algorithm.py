
import pandas as pd
import pickle
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def get_association_rules(df, min_support, min_confidence):
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules.sort_values('confidence', ascending=False)
    return rules

pkl_path = 'data\input_data.pkl'
with open(pkl_path, 'rb') as f:
    input = pickle.load(f)
input = input.drop('주문번호', axis=1)
input = input.fillna(False)
input = input.dropna(how='all')
df = input.astype(bool)

min_supports = [0.01, 0.001, 0.0001]
min_confidence = 0.001

for min_support in min_supports:
    try:
        rules = get_association_rules(df, min_support, min_confidence)
        if len(rules) > 0:
            print(f"Using min_support {min_support}, we have found {len(rules)} rules.")
            print(rules[['antecedents', 'consequents', 'support', 'confidence']])
            with open('data\association_rules.pkl', 'wb') as f:
                pickle.dump(rules, f)
            break
    except:
        print(f"No rules found for min_support {min_support}. Trying next value.")

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

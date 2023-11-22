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

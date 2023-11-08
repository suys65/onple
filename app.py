# # app.py
# from flask import Flask, render_template
# from flask import Flask, request
# from algorithm import get_recommendations
# from flask import Flask, request, render_template
# import pickle

# app = Flask(__name__)


# # Load product data
# import pandas as pd

# with open('C:\onple\onple\data\product.pkl', 'rb') as f:
#     products = pd.read_pickle(f)


# @app.route('/product/<product_id>', methods=['GET'])
# def product_page(product_id):
#     # Find the category of the clicked product
#     product = products[products['product_id'] == product_id]  #상품코드
#     category = product['category'].values[0]      #중 카테고리
    
#     # Get recommendations
#     recommendations = get_recommendations(category)
    
#     # Render the product page with recommendations
#     return render_template('product.html', product=product, recommendations=recommendations)


# @app.route('/')
# def home():
#     return render_template('index.html')
# if __name__ == '__main__':
#     app.run(debug=True)


# # 박정한 추가

# @app.route('/product', methods=['POST'])
# def product_form():
#     product_id = request.form.get('number')
#     return redirect(url_for('product_page', product_id=product_id))

# app.py
from flask import Flask, render_template, request, redirect, url_for
from algorithm import get_recommendations
import pandas as pd
import pickle

app = Flask(__name__)

# Load product data
with open('C:\onple\onple\data\product.pkl', 'rb') as f:
    products = pd.read_pickle(f)
#print(products[products['상품코드'] == "G0001226774"]['중 카테고리'].values[0])

@app.route('/product/<product_id>', methods=['GET'])
def product_page(product_id):
    # Check if the product_id exists in the data
    if product_id not in products['상품코드'].values:
        return "The product does not exist.", 404

    # Find the category of the clicked product
    product = products[products['상품코드'] == product_id]  #상품코드
    category = product['중 카테고리'].values[0]      #중 카테고리
    
    # Get recommendations
    recommendations = get_recommendations(category)
    
    # Render the product page with recommendations
    return render_template('product.html', product=product, recommendations=recommendations)

@app.route('/product', methods=['POST'])
def product_form():
    product_id = request.form.get('number')

    # Check if the product_id exists in the data
    if product_id not in products['상품코드'].values:
        return "The product does not exist.", 404

    return redirect(url_for('product_page', product_id=product_id))

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
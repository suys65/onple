
# app.py
from flask import Flask, render_template, request, redirect, url_for
from algorithm import get_recommendations
import pandas as pd
import pickle
from flask import Flask, send_from_directory

app = Flask(__name__, static_url_path='')

# Load product data
with open('data\product.pkl', 'rb') as f:
    products = pd.read_pickle(f)

# 상품 추천하는 라우터
@app.route('/product/<product_id>', methods=['GET'])
def product_page(product_id):
    # Check if the product_id exists in the data
    if product_id not in products['상품코드'].values:
        return "The product does not exist.", 404

    # Find the category of the clicked product
    product = products[products['상품코드'] == product_id]  #상품코드
    category = product['중 카테고리'].values[0]      #중 카테고리
    print(product['중 카테고리'])
    # Get recommendations
    recommendations = get_recommendations(category)
    #print(recommendations)
    return render_template('product.html', product=product, recommendations=recommendations) # 추천 상품 데이터프레임의 첫 번째 행을 전달합니다.

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    # 상품 DataFrame을 불러옵니다.
    products = pd.read_pickle('data\product.pkl')
    products.rename(columns={'상품코드': 'product_code', '상품명': 'product_name'}, inplace=True)

    # DataFrame에서 랜덤으로 상품을 선택합니다.
    selected_products = products.sample(1)

    # selected_products를 HTML 파일에 전달하여 렌더링합니다.
    # 각 행을 사전 형태로 변환합니다.
    return render_template('cart.html', products=selected_products.to_dict('records'))
    # 장바구니 페이지를 렌더링합니다.

# 장바구니 - 상품 추천하는 라우터
@app.route('/cart/buy/<product_id>', methods=['GET'])
def cart_buy(product_id):
    # Check if the product_id exists in the data
    if product_id not in products['상품코드'].values:
        return "The product does not exist.", 404

    # Find the category of the clicked product
    product = products[products['상품코드'] == product_id]  #상품코드
    category = product['중 카테고리'].values[0]      #중 카테고리
    print(product['중 카테고리'])
    # Get recommendations
    recommendations = get_recommendations(category)
    #print(recommendations)
    return render_template('product.html', product=product, recommendations=recommendations) # 추천 상품 데이터프레임의 첫 번째 행을 전달합니다.

@app.route('/cart/buy', methods=['POST'])
def buy_form():
    product_id = request.form.get('product_code')  # 'product_code'를 통해 상품 코드를 받습니다.

    # Check if the product_id exists in the data
    if product_id not in products['상품코드'].values:
        return "The product does not exist.", 404

    return redirect(url_for('product_page', product_id=product_id))

#페이지 넘어가는 라우터 
@app.route('/product', methods=['POST'])
def product_form():
    product_id = request.form.get('product_code')  # 'product_code'를 통해 상품 코드를 받습니다.

    # Check if the product_id exists in the data
    if product_id not in products['상품코드'].values:
        return "The product does not exist.", 404

    return redirect(url_for('product_page', product_id=product_id))


@app.route('/', methods=['GET', 'POST'])
def home():
    # 상품 DataFrame을 불러옵니다.
    products = pd.read_pickle('data\product.pkl')
    products.rename(columns={'상품코드': 'product_code', '상품명': 'product_name'}, inplace=True)

    # DataFrame에서 랜덤으로 상품을 선택합니다.
    selected_products = products.sample(10)

    # selected_products를 HTML 파일에 전달하여 렌더링합니다.
    # 각 행을 사전 형태로 변환합니다.
    return render_template('index.html', products=selected_products.to_dict('records'))

@app.route('/templates/image/<path:path>')
def send_image(path):
    return send_from_directory('templates/image', path)


if __name__ == "__main__":
    app.run()

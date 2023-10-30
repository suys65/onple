# app.py
from flask import Flask, render_template
from flask import Flask, request
from algorithm import factorial

app = Flask(__name__)

@app.route('/factorial', methods=['GET'])   #라우터 만들기
def get_factorial():
    number = int(request.args.get('number'))
    result = factorial(number)
    return {'result': result}    # 반환 부분


@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
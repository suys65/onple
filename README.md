# onple 코드 사용법

## 필요한 라이브러리 다운
다운 방법: ctrl + `을 눌러 TERMINAL을 연 후, pip install (라이브러리명)을 입력한다.(vscode 하단에 terminal에서 'pip install (라이브러리명)' 라고 입력)

- pandas
- pickle
- mlxtend
- flask

ex) pip install pandas

## 핵심 파일
자세한 코드 설명은 각 파일에 주석으로 설명한다

### app.py : 실행 파일
코드를 실행시킬때 app.py 화면에서 오른쪽 위 삼각형( 실행버튼 ) 클릭

### practice.py : 연관규칙 결과 생성 파일 **가장 중요
1. 연관규칙 함수의 'INPUT'으로 input_data.pkl을 사용함
2. 연관규칙 함수를 적용
3. 연관규칙 함수의 결과를 ssociation_rules.pkl에 저장

### algorithm.py : 연관규칙 적용하는 함수 생성 파일
아이템 입력 -> 추천 상품 출력  
1. 아이템 입력
2. 입력된 아이템의 카테고리가 무엇인지 찾기
3. 그 카테고리와 가장 연관성이 높은 카테고리를 연관규칙 결과(ssociation_rules.pkl)를 통해 찾기  
4. 추천된 카테고리 내에서 가장 인기가 많은 상품을 추천


## 데이터 설명
코드의 편의성(속도)을 위하여 엑셀 파일을 그대로 사용하지 않고 pkl을 사용하였음.  
(Vscode에서 바로 못열어보지 못하지만, data 폴더 -> 엑셀파일 에 들어가면 동일한 이름의 열어볼 수 있는 엑셀 파일로 존재함)


### input_data.pkl
연관규칙 함수에 input으로 들어가는 파일 - 이 형식을 꼭 지켜야 한다.  
각 행은 주문 1건에 해당하고 각 열은 카테고리임. 각 셀에는 0 또는 1이 기입되어 있으며, 주문한 상품의 카테고리는 1이 적혀있는 열의 이름이다. (2개의 상품을 주문하였을 때, 행에는 2개의 1이 존재. 나머지는 0이 적혀있음.)

### product.pkl
상품 목록 파일  
알고리즘 구현에서 상품에 대한 정보를 찾기 위한 데이터로 onple에서 판매하는 제품들의 정보가 적혀 있음.  
데이터 구축 단계에서 사용되며, 연관규칙 함수에서는 쓰이지 않음.

### ssociation_rules.pkl
연관규칙 결과를 저장할 파일  
연관규칙 결과의 형식은 보고서에 나와 있다.
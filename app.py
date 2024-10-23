from flask import Flask, render_template
from sympy import symbols, pretty, simplify
from test import generate_valid_expression, find_min_steps  # Import các hàm đã viết

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Định nghĩa các biến logic
p, q, r = symbols('p q r')

# Trang chính
@app.route('/')
def home():
    return render_template('index.html')  # Template HTML chính

# Tạo câu hỏi ngẫu nhiên và hiển thị luôn đáp án
@app.route('/generate_question', methods=['POST'])
def generate_question():
    # Tạo biểu thức ngẫu nhiên
    expr = generate_valid_expression([p, q, r], 3)
    expr_pretty = pretty(expr)
    
    # Rút gọn biểu thức và các bước đơn giản hóa
    simplified_expr = simplify(expr)
    result_steps = find_min_steps(expr)
    
    expr_kq = pretty(simplified_expr)

    # Trả về kết quả và các bước
    return render_template(
        'index.html', 
        expr=expr_pretty,         # Hiển thị biểu thức ban đầu
        ketqua=expr_kq,           # Hiển thị kết quả rút gọn
        steps=result_steps        # Hiển thị các bước đơn giản hóa
    )

if __name__ == '__main__':
    app.run(debug=True)

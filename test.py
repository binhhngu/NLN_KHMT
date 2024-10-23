from sympy import symbols, And, Or, Not, Implies, simplify, satisfiable, pretty, latex
import random

# Tạo các biến
p, q, r = symbols('p q r')

# Định nghĩa các quy tắc logic cơ bản
def apply_implication_rule(expr):
    """
    Áp dụng quy tắc khử suy diễn (implies) từ trong ra ngoài:
    P → Q tương đương với ¬P ∨ Q.
    """
    # Trước hết xử lý đệ quy các phần tử con (nếu có)
    if expr.args:
        new_args = [apply_implication_rule(arg) for arg in expr.args]
        expr = expr.func(*new_args)

    # Sau đó, nếu biểu thức là một phép suy diễn, áp dụng quy tắc
    if isinstance(expr, Implies):
        P, Q = expr.args
        return Or(Not(P), Q)

    # Trả về biểu thức sau khi áp dụng quy tắc
    return expr


def apply_demorgan(expr):
    if isinstance(expr, Not):
        if isinstance(expr.args[0], And):
            return Or(*[Not(arg) for arg in expr.args[0].args])
        elif isinstance(expr.args[0], Or):
            return And(*[Not(arg) for arg in expr.args[0].args])
    if expr.args:
        new_args = [apply_demorgan(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_double_negation(expr):
    if isinstance(expr, Not) and isinstance(expr.args[0], Not):
        return expr.args[0].args[0]
    if expr.args:
        new_args = [apply_double_negation(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_distributive(expr):
    """
    Áp dụng quy tắc phân phối để đơn giản hóa biểu thức logic.
    """
    if isinstance(expr, And) or isinstance(expr, Or):
        operands = expr.args
        if len(operands) > 1:
            result = None
            for i in range(len(operands)):
                for j in range(i+1, len(operands)):
                    if isinstance(expr, And):
                        temp_result = Or(And(operands[i], operands[j]), And(operands[j], operands[i]))
                    else:
                        temp_result = And(Or(operands[i], operands[j]), Or(operands[j], operands[i]))
                    temp_result = simplify(temp_result)
                    
                    if result is None:
                        result = temp_result
                    else:
                        result = Or(result, temp_result) if isinstance(expr, Or) else And(result, temp_result)
            return result
    return expr

def handle_nested_implications(expr):
    """
    Xử lý các biểu thức chứa nhiều mũi tên (implies), xử lý từ trong ra ngoài.
    """
    if isinstance(expr, Implies):
        P, Q = expr.args
        return apply_implication_rule(Implies(handle_nested_implications(P), handle_nested_implications(Q)))
    
    if isinstance(expr, And) or isinstance(expr, Or):
        new_args = [handle_nested_implications(arg) for arg in expr.args]
        return expr.func(*new_args)
    
    return expr

def apply_absorption(expr):
    if isinstance(expr, And):
        # Kiểm tra luật hấp thụ dạng A ∧ (A ∨ B) = A
        for arg in expr.args:
            if isinstance(arg, Or):
                for or_arg in arg.args:
                    if or_arg in expr.args:
                        return And(*(a for a in expr.args if a != arg))  # Loại bỏ phần dư thừa
    elif isinstance(expr, Or):
        # Kiểm tra luật hấp thụ dạng A ∨ (A ∧ B) = A
        for arg in expr.args:
            if isinstance(arg, And):
                for and_arg in arg.args:
                    if and_arg in expr.args:
                        return Or(*(a for a in expr.args if a != arg))  # Loại bỏ phần dư thừa
    if expr.args:
        new_args = [apply_absorption(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr


def apply_dominance(expr):
    if isinstance(expr, Or):
        if any(arg == True for arg in expr.args):
            return True
        if any(arg == False for arg in expr.args):
            return Or(*(arg for arg in expr.args if arg != False))
    elif isinstance(expr, And):
        if any(arg == False for arg in expr.args):
            return False
        if any(arg == True for arg in expr.args):
            return And(*(arg for arg in expr.args if arg != True))
    if expr.args:
        new_args = [apply_dominance(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_identity(expr):
    if isinstance(expr, Or):
        if any(arg == False for arg in expr.args):
            return Or(*(arg for arg in expr.args if arg != False))
    elif isinstance(expr, And):
        if any(arg == True for arg in expr.args):
            return And(*(arg for arg in expr.args if arg != True))
    if expr.args:
        new_args = [apply_identity(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_commutativity(expr):
    if isinstance(expr, And) or isinstance(expr, Or):
        new_args = sorted(expr.args, key=lambda x: str(x))
        return expr.func(*new_args)
    if expr.args:
        new_args = [apply_commutativity(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_complementarity(expr):
    # Xử lý luật phần tử bù
    if isinstance(expr, Or):
        if any(Not(arg) in expr.args for arg in expr.args):
            return True  # p ∨ ¬p → True
    elif isinstance(expr, And):
        if any(Not(arg) in expr.args for arg in expr.args):
            return False  # p ∧ ¬p → False
    if expr.args:
        new_args = [apply_complementarity(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_associativity(expr):
    if isinstance(expr, And):
        if isinstance(expr.args[0], And):
            return And(*(expr.args[0].args + expr.args[1:]))
        elif isinstance(expr.args[1], And):
            return And(*(expr.args[:1] + expr.args[1].args))
    elif isinstance(expr, Or):
        if isinstance(expr.args[0], Or):
            return Or(*(expr.args[0].args + expr.args[1:]))
        elif isinstance(expr.args[1], Or):
            return Or(*(expr.args[:1] + expr.args[1].args))
    if expr.args:
        new_args = [apply_associativity(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_nullification(expr):
    if isinstance(expr, And):
        if any(arg == True for arg in expr.args):
            return And(*(arg for arg in expr.args if arg != True))
        if any(arg == False for arg in expr.args):
            return False
    elif isinstance(expr, Or):
        if any(arg == False for arg in expr.args):
            return Or(*(arg for arg in expr.args if arg != False))
        if any(arg == True for arg in expr.args):
            return True
    if expr.args:
        new_args = [apply_nullification(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def apply_termination(expr):
    if isinstance(expr, Or):
        if any(arg == True for arg in expr.args):
            return True
    elif isinstance(expr, And):
        if any(arg == False for arg in expr.args):
            return False
    return expr

def apply_all_rules(expr):
    rules = [
        apply_implication_rule, 
        apply_demorgan, 
        apply_double_negation, 
        apply_absorption, 
        apply_dominance, 
        apply_identity, 
        apply_commutativity, 
        apply_associativity, 
        apply_distributive,
        apply_nullification,
        apply_complementarity
    ]
    new_expr = expr
    applied = False
    for rule in rules:
        temp_expr = rule(new_expr)
        if temp_expr != new_expr:
            print(f"Áp dụng quy tắc {rule.__name__}: {pretty(temp_expr)}")
            new_expr = temp_expr
            applied = True
    if not applied:
        print(f"Không áp dụng quy tắc nào.")
    return new_expr, applied

def expand_and_simplify(expr):
    if isinstance(expr, Or) or isinstance(expr, And):
        new_args = [expand_and_simplify(arg) for arg in expr.args]
        return expr.func(*new_args)
    return expr

def find_min_steps(expr, max_iterations=100):
    simplified_expr = simplify(expr)  # Simplify once at the start
    current_expr = expr

    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}")
        print("Biểu thức hiện tại:", pretty(current_expr))

        # Xử lý suy diễn nhiều cấp trước
        current_expr = handle_nested_implications(current_expr)
        
        # Áp dụng tất cả các quy tắc
        new_expr, applied = apply_all_rules(current_expr)

        # Phá ngoặc và rút gọn biểu thức
        new_expr = expand_and_simplify(new_expr)

        # Kiểm tra và áp dụng các quy tắc thêm
        new_expr = apply_nullification(new_expr)
        new_expr = apply_identity(new_expr)
        new_expr = apply_commutativity(new_expr)
        new_expr = apply_associativity(new_expr)
        new_expr = apply_termination(new_expr)

        # print("Biểu thức sau khi áp dụng quy tắc:")
        print(pretty(new_expr))

        # So sánh với biểu thức đã rút gọn bằng simplify
        if not applied:
            print("Không áp dụng quy tắc nào.")
            print("Biểu thức sau khi simplify:")
            print(pretty(simplified_expr))
            return

        if new_expr == simplified_expr:
            print("Kết quả đúng với simplify! Biểu thức sau khi rút gọn:")
            print(pretty(new_expr))
            print("\nBiểu thức rút gọn bằng simplify:")
            print(pretty(simplified_expr))
            return

        current_expr = new_expr

    print("Không tìm được đáp án.")

# def find_min_steps(expr, max_iterations=100):
#     simplified_expr = simplify(expr)  # Simplify once at the start
#     current_expr = expr
#     steps = []  # Danh sách lưu trữ các bước

#     for iteration in range(max_iterations):
#         # Xử lý suy diễn nhiều cấp trước
#         current_expr = handle_nested_implications(current_expr)
        
#         # Áp dụng tất cả các quy tắc
#         new_expr, applied = apply_all_rules(current_expr)

#         # Phá ngoặc và rút gọn biểu thức
#         new_expr = expand_and_simplify(new_expr)

#         # Kiểm tra và áp dụng các quy tắc thêm
#         new_expr = apply_nullification(new_expr)
#         new_expr = apply_identity(new_expr)
#         new_expr = apply_commutativity(new_expr)
#         new_expr = apply_associativity(new_expr)
#         new_expr = apply_termination(new_expr)

#         # Lưu trữ bước rút gọn
#         steps.append(pretty(new_expr))

#         if not applied or new_expr == simplified_expr:
#             steps.append("=>")  # Dấu hiệu kết thúc chuỗi các bước
#             steps.append(pretty(simplified_expr))  # Thêm biểu thức rút gọn cuối cùng
#             return steps  # Trả về các bước sau khi rút gọn

#         current_expr = new_expr

#     print("Không tìm được đáp án.")
#     return steps  # Trả về các bước rút gọn (nếu có)




def generate_random_expression(variables, depth):
    if depth == 0:
        return random.choice(variables)
    operators = [And, Or, Not, Implies]
    operator = random.choice(operators)
    if operator == Not:
        return Not(generate_random_expression(variables, depth - 1))
    else:
        return operator(
            generate_random_expression(variables, depth - 1),
            generate_random_expression(variables, depth - 1)
        )

def generate_valid_expression(variables, depth, max_attempts=100):
    for _ in range(max_attempts):
        expr = generate_random_expression(variables, depth)
        simplified_expr = simplify(expr)
        if simplified_expr != True and simplified_expr != False:
            if expr != simplified_expr:
                return expr
    raise ValueError("Không thể tạo biểu thức hợp lệ trong số lần thử cho phép.")

# Tạo biểu thức ngẫu nhiên hợp lệ
try:
    expr = generate_valid_expression([p, q, r], 4)
    print("Biểu thức ngẫu nhiên:", pretty(expr))
    print("Biểu thức ngẫu nhiên:", latex(expr))
    print("Biểu thức ngẫu nhiên:", expr)
    if satisfiable(expr):
        print("Biểu thức là khả thi (có thể đúng)")
    else:
        print("Biểu thức không khả thi (luôn sai)")

    find_min_steps(expr)
except ValueError as e:
    print(e)

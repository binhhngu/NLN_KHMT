import random
from sympy import gcd, isprime, totient

# Tạo đề thi
def create_modular_question():
    a = random.randint(2, 10)  # Chọn số cơ bản a
    b = random.randint(10, 500)  # Chọn số mũ b
    while True:
        m = random.randint(5, 20)  # Chọn số m là số nguyên tố
        if isprime(m):  # Đảm bảo m là số nguyên tố
            break
    return a, b, m

# Tính toán đáp án sử dụng định lý Euler với các bước chi tiết
def solve_modular_question(a, b, m):
    if gcd(a, m) == 1:  # Kiểm tra điều kiện áp dụng định lý Euler
        print(f"Vì ({a},{m}) = 1 nên áp dụng định lý Euler.")
        
        # Tính φ(m)
        phi_m = int(totient(m))
        print(f"Vì {m} là số nguyên tố nên φ({m}) = {phi_m}.")
        
        # Sử dụng định lý Euler: a^phi(m) ≡ 1 (mod m)
        print(f"Theo định lý Euler: {a}^{phi_m} ≡ 1 (mod {m}).")
        
        # Tính b mod phi(m)
        b_mod_phi_m = b % phi_m
        print(f"Do đó: {a}^{b} ≡ {a}^{phi_m}×{b//phi_m}+{b_mod_phi_m} (mod {m}).")
        
        # Tính a^b_mod_phi_m mod m
        result = pow(a, b_mod_phi_m, m)
        print(f"Vì {a}^{b_mod_phi_m} ≡ {result} (mod {m}), nên số dư của {a}^{b} chia cho {m} là {result}.")
        
        return result
    else:
        print(f"({a},{m}) ≠ 1 nên không thể áp dụng định lý Euler.")
        return None

# Tạo đề thi và đáp án
a, b, m = create_modular_question()
print(f"Đề bài: Tìm số dư khi chia {a}^{b} cho {m}")
answer = solve_modular_question(a, b, m)

import random
from sympy import symbols, Eq, gcd, diophantine

# Hàm tạo phương trình Diophantine ngẫu nhiên
def tao_phuong_trinh(so_an=2):
    if so_an == 2:
        # Tạo phương trình dạng ax + by = c với hệ số ngẫu nhiên
        a, b, c = random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)
        x, y = symbols('x y')
        pt = Eq(a*x + b*y, c)
        return pt, (x, y)
    
    elif so_an == 3:
        # Tạo phương trình dạng ax + by + cz = d với hệ số ngẫu nhiên
        a, b, c, d = random.randint(1, 20), random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)
        x, y, z = symbols('x y z')
        pt = Eq(a*x + b*y + c*z, d)
        return pt, (x, y, z)

# Hàm giải phương trình Diophantine
def giai_phuong_trinh(pt, bien):
    # Kiểm tra nếu phương trình có 2 hoặc 3 ẩn
    if len(bien) == 2:
        a, b = pt.lhs.as_coefficients_dict()[bien[0]], pt.lhs.as_coefficients_dict()[bien[1]]
        d = gcd(a, b)
        c = pt.rhs
        if c % d != 0:
            return "Phương trình vô nghiệm"
        else:
            nghiem = list(diophantine(pt))
            nghiem_rieng = nghiem[0]
            x_rieng, y_rieng = nghiem_rieng
            nghiem_tong_quat_x = x_rieng + (b//d) * symbols('t')
            nghiem_tong_quat_y = y_rieng - (a//d) * symbols('t')
            return f"Một nghiệm riêng là: ({x_rieng}, {y_rieng}), nghiệm tổng quát: x = {nghiem_tong_quat_x}, y = {nghiem_tong_quat_y}"

    elif len(bien) == 3:
        # Giải phương trình 3 ẩn
        nghiem = list(diophantine(pt))
        if not nghiem:
            return "Phương trình vô nghiệm"
        return f"Nghiệm: {nghiem}"

# Chạy chương trình tạo phương trình với 2 hoặc 3 ẩn
so_an = random.choice([2, 3])
pt, bien = tao_phuong_trinh(so_an)
loi_giai = giai_phuong_trinh(pt, bien)

# In bài toán và lời giải
print("Bài toán:", pt)
print("Lời giải:", loi_giai)

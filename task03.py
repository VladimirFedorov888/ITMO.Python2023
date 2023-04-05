import math

def get_input_values():
    d1 = 8
    d2 = 10
    h = 50
    vsand = 5
    n = 2
    return (d1, d2, h, vsand, n)

def to_radians(degrees):
    return degrees * (math.pi / 180)

def calculate_time(d1, d2, h, vsand, n, theta1):
    theta1_rad = to_radians(theta1)
    d1 = d1 * 3  # переводим ярды в футы
    h = h * 3  # переводим ярды в футы
    vsand = vsand * 5280 / 3600  # переводим мили в час в футы в секунду
    x = d1 * math.tan(theta1_rad)
    L1 = math.sqrt(x ** 2 + d1 ** 2)
    L2 = math.sqrt((h - x) ** 2 + d2 ** 2)
    t = (L1 + n * L2) / vsand
    return t

def find_optimal_angle(d1, d2, h, vsand, n):
    min_time = float('inf')
    optimal_angle = 0
    for angle in range(1, 90):  # Проверяем углы от 1 до 89 градусов
        time = calculate_time(d1, d2, h, vsand, n, angle)
        if time < min_time:
            min_time = time
            optimal_angle = angle
    return optimal_angle, min_time

def main(d1, d2, h, vsand, n):
    optimal_angle, min_time = find_optimal_angle(d1, d2, h, vsand, n)
    print(f"Спасателю потребуется {min_time:.1f} секунд, чтобы добраться до утопающего при угле {optimal_angle} градусов.")

if __name__ == "__main__":
    input_values = get_input_values()
    main(*input_values)
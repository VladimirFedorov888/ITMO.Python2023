import math


def get_input_values():
    d1 = float(input("Введите кратчайшее расстояние от спасателя до кромки воды, d1 (в ярдах): "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега, d2 (в футах): "))
    h = float(input("Введите боковое смещение между спасателем и утопающим, h (в ярдах): "))
    vsand = float(input("Введите скорость движения спасателя по песку, vsand (в милях в час): "))
    n = float(input("Введите коэффициент замедления спасателя при движении в воде, n: "))
    theta1 = float(input("Введите направление движения спасателя по песку, θ1 (в градусах): "))
    return (d1, d2, h, vsand, n, theta1)


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


def main(d1, d2, h, vsand, n, theta1):
    time = calculate_time(d1, d2, h, vsand, n, theta1)
    print(f"Спасателю потребуется {time:.1f} секунд, чтобы добраться до утопающего при угле {theta1:.0f} градусов.")


if __name__ == "__main__":
    main(8, 10, 50, 5, 2, 39.413)
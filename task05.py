import argparse
from typing import Tuple
from PIL import Image, ImageDraw
# Функция для чтения начальной конфигурации поля из входного файла
def parse_input_file(file_path: str) -> Tuple[int, int, list]:
    with open(file_path, 'r') as f:
        lines = f.readlines()
    rows, cols = map(int, lines[0].strip().split())
    grid = [list(map(int, line.strip().split())) for line in lines[1:]]
    return rows, cols, grid
# Функция для генерации RGB-цвета на основе заданного "чистого цвета"
def generate_color(base_color: str, age: int) -> Tuple[int, int, int]:
    base_color_map = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
    }
    base_color_rgb = base_color_map.get(base_color.lower(), (255, 255, 255))
    factor = 1 - min(age / 10, 1)
    color = tuple(int(channel * factor) for channel in base_color_rgb)
    return color
# Функция для подсчёта количества соседей у клетки с координатами (x, y)
def count_neighbors(grid: list, x: int, y: int) -> int:
    rows, cols = len(grid), len(grid[0])
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= x + i < rows and 0 <= y + j < cols:
                neighbors += grid[x + i][y + j]
    return neighbors
# Функция для получения следующего поколения сетки на основе текущей сетки
def next_generation(grid: list, ages: list) -> Tuple[list, list]:
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    new_ages = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j)
            if grid[i][j] == 1:
                if 2 <= neighbors <= 3:
                    new_grid[i][j] = 1
                    new_ages[i][j] = ages[i][j] + 1
            elif neighbors == 3:
                new_grid[i][j] = 1
                new_ages[i][j] = 1
    return new_grid, new_ages
# Функция для создания и сохранения изображения сетки в формате PNG
def create_image(grid: list, ages: list, base_color: str, image_path: str) -> None:
    rows, cols = len(grid), len(grid[0])
    cell_size = 10
    img = Image.new('RGB', (cols * cell_size, rows * cell_size))
    draw = ImageDraw.Draw(img)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                color = generate_color(base_color, ages[i][j])
                draw.rectangle([(j * cell_size, i * cell_size), ((j + 1) * cell_size - 1, (i + 1) * cell_size - 1)], fill=color)
    img.save(image_path)

# Функция для сохранения текущей конфигурации сетки в файл
def save_configuration_to_file(grid: list, file_path: str) -> None:
    rows, cols = len(grid), len(grid[0])
    with open(file_path, 'w') as f:
        f.write(f"{rows} {cols}\n")
        for row in grid:
            f.write(" ".join(str(cell) for cell in row) + "\n")
# Основная функция для выполнения игры "Жизнь"

def main(args: argparse.Namespace) -> None:
    rows, cols, grid = parse_input_file(args.input_file)
    base_color = args.base_color
    ages = [[0 for _ in range(cols)] for _ in range(rows)]

    for step in range(args.steps):
        grid, ages = next_generation(grid, ages)
        image_name = f"generation_{step + 1}.png"
        create_image(grid, ages, base_color, image_name)
        config_name = f"config_{step + 1}.txt"
        save_configuration_to_file(grid, config_name)

# Обработка аргументов командной строки и вызов основной функции пример: python task05.py input.txt 5 blue
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Игра Жизнь")
    parser.add_argument("input_file", help="Имя и путь файла")
    parser.add_argument("steps", type=int, help="Сколько шагов симуляции будет сделано")
    parser.add_argument("base_color", help="базовый цвет")
    args = parser.parse_args()
    main(args)
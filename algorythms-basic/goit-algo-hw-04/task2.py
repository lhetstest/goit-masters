import math
import matplotlib.pyplot as plt

def koch_segment(x1, y1, x2, y2, level, x_points, y_points):
    """
    Рекурсивно генерує точки фракталу сніжинка Коха.
    Додає координати у списки x_points, y_points.
    """
    if level == 0:
        x_points.append(x1)
        y_points.append(y1)
        # Кінцева точка додається на наступному сегменті або після завершення
    else:
        dx = (x2 - x1) / 3
        dy = (y2 - y1) / 3

        xA, yA = x1, y1
        xB, yB = x1 + dx, y1 + dy

        angle = math.atan2(y2 - y1, x2 - x1) - math.pi / 3
        length = math.sqrt(dx*dx + dy*dy)
        xC = xB + length * math.cos(angle)
        yC = yB + length * math.sin(angle)

        xD, yD = x1 + 2 * dx, y1 + 2 * dy
        xE, yE = x2, y2

        koch_segment(xA, yA, xB, yB, level - 1, x_points, y_points)
        koch_segment(xB, yB, xC, yC, level - 1, x_points, y_points)
        koch_segment(xC, yC, xD, yD, level - 1, x_points, y_points)
        koch_segment(xD, yD, xE, yE, level - 1, x_points, y_points)

def koch_snowflake(level):
    height = math.sqrt(3) / 2
    p1 = (0, 0)
    p2 = (1, 0)
    p3 = (0.5, height)

    x_points = []
    y_points = []

    koch_segment(*p1, *p2, level, x_points, y_points)
    koch_segment(*p2, *p3, level, x_points, y_points)
    koch_segment(*p3, *p1, level, x_points, y_points)
    # Додаємо останню точку, щоб замкнути фігуру
    x_points.append(p1[0])
    y_points.append(p1[1])

    plt.figure(figsize=(8, 8))
    plt.plot(x_points, y_points, 'b-')
    plt.axis('equal')
    plt.axis('off')
    plt.title(f"Сніжинка Коха, рівень рекурсії: {level}")
    plt.show()

if __name__ == "__main__":
    level = int(input("Введіть рівень рекурсії (наприклад, 0-5): "))
    koch_snowflake(level)

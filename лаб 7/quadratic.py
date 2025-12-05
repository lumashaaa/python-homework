import math
from logger_decorator import logger

@logger()
def solve_quadratic(a, b, c):
    """пример решения квадратного уравнения"""

    if not isinstance(a, (int, float)):
        raise TypeError("Коэффициент a должен быть числом")

    if a == 0 and b == 0:
        raise Exception("CRITICAL: нельзя решить уравнение без коэффициентов")

    D = b * b - 4 * a * c

    if D < 0:
        print("WARNING: дискриминант < 0 => корней нет")
        return None

    if D == 0:
        return -b / (2 * a)

    x1 = (-b + math.sqrt(D)) / (2 * a)
    x2 = (-b - math.sqrt(D)) / (2 * a)
    return x1, x2
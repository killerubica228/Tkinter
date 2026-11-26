# Задание 6. Проверка списка
#
# Найденные ошибки:
#   1) знак сравнения был перепутан: «number < maximum» ищет минимум;
#      нужно «number > maximum»;
#   2) начальное значение maximum = 0 ломает программу для списка из
#      отрицательных чисел (максимум оказался бы 0, которого в списке нет).
#      Исправление: начинать с первого элемента списка.


def find_max(numbers):
    if not numbers:
        raise ValueError("Список пуст: максимума нет.")
    maximum = numbers[0]
    for number in numbers:
        if number > maximum:
            maximum = number
    return maximum


numbers = [5, 12, 3, 21, 8]
print("Максимальное число:", find_max(numbers))        # 21

print("\nДополнительные проверки:")
tests = [([5, 12, 3, 21, 8], 21), ([-5, -12, -3, -21, -8], -3),
         ([7], 7), ([-1, 0, -2], 0), ([3, 3, 3], 3)]
for data, expected in tests:
    result = find_max(data)
    status = "OK" if result == expected else "ОШИБКА"
    print(f"  {data} -> {result} (ожидалось {expected}) {status}")

try:
    find_max([])
except ValueError as e:
    print("  [] ->", e)

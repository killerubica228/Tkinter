# Задание 5. Тестирование функции
#
# Найденные ошибки:
#   1) в условии стоял один знак «=» (присваивание), а нужно «==» (сравнение);
#      из-за этого была синтаксическая ошибка;
#   2) логика была перевёрнута: при остатке 0 возвращалось «Нечётное».


def check_even(number):
    if number % 2 == 0:
        return "Чётное"
    else:
        return "Нечётное"


print(check_even(8))

print("\nТестирование:")
tests = [(8, "Чётное"), (7, "Нечётное"), (0, "Чётное"), (-4, "Чётное"), (-9, "Нечётное")]
for value, expected in tests:
    result = check_even(value)
    status = "OK" if result == expected else "ОШИБКА"
    print(f"  check_even({value}) = {result} -> {status}")

def decline_word(count: int, word: str):
    rubles = ['рублей', 'рубля', 'рубль']
    years = ['лет', 'года', 'год']

    current_word = rubles if word == 'рубли' else years

    remainderHundred = count % 100
    remainderTen = count % 10
    if remainderTen == 0 or 5 <= remainderTen <= 9 or 11 <= remainderHundred <= 19:
        return current_word[0]
    elif 2 <= remainderTen <= 4:
        return current_word[1]
    else:
        return current_word[2]


def is_correct_input(user_input: str, input_type: str) -> bool:
    if user_input == "" or input_type == "":
        return False
    elif input_type == 'bool':
        if user_input in ['да', 'нет']:
            return True
        else:
            return False
    elif input_type == 'int':
        if user_input.isdigit():
            return True
        else:
            return False
    else:
        return True


to_ask = ["Введите название вакансии: ",
          "Введите описание вакансии: ",
          "Введите требуемый опыт работы (лет): ",
          "Введите нижнюю границу оклада вакансии: ",
          "Введите верхнюю границу оклада вакансии: ",
          "Есть ли свободный график (да / нет): ",
          "Является ли данная вакансия премиум-вакансией (да / нет): "]

user_inputs = []
i = 0
while i < len(to_ask):
    t = input(to_ask[i])
    if (is_correct_input(t, 'string') and i < 2) or (is_correct_input(t, 'bool') and 5 <= i <= 7):
        user_inputs.append(t)
        i += 1
    elif is_correct_input(t, 'int') and 2 <= i <= 4:
        user_inputs.append(int(t))
        i += 1
    else:
        print("Данные некорректны, повторите ввод")

user_inputs[3] = (user_inputs[3] + user_inputs.pop(4)) // 2  # Подсчёт среднего оклада

titles = ["", "Описание: ", "Требуемый опыт работы: ",
          "Средний оклад: ", "Свободный график: ", "Премиум-вакансия: "]

for user_input, title in zip(user_inputs, titles):
    if title in ["", "Описание: ", "Свободный график: ", "Премиум-вакансия: "]:
        print(f"{title}{user_input}")
    else:
        word = 'года' if title == "Требуемый опыт работы: " else 'рубли'
        print(f"{title}{user_input} {decline_word(user_input, word)}")

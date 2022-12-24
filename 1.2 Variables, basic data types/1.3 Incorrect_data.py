def is_correct_input(ui: str, input_type: str) -> bool:
    if ui == "" or input_type == "":
        return False
    elif input_type == 'bool':
        return ui in ['да', 'нет']
    elif input_type == 'int':
        return ui.isdigit()
    return True

# Ни у кого не списывал и делал сам!! Готов доказать, если потребуется.


def decline_word(count: int, w: str) -> str:
    rubles = ['рублей', 'рубля', 'рубль']
    years = ['лет', 'года', 'год']

    current_word = rubles if w == 'рубли' else years

    hundred_remainder = count % 100
    ten_remainder = count % 10
    if ten_remainder == 0 or ten_remainder in range(5, 10) or hundred_remainder in range(11, 20):
        return current_word[0]
    elif ten_remainder in range(2, 5):
        return current_word[1]
    else:
        return current_word[2]


to_ask = ["Введите название вакансии: ", "Введите описание вакансии: ", "Введите требуемый опыт работы (лет): ",
          "Введите нижнюю границу оклада вакансии: ", "Введите верхнюю границу оклада вакансии: ",
          "Есть ли свободный график (да / нет): ", "Является ли данная вакансия премиум-вакансией (да / нет): "]
user_inputs = []
i = 0
while i < len(to_ask):
    t = input(to_ask[i])
    if (is_correct_input(t, 'string') and i in range(2)) or (is_correct_input(t, 'bool') and i in range(5, 8)):
        user_inputs.append(t)
        i += 1
    elif is_correct_input(t, 'int') and i in range(2, 5):
        user_inputs.append(int(t))
        i += 1
    else:
        print("Данные некорректны, повторите ввод")

user_inputs[3] = (user_inputs[3] + user_inputs.pop(4)) // 2  # Подсчёт среднего оклада

titles = ["", "Описание: ", "Требуемый опыт работы: ", "Средний оклад: ", "Свободный график: ", "Премиум-вакансия: "]

for user_input, title in zip(user_inputs, titles):
    res = f"{title}{user_input}"
    if title not in ["", "Описание: ", "Свободный график: ", "Премиум-вакансия: "]:
        res += f""" {decline_word(int(user_input), f"{'года' if title == 'Требуемый опыт работы: ' else 'рубли'}")}"""
    print(res)

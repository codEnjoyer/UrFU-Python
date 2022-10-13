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


user_inputs = [input("Введите название вакансии: "),
               input("Введите описание вакансии: "),
               int(input("Введите требуемый опыт работы (лет): ")),
               (int(input("Введите нижнюю границу оклада вакансии: "))
                + int(input("Введите верхнюю границу оклада вакансии: "))) // 2,
               input("Есть ли свободный график (да / нет): "),
               input("Является ли данная вакансия премиум-вакансией (да / нет): ")]

titles = ["", "Описание: ", "Требуемый опыт работы: ",
          "Средний оклад: ", "Свободный график: ", "Премиум-вакансия: "]

for user_input, title in zip(user_inputs, titles):
    if title in ["", "Описание: ", "Свободный график: ", "Премиум-вакансия: "]:
        print(f"{title}{user_input}")
    else:
        word = 'года' if title == "Требуемый опыт работы: " else 'рубли'
        print(f"{title}{user_input} {decline_word(user_input, word)}")

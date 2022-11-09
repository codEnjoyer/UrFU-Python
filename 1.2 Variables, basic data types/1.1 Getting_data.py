to_ask = ["Введите название вакансии: ",
          "Введите описание вакансии: ",
          "Введите требуемый опыт работы (лет): ",
          "Введите нижнюю границу оклада вакансии: ",
          "Введите верхнюю границу оклада вакансии: ",
          "Есть ли свободный график (да / нет): ",
          "Является ли данная вакансия премиум-вакансией (да / нет): "]

inputs = [input(question) for question in to_ask]

for user_input in inputs:
    if user_input in ["да", "нет"]:
        print(f"{user_input == 'да'} (bool)")
    else:
        print(f"{user_input} {'(int)' if user_input.isdigit() else '(str)'}")

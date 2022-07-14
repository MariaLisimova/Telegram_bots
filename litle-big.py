number = 20
count_of_attempts = 1

while True:
    try:
        answer = int(input(' Введите целое число '))


        if number == answer:
            print('Вы угадали!')
            print(f'Количество попыток: {count_of_attempts}')
            break
        elif answer > number:
              print('Ваше число больше загаданного\n')
              count_of_attempts += 1
        else:
            print('Ваше число меньше загаданного\n')
            count_of_attempts += 1

    except ValueError:
         print("\n['ERROR']Пожалуйста,введите целое число\n")
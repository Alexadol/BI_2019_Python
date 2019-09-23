while True:
    while True:
        first_number = input('Please enter first number: ')
        if first_number.isdigit():
            break
        else:
            print('Please, use digits only! Let\'s try again!')
    operator = input('Please enter one of operator from [+,-,*,/]!/n Enter \'A\' for advanced version : ')
    if operator == 'A':
        print(
            'To get integer remainder after dividing use \'//\'\nTo raise to a power use \'**\'\nTo get remainder from division use \'%\'')
        operator = input('Please enter operator:')
    while True:
        second_number = input('Please enter first number: ')
        if first_number.isdigit():
            break
        else:
            print('Please, use digits only! Let\'s try again!')
    a = first_number
    b = second_number
    c = operator
    answer = 0
    if c in ['%', '/', '//'] and second_number == 0:
        print('If you like forbidden things division by zero is not the best choice:) Let\'s try again!')
        second_number = input('Please enter second number! Use digits only :')
    elif c == '+':
        answer = (int(a) + int(b))
    elif c == '-':
        answer = (int(a) - int(b))
    elif c == '/':
        answer = (int(a) / int(b))
    elif c == '*':
        answer = (int(a) * int(b))
    elif c == '%':
        answer = (int(a) % int(b))
    elif c == '**':
        answer = (int(a) ** int(b))
    elif c == '//':
        answer = (int(a) // int(b))
    print('Answer for your expression {}{}{} is {}'.format(first_number, operator, second_number, answer))
    again = input('For new calculation enter \'new\', for exit enter \'exit\'')
    if again == 'exit':
        break

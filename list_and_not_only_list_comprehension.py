# 1. Составить список из чисел от 1 до 1000, которые имеют в своём составе 7.
list_contains_seven = [el for el in range(1, 1001) if '7' in str(el)]
# print(list_contains_seven)


# 2. Взять предложение Would it save you a lot of time if I just gave up and went mad now? и сделать его же без гласных.
sentence_with_vowels = 'Would it save you a lot of time if I just gave up and went mad now?'
sentence_wo_vowels = ''.join([el for el in list(sentence_with_vowels) if el not in 'aeoiuyAEOUIY'])
# print(sentence_wo_vowels)


# 3. Для предложения The ships hung in the sky in much the same way that bricks don't составить словарь,
# где слову соответствует его длина.
sentence_for_dict = 'The ships hung in the sky in much the same way that bricks don\'t'
dict_with_len = dict([(el, len(el)) for el in sentence_for_dict.split(' ')])
# print(dict_with_len)


# 4*. Для чисел от 1 до 1000 наибольшая цифра, на которую они делятся (1-9).
# Не совсем поняла, список здесь нужен или словарь, поэтому 2 варианта

# список
list_with_max_div = [max([i for i in range(1, 10) if x % i == 0]) for x in range(1, 1001)]
# print(list_with_max_div)

# словарь
dict_with_max_div = dict([(x, max([i for i in range(1, 10) if x % i == 0])) for x in range(1, 1001)])
# print(dict_with_max_div)


# 5*. Список всех чисел от 1 до 1000, не имеющих делителей среди чисел от 2 до 9.
list_not_div_fromtwotonine = [x for x in range(1, 1001) if
                              not any(y in [i for i in range(1, 10) if x % i == 0] for y in [i for i in range(2, 10)])]
# print(list_not_div_fromtwotonine)

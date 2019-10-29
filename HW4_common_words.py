def common_words(first, second):
    common = []
    first = first.split(',')
    second = second.split(',')
    for el in first:
        if el in second:
            common.append(el)
    return ','.join(sorted(common))

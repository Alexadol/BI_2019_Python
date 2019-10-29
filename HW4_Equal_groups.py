def equal_groups(data):
    b = []
    final = []
    for i in range(len(data)):
        if data[i] == data[i - 1] or i == 0:
            b.append(data[i])
            if i == len(data) - 1:
                final.append(b)
        elif i != 0 and data[i] != data[i - 1]:
            final.append(b)
            b = [data[i]]
            if i == len(data) - 1:
                final.append(b)
    return final

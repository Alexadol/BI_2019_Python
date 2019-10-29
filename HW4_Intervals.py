def create_intervals(data):
    needforlist = list(data)
    needforlist.sort()
    stock = []
    for i in range(0, len(needforlist)):
        if i != len(needforlist) - 1 and needforlist[i + 1] - needforlist[i] != 1:
            stock.append(needforlist[i])
        if needforlist[i] - needforlist[i - 1] != 1:
            stock.append(needforlist[i])
        if i == len(needforlist) - 1:
            stock.append(needforlist[i])
    if len(stock) % 2 == 1:
        stock.append(stock[len(stock) - 1])
    pairs = zip(stock[::2], stock[1::2])
    return list(pairs)

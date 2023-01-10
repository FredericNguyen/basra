card = 10
card1 = 10
card2 = 2
length = 4
def capture(card1):
    sortie = False
    sum = []
    while not sortie:
        sum.append(card1)
        if sum == card:
            return sum
        if card == length:
            sortie = True
        else:
            capture(sum +card2)

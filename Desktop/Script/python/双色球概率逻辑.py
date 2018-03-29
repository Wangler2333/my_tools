import random
red_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0]
blues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(1000):
    red1 = random.randint(1, 33)
    red_totals[red1] +=1
    red2 = random.randint(1, 33)
    while red2 == red1:
        red2 = random.randint(1, 33)
    red_totals[red2] += 1
    red3 = random.randint(1, 33)
    while red3 == red2 or red3 == red1:
        red3 = random.randint(1, 33)
    red_totals[red3] += 1
    red4 = random.randint(1, 33)
    while red4 ==red3 or red4 == red2 or red4 == red1:
        red4 = random.randint(1, 33)
    red_totals[red4] += 1
    red5 = random.randint(1, 33)
    while red5 == red4 or red5 == red3 or red5 == red2 or red5 == red1:
        red5 = random.randint(1, 33)
    red_totals[red5] += 1
    red6 = random.randint(1, 33)
    while red6 == red5 or red6 == red4 or red6 == red3 or red6 == red2 or red1:
        red6 = random.randint(1, 33)
    red_totals[red6] += 1
    blue = random.randint(1,13)
    blues[blue] += 1
for i in range(1,33):
    print red_totals[i]
for i in range(1,13):
    print blues[i]
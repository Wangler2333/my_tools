import random
import sys


def check_args(args, Useged):
    if len(args) > 1:
        if args[1] in ['-h', 'h', '-H', 'H', '-help', '-v']:
            print(Useged)
            sys.exit(0)
    dict = {}
    try:
        for i in args:
            if '-' in i:
                dict[i] = args[int(args.index(i)) + 1]
    except:
        pass
    return dict


class guess_number(object):
    def __init__(self, number=3, lower_limit=0, upper_limit=9):
        self.number = number
        self.lower_limit = int(lower_limit)
        self.upper_limit = int(upper_limit)

    def create_number(self):
        self.number = random.randint(self.lower_limit, self.upper_limit)

    def guess(self):
        while True:
            guessNumber = input('请输入你猜测的数字:')
            if guessNumber.isdigit():
                break
            print('您输入的不是数字，请重新输入.\n')
        return guessNumber

    def cycle_time(self, times=3, randomly=True):
        count = int(times)
        while True:
            if randomly == True:
                self.create_number()
            guessNumber = int(self.guess())

            if guessNumber > self.number:
                print('你猜的数字大了。')
            elif guessNumber < self.number:
                print('你猜的数字小了。')
            elif guessNumber == self.number:
                print('你真厉害，这都能猜对！')
                break

            count -= 1

            if randomly == True:
                print('--> 随机数字猜测，[数字为 %s]，允许猜测次数为 %s, 你还剩 %s 次机会，加油哦!\n' %
                      (str(self.number), str(times), str(count)))
            if randomly == False and count == 0:
                print('--> 固定猜测猜测，[数字为 %s]，允许猜测次数为 %s, 你还剩 %s 次机会，加油哦!\n' %
                      (str(self.number), str(times), str(count)))
            elif randomly == False and count != 0:
                print('固定数字猜测，允许猜测次数为 %s, 你还剩 %s 次机会，加油哦!\n' %
                      (str(times), str(count)))

            if count == 0:
                print('可惜了，次数用完了，游戏结束！')
                break


t = guess_number(upper_limit=9, lower_limit=0)
t.cycle_time(times=5, randomly=True)

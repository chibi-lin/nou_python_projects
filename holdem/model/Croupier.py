import random

from model.Poker import Poker

# 發牌器類


class Croupier:
    __slots__ = ("__pokers", "__cursor")

    def __init__(self):
        self.__pokers = []
        self.__cursor = 0

        # 生成牌堆
        for color in range(1, 5):
            for num in range(2, 15):
                self.__pokers.append(Poker(color, num))

        print("#==============#")
        print("   空大專題作業   ")
        print("#==============#\n")

    def shuffle_pokers(self):
        # 洗牌
        random.shuffle(self.__pokers)

    def deal_pokers(self, deal_num):
        # 發牌
        pokers = []
        if len(self.__pokers[self.__cursor: -1]) < 5:
            self.shuffle_pokers()
            self.__cursor = 0
        for d in range(0, deal_num):
            pokers.append(self.__pokers[self.__cursor])
            self.__cursor += 1
        return pokers

from model.Croupier import Croupier
from model.User import User


def main():
    # 荷官入場
    croupier = Croupier()

    # 賭徒入場
    user_a = User(1, "A", 100)
    user_b = User(2, "B", 100)

    times = input("幾場賭局：")
    print("#==================================#")
    try:
        times = int(times)
        for x in range(0, times):
            # 洗牌
            croupier.shuffle_pokers()

            # 發牌
            user_a.pokers = croupier.deal_pokers(5)
            user_b.pokers = croupier.deal_pokers(5)

            # 判定
            type_a, j_info_a = user_a.get_pokers_info()
            type_b, j_info_b = user_b.get_pokers_info()


            # 輸出手牌信息
            print(user_a.name, type_a, user_a.pokers)
            print(user_b.name, type_b, user_b.pokers)

            # 判斷結果
            if j_info_a > j_info_b:
                user_a.add_money(10)
                user_b.sub_money(10)
                print("\nA 獲勝\n")
            elif j_info_a < j_info_b:
                user_b.add_money(10)
                user_a.sub_money(10)
                print("\nB 獲勝\n")
            else:
                print("\n平局\n")

            print("賭資：")
            print(user_a.name, user_a.money)
            print(user_b.name, user_b.money)
            print("#==================================#")

            # 調試用：查看 判斷信息
            # print("Judge_Info_A:", j_info_a)
            # print("Judge_Info_B:", j_info_b)
    except ValueError:
        print("輸入異常")


main()

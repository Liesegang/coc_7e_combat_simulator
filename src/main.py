import random

def roll_dice(n, sides):
    """n個のsides面ダイスを振る"""
    return sum(random.randint(1, sides) for _ in range(n))

def simulate_battle(p_a, m_a, n_a, p_b, m_b, n_b, trials):
    """バトルをシミュレートして、AとBの勝率を計算する"""
    wins_a = 0
    wins_b = 0

    for _ in range(trials):
        # キャラクターの体力を3D6で決定
        hp_a = 100 # roll_dice(3, 6)
        hp_b = 100 # roll_dice(3, 6)

        # 最初の攻撃者をランダムに決定
        turn_a = random.choice([True, False])

        while hp_a > 0 and hp_b > 0:
            if turn_a:
                # Aの攻撃
                if random.random() < p_a / 100:
                    hp_b -= roll_dice(m_a, n_a)
            else:
                # Bの攻撃
                if random.random() < p_b / 100:
                    hp_a -= roll_dice(m_b, n_b)

            # 次のターンへ
            turn_a = not turn_a

        # 勝利者を記録
        if hp_a > 0:
            wins_a += 1
        else:
            wins_b += 1

    return wins_a / trials, wins_b / trials


# シミュレーションパラメータ
p_a, m_a, n_a = 75, 2, 4  # Aの攻撃成功率75%、2D4ダメージ
p_b, m_b, n_b = 50, 3, 6  # Bの攻撃成功率50%、3D6ダメージ
trials = 10000  # 試行回数

# シミュレーション実行
win_rate_a, win_rate_b = simulate_battle(p_a, m_a, n_a, p_b, m_b, n_b, trials)

print(f"Aの勝率: {win_rate_a:.2f}, Bの勝率: {win_rate_b:.2f}")

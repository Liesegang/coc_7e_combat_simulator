# .新クトゥルフ神話TRPG 戦闘シミュレータ

このリポジトリには、新クトゥルフ神話TRPGのためのPythonベースの戦闘シミュレータが含まれています。このシミュレータは、CoCにおける戦闘シナリオをモデル化しています。キャラクターの能力値、スキル、そしてダイスロールのランダムな性質を考慮してシミュレーションを行います。ゲームマスターやシナリオの作者が能力値とスキルを設定してキャラクター間の戦闘結果を簡単にシミュレートするためのツールを提供することを目的としています。

このプログラムにより、シナリオにおける先頭のバランス調整を簡単に行うことができます。

## 特徴

- **キャラクター能力値**: STR（筋力）、CON（体力）、SIZ（体格）、DEX（敏捷性）、APP（外見）、INT（知力）、POW（精神力）、EDU（教育）、LUCK（幸運）を含む、クトゥルフ神話TRPG 第7版の全範囲のキャラクター属性をサポートします。
- **ダメージボーナスとビルドの計算**: キャラクターのSTRとSIZ属性に基づいて、自動的にダメージボーナスとビルドを計算します。
- **スキルシステム**: 戦闘でのパフォーマンスに影響を与えるスキルをキャラクターが持つことができます。これには成功率とダメージポテンシャルが含まれます。
- **戦闘シミュレーション**: スキルの成功率、ダメージ計算、キャラクターのHPを考慮して、2つのキャラクター間の戦闘をシミュレートします。
- **様々な戦略の選択**: 本シミュレーターは以下の3つの部分の戦略をカスタマイズすることができます。キャラクターごとに別な戦略を選択することが可能です。戦略を自分でカスタマイズすることもできます。
  - 敵の選択戦略: ランダム、HPが最も少ない敵を優先、HPが最も多い敵を優先の3種h類が実装されています。
  - スキルの選択戦略: ランダム、ダメージの期待値が最大のもの(ダメージの期待値 x スキルの成功率)の2種類が実装されています。
  - 応戦、回避の戦略: 常に何もしない、常に応戦、常に回避の3種類が実装されています。

## 使用方法

戦闘シミュレータを使用するには、Python 3.6以降が必要です。このリポジトリをローカルマシンにクローンし、リポジトリのディレクトリにナビゲートして、コマンドラインからシミュレータスクリプトを実行します。

### 前提条件

- Python 3.6+

### シミュレーションの実行

1. **キャラクターの定義**: それぞれの属性とスキルを指定してキャラクターインスタンスを作成します。この目的のために、提供された`Character`および`Skill`クラスを使用します。

2. **戦闘シミュレーション**: 2つのキャラクターを引数として`combat_simulation`関数を呼び出し、それらの間の戦闘シナリオをシミュレートします。

例:

```python
from coc7e_combat_simulator.combat_simulator import CombatSimulator
from coc7e_combat_simulator.character import Character
from coc7e_combat_simulator.strategies.skill_selection import ExpectedDamageMaximizationSkillSelectionStrategy
from coc7e_combat_simulator.strategies.target_selection import MaximumHpTargetSelectionStrategy, RandomTargetSelectionStrategy
from coc7e_combat_simulator.strategies.reaction import FightBackReactionStrategy
from coc7e_combat_simulator.skill import FightingBrawl, FirearmHandgun

# group A has 4 members, group B has 3 members
# Status of all characters are generated randomly before every combat
def group_a_character_init():
    characters = [Character.of_random(f"A_{i}", skills=[FightingBrawl, FirearmHandgun]) for i in range(4)]
    for character in characters:
        character.skill_selection_strategy = ExpectedDamageMaximizationSkillSelectionStrategy()
        character.target_selection_strategy = MaximumHpTargetSelectionStrategy()
        character.reply_strategy = FightBackReactionStrategy()
    return characters

def group_b_character_init():
    characters = [Character.of_random(f"B_{i}", skills=[FightingBrawl]) for i in range(3)]
    for character in characters:
        character.target_selection_strategy = RandomTargetSelectionStrategy()
        character.reply_strategy = FightBackReactionStrategy()
    return characters

simulator = CombatSimulator(group_a_character_init, group_b_character_init)
results = simulator.simulate_multiple_combats(10000)
print(results)

```

## カスタマイズ

- **キャラクターの作成**: 必要に応じてスキルや属性を追加・変更することで、キャラクターをさらにカスタマイズすることができます。
- **戦闘戦略**： キャラクターごとに、攻撃対象、使用スキル、応戦・回避の使用の戦略をカスタマイズできます。

## 貢献

戦闘シミュレータへの貢献を歓迎します。リポジトリをフォークし、変更を加え、プルリクエストを提出してください。大きな変更については、まずissueを開き、変更したい点を議論してください。

## ライセンス

このプロジェクトのライセンスは MIT License です - 詳細は LICENSE ファイルを参照してください。

### 著作権上の注意

このプロジェクトは、Chaosium Inc.の製品であるCall of Cthulhu 7th Edition（CoC7e）及びその日本語版である『新クトゥルフ神話TRPG』のキャラクターシミュレーターです。すべてのルール、設定、翻訳等はChaosium Inc. または「株式会社アークライト」及び「株式会社KADOKAWA」に帰属します。

このシミュレーターは、ファンによって作成された非公式のツールであり、Chaosium Inc.、株式会社アークライト 及び 株式会社KADOKAWA とは直接の関係がありません。

このシミュレーターは、個人的な使用や非営利目的でのみ利用することを意図しています。

本プロジェクトの開発者は、Chaosium Inc.、「株式会社アークライト」及び「株式会社KADOKAWA」に感謝し、CoCの世界を愛するファンであることを明記します。Chaosium Inc.、株式会社アークライト及び株式会社KADOKAWAの著作権と知的財産権を尊重し、それらの権利を侵害しないよう努めます。

### 著作権

本作は、「株式会社アークライト」及び「株式会社KADOKAWA」が権利を有する『新クトゥルフ神話TRPG』の二次創作物です。

Call of Cthulhu is copyright ©1981, 2015, 2019 by Chaosium Inc. ;all rights reserved. Arranged by Arclight Inc.
Call of Cthulhu is a registered trademark of Chaosium Inc.
PUBLISHED BY KADOKAWA CORPORATION　「新クトゥルフ神話TRPG ルールブック」


シミュレータプログラム: @liesegang

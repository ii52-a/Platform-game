
class Screen:
    ScreenX=1280
    ScreenY=720

class Version:
    VERSION_STR="a5.4"


class Show:
    """标准 ：0"""
    #标准 0 增加将极大提升难度
    TRAP_ADD=0
    #增加冰蓝释放技能时的冰寒召唤数量
    ICE_BLUE_SUMMON_ADD=0

    #跳过枢纽动画
    SKIP_NEX=True

class Config:
    #test 自移动平台,生成一个随玩家移动的平台代替初始平台
    #标准 False
    TEST_PLATFORM=False

    #免疫掉落死亡
    #标准 False
    PLAYER_NO_DAMP=True

    #表演模式:trap生成数量增加

    #初始分数  决定阶段
    #标准 0
    INIT_SCORE=22000


    #玩家生命值
    #标准 100
    # PLAYER_HEALTH=9999999.9
    PLAYER_HEALTH=2000
    #额外分数获得
    #标准 100
    EXTRA_SCORE=150


    #第一boss伤害间隔，可以加快阶段，用于测试
    #标准 400, 最低180
    FIRST_BOSS_INTERNAL=180

    #第二boss伤害间隔，可以加快阶段，用于测试
    #标准 600, 最低180
    SECONDE_BOSS_INTERNAL = 600
    #第一boss生命值
    #标准 300
    FIRST_BOSS_HEALTH=60

    #第二boss生命值
    SECOND_BOSS_HEALTH=0
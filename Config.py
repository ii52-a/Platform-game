
class Screen:
    ScreenX=1280
    ScreenY=720

class Version:
    VERSION_STR="a3.3"

class Config:
    #免疫掉落死亡
    #标准 False
    PLAYER_NO_DAMP=True



    #初始分数
    INIT_SCORE=0
    #初始阶段
    #标准 1
    START_STAGE = 1


    #玩家生命值
    #标准 100
    PLAYER_HEALTH=9999999.9

    #额外分数获得
    #标准 200
    EXTRA_SCORE=200


    #第一boss伤害间隔，可以加快阶段，用于测试
    #标准 400, 最低180
    FIRST_BOSS_INTERNAL=400
    #第一boss生命值
    #标准 300
    FIRST_BOSS_HEALTH=300
from operator import itemgetter

# 하루동안 갑자기 베이지 활률을 공부해서.. 어떻게 될지는 모르겠네요..ㅋㅋ&땜방코드가 몇개 있습니다...
# pycon2016 홧팅
# p.s. 재미삼아 일부러 한글코딩 해봤습니다 ㅋ
"""
작동구조
-------
1. 게임 플레이 30회 까지는 임의로 정한 가위,바위,보 순서에 맞게 차례대로 진행됩니다.
2. 30회 이후부터는 가위,바위,보에 대한 조건확률을 구하고 가장 높은 확률을 정답을 내보냅니다.
3. 간혹 운이 나뻐 패배를 하는데 그 격차가 상당하기에 격차를 줄이기 위하여 500회 ~ 1000회의 시점에서는 매회 승률을 계산하여 적의 승률이 40%이상일경우 알고리즘을 변경합니다.
4. 변경될 알고리즘은 상대방의 기준으로 유리한 행동을 고르고 해당 행동과 반대되는 행동을 내보냅니다.
"""


# 내가 이길확률로 값을 결정
def 내전적추적(전적):
    내전적 = []
    for 기록 in 전적:
        손모양, 승부 = 기록
        if 승부 == 0:
            내전적.append((손모양, 승부))
        elif 승부 == 1:
            내전적.append((거울2(손모양), -1))
        else:
            내전적.append((거울(손모양), 1))
    return 내전적

# 내가 이길확률로 값을 결정

def 승부계수추가(승부계수,값):
    """ 승부여부 숫자값을 바탕으승부계수 딕셔너리에 값을 추가"""
    if 값 == 1:
       승부계수['승'] += 1
    elif 값 == 0:
       승부계수['무'] += 1
    else:
       승부계수['패'] += 1
    return 승부계수


def 전적분석(전적):
    """상대 전적을 분석줌하여 각 패의 활과승부계수을 알려줌"""

    # 행동계수 분석
    진행횟수 = len(전적)
    초기화 = {'gawi':0,'bawi':0,'bo':0}
    행동계수 = 초기화  # 전적에서 각 행동이 발생한 횟수
    행동확률 = 초기화  # 전적에서 각 행동이 발생한 학률
    승부행동계수 = 초기화    # 전적에서 승리 했을때의 각 행동 수
    승부행동확률 = 초기화    # 전적에서 승리 했을때의 각 행동 확률
    총승부계수 = {'승':0,'패':0,'무':0}
    for 기록 in 전적:
        손모양, 승부 = 기록
        # 승부 통계를 위한 데이터
        승부계수추가(총승부계수,승부)
        행동계수[손모양] += 1
        # 내가 이겼을 경우 (적이 졌을경우) -1 // 적이 이겼을 경우는 1
        if 승부 == 1:
            승부행동계수[손모양] += 1

        # 분석
        승률 = 총승부계수['승']/진행횟수
        for 행동 in ['gawi','bawi','bo']:
            행동확률[행동] = 행동계수[행동]/진행횟수
            if 총승부계수['승'] == 0: # 총승부 계수가 0일 경우 계산을 위해 임의로 매우 낮은 활률을 입력
                승부행동확률[행동] = 승부행동계수[행동] / 0.0000001
            else:
                승부행동확률[행동] = 승부행동계수[행동]/총승부계수['승']
    return 승률,행동확률,승부행동확률

def 거울(손모양):
    """입력값의 반대되는 값을(승리값)반환해"""
    if 손모양 == 'gawi':
        return 'bawi'
    elif 손모양 == 'bawi':
        return 'bo'
    else:
        return 'gawi'

def 거울2(손모양):
    """입력값의 반대되는 값을(패배값)반환해"""
    if 손모양 == 'gawi':
        return 'bo'
    elif 손모양 == 'bawi':
        return 'gawi'
    else:
        return 'bawi'

def show_me_the_hand(전적):
    # 30회 까지는 임의로 가위바위적
    내전적 = []
    내전적 += 내전적추적(전적)

    if len(내전적) == 0:
        print(내전적)
        return 'gawi'
    elif len(내전적) < 30:
        if len(내전적) < 15:
            print(내전적)
            if 내전적[-1][0] == 'gawi':
                return 'bawi'
            elif 내전적[-1][0] == 'bawi':
                return 'bo'
            elif 내전적[-1][0] == 'bo':
                return 'gawi'
        else:
            if 내전적[-1][0] == 'bawi':
                return 'bo'
            elif 내전적[-1][0] == 'gawi':
                return 'bawi'
            else:
                return 'gawi'

    elif 500 < len(전적) <= 1000 and 전적분석(전적)[0]>0.4:
        try:
            승률, 행동확률, 승부행동확률 = 전적분석(전적)
            행동별승률 = {'gawi':0,'bawi':0,'bo':0}

            # 베이지안 확률로 각 행동별 승률을 구한다
            for 행동 in ['gawi', 'bawi', 'bo']:
                if 행동확률[행동] == 0:
                    행동별승률[행동] = 승률 * 승부행동확률[행동] / 0.3333333
                else:
                    행동별승률[행동] = 승률*승부행동확률[행동]/행동확률[행동]

            # 적에게 승률이 제일 높은 값의 반대값으로 리턴함

            상대방예상값 = sorted(행동별승률.items(), key=itemgetter(1),reverse=True)[0][0]
            return 거울(상대방예상값)
        except:
            return 'bawi'
    else:
        try:
            승률, 행동확률, 승부행동확률 = 전적분석(내전적)
            행동별승률 = {'gawi':0,'bawi':0,'bo':0}

            # 베이지안 확률로 각 행동별 승률을 구한다
            for 행동 in ['gawi', 'bawi', 'bo']:
                if 행동확률[행동] == 0:
                    행동별승률[행동] = 승률 * 승부행동확률[행동] / 0.3333333
                else:
                    행동별승률[행동] = 승률*승부행동확률[행동]/행동확률[행동]

            # 적에게 승률이 제일 높은 값의 반대값으로 리턴함

            상대방예상값 = sorted(행동별승률.items(), key=itemgetter(1),reverse=True)[0][0]
            return 상대방예상값
        except:
            return 'bawi'
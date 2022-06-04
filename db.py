import pymysql

db = pymysql.connect(host="localhost", user="s2020112547", password="", charset="utf8")

cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('USE s2020112547_final_project;')

options = ["회원", "메뉴", "매장", "회원방문관리", "본사정보", "재료재고정보", "재료공급내역", "재료사용기록", "시스템종료"]
subOptions = [["전체회원조회", "아이디로회원검색", "회원등록", "홈으로"], ["전체메뉴조회", "메뉴검색", "메뉴추가", "홈으로"], ["전체매장조회", "매장검색", "매장추가", "홈으로"], ["전체방문기록조회", "매장별 방문기록조회", "방문기록추가", "홈으로"], ["본사정보조회", "본사정보수정", "홈으로"], ["전체재고조회", "재고검색", "재료추가", "홈으로"], ["전체공급내역조회", "공급내역검색", "공급내역등록", "홈으로"], ["전체재료사용내역조회", "사용내역검색", "사용내역등록", "홈으로"]]
bar = "--------------------------------------"

# 기능 출력
def getOptionFromUser():
    i = 1
    print(bar)
    for option in options:
        print("%d. " %i, end="")
        print(option)
        i += 1
    print(bar)
    select = int(input('옵션을 선택하세요 >> '))
    print()
    return select

# 서브 기능 출력
def getSubOptionFromUser(select):
    i = 1
    print(bar)
    for subOption in subOptions[select-1]:
        print("%d " %i, end="")
        print(subOption)
        i += 1
    print(bar)
    subSelect = int(input('세부 옵션을 선택하세요 >> '))
    print()
    return subSelect;

# 옵션 선택했을 때 상단바 출력해줌
def printTopBar(optionName):
    stars = 18 - len(optionName)
    i = 0
    while(i < stars):
        print("*", end="")
        i += 1
    print(" " + optionName + " ", end="")
    i = 0
    while(i < stars):
        print("*", end="")
        i += 1
    print()

# 데이터의 모든 정보 출력해줌
def printAllInfoInData(userInfo):
    print(bar)
    for key in userInfo:
        print(key, "\t:", userInfo.get(key))
    print(bar)

# 1. 1) 전체회원조회
def viewAllUsers():
    cursor.execute('SELECT * FROM 회원;')
    userInfoList = cursor.fetchall()
    i = 0
    while(i<len(userInfoList)):
        printAllInfoInData(userInfoList[i])
        i += 1
    db.commit()

# 1. 2) 아이디로회원검색
def searchUserById():
    userIdInput = input('검색할 회원 아이디 입력 >> ')
    cursor.execute('SELECT * FROM 회원 WHERE 회원아이디 = %s', userIdInput)
            
    userInfo = cursor.fetchall()
    printAllInfoInData(userInfo[0])
    print()
    db.commit()

# 1. 3) 회원등록
def addNewUser():
    userInfoInput = []
    userInfoInput.append(input('아이디(중복안됨) >> '))
    userInfoInput.append(input('이름 >> '))
    userInfoInput.append(input('전화번호 >> '))

    userInfoInput = tuple(userInfoInput)

    cursor.execute('INSERT INTO 회원 VALUES(%s, %s, %s)', userInfoInput)
    cursor.execute('SELECT * FROM 회원 WHERE 회원아이디 = %s', userInfoInput[0])

    userInfo = cursor.fetchall()
    print("\n회원이 등록되었습니다.")
    printAllInfoInData(userInfo[0])
    print()
    db.commit()

# 2. 1) 전체메뉴조회
category = {1: "COFFEE", 2: "FRAPPUCCINO", 3: "TEA", 4: "CAKE"}
def viewAllMenus():
    cursor.execute('SELECT * FROM 메뉴;')
    menuInfoList = cursor.fetchall()
    i = 0
    while(i<len(menuInfoList)):
        printAllInfoInData(menuInfoList[i])
        i += 1
    db.commit()

"""
--- 전체 기능 ---
1. 회원
    1) 전체회원조회
    2) 아이디로회원검색
    3) 회원등록
2. 메뉴
    1) 전체메뉴조회
    2) 메뉴검색
    3) 메뉴추가
3. 매장
    1) 전체매장조회
    2) 매장검색
    3) 매장추가
4. 회원방문관리
    1) 전체방문기록조회
    2) 매장별 방문기록조회
    3) 방문기록추가
5. 본사정보
    1) 본사정보조회
    2) 본사정보수정
6. 재료재고정보
    1) 전체재고조회
    2) 재고검색
    3) 재료추가
7. 재료공급내역
    1) 전체공급내역조회
    2) 공급내역검색
    3) 공급내역기록
8. 재료사용기록
    1) 전체재료사용내역조회
    2) 사용내역검색
    3) 사용내역등록
9. 시스템종료
"""

print("------- 스타벅스에 운영 시스템 -------")
while(True):
    # 기능 계속 출력(종료 선택할 때까지)
    select = getOptionFromUser()
    printTopBar(options[select-1])
        
    # 1. 회원
    if(select == 1):
         while(True):
            subSelect = getSubOptionFromUser(select)
            printTopBar(subOptions[select-1][subSelect-1])
            # 1) 전체회원조회
            if(subSelect == 1):
                viewAllUsers()
            # 2) 아이디로회원검색
            elif(subSelect == 2):
                searchUserById()
            # 3) 회원등록
            elif(subSelect == 3):
                addNewUser()
            else:
                print("홈으로 가기")
                break
    elif(select == 2):
        while(True):
            subSelect = getSubOptionFromUser(select)
            printTopBar(subOptions[select-1][subSelect-1])
            # 1) 전체메뉴조회
            if(subSelect == 1):
                viewAllMenus()
            # 2) 메뉴검색
            # 3) 메뉴추가
    elif(select == 3):
        # 1) 전체매장조회
        # if(subSelect == 1):

        # 2) 매장검색
        # 3) 매장추가
        print("\n**************** 매장 ****************")
    elif(select == 4):
        print("\n************ 회원 방문 관리 ************")
    elif(select == 5):
        print("\n************** 본사 정보 **************")
    elif(select == 6):
        print("\n************** 본사 정보 **************")
    elif(select == 7):
        print("----------------종료합니다----------------")
        break


db.commit()
db.close()
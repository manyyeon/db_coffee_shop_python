import pymysql

db = pymysql.connect(host="localhost", user="s2020112547", password="", charset="utf8")

cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('USE s2020112547_final_project;')

options = ["회원", "메뉴", "매장", "회원방문관리", "본사정보", "재료재고정보", "재료공급내역", "재료사용기록", "시스템종료"]
subOptions = [["전체회원조회", "아이디로회원검색", "회원등록"], ["전체메뉴조회", "메뉴검색", "메뉴추가"], ["전체매장조회", "매장검색", "매장추가"], ["전체방문기록조회", "매장별 방문기록조회", "방문기록추가"], ["본사정보조회", "본사정보수정"], ["전체재고조회", "재고검색", "재료추가"], ["전체공급내역조회", "공급내역검색", "공급내역등록"], ["전체재료사용내역조회", "사용내역검색", "사용내역등록"]]
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

def printMemberInfo(memberInfo):
    print(bar)
    for key in memberInfo:
        print(key, "\t:", memberInfo.get(key))
    print(bar)

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

print("-------- 스타벅스에 운영 시스템 --------")
while(True):
    # 기능 계속 출력(종료 선택할 때까지)
    select = getOptionFromUser()
    printTopBar(options[select-1])
    subSelect = getSubOptionFromUser(select)
    printTopBar(subOptions[select-1][subSelect-1])

    if(select == 1):
        # 전체회원조회
        if(subSelect == 1):
            cursor.execute('SELECT * FROM 회원;')
            memberInfoList = cursor.fetchall()
            i = 0
            while(i<len(memberInfoList)):
                printMemberInfo(memberInfoList[i])
                i += 1
            db.commit()
        elif(subSelect == 2):
            userIdInput = input('검색할 회원 아이디 입력 >> ')
            cursor.execute('SELECT * FROM 회원 WHERE 회원아이디 = %s', userIdInput)
            
            memberInfo = cursor.fetchall()
            printMemberInfo(memberInfo[0])
            print()
            db.commit()

            print(bar)
            print("1. 회원 정보 수정\n2. 회원 삭제")
            print(bar)
            subSubSelect = int(input('더 세부적인 기능을 선택하세요 >> '))
            if(subSubSelect == 1):
                print("수정 기능 안됨")
                memberInfoInput = []
                userId = input('아이디(중복안됨) >> ')
                memberInfoInput.append(userId)
                memberInfoInput.append(input('이름 >> '))
                memberInfoInput.append(input('전화번호 >> '))
                memberInfoInput.append(userId) # WHERE = 회원아이디=%s를 위해서 아이디을 한 번 더 넣어줌

                memberInfoInput = tuple(memberInfoInput)
                print(memberInfoInput)
                print(userId)
                cursor.execute('UPDATE 회원 SET 회원아이디=%s, 회원이름=%s, 전화번호=%s WHERE 회원아이디=%s', memberInfoInput)
                db.commit()
                cursor.execute('SELECT * FROM 회원 WHERE 회원아이디 = %s', memberInfoInput[0])

                memberInfo = cursor.fetchall()
                print(memberInfo)
                print("\n회원 정보가 수정되었습니다.")
                printMemberInfo(memberInfo)
                print()
                db.commit()

            elif(subSubSelect == 2):
                print("\n************** 회원 삭제 **************")
        # 회원등록
        elif(subSelect == 3):
            memberInfoInput = []
            memberInfoInput.append(input('아이디(중복안됨) >> '))
            memberInfoInput.append(input('이름 >> '))
            memberInfoInput.append(input('전화번호 >> '))

            memberInfoInput = tuple(memberInfoInput)

            cursor.execute('INSERT INTO 회원 VALUES(%s, %s, %s)', memberInfoInput)
            cursor.execute('SELECT * FROM 회원 WHERE 회원아이디 = %s', memberInfoInput[0])

            memberInfo = cursor.fetchall()
            print("\n회원이 등록되었습니다.")
            printMemberInfo(memberInfo[0])
            print()
            db.commit()
    elif(select == 2):
        print("\n**************** 메뉴 ****************")
        print("--------------------------------------")
        print("1. 전체 회원 조회\n2. 아이디로 회원 검색\n3. 회원 등록")
        print("--------------------------------------")
        subSelect = int(input('세부 기능을 선택하세요 >> '))
    elif(select == 3):
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
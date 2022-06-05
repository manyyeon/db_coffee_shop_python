import pymysql

db = pymysql.connect(host="localhost", user="s2020112547", password="", charset="utf8")

cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('USE s2020112547_final_project;')

options = ["본사", "매장", "메뉴", "주문", "시스템종료"]
subOptions = [["전체본사조회", "이름으로본사검색", "본사등록", "홈으로"], ["본사별매장조회", "매장등록", "홈으로"], ["본사별메뉴조회", "메뉴등록", "홈으로"], ["본사별주문조회", "주문등록", "홈으로"]]
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
def printAllInfoInData(info):
    print(bar)
    for key in info:
        print(key, "\t:", info.get(key))
    print(bar)

# 본사 이름들만 전체 출력해줌
def getCompanyNames():
    print(bar)
    cursor.execute('SELECT 본사이름 FROM 본사;')
    companyNameList = cursor.fetchall()
    i = 0
    while(i<len(companyNameList)):
        print(i+1, end="")
        print(". " + companyNameList[i].get('본사이름'), end=" ")
        i += 1
    print()
    print(bar)

#1. 1) 전체본사조회
def viewAllCompany():
    cursor.execute('SELECT * FROM 본사;')
    companyInfoList = cursor.fetchall()
    i = 0
    while(i<len(companyInfoList)):
        printAllInfoInData(companyInfoList[i])
        i += 1
    db.commit()

# 1. 2) 이름으로본사검색
def searchCompanyByName():
    companyNameInput = input('검색할 본사 이름 입력 >> ')
    # 공백 제거
    companyNameInput = companyNameInput.replace(" ", "")
    
    cursor.execute('SELECT * FROM 본사 WHERE 본사이름 = %s', companyNameInput)
            
    companyInfo = cursor.fetchall()
    print()
    printTopBar("검색결과")
    printAllInfoInData(companyInfo[0])
    print()
    db.commit()

# 1. 3) 본사등록
def addNewCompany():
    companyInfoInput = []
    companyInfoInput.append(input('본사이름 입력 >> '))
    companyInfoInput.append(input('위치 입력 >> '))
    companyInfoInput.append(input('전화번호 입력 >> '))

    companyInfoInput = tuple(companyInfoInput)

    cursor.execute('INSERT INTO 본사 VALUES(%s, %s, %s)', companyInfoInput)
    cursor.execute('SELECT * FROM 본사 WHERE 본사이름 = %s', companyInfoInput[0])

    companyInfoInput = cursor.fetchall()
    print("\n본사가 새롭게 등록되었습니다.")
    printAllInfoInData(companyInfoInput[0])
    print()
    db.commit()

# 2. 1) 본사별매장조회
def viewStoreByCompany():
    companyNameInput = input('검색할 매장들의 본사 이름 입력 >> ')
    # 공백 제거
    companyNameInput = companyNameInput.replace(" ", "")
    cursor.execute('SELECT 매장번호, 지점명, 위치, 영업시간, 전화번호 FROM 매장 WHERE 본사 = %s;', companyNameInput)
    storeInfoList = cursor.fetchall()
    print()
    printTopBar(companyNameInput + "의 매장들")
    i = 0
    while(i<len(storeInfoList)):
        printAllInfoInData(storeInfoList[i])
        i += 1
    db.commit()
    

# 2. 2) 매장등록
def addNewStore():
    storeInfoInput = []
    storeInfoInput.append(input(''))

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
1. 본사
    1) 전체본사조회
    2) 이름으로본사검색
    3) 본사등록
2. 매장
    1) 본사별매장조회
    2) 매장등록
3. 메뉴
    1) 본사별메뉴조회
    2) 메뉴등록
4. 주문
    1) 본사별주문조회
    2) 주문등록
5. 시스템종료
"""

print("-------- 커피숍 운영 시스템 --------")
while(True):
    # 기능 계속 출력(종료 선택할 때까지)
    select = getOptionFromUser()
    printTopBar(options[select-1])
        
    # 1. 본사
    if(select == 1):
         while(True):
            subSelect = getSubOptionFromUser(select)
            printTopBar(subOptions[select-1][subSelect-1])
            # 1) 전체회원조회
            if(subSelect == 1):
                viewAllCompany()
            # 2) 이름으로본사검색
            elif(subSelect == 2):
                getCompanyNames()
                searchCompanyByName()
            # 3) 본사등록
            elif(subSelect == 3):
                addNewCompany()
            else:
                print("홈으로 가기")
                break
    # 2. 매장
    elif(select == 2):
        while(True):
            subSelect = getSubOptionFromUser(select)
            printTopBar(subOptions[select-1][subSelect-1])
            # 1) 본사별매장조회
            if(subSelect == 1):
                getCompanyNames()
                viewStoreByCompany()
            # 2) 매장등록
            elif(subSelect == 2):
                getCompanyNames()
    # 3. 메뉴
    elif(select == 3):
        subSelect = getSubOptionFromUser(select)
        printTopBar(subOptions[select-1][subSelect-1])
        # 1) 전체매장조회
        if(subSelect == 1):
            viewAllStore()
    # 4. 주문
    elif(select == 4):
        while(True):
            subSelect = getSubOptionFromUser(select)
            printTopBar(subOptions[select-1][subSelect-1])
            # 1) 전체방문기록조회
            if(subSelect == 1):
                viewAllVisit()
            # 2) 매장별 방문기록조회
            # 3) 방문기록추가
            # 4) 홈으로
    elif(select == 7):
        print("\n************** 본사 정보 **************")
    elif(select == 8):
        print("\n************** 본사 정보 **************")
    elif(select == 9):
        print("\n************** 본사 정보 **************")
    elif(select == 10):
        print("----------------종료합니다----------------")
        break


db.commit()
db.close()
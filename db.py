from nis import cat
import pymysql

db = pymysql.connect(host="localhost", user="s2020112547", password="", charset="utf8")

cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('USE s2020112547_final_project;')

options = ["본사", "매장", "메뉴", "주문", "시스템종료"]
subOptions = [["전체본사조회", "이름으로본사검색", "본사등록", "홈으로"], ["본사매장조회", "매장등록", "홈으로"], ["본사메뉴조회", "메뉴등록", "홈으로"], ["본사주문조회", "본사별 총 주문수량 조회", "홈으로"]]
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
        if(len(key) < 4):
            print(key, "\t\t:", info.get(key))
        else:
            print(key, "\t:", info.get(key))
    print(bar)

# 릴레이션 모두 출력
def viewAll(relationName):
    query = 'SELECT * FROM ' + relationName
    cursor.execute(query)
    infoList = cursor.fetchall()
    i = 0
    while(i<len(infoList)):
        printAllInfoInData(infoList[i])
        i += 1
    db.commit()

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

# 2. 1) 본사매장조회
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
    print()
    cursor.execute('SELECT MAX(매장번호) AS 마지막번호 FROM 매장;')
    lastNum = cursor.fetchall()
    lastNum = lastNum[0].get('마지막번호')
    db.commit()
    
    getCompanyNames()
    companyNameInput = input('등록할 매장의 본사 이름 입력 >> ')
    # 공백 제거
    companyNameInput = companyNameInput.replace(" ", "")
    
    storeInfoInput = []
    storeInfoInput.append(companyNameInput)
    storeInfoInput.append(input('지점명 입력 >> '))
    storeInfoInput.append(input('위치 입력 >> '))
    storeInfoInput.append(input('영업시간 입력 >> '))
    storeInfoInput.append(input('전화번호 입력 >> '))
    inputQuery = "INSERT INTO 매장 VALUES(" + str(lastNum+1) + ", '%s', '%s', '%s', '%s', '%s');" %(storeInfoInput[0], storeInfoInput[1], storeInfoInput[2], storeInfoInput[3], storeInfoInput[4])
    cursor.execute(inputQuery)
    db.commit()

    cursor.execute('SELECT * FROM 매장 WHERE 매장번호=' + str(lastNum+1) + ';')
    storeInfo = cursor.fetchall()

    print("\n매장이 새롭게 등록되었습니다.")
    printAllInfoInData(storeInfo[0])
    print()
    db.commit()

# 3. 1) 본사메뉴조회
category = {1: "COFFEE", 2: "FRAPPUCCINO", 3: "TEA", 4: "CAKE"}
def viewMenuByCompany():
    companyNameInput = input('검색할 메뉴들의 본사 이름 입력 >> ')
    # 공백 제거
    companyNameInput = companyNameInput.replace(" ", "")
    cursor.execute('SELECT 메뉴번호, 메뉴이름, 가격 FROM 메뉴 WHERE 본사 = %s;', companyNameInput)
    menuInfoList = cursor.fetchall()
    print()
    printTopBar(companyNameInput + "의 메뉴들")
    i = 0
    while(i<len(menuInfoList)):
        printAllInfoInData(menuInfoList[i])
        i += 1
    db.commit()

# 카테고리 출력
def printCategoryList():
    print(bar)
    for key in category:
        print(str(key) + "." + category[key], end=" ")
    print()
    print(bar)

# 3. 2) 메뉴등록
def addNewMenu():
    cursor.execute('SELECT MAX(메뉴번호) AS 마지막번호 FROM 메뉴;')
    lastNum = cursor.fetchall()
    lastNum = lastNum[0].get('마지막번호')
    db.commit()
    
    getCompanyNames()
    companyNameInput = input('등록할 메뉴의 본사 이름 입력 >> ')
    # 공백 제거
    companyNameInput = companyNameInput.replace(" ", "")
    
    menuInfoInput = []
    menuInfoInput.append(companyNameInput)
    menuInfoInput.append(input('메뉴이름 입력 >> '))
    menuInfoInput.append(input('가격 입력 >> '))
    printCategoryList()
    categoryNum = int(input('카테고리 번호 입력 >> '))
    categoryName = category.get(categoryNum)
    menuInfoInput.append(categoryName)
    inputQuery = "INSERT INTO 메뉴 VALUES(" + str(lastNum+1) + ", '%s', '%s', '%s', '%s');" %(menuInfoInput[0], menuInfoInput[1], menuInfoInput[2], menuInfoInput[3])
    cursor.execute(inputQuery)
    db.commit()

    cursor.execute('SELECT * FROM 메뉴 WHERE 메뉴번호=' + str(lastNum+1) + ';')
    menuInfo = cursor.fetchall()

    print("\n메뉴가 새롭게 등록되었습니다.")
    printAllInfoInData(menuInfo[0])
    print()
    db.commit()

# 4. 1) 본사주문조회
def viewOrderByCompany():
    companyNameInput = input('검색할 주문내역들의 본사 이름 입력 >> ')
    # 공백 제거
    companyNameInput = companyNameInput.replace(" ", "")
    cursor.execute('select 지점명, 메뉴이름, 가격, 주문수량, 주문일자, 카테고리 from 주문, 매장, 메뉴 where 주문.매장번호 = 매장.매장번호 and 주문.메뉴번호 = 메뉴.메뉴번호 and 매장.본사=%s;', companyNameInput)
    orderInfoList = cursor.fetchall()
    print()
    printTopBar(companyNameInput + "의 주문목록")
    i = 0
    while(i<len(orderInfoList)):
        printAllInfoInData(orderInfoList[i])
        i += 1
    db.commit()

# 4. 2) 본사별 총 주문수량 조회
def viewSumOrderNumByCompany():
    cursor.execute('select 매장.본사, sum(주문수량) as "총 주문수량" from 주문, 매장, 메뉴 where 주문.매장번호 = 매장.매장번호 and 주문.메뉴번호 = 메뉴.메뉴번호 group by 매장.본사;')
    sumOrderNumByCompnayList = cursor.fetchall()
    print()
    i = 0
    while(i<len(sumOrderNumByCompnayList)):
        printAllInfoInData(sumOrderNumByCompnayList[i])
        i += 1
    db.commit()

"""
--- 전체 기능 ---
1. 본사
    1) 전체본사조회
    2) 이름으로본사검색
    3) 본사등록
2. 매장
    1) 본사매장조회
    2) 매장등록
3. 메뉴
    1) 본사메뉴조회
    2) 메뉴등록
4. 주문
    1) 본사주문조회
    2) 본사별 총 주문수량 조회
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
                viewAll("본사")
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
                viewAll("매장")
                addNewStore()
            else:
                print("홈으로 가기")
                break
    # 3. 메뉴
    elif(select == 3):
        while(True):
            subSelect = getSubOptionFromUser(select)
            printTopBar(subOptions[select-1][subSelect-1])
            # 1) 본사별메뉴조회
            if(subSelect == 1):
                getCompanyNames()
                viewMenuByCompany()
            # 2) 메뉴등록
            elif(subSelect == 2):
                addNewMenu()
            else:
                print("홈으로 가기")
                break
    # 4. 주문
    elif(select == 4):
        while(True):
            subSelect = getSubOptionFromUser(select)
            printTopBar(subOptions[select-1][subSelect-1])
            # 1) 본사별주문조회
            if(subSelect == 1):
                getCompanyNames()
                viewOrderByCompany()
            # 2) 주문등록
            elif(subSelect == 2):
                viewSumOrderNumByCompany()
            else:
                print("홈으로 가기")
                break;
    elif(select == 5):
        print("----------------종료합니다----------------")
        break


db.commit()
db.close()
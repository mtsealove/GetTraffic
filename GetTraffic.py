from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time
import IC
import FileRW
from operator import eq

NodeOnclick = FileRW.NodeFIle()
Nodes = []
IcFile = open('ICList.csv', 'r')  # IC 파일을 읽어옴
while True:
    line = IcFile.readline()
    if not line: break
    StartNode = line.split(',')[0]
    EndNode = line.split(',')[1]
    Nodes.append(IC.Ic(StartNode, EndNode))  # 노드에 추가

IcFile.close()
print('IC 개수:', len(Nodes))  # 읽은 IC의 개수 출력

GoalUrl = 'http://www.roadplus.co.kr/forecast/stagnation/selectStagnationView.do#none'  # 목표 URL
driver = webdriver.Chrome('C:\chromedriver.exe')


def GetResult():  # 검색 버튼을 누르고 출력
    SearchBtn.click()  # 검색 오래걸린다...
    print('검색버튼 클릭')
    time.sleep(7)  # 10초의 기다림
    ResultHour = driver.find_element_by_id('tgHour')
    ResultMin = driver.find_element_by_id('tgMin')
    print(ResultHour.text)
    print(ResultMin.text)


driver.implicitly_wait(3)  # 드라이버 로드를 위해 기다림
driver.get(GoalUrl)  # 페이지 오픈
# time.sleep(3)  # 로딩 기다리기

driver.find_element_by_xpath("//a[@class='btn btn_mint_circle']").click()
print('TG간 소요시간 예상 버튼 클릭')

InputStart = driver.find_element_by_id('ST_NODE_ID_NM')  # 시작 input
InputEnd = driver.find_element_by_id('ED_NODE_ID_NM')  # 도착 input
NextBtn = driver.find_element_by_id('tgNextTime')  # 시간 다음 버튼
PrevBtn = driver.find_element_by_id('tgPreTime')  # 시간 이전 버튼
SearchBtn = driver.find_element_by_id('tgBtnSearch')  # 검색 버튼
ResultTime = driver.find_element_by_id('tgStime')  # 검색 시간
DatePicker = driver.find_element_by_id('datepicker2')  # 날짜 선택

for i in range(len(Nodes)):
    InputStart.clear()
    InputEnd.clear()

    InputStart.send_keys(Nodes[i].getStartNode())  # 시작 IC 입력
    time.sleep(1.5)  # 자동완성 입력까지 딜레이

    startOnclick = NodeOnclick.getStartOnClick(Nodes[i].getStartNode())
    driver.execute_script(startOnclick)

    InputEnd.send_keys(Nodes[i].getEndNode())  # 도착 IC 입력

    time.sleep(1.5)

    endOnclick = NodeOnclick.getEndOnClick(Nodes[i].getEndNode())
    driver.execute_script(endOnclick)  # 도착 입력 스크립트 실행

    dates = driver.find_elements_by_xpath("//td[@*]/a[@href='#']")  # 날짜 입력 클릭 가능
    print(len(dates))
    for dateIndex in range(6):  # 7일 동안
        DatePicker.click()  # 날짜 선택
        date = dates[dateIndex + 1].click()  # 날짜 진짜 선택
        CurrentTime = ResultTime.get_attribute('value')  # 현재 선택되어 있는 시간
        
        while CurrentTime != '00 : 00': # 이전 시간으로 변경
            PrevBtn.click()
            CurrentTime = ResultTime.get_attribute('value')  # 선택 시간 업데이트

        while CurrentTime != '23 : 00':  # 이후 시간으로 변경
            NextBtn.click()
            GetResult() # 결과 반환
            CurrentTime = ResultTime.get_attribute('value')  # 선택 시간 업데이트

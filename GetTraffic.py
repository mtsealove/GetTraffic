from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from multiprocessing import Process, Queue
import time
import FileRW
import IC

Results = []


def GetResult(StartIC, EndIC, Date, CurrentTime, driver, ResultFile):  # 검색 버튼을 누르고 출력
    SearchBtn = driver.find_element_by_id('tgBtnSearch')  # 검색 버튼
    SearchBtn.send_keys(Keys.ENTER)  # 검색 오래걸린다...
    time.sleep(5)  # 10초의 기다림
    ResultHour = driver.find_element_by_id('tgHour')
    ResultMin = driver.find_element_by_id('tgMin')
    print("시간대: " + CurrentTime)
    print(ResultHour.text + "시간 " + ResultMin.text + "분")
    ResultFile.Write(StartIC, EndIC, Date, CurrentTime, ResultHour.text + " : " + ResultMin.text)


def OneThread(Nodes, FileName):
    ResultFile=FileRW.Result(FileName)

    GoalUrl = 'http://www.roadplus.co.kr/forecast/stagnation/selectStagnationView.do#none'  # 목표 URL
    driver = webdriver.Chrome('chromedriver.exe')
    NodeOnclick = FileRW.NodeFIle()

    driver.implicitly_wait(3)  # 드라이버 로드를 위해 기다림
    driver.get(GoalUrl)  # 페이지 오픈
    # time.sleep(3)  # 로딩 기다리기

    driver.find_element_by_xpath("//a[@class='btn btn_mint_circle']").click()
    print('TG간 소요시간 예상 버튼 클릭')

    InputStart = driver.find_element_by_id('ST_NODE_ID_NM')  # 시작 input
    InputEnd = driver.find_element_by_id('ED_NODE_ID_NM')  # 도착 input
    NextBtn = driver.find_element_by_id('tgNextTime')  # 시간 다음 버튼
    PrevBtn = driver.find_element_by_id('tgPreTime')  # 시간 이전 버튼
    ResultTime = driver.find_element_by_id('tgStime')  # 검색 시간
    DatePicker = driver.find_element_by_id('datepicker2')  # 날짜 선택

    for i in range(len(Nodes)):  # 노드 개수만큼
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

        for index in range(7):  # 7일 동안
            DatePicker.send_keys(Keys.ENTER)  # 날짜 선택 클릭

            date = driver.find_elements_by_xpath(
                "//table[@class='ui-datepicker-calendar']/tbody/tr/td[@data-handler='selectDay']/a")[index + 1]
            date.send_keys(Keys.ENTER)
            CurrentDate = driver.find_element_by_id('datepicker2').get_attribute('value')
            print("날짜 클릭함")
            CurrentTime = ResultTime.get_attribute('value')  # 현재 선택되어 있는 시간

            while CurrentTime != '01 : 00':  # 이전 시간으로 변경
                CurrentTime = ResultTime.get_attribute('value')  # 선택 시간 업데이트
                PrevBtn.click()
                time.sleep(0.2)

            isFirst = True
            while CurrentTime != '23 : 00':  # 이후 시간으로 변경
                if not isFirst:
                    NextBtn.send_keys(Keys.ENTER)
                if isFirst:
                    isFirst = False
                CurrentTime = ResultTime.get_attribute('value')  # 선택 시간 업데이트
                GetResult(Nodes[i].getStartNode(), Nodes[i].getEndNode(), CurrentDate, CurrentTime, driver, ResultFile)  # 결과 반환


def run():
    AllNodes = []
    IcFile = open('ICList.csv', 'r')  # IC 파일을 읽어옴
    while True:
        line = IcFile.readline()
        if not line: break
        StartNode = line.split(',')[0]
        EndNode = line.split(',')[1]
        AllNodes.append(IC.Ic(StartNode, EndNode))  # 노드에 추가

    IcFile.close()
    print('IC 개수:', len(AllNodes))  # 읽은 IC의 개수 출력
    nodeCount = len(AllNodes)
    nodeExt = nodeCount % 4
    NodesSp = []
    for i in range(4):
        NodesSp.append([])

    index = 0
    for node in AllNodes:  # 4개로
        NodesSp[index].append(node)
        index += 1
        if index == 4:
            index = 0

    if __name__ == '__main__':
        pr0 = Process(target=OneThread, args=(NodesSp[0], '.\\data\\Result0.csv'))
        pr1 = Process(target=OneThread, args=(NodesSp[1], '.\\data\\Result1.csv'))
        pr2 = Process(target=OneThread, args=(NodesSp[2], '.\\data\\Result2.csv'))
        pr3 = Process(target=OneThread, args=(NodesSp[3], '.\\data\\Result3.csv'))
        pr0.start()
        pr1.start()
        pr2.start()
        pr3.start()

        pr0.join()
        pr1.join()
        pr2.join()
        pr3.join()


run()
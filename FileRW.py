class Node(object):
    def __init__(self, NodeName, onClick):
        self.NodeName = NodeName
        self.onClick = onClick

    def getNodeName(self):
        return self.NodeName

    def getOnClick(self):
        return self.onClick


class NodeFIle(object):
    StartNodes = []
    EndNodes = []

    def __init__(self):
        StartFile = open('StartNode.csv', 'r')
        EndFile = open('EndNode.csv', 'r')
        while True:  # 시작 노드 읽기
            line = StartFile.readline()
            if not line: break
            Nm = line.split('\t')[0]
            onclick = line.split('\t')[1]
            self.StartNodes.append(Node(Nm, onclick))
        StartFile.close()

        print(len(self.StartNodes))
        while True:  # 종료 노드 읽기
            line = EndFile.readline()
            if not line: break
            Nm = line.split('\t')[0]
            onclick = line.split('\t')[1]
            self.EndNodes.append(Node(Nm, onclick))
        EndFile.close()
        print(len(self.EndNodes))

    def getStartOnClick(self, NodeName):  # 시작 노드의 onclick 반환
        for node in self.StartNodes:
            if node.getNodeName() == NodeName:
                return node.getOnClick()

    def getEndOnClick(self, NodeName):  # 종료 노드의 onclick 반환
        for node in self.EndNodes:
            if node.getNodeName() == NodeName:
                return node.getOnClick()


class Result(object):

    def __init__(self, FileName):  # 파일 생성 및 기본 정보 설정
        self.FileName=FileName
        self.ResultFile = open(FileName, 'w')
        self.ResultFile.write('시작 IC,도착 IC,날짜,시간대,예상 시간\n')
        self.ResultFile.close()

    def Write(self, StartIC, EndIC, Date, StdTime, PredictionTime):
        self.ResultFile=open(self.FileName, 'a')
        self.ResultFile.write(StartIC+",")
        self.ResultFile.write(EndIC+",")
        self.ResultFile.write(Date+",")
        self.ResultFile.write(StdTime+",")
        self.ResultFile.write(PredictionTime+"\n")
        self.ResultFile.close()
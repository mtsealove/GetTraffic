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

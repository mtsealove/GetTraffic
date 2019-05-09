class Ic(object):
    def __init__(self, StartNode, EndNode):
        self.StartNode = (StartNode.replace("\n", "")).replace(" ", "")  # 시작 IC
        self.EndNode = (EndNode.replace("\n", "")).replace(" ", "")  # 도착 IC

    def getStartNode(self):
        return self.StartNode

    def getEndNode(self):
        return self.EndNode


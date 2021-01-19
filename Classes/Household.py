class Household:
    def __init__(self,id=0,C=0,C_NT=0,L_max=0,list_DS=[],list_GE=[],list_MQ=[],list_RE=[],list_ME=[],list_appliance=[],list_storage=[],list_renewable=[]):
        self.id = id
        self.C = C
        self.C_NT = C_NT
        self.L_max = L_max
        self.list_DS = list_DS
        self.list_GE = list_GE
        self.list_MQ = list_MQ
        self.list_RE = list_RE
        self.list_ME = list_ME
        self.list_appliance = list_appliance
        self.list_storage = list_storage
        self.list_renewable = list_renewable
        pass

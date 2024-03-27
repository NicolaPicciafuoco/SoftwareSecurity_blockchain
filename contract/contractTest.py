from deploy import ContractInteractions


class Patient:

    def __init__(self):
        self.address = "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4"

class Medic:

    def __init__(self):
        self.address = "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2"
        self.private_key = test.private_key


test = ContractInteractions()
patient = Patient()
medic = Medic()


test.log_action(patient, medic, "Create")

test.log_action(patient, medic, "Update")

test.log_action(patient, medic, "Delete")

test.log_action(patient, medic, "Read")
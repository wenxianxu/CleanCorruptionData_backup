

class litigant(object):
    """
    litigant basic information.
    """

    docid = ''
    name = ''
    gender = ''
    birthday = ''

    
    def __init__(self, docid):
        self.docid = docid

    def set_name(self, name):
        self.name = name
    
    def set_name(self, gender):
        self.gender = gender

    def set_name(self, birthday):
        self.birthday = birthday

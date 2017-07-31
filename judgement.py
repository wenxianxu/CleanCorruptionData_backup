
import textAnalysis

class judgement(object):
    """
    judgement document basic information.
    """

    def set_contenthtml(self, content_html):
        self.content_html = content_html

    def get_contenthtml(self):
        return self.content_html

class criminalJudgement(judgement):
    """
    criminal judgement document.
    """

    content_html = ""
    paragraphs = []

    litigant_list = []
    
    def __init__(self, sql_line):
        self.docid = sql_line.docid
        self.content_html = sql_line.content_html
        self.paragraphs = textAnalysis.paragraphing(sql_line.content_html)
        self.content_progress = sql_line.content_progress

        #self.get_litigants()

        #self.litigant_list = textAnalysis.get_litigant_list(sql_line.content_html, sql_line.docid)

    def get_litigants(self):
        if self.content_progress == "一审":
            litigant_list = textAnalysis.get_litigants_FI(self.paragraphs)

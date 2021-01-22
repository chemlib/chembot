from PyPDF2 import PdfFileReader
import io
import requests
import qparser
import random
import pickle

def random_question() -> dict:
    while True:
        try:
            grp = random.randint(1, 12)
            rond = random.randint(1, 14)
            with open(f"sets/group{grp}/round{rond}.txt", 'rb') as f:
                p = pickle.load(f)
            q = random.choice(p.questions)
            if q['Subject']in ('MATH'): raise ValueError
            if q['Type'] != 'Multiple Choice': raise ValueError
            if len(q['Question']) > 256: raise ValueError
            return q
        except:
            return random_question()

class Packet():
    def __init__(self, url: str) -> None:
        r = requests.get(url)
        f = io.BytesIO(r.content)
        self.reader = PdfFileReader(f)
        self.info = self.reader.getDocumentInfo()
        self.txt = self.reader.getPage(0).extractText().strip().replace('\n','')
        self.pages = [self.reader.getPage(i) for i in range(self.reader.getNumPages())]        
        self.load_questions()
    
    def load_questions(self):
        self.questions = []
        for page in self.pages:
            self.questions.extend(qparser.parse_questions(page))
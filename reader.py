from PyPDF2 import PdfFileReader
import io
import requests
import json
import random
import re
import PyPDF2

def extract_questions(page: PyPDF2.pdf.PageObject) -> list:
    txt = page.extractText().strip().replace('\n','')
    matches = list(re.finditer(r' [1-9]\)\s+[A-Z][A-Z]| [1-9][1-9]\)\s+[A-Z][A-Z]| [1-9]\.\s+[A-Z][A-Z]| [1-9][1-9]\.\s+[A-Z][A-Z]', txt))
    questions = []
    for i in range(len(matches)):
        end = len(txt) if i == len(matches) - 1 else matches[i+1].end()
        q = txt[matches[i].start():end]
        questions.append(q)
    return [x.strip() for x in questions]

def parse_questions(page: PyPDF2.pdf.PageObject) -> list:
    rlist = []
    for q in extract_questions(page):
        try:
            qdict = {}
            splitted = re.split('\s+', q)

            try: num = int(splitted[0][:2])
            except:num = int(splitted[0][0])
            typnums = [2, 3]

            if splitted[1] == "EARTH": 
                subj = "EARTH AND SPACE"
                typnums = [4, 5]
            else: 
                subj = splitted[1]

            typ = splitted[typnums[0]] + " " + splitted[typnums[1]]

            qdict = {'Number': num, 'Subject': subj, 'Type': typ}

            if typ == 'Multiple Choice':
                quest = q[q.find(typ) + len(typ):q.find('W)')].strip()
                opts = re.split(r'[W-Z]\)', q[q.find('W)'):q.find('ANS')])[1:]
                opts = dict(zip(["W", "X", "Y", "Z"], [x.strip() for x in opts]))
                ans = re.search(r'[W-Z]\)', q[q.find('ANSWER')+7:]).group(0)[0]
                qdict.update({"Question": quest, "Options": opts, "Answer": ans})

            else: #Short Answer
                quest = q[q.find(typ) + len(typ):q.find('ANS')].strip()
                ans = q[q.find('ANSWER')+6:].strip()
                ans = re.split(r'\: | \(| [BT]O|\? ', ans)[1].strip()
                qdict.update({"Question": quest, "Answer": ans})
        except:
            continue

        rlist.append(qdict)

    return rlist

def random_question(subject: str) -> dict:
    with open(f"resources/json/{subject.upper()}.json") as f:
        data = json.load(f)

    q = {}
    while 'Options' not in q:
        q = random.choice(data)
        
    return q
        

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
            self.questions.extend(parse_questions(page))
import PyPDF2
import glob
from tqdm import tqdm
from datetime import datetime
import warnings
import os
warnings.filterwarnings("ignore", category=FutureWarning)


class PreprocessFiles:
    
    def __init__(self,path,out=""):
        if path == "":
            print("No input path.")
            return 
        else:
            self.files = glob.glob(path)
            self.out = out
            #self.convert()
        
    
    def pdf2txt(self, path, out):

        
        pdffileobj=open(path,'rb')
        pdfreader=PyPDF2.PdfFileReader(pdffileobj)
        x=pdfreader.numPages

        text = ""
        for i in range(x):
            pageobj=pdfreader.getPage(i)
            text+=pageobj.extractText()

        out_file=open(out,"a")
        out_file.writelines(text)
        
    def getMetaData(self):
        
        l = []
        for f in self.files:
            mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
            ctime = datetime.fromtimestamp(os.path.getctime(f)).strftime('%Y-%m-%d %H:%M:%S')
            size = os.path.getsize(f)
            name = f
            
            
            d = {'path':name, 'mtime': mtime, 'ctime':ctime, 'size':size/1000}
            l.append(d)
        return l
            
    
    def convertToPDF(self):

        for f in tqdm(self.files):
            self.pdf2txt(f,self.out+f.replace(".pdf",".txt"))
        
    
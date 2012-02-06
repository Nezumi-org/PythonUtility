#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys,codecs, re
from BeautifulSoup import BeautifulSoup

class MergeSourceTarget:
    '''am amount: amount spent in this transaction'''
    def __init__(self, source, target):
        self.sourceFile = source
        self.targetFile = target
        #self.endOfSentenceEng = '[.:!?]\s+'
        #self.endOfSentenceJp =u'[。:]' 
        #self.segmentDic = {}
        self.tagList = 'abstract','title', 'note', 'comment', 'warn', 'p'
        self.unwantedTag = 'path', 'uri', 'e','b'  
        self.sourceList = self.removeTags(self.sourceFile)
        self.targetList = self.removeTags(target)
        self.outFile = source + '.dat'
        index = 1
        
        #For some reasons, split by marudoes not work here.
        #but works in string from readlines() so do this in tmx.py 
        #for s in self.targetList:
         #   st = re.split(u'[。:!]', s, re.U )
            #st = s.split('。')
          #  for sn in st:
           #     print len(st), sn
                
    def removeTags(self, infile):
        infile = codecs.open(infile, encoding='utf-8')
        lines =infile.read()#load the file into a string because B.S takes string
        infile.close()
      
       # remove '\n' : \n unnecesarily appear in a middle of a sentence in some files
        noNewLines = re.sub('(\n)+', ' ', lines)           
  
        soup = BeautifulSoup(noNewLines)
        
        #remove child tags appears within the wanted tags's sentences. 
        for tag in soup.findAll(True):
            if tag.name in self.unwantedTag:
                tag.replaceWith(tag.renderContents())
        #print soup.renderContents() 
        
        #build a list of texts from the wanted tags's content
        list = []
        for tag in self.tagList:
            for t in soup(tag):
                list.append(t.renderContents().strip())        
        return list    
        
    def write(self):
        out = open( self.outFile, 'w')
        index = 1
        for (s,t) in zip(self.sourceList,self.targetList):
           #self.segmentDic[s] = t
            #out.write(str(index))
            #out.write(': ')
            out.write('EN: ')
            out.write(s)
            out.write('\n')
            out.write('JP: ')
            out.write(t)
            out.write('\n')
            index = index + 1

    def writeSingleFile(self):
        for tag in self.tagList:
            header = 'Tag: ' + tag + '| The number of tag:' + str(len(soup(tag)))+'-------------------\n'
            outFile.write(header)
        #outFile.write('\n')
            id = 1 
            for t in soup(tag):
                outFile.write(str(id))
                outFile.write(': ')
                outFile.write( t.renderContents().strip())
                outFile.write('\n')
                id = id + 1
            outFile.write('\n')    
        outFile.close()
    
if __name__=='__main__':

    if len(sys.argv) < 3:
        print 'Usage: \'python ', sys.argv[0], ' eg.xml jp.xml\''
        sys.exit
    m = MergeSourceTarget(sys.argv[1],sys.argv[2])

    m.write()
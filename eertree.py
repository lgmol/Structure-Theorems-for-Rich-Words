from morphisms import *

class eerTree():

    def __init__(self,word):
        self._word=''
        self._vertices={'':0,-1:-1}
        self._edges={'':{},-1:{}}
        self._links={'':-1,-1:-1}
        self._palSuf=-1
        self._palSufStack=[-1]
        self._newPalStack=[None]
        self._numPals=0
        for i in range(len(word)):
            self.add(word[i])
       
    def __repr__(self):
        return "An eerTree for a string with %s palindromes."%(self._numPals)
    
    def DistinctPalindromes(self):
        D={}
        L=self._palSufStack
        for i in range(1,len(L)):
            if L[i] not in D.keys():
                D[L[i]]=self._word[0:i]
        return D
   
    def add(self,letter):
        cs=self._palSuf
        self._newPal=False
        
        while not cs==-1:
            
            if len(cs)==len(self._word):
                cs=self._links[cs]
            
            csl=self._vertices[cs]
            
            if self._word[-csl-1]==letter:
                
                pal=letter+cs+letter
                
                if self._edges[cs].get(letter)==None:
                    self._newPal=True
                    self._vertices[pal]=len(pal)
                    self._edges[pal]={}
                    self._edges[cs][letter]=pal
                    ns=self._links[cs]
                    
                    while not ns==-1:
                        nsl=self._vertices[ns]
                        if self._word[-nsl-1]==letter:
                            
                            nextpal=letter+ns+letter
                            break
                        
                        ns=self._links[ns]
                            
                    if ns==-1:
                        nextpal=letter
                        
                    self._links[pal]=nextpal
                
                self._palSuf=pal
                
                break
            
            cs=self._links[cs]
            
        if cs==-1:
            if self._edges[cs].get(letter)==None:
                self._newPal=True
                self._vertices[letter]=1
                self._edges[letter]={}
                self._edges[-1][letter]=letter
                self._links[letter]=''
            self._palSuf=letter
            
        self._word+=letter
        self._palSufStack+=[self._palSuf]
        # print(self._word,self._palSuf,self._newPal)
        if self._newPal:
            self._newPalStack+=[cs]
            self._numPals+=1
        else:
            self._newPalStack+=[None]
        
    def pop(self):
        u=self._palSuf
        indicator=self._newPalStack.pop()
        if not indicator==None:
            del self._vertices[u]
            del self._links[u]
            del self._edges[u]
            self._numPals-=1
                
            if len(u)>1:
                v=u[1:-1]
            else:
                v=-1
            del self._edges[v][u[-1]]
        
        self._palSufStack.pop()
        self._palSuf=self._palSufStack[-1]
        self._word=self._word[:-1]
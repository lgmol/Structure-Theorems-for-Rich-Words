class morphism():

    def __init__(self,blocks):
        
        self._blocks=blocks

        self._input_alphabet_size=len(blocks)

        self._input_alphabet=[str(a) for a in range(self._input_alphabet_size)]

        def longest_common_prefix(u,v):
          i=0
          p=''
          l=min(len(u),len(v))
          while i<l and u[i]==v[i]:
              p+=u[i]
              i+=1
          return p
        
        def longest_common_suffix(u,v):
            return longest_common_prefix(u[::-1],v[::-1])[::-1]
        
        self._lcp=self.apply('0')
        for a in self._input_alphabet:
            self._lcp=longest_common_prefix(self._lcp,self.apply(a))
        self._lcs=self.apply('0')
        for a in self._input_alphabet:
            self._lcs=longest_common_suffix(self._lcs,self.apply(a))
      
            



        max_letter=0
        for block in blocks:
            for i in range(len(block)):
                if int(block[i])>max_letter:
                    max_letter=int(block[i])
        self._output_alphabet_size=max_letter+1

        self._matrix=[[blocks[j].count(str(i)) for j in range(self._input_alphabet_size)] for i in range(self._output_alphabet_size)]

        self._prefix_letters=[]
        for a in self._input_alphabet:
            for b in self._input_alphabet:
                if a!=b and self.apply(b).startswith(self.apply(a)):
                    self._prefix_letters.append(a)
                    break
        
        def input_strings(n):
            if n==0:
                return ['']
            else:
                S=[]
                for w in input_strings(n-1):
                    for a in self._input_alphabet:
                        S.append(w+a)
                return S
        
        self._length_one_extensions=input_strings(0)+input_strings(1)
        self._length_two_extensions=input_strings(0)+input_strings(1)+input_strings(2)
        
        self._left_extensions=dict()
        for a in self._length_one_extensions:
            for b in self._length_one_extensions:
                image_a=self._lcs+self.apply(a)
                image_b=self._lcs+self.apply(b)
                lcs=longest_common_suffix(image_a,image_b)
                l=len(lcs)
                next_a=image_a[-l-1] if len(image_a)>l else ''
                next_b=image_b[-l-1] if len(image_b)>l else ''
                self._left_extensions[(a,b)]=(Parikh(lcs,self._output_alphabet_size),next_a,next_b) 

        self._right_extensions=dict()
        for a in self._length_one_extensions:
            for b in self._length_one_extensions:
                image_a=self.apply(a)+self._lcp
                image_b=self.apply(b)+self._lcp
                lcp=longest_common_prefix(image_a,image_b)
                l=len(lcp)
                next_a=image_a[l] if len(image_a)>l else ''
                next_b=image_b[l] if len(image_b)>l else ''
                self._right_extensions[(a,b)]=(Parikh(lcp,self._output_alphabet_size),next_a,next_b) 

    def apply(self,word):
        image=''
        for i in range(len(word)):
            image+=self._blocks[int(word[i])]
        return image
    
    def iterate(self,start,k):
        if k==0:
            return start
        return self.apply(self.iterate(start,k-1))
    
    def apply_matrix(self,vector):
        return [sum(self._matrix[i][j]*vector[j] for j in range(self._input_alphabet_size)) for i in range(self._output_alphabet_size)]

    def extend_repetition(self,vector,a,b,c,d):
        (lcp,next_a,next_b)=self._right_extensions[(a,b)]
        (lcs,next_c,next_d)=self._left_extensions[(c,d)]
        next_vector=[sum(x) for x in zip(self.apply_matrix(vector),lcp,lcs)]
    
        return next_vector,next_a,next_b,next_c,next_d
    
    def images_of_letters(self):
        P=''
        for a in self._input_alphabet:
            P=P+str(a)+'->'+self.apply(a)+', '
        return P[:-2]
    
    
def compose(f,g):
    return morphism([f.apply(g.apply(a)) for a in g._input_alphabet])



def iterate(f,n):
    if n==0:
        return morphism([a for a in f._input_alphabet])
    else:
        return compose(f,iterate(f,n-1))

def Parikh(w,k):
    n=len(w)
    vector=[0]*k
    for i in range(n):
        vector[int(w[i])]+=1
    return vector

def ParikhComparison(x,y,k,top,bottom):
    vecx=Parikh(x,k)
    vecy=Parikh(y,k)
    sumx=vecx[-1]
    sumy=vecy[-1]
    for i in range(1,k+1):
        if bottom*sumy<top*sumx:
            return False
        if i<k:
            sumx+=vecx[-1-i]
            sumy+=vecy[-1-i]
    return True
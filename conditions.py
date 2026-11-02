from eertree import eerTree
from morphisms import *
import itertools

quiet=True

class Condition:
    """A superclass for all conditions."""

    pass

class FunctionCondition(Condition):
    """A stateless condition."""

    def __init__(self, func):
        super().__init__()
        self.func = func

    def __str__(self):
        return f"FunctionCondition({str(self.func)})"

    def add(self, w, a):
        return self.func(w, a)

    def pop(self):
        pass

class RichnessCondition(Condition):
    """A condition that enforces richess."""

    def __init__(self):
        self.eertree = eerTree('')

    def __str__(self):
        return f'RichnessCondition()'

    def add(self, w, a):
        self.eertree.add(a)
        return f'This word is not rich, as it contains a complete return to {self.eertree._palSufStack[-1]} which is not a palindrome.' if not self.eertree._newPal else None

    def pop(self):
        self.eertree.pop()

class RichnessAndCompatibilityCondition(Condition):
    """A condition that enforces richness and compatibility of returns to a specified word (marker) with all factors in a specified list (known_factors)"""

    def __init__(self,marker,known_factors):
        self.eertree = eerTree('')
        self.marker = marker
        self.known_factors = known_factors
        p=marker
        known_prefixes={}
        for u in known_factors:
            assert u[:len(p)]==p, 'Known factors must begin with the marker.'
            Tu=eerTree(u)
            Du=Tu.DistinctPalindromes()
            for q in Du.keys():
                # if nonoverlapping(p,q):
                    if q in known_prefixes.keys():
                        assert Du[q]==known_prefixes[q], f'The given factors contain different shortest prefixes with the palindrome {q}: {Du[q]} and {known_prefixes[q]}.'
                    else:
                        known_prefixes[q]=Du[q]
        self.known_prefixes=known_prefixes

    def __str__(self):
        return f'RichnessAndCompatibilityCondition({self.marker},{self.known_factors})'

    def add(self,w,a):
        self.eertree.add(a)
        q=self.eertree._palSufStack[-1]
        if not self.eertree._newPal:
            return f'This word is not rich, as it contains a complete return to {q} which is not a palindrome.'
        elif q in self.known_prefixes.keys():
            if not (w+a).startswith(self.known_prefixes[q]):
                return f'This word is incompatible with the marker, as their longest common prefix does not contain {q}.'
        return None
    
    def pop(self):
        self.eertree.pop()

class ForbiddenSuffixCondition(Condition):
    """A condition that enforces no factors from a specified list (forbidden)."""

    def __init__(self, forbidden):
        for x in forbidden:
            assert len(x) > 0, 'Forbidden factors must be nonempty.'
        self.forbidden = forbidden

    def __str__(self):
        return f'ForbiddenSuffixCondition({self.forbidden})'

    def add(self, w, a):
        for x in self.forbidden:
            if (w+a).endswith(x):
                return f'This word contains the forbidden factor {x}.'
        return None

    def pop(self):
        pass


def PermutationClass(w,k):
    """Computes all permutations of a word w over k letters."""
    
    id=''
    for i in range(k):
        id+=str(i)

    C=[]
    for P in itertools.permutations(id):
        Pw=''
        for i in range(len(w)):
            Pw+=P[int(w[i])]
        if Pw not in C:
            C+=[Pw]
    return C

def largest_int(w):
    m=0
    n=len(w)
    for i in range(len(w)):
        if int(w[i])>m:
            m=int(w[i])
    return m
    
class PowerSuffixCondition(Condition):
    """A condition that enforces top/bottom-power-freeness."""
    
    def __init__(self, top, bottom):
        self.top=top
        self.bottom=bottom
        pass
    
    def __str__(self):
        return f'PowerSuffixCondition({self.top},{self.bottom})'

    def add(self, w, a):
        wa=w+a
        n = len(wa)
        p = 1
        while n*self.bottom >= p*self.top:
            i = 0
            while 1+i+p<=n and wa[-1 - i] == wa[-1 - i - p]:
                if (i + 1 + p)*self.bottom >= p*self.top:
                    return f'This word contains the {self.top}/{self.bottom}-power {wa[-1 - i - p:]}.'
                i += 1
                if i + p >= n:
                    break
            p += 1

        return None
    
    def pop(self):
        pass


# def lexicographically_smallest_permutation(w,k):
#     order_of_appearance=[]
#     i=0
#     while i<len(w) and len(order_of_appearance)<k:
#         if int(w[i]) not in order_of_appearance:
#             order_of_appearance.append(int(w[i]))
#         i+=1
#     for i in range(k):
#         if i not in order_of_appearance:
#             order_of_appearance.append(i)
#     P=[0]*k
#     for i in range(k):
#         P[order_of_appearance[i]]=str(i)
#     P=morphism(P)

#     return P.apply(w)

class LexicographicCondition(Condition):
    """A condition that enforces the lexicographic trick described in Lemma 6.2."""
    
    def __init__(self,prefix):
        self.prefix=prefix
        self.length=len(prefix)
        pass
    
    def __str__(self):
        return f'LexicographicCondition({self.prefix})'
    
    def add(self,w,a):
        wa=w+a
        n=len(wa)-self.length
        for p in range(1,n):
            if wa[-p-self.length:-p]==self.prefix and wa[-p:]<wa[self.length:p+self.length]:
                return f'This word has factor {wa[-p-self.length:]}, which has prefix {self.prefix} and is less than {wa} in the lexicographic order.'
        
        return None
            
    def pop(self):
        pass
    


# Persistent Powers

def power_from_parikh_vectors(y,x,top,bottom):
    k=len(y)
    if not quiet:
        print(sum(y)/sum(x),sum(y),sum(x))
    if bottom*sum(y)<top*sum(x):
        return False
    return True

def top_heavy_power_from_parikh_vectors(y,x,top,bottom):  # If y=x^r, checks if x^r is a top-heavy factor of exponent at least top/bottom
    k=len(x)
    sumx=x[-1]
    sumy=y[-1]
    for i in range(1,k+1):
        if bottom*sumy<top*sumx:
            return False
        if i<k:
            sumx+=x[-1-i]
            sumy+=y[-1-i]
    return True

def is_persistent(y,x,left_extension,right_extension,psi,phi,pi,outer_top,outer_bottom,max_tipping_point):
        
        p=len(x)

        if psi==None:
            k=phi._input_alphabet_size  
        else:
            k=psi._input_alphabet_size

        xvec=Parikh(x,k)
        yvec=Parikh(y,k)

        alphabet=[str(a) for a in range(k)]

        right_periodic_extension=y[-p]
        left_periodic_extension=y[p-1]
        
        if psi==None:
            next_xvec,next_yvec,next_re,next_rpe,next_le,next_lpe=xvec,yvec,right_extension,right_periodic_extension,left_extension,left_periodic_extension
        else:
            next_yvec,next_re,next_rpe,next_le,next_lpe=psi.extend_repetition(yvec,right_extension,right_periodic_extension,left_extension,left_periodic_extension)
            next_xvec=psi.apply_matrix(xvec)
        if not quiet:
            print(f'xvec: {next_xvec}, yvec: {next_yvec}, re: {next_re}, rpe: {next_rpe}, le: {next_le}, lpe: {next_lpe}')
            

        i=0
        while i<=max_tipping_point:
            if not quiet:
                print(i)
            if top_heavy_power_from_parikh_vectors(next_yvec,next_xvec,outer_top,outer_bottom):
                if not quiet:
                    print(f'{left_extension+y+right_extension},{x}: Found a top-heavy {outer_top}/{outer_bottom}-power after {i} additional iterates.')
                return [True,i]
            j=0
            pi_xvec,pi_yvec,pi_re,pi_rpe,pi_le,pi_lpe=next_xvec,next_yvec,next_re,next_rpe,next_le,next_lpe
            pi_yvec,_,_,_,_=pi.extend_repetition(pi_yvec,pi_re,pi_rpe,pi_le,pi_lpe)
            pi_xvec=pi.apply_matrix(pi_xvec)
            if not quiet:
                print(f'pi_xvec: {pi_xvec}, pi_yvec: {pi_yvec}')
            if not power_from_parikh_vectors(pi_yvec,pi_xvec,outer_top,outer_bottom):
                if not quiet:
                    print(f'{left_extension+y+right_extension},{x}: No {outer_top}/{outer_bottom}-power after applying phi {i} additional times followed by pi.')
                return False
            i+=1
            next_yvec,next_re,next_rpe,next_le,next_lpe=phi.extend_repetition(next_yvec,next_re,next_rpe,next_le,next_lpe)
            next_xvec=phi.apply_matrix(next_xvec)
            if not quiet:
                print(f'xvec: {next_xvec}, yvec: {next_yvec}, re: {next_re}, rpe: {next_rpe}, le: {next_le}, lpe: {next_lpe}')            
        if i==max_tipping_point+1: 
            assert False, f'{left_extension+y+right_extension},{x}: Max tipping point exceeded!'               
                                
        return False

class PersistentCondition(Condition):
    """A condition that enforces top/bottom-persistent-power-freeness with respect to pi and phi."""
    
    def __init__(self,psi,phi,pi,known_pre_seeds,outer_top,outer_bottom,max_tipping_point):
        self.outer_top=outer_top
        self.outer_bottom=outer_bottom
        self.known_pre_seeds=known_pre_seeds
        self.psi=psi
        self.phi=phi
        self.pi=pi
        self.max_tipping_point=max_tipping_point
        self.alphabet_size=self.psi._input_alphabet_size if psi!=None else self.phi._input_alphabet_size
        self.alphabet=[str(a) for a in range(self.alphabet_size)]
        self.largest_observed_tipping_point=0
        pass
    
    def __str__(self):
        return f'PersistentCondition({self.outer_top},{self.outer_bottom})'
    
    def HasSuffix(self,w,s):
        n=len(s)
        if len(w)>n and w[-n:]==s:
            return True
        return False   
    
    def add(self, w, a):
        wa=w+a
        # for x in self.known_pre_seeds:
        #     if wa.endswith(x):
        #         return x
        
        for p in range(1,len(wa)+1):
            if p==1:
                inner_top=1
                inner_bottom=1
            else:
                inner_top=2*p-1
                inner_bottom=p
            i=0
            while i+p+1<=len(wa) and wa[-i-p-1]==wa[-i-1]:
                i+=1
            if (i+p)*inner_bottom>=p*inner_top:
                y=wa[-i-p:]
                x=y[0:p]
                candidate=[y,x,'','']
                bad_seed=is_persistent(*candidate,self.psi,self.phi,self.pi,self.outer_top,self.outer_bottom,self.max_tipping_point)
                if bad_seed:
                    seed=y
                    self.known_pre_seeds.append(seed)
                    
                    if bad_seed[1]>self.largest_observed_tipping_point:
                        self.largest_observed_tipping_point=bad_seed[1]
              
                    return f'This word contains the factor {candidate[2]+candidate[0]+candidate[3]}, and the corresponding bookended repetition ({candidate[2]},{candidate[0]},{candidate[3]},{candidate[1]}) is {self.outer_top}/{self.outer_bottom}-persistent with tipping point {bad_seed[1]}.'

                if i+p<len(wa):
                    left_extension=wa[-i-p-1]
                    candidate=[y,x,left_extension,'']
                    bad_seed=is_persistent(*candidate,self.psi,self.phi,self.pi,self.outer_top,self.outer_bottom,self.max_tipping_point)
                    if bad_seed: 
                        seed=left_extension+y
                        self.known_pre_seeds.append(seed)

                        if bad_seed[1]>self.largest_observed_tipping_point:
                            self.largest_observed_tipping_point=bad_seed[1]
                        return f'This word contains the factor {candidate[2]+candidate[0]+candidate[3]}, and the corresponding bookended repetition ({candidate[2]},{candidate[0]},{candidate[3]},{candidate[1]}) is {self.outer_top}/{self.outer_bottom}-persistent with tipping point {bad_seed[1]}.'                  
                                             
        for p in range(1,len(w)+1):
            if p==1:
                inner_top=1
                inner_bottom=1
            else:
                inner_top=2*p-1
                inner_bottom=p
            i=0
            if 1+p<=len(wa) and wa[-1]!=wa[-1-p]:
                while i+p+1<=len(w) and w[-i-p-1]==w[-i-1]:
                    i+=1
                if (i+p)*inner_bottom>=p*inner_top:
                    y=w[-i-p:]
                    x=y[0:p]
                    candidate=[y,x,'',a]
                    bad_seed=is_persistent(*candidate,self.psi,self.phi,self.pi,self.outer_top,self.outer_bottom,self.max_tipping_point)
                    if bad_seed:
                        seed=y+a
                        self.known_pre_seeds.append(seed)
                        
                        if bad_seed[1]>self.largest_observed_tipping_point:
                            self.largest_observed_tipping_point=bad_seed[1]
                        return f'This word contains the factor {candidate[2]+candidate[0]+candidate[3]}, and the corresponding bookended repetition ({candidate[2]},{candidate[0]},{candidate[3]},{candidate[1]}) is {self.outer_top}/{self.outer_bottom}-persistent with tipping point {bad_seed[1]}.'
                                                
                    if i+p<len(w):
                        left_extension=w[-i-p-1]
                        candidate=[y,x,left_extension,a]
                        bad_seed=is_persistent(*candidate,self.psi,self.phi,self.pi,self.outer_top,self.outer_bottom,self.max_tipping_point)
                        if bad_seed:
                            seed=left_extension+y+a
                            self.known_pre_seeds.append(seed)

                            if bad_seed[1]>self.largest_observed_tipping_point:
                                self.largest_observed_tipping_point=bad_seed[1]
                            return f'This word contains the factor {candidate[2]+candidate[0]+candidate[3]}, and the corresponding bookended repetition ({candidate[2]},{candidate[0]},{candidate[3]},{candidate[1]}) is {self.outer_top}/{self.outer_bottom}-persistent with tipping point {bad_seed[1]}.'
                                   
        return None     
        
    def pop(self):
        pass
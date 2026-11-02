from backtrack import *
from morphisms import *
import itertools

quiet = True

def compatible_pair(p,u,v):
    Tu=eerTree(u)
    Tv=eerTree(v)
    Du=Tu.DistinctPalindromes()
    Dv=Tv.DistinctPalindromes()
    for q in Du.keys():
        if q in Dv.keys():
            if not Du[q]==Dv[q]:
                # print(f'Different shortest prefixes containing the palindrome {q}: {u[0:Du[q]]} and {v[0:Dv[q]]}')
                return False
                
    return True

def compatible_with_all(p,u,V):
    for v in V:
        if not compatible_pair(p,u,v):
            return False
    return True

def maximal_compatible_sets(p,U):
    
    current_compatible_sets=[]
    maximal=[]
    
    for u in U:
        if u.startswith(p):
            current_compatible_sets.append(set([u]))

    while len(current_compatible_sets)>0:
        next_compatible_sets=[]
        for V in current_compatible_sets:
            maximal_indicator=1
            for u in U:
                if not u in V and compatible_with_all(p,u,V):
                    maximal_indicator=0
                    new_compatible_set=set(V)
                    new_compatible_set.add(u)
                    if not new_compatible_set in next_compatible_sets:
                        next_compatible_sets.append(new_compatible_set)
            if maximal_indicator==1:
                V=list(V)
                V.sort(key=len)
                V.sort(key=largest_int)
                if not V in maximal:
                    maximal.append(V)
        current_compatible_sets=next_compatible_sets
    
    # print(len(maximal))
    # for M in maximal:
    #     print(len(M),M)

    return maximal

def inner_layers(top,bottom,backtrack_length,pi_hat,phi,num_phi_iterates,max_tipping_point):

    print(f'Consider a recurrent word x such that phi^{num_phi_iterates}(x) is rich and x contains no {top}/{bottom}-persistent bookended repetition with respect to phi and pi_hat.')

    # We first show that x must contain 0.

    largest_observed_tipping_point=0
    
    preconditions = [                                      
            RichnessCondition(),
            PersistentCondition(None,phi,pi_hat,[],top,bottom,max_tipping_point),
            ForbiddenSuffixCondition(['0'])
        ]
    postconditions = [
            RichnessCondition()
    ]
    w,l,tip = backtrack(backtrack_length, phi._input_alphabet_size, preconditions=preconditions, postconditions=postconditions, prefix='', morph=iterate(phi,num_phi_iterates), quiet=quiet)
    assert w==None and type(l)==int,'Proof of structure theorem failed at beginning of inner layer: Unable to show that x contains 0.'
    if tip>largest_observed_tipping_point:
        largest_observed_tipping_point=tip

    print('')
    print(f'We see that x contains 0, as the longest word with no 0 whose image under phi^{num_phi_iterates} is rich and which contains no {top}/{bottom}-persistent bookended repetition with respect to phi and pi_hat has length {l}.')
    print(f'The largest tipping point of a {top}/{bottom}-persistent repetition encountered in this search was {tip}.')
    print('')

    # Now we find the set of all possible return words to the marker 0 in x.

    marker='0'
    preconditions = [                                      
        RichnessCondition(),
        # PowerSuffixCondition(top, bottom),
        # ForbiddenSuffixCondition(known_post_seeds)
        PersistentCondition(None,phi,pi_hat,[],top,bottom,max_tipping_point)
        # ForbiddenSuffixCondition() 
    ]
    postconditions = [
        RichnessCondition()
        # PowerSuffixCondition(top,bottom)  
    ]
    S = ReturnWords(n=backtrack_length, k=phi._input_alphabet_size, marker=marker, preconditions=preconditions,postconditions=postconditions,morph=iterate(phi,num_phi_iterates),prefix=marker, quiet=quiet)
    assert S!=False, 'The search for possible returns to 0 in x did not finish.'
    print(f'By a backtracking search for complete returns to 0 in x, the only possible return words to 0 in x are the following:')
    print(S)
    print('')

    # Now we find all maximal compatible sets among these possible returns to 0.

    MCS=maximal_compatible_sets('0',S)
    print(f'There are {len(MCS)} maximal compatible subsets of S, each corresponding to a morphism listed below:')
    count=0
    for psi in MCS:
        psi=morphism(psi)
        count+=1
        print(f'psi_{count}: {psi.images_of_letters()}')

    # Each compatible set corresponds to a morphism psi.  So we have x=psi(y) for one of these morphisms psi.
    # Our goal is to show that in fact psi=phi is the only morphism such that there is an infinite word y for which pi_hat(phi^n(psi(y))) is top/bottom-free and rich.  We do this using a backtracking search for each psi!=phi.

    count=0
    for psi in MCS:
        psi=morphism(psi)
        count+=1
        print('')

        if psi._blocks==phi._blocks:
            
            print(f'psi_{count}:{psi.images_of_letters()} is equal to phi.')
            
        else:
            
            print(f'Now checking psi_{count}: {psi.images_of_letters()}.')
            
            w,l,tip=backtrack(backtrack_length,psi._input_alphabet_size,
                              preconditions=[RichnessCondition(),PersistentCondition(psi,phi,pi_hat,[],top,bottom,max_tipping_point)],
                              postconditions=[RichnessCondition()],
                              morph=compose(iterate(phi,num_phi_iterates),psi),quiet=quiet)
            assert w==None and type(l)==int,f'Proof of the inner layers of the structure theorem failed at morphism number {count}.'
            if tip>largest_observed_tipping_point:
                    largest_observed_tipping_point=tip
                
            print(f'The longest word y such that phi^{num_phi_iterates}(psi_{count}(y)) is rich and psi_{count}(y) contains no {top}/{bottom}-persistent bookended repetition with tipping point at most {max_tipping_point} has length {l}.')
            print(f'The largest tipping point of a {top}/{bottom}-persistent repetition encountered in the search was {tip}.')


    print('')
    print(f'The largest tipping point of a {top}/{bottom}-persisten repetition encountered in the entire proof of the inner layers was {largest_observed_tipping_point}.')
    

    return True
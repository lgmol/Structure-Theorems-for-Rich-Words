from backtrack import *
from inner_layers import *
import time

quiet = False

start_time=time.time()

# EXAMPLES

# Example 3.4

print('')
print('------ Example 3.4 ------')
print('')

S=['01','0121','012121','02','022','0212']
print(f'The maximal compatible subsets of S={S} are:') 
print(maximal_compatible_sets('0',S))

print('')
print('--------------------------------------------------------------')
print('')




# Example 3.5

print('')
print('------ Example 3.5 ------')
print('')

top=14
bottom=5
backtrack_length=1000
outer_alphabet_size=2

marker='00'
known_factor='0011011'

print(f'Searching for possible returns to {marker} in an infinite {top}/{bottom}-power-free word over {outer_alphabet_size} letters containing the factor {known_factor}.')
print('')

preconditions = [                                      
    RichnessAndCompatibilityCondition(marker,[known_factor]),
    PowerSuffixCondition(top,bottom)
]
R = ReturnWords(backtrack_length, outer_alphabet_size, marker=marker, preconditions=preconditions, prefix=marker, quiet=False)

print('')

print(f'If z is an infinite {top}/{bottom}-power-free rich word over {outer_alphabet_size} letters containing the factor {known_factor}, then the only possible returns to {marker} in z are:')
print(R)

print('')

print('')
print('--------------------------------------------------------------')
print('')






# Example 3.6

print('')
print('------ Example 3.6 ------')
print('')

top=16
bottom=7
backtrack_length=1000
outer_alphabet_size=3

A,B,C,D='00101101','001','00202202','002'
pi=morphism([A,A+D,A+C,A+C+C,A+C+C+B+C+C])

marker=A+'00'
known_factor=A+C+C+B+D

print(f'Let z be an infinite {top}/{bottom}-power-free rich word over {outer_alphabet_size} letters.')
print('')
print(f'We first show that z must contain some permutation of the word {known_factor}.')

preconditions = [
    RichnessCondition(),
    PowerSuffixCondition(top,bottom),
    ForbiddenSuffixCondition(PermutationClass(known_factor,outer_alphabet_size))
]
w,l,tip=backtrack(backtrack_length,outer_alphabet_size,preconditions=preconditions,prefix='0',quiet=True)

assert w==None and type(l)==int, f'The initial backtracking search failed.'
print(f'By a backtracking search, the longest {top}/{bottom}-power-free rich word over {outer_alphabet_size} letters with no permutation of {known_factor} has length {l}.')
print(f'So by permuting the letters of z if necessary, we may assume that z contains {known_factor}.')
print('')
print(f'Now we find all possible returns to {marker} in z compatible with {known_factor}.')

preconditions = [                                      
    RichnessAndCompatibilityCondition(marker,[known_factor]),
    PowerSuffixCondition(top,bottom)
]
S = ReturnWords(backtrack_length, outer_alphabet_size, marker=marker, preconditions=preconditions, prefix=marker, quiet=quiet)

assert S!=False, 'The search for possible returns to the marker did not finish.'
S_as_morphism=morphism(sorted(S,key=len))
print(f'By a backtracking search for complete returns to the marker {marker} in z compatible with {known_factor}, the only possible return words to the marker in z are the following:')
print(S_as_morphism._blocks)
print('')

# Now we check that this set S is exactly the set of all images of letters under pi.  
assert set(S_as_morphism._blocks)==set(pi._blocks),'Proof of structure theorem failed at outer layer.  Returns to the given marker are not exactly the blocks of pi_hat.'
print('These are exactly the blocks of pi.')

print('')
print('--------------------------------------------------------------')
print('')






# Example A.1

print('')
print('------ Example A.1 ------')
print('')

alphabet_size=5
top=16                    
bottom=7                  
backtrack_length=1000     
num_phi_iterates=2
max_tipping_point=100     

phi=morphism(['01','02','03','04','044'])

A,B,C,D='00101101','001','00202202','002'
pi=morphism([A,A+D,A+C,A+C+C,A+C+C+B+C+C])
pihat=compose(pi,iterate(phi,num_phi_iterates))

marker='0'
prefix='0'      # With prefix='0', we obtain the set of all possible returns to 0 reported in the proof of Lemma 5.3.  Set prefix='03' to get only the output reported in Example A.1.

print(f'We search for all possible complete return words w to 0 over {alphabet_size} letters such that phi^{num_phi_iterates}(w) is rich and w contains no {top}/{bottom}-persistent bookended repetition with respect to phi and pihat with tipping point at most {max_tipping_point}.')
print('')

preconditions=[
                RichnessCondition(),
                PersistentCondition(psi=None,phi=phi,pi=pihat,known_pre_seeds=[],outer_top=top,outer_bottom=bottom,max_tipping_point=max_tipping_point)
]
postconditions=[RichnessCondition()]

S=ReturnWords(n=backtrack_length,k=alphabet_size,marker=marker,preconditions=preconditions,postconditions=postconditions,morph=iterate(phi,num_phi_iterates),prefix=prefix,quiet=quiet)

assert S!=False, f'Unable to find all possible returns to {marker}.'

print('')
print(f'The returns to {marker} satisfying the given conditions are the following:')
print(S)

print('')
print('--------------------------------------------------------------')
print('')




# Example A.2

print('')
print('------ Example A.2 ------')
print('')

top=16                    
bottom=7                  
backtrack_length=1000     
num_phi_iterates=2
max_tipping_point=100     

phi=morphism(['01','02','03','04','044'])

A,B,C,D='00101101','001','00202202','002'
pi=morphism([A,A+D,A+C,A+C+C,A+C+C+B+C+C])
pihat=compose(pi,iterate(phi,num_phi_iterates))

psi4=morphism(['01','02','0131','0141'])

prefix=''

print(f'We aim to show that there are only finitely many words over {psi4._input_alphabet_size} letters such that phi^{num_phi_iterates}(w) is rich and w contains no {top}/{bottom}-persistent bookended repetition with respect to phi and pihat with tipping point at most {max_tipping_point}.')
print('')

preconditions=[
                RichnessCondition(),
                PersistentCondition(psi=psi4,phi=phi,pi=pihat,known_pre_seeds=[],outer_top=top,outer_bottom=bottom,max_tipping_point=max_tipping_point)
]
postconditions=[RichnessCondition()]

w,l,tip=backtrack(n=backtrack_length,k=psi4._input_alphabet_size,preconditions=preconditions,postconditions=postconditions,morph=compose(iterate(phi,num_phi_iterates),psi4),prefix=prefix,quiet=quiet)
assert w==None and type(l)==int, f'Unable to confirm that there are only finitely many such words.'
print('')
print(f'By a backtracking search, the longest word satisfying the given conditions has length {l}.')

print('')
print('--------------------------------------------------------------')
print('')

end_time=time.time()

print(f'Total time taken: {end_time-start_time}')
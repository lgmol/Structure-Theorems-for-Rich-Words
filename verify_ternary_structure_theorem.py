from inner_layers import *
import time

quiet = True              # Do not display progress of backtracking searches

# INITIALIZE

initial_search=True       # Set to True to perform the initial backtracking search (which may be time-consuming)

outer_alphabet_size=3
top=16                    
bottom=7                  # We are interested in 16/7-power-free ternary rich words
backtrack_length=10000    # Stop any backtracking search if a word of this length is found (to prevent running indefinitely)
num_phi_iterates=2        # Number of iterations of phi to roll into the outer layer
max_tipping_point=100     # Number of iterations to check for persistent powers

phi=morphism(['01','02','03','04','044'])

A,B,C,D='00101101','001','00202202','002'
pi=morphism([A,A+D,A+C,A+C+C,A+C+C+B+C+C])
pihat=compose(pi,iterate(phi,num_phi_iterates))

known_factor=A+A+D+A+A+C+C+B+C+C+A+D
marker=A+A+D+A+A+'00'

# OUTER LAYER (Lemma 5.2)

outer_layer_start=time.time()

print('')
print(f'------ Proof of Structure Theorem for {top}/{bottom}-power-free rich words over {outer_alphabet_size} letters ------')
print('')
print('------ Proof of Outer Layer (Lemma 5.2) ------')
print('')

print(f'Let z be a recurrent {top}/{bottom}-power-free rich word over {outer_alphabet_size} letters.')
print('')
print(f'We first use a backtracking search to show that there are only finitely many 16/7-power-free ternary rich words that contain no permutation of P=AADAACCBCCAD.')
print('')

# By symmetry, we may consider only words with prefix 0.

if initial_search:
    preconditions=[RichnessCondition(),
                  ForbiddenSuffixCondition(PermutationClass(known_factor,outer_alphabet_size)),
                  PowerSuffixCondition(top,bottom)
                  ]
    w,l,tip=backtrack(backtrack_length,outer_alphabet_size,preconditions=preconditions,prefix='0',quiet=True)
    assert w==None and type(l)==int,'Proof of structure theorem failed at outer layer.  Initial backtracking search failed.'
    print('Initial backtracking search completed.')
    
else:
    print(f'------ WARNING: Initial backtracking search skipped. ------')
    
print('')
print(f'By the initial backtracking search, the longest 16/7-power-free ternary rich word with no permutation of P=AADAACCBCCAD has length {l}.')
print('')
print(f'So by permuting the letters and taking a suffix if necessary, we may assume that z contains P=AADAACCBCCAD.')

preconditions = [RichnessAndCompatibilityCondition(marker,[known_factor]),
                 PowerSuffixCondition(top,bottom)
                ]
S = ReturnWords(backtrack_length, outer_alphabet_size, marker=marker, preconditions=preconditions, prefix=marker, quiet=quiet)

assert S!=False, 'The search for complete returns to the marker p=AADAA00 in z compatible with P=AADAACCBCCAD did not finish.'
S_as_morphism=morphism(sorted(S,key=len))
print('')
print(f'By a backtracking search for complete returns to the marker p=AADAA00 in z compatible with P=AADAACCBCCAD, the only possible return words to p=AADAA00 in z are the following:')
print(S_as_morphism._blocks)
print('')

# Now we check that this set S is exactly the set of all images of letters under pihat.  
assert set(S_as_morphism._blocks)==set(pihat._blocks),'Proof of structure theorem failed at outer layer.  Returns to the given marker are not exactly the blocks of pihat.'

print(f'These are exactly the blocks of pihat.')
print('')
print('------ Outer Layer (Lemma 5.2) confirmed!  We have z=pihat(x) for some infinite word x. ------')
print('')
outer_layer_end=time.time()
print(f'Total time taken for outer layers: {outer_layer_end-outer_layer_start}')
print('')
print('')

# INNER LAYERS (Lemma 5.3)

inner_layers_start=time.time()

print('------ Proof of Inner Layers (Lemma 5.3) ------')
print('')

assert inner_layers(top,bottom,backtrack_length,pihat,phi,num_phi_iterates,max_tipping_point),f'Proof of structure theorem failed at inner layers.'

print('')
print('------ Inner Layers (Lemma 5.3) confirmed! ------')

print('')

inner_layers_end=time.time()
print(f'Time taken for inner layers: {inner_layers_end-inner_layers_start}')
print('')
print(f'Total time taken: {inner_layers_end-outer_layer_start}')
from backtrack import *
from morphisms import *
from inner_layers import *
import itertools
import time

quiet = True               # Do not display progress of backtracking searches

# INITIALIZE

initial_search=True        # Set to True to perform the initial backtracking searches, which are very time-consuming.

outer_alphabet_size=4
top=53
bottom=25
backtrack_length=100000
num_phi_iterates=4
max_tipping_point=100

# The morhpism phi_7 is called phi here.
phi=morphism(['01','02','03','04','05','06','066'])

# The morphisms pi_1,pi_2,...,pi_7 are stored in a list called pi_list.
pi_list=[]
pi_list.append(morphism(['0', '01', '011', '02', '022', '022322', '0223223322322']))
pi_list.append(morphism(['01','0','011','02','0232','0232232','023223233232232']))
pi_list.append(morphism(['01','011','0','02','0232','023233232','02323323223233232']))
pi_list.append(morphism(['0110', '01102', '0110232', '01102332', '011023322332', '011023322332023322332', '01102332233202332233201023322332023322332']))
pi_list.append(morphism(['01011', '01022', '0102', '010232', '01023233232', '010232332320023233232','0102323323200232332320232332320023233232']))
pi_list.append(morphism(['00101101002', '001011010022', '001011010022322', '00101101002232332322', '0010110100223233232202232332322', '001011010022323323220223233232200223233232202232332322', '0010110100223233232202232332322002232332322022323323220010022323323220223233232200223233232202232332322']))
pi_list.append(morphism(['0101100110102', '010110011010232', '01011001101023233232', '010110011010232332233232', '0101100110102323322332320232332233232', '01011001101023233223323202323322332320102323322332320232332233232', '010110011010232332233232023233223323201023233223323202323322332320101101023233223323202323322332320102323322332320232332233232']))

# The morphisms pihat_1,pihat_2,...,pihat_7 are stored in a list called pihat_list.
# The factors pihat_1(5),pihat_2(5),...,pihat_7(5) stored in a list called pihat_at_5_list.
pihat_list=[]
pihat_at_5_list=[]
for i in range(len(pi_list)):
    pihat_list.append(compose(pi_list[i],iterate(phi,num_phi_iterates)))
    pihat_at_5_list.append(pihat_list[i].apply('5'))

# The markers associated with the morphisms pihat_1,...,pihat_7 are stored in a list called marker_list.
marker_list=[]
marker_list.append('0010011001002001001100100')
marker_list.append('01001011010010201001011010010')
marker_list.append('010110100101101020101101001011010')
marker_list.append('011001102011001102320110011020110011023320110011020110011023201100110201100110')
marker_list.append('01011010220101101020101101022010110102320101101022010110102010110102201011010')
marker_list.append('0010110100200101101002200101101002001011010022322001011010020010110100220010110100200101101002232332322001011010020010110100220010110100200101101002232200101101002001011010022001011010020010110100')
marker_list.append('010110011010201011001101023201011001101020101100110102323323201011001101020101100110102320101100110102010110011010232332233232010110011010201011001101023201011001101020101100110102323323201011001101020101100110102320101100110102010110011010')

# The words w_1,w_2,...,w_7 used in the proof of Lemma 6.2 are stored in a list called w_list.
w_list=[]
w_list.append('0010011001002')
w_list.append('010010110100102')
w_list.append('01011010010110102')
w_list.append('011001102')
w_list.append('0101101022')
w_list.append('00101101002')
w_list.append('0101100110102')

# Construct a list containing all permutations of w_1,w_2,...,w_7
all_permutations_of_w=[]
for w in w_list:
    all_permutations_of_w+=PermutationClass(w,outer_alphabet_size)


outer_layer_start=time.time()

print('')
print(f'------ Proof of Structure Theorem for {top}/{bottom}-power-free rich words over {outer_alphabet_size} letters ------')
print('')

# OUTER LAYER (Lemma 6.2)

print('------ Proof of Outer Layer (Lemma 6.2) ------')
print('')
print('Let z be a recurrent 53/25-power-free quaternary rich word.')
print('')

if initial_search:

    # First show that we may assume that z has prefix 001.

    preconditions=[RichnessCondition(),
                ForbiddenSuffixCondition(['00','11','22','33']),
                PowerSuffixCondition(top,bottom)
                ]

    w,l,tip=backtrack(backtrack_length,outer_alphabet_size,preconditions=preconditions,prefix='0',quiet=True)
    assert w==None and type(l)==int,'Proof of structure theorem failed at outer layer.  Unable to confirm that z contains 00, 11, 22, or 33.'
    print(f'There are only finitely many {top}/{bottom}-power-free rich words over {outer_alphabet_size} letters containing no 00, 11, 22, or 33.')
    print(f'The longest such word has length {l}.')
    print('So by permuting the letters and taking a suffix if necessary, we may assume that z has prefix 001.')
    print('')

    # Now show that z contains some permutation of one of the w_i's, i.e., some permutation of a word in shorter_known_factors.   

    prefix='001'
    preconditions=[RichnessCondition(),
                    ForbiddenSuffixCondition(all_permutations_of_w),
                    PowerSuffixCondition(top,bottom),
                    LexicographicCondition(prefix)
                    ]

    w,l,tip=backtrack(backtrack_length,outer_alphabet_size,preconditions=preconditions,prefix=prefix,quiet=True)
    assert w==None and type(l)==int,'Proof of structure theorem failed at outer layer.  Unable to confirm that z contains some permutation of at least one of w_1,w_2,...,w_7.'
    print(f'There are only finitely many {top}/{bottom}-power-free rich words over {outer_alphabet_size} letters with prefix {prefix} containing no permutation of one of w_1,w_2,...w_7.')
    print(f'The longest such word has length {l}.')
    print('So by permuting the letters and taking a suffix if necessary, we may assume that z has prefix w_i for some i=1,2,...,7.')

    # Now show for each i=1,2,...,7 that if z has prefix w_i, then z contains some permutation of pihat_i(5).
    for i in range(len(pi_list)):
        print(f'------ i={i+1} ------')
        print('')
        print(f'Checking that if z has prefix w_{i+1}={w_list[i]}, then z contains some permutation of pihat_{i+1}(5)={pihat_at_5_list[i]}.')
        
        prefix=w_list[i]
        
        preconditions=[RichnessCondition(),
                       PowerSuffixCondition(top,bottom),
                       ForbiddenSuffixCondition(PermutationClass(pihat_at_5_list[i],outer_alphabet_size)),
                       LexicographicCondition(prefix)]
        
        w,l,tip=backtrack(backtrack_length,outer_alphabet_size,preconditions=preconditions,prefix=prefix,quiet=True)

        assert w==None and type(l)==int,f'Proof of structure theorem failed at outer layer.  Unable to confirm that if z has prefix w_{i+1}, then z contains some permutation of pihat_{i+1}'
        print(f'There are only finitely many {top}/{bottom}-power-free rich words over {outer_alphabet_size} letters with prefix w_{i+1} containing no permutation of pihat_{i+1}(5).')
        print(f'The longest such word has length {l}.')
        print(f'So if z contains w_{i+1}, then by permuting the letters if necessary, we may assume that z contains pihat_{i+1}(5).')
        print('')
    
else:
    print(f'------ WARNING: Initial backtracking searches skipped. ------')

print('')
print(f'By the initial backtracking search, we may assume that z contains pihat_i(5) for some i=1,2,...,7.')
print('')

for i in range(len(pi_list)):

    print(f'------ i={i+1} ------')
    print('')
    print(f'Checking that if z contains pihat_{i+1}(5), then return words to the marker {marker_list[i]} in z are exactly the blocks of pihat_{i+1}.')
    
    preconditions = [RichnessAndCompatibilityCondition(marker_list[i],[pihat_at_5_list[i]]),
                 PowerSuffixCondition(top,bottom)
                ]
    S = ReturnWords(backtrack_length, outer_alphabet_size, marker=marker_list[i], preconditions=preconditions, prefix=marker_list[i], quiet=quiet)

    assert S!=False, f'The search for possible returns to the marker {marker_list[i]} did not finish.'
    S_as_morphism=morphism(sorted(S,key=len))
    print('')
    print(f'By a backtracking search for complete returns to the marker in z compatible with pihat_{i+1}(5), the only possible return words to the marker in z are the following:')
    print(S_as_morphism._blocks)
    print('')

    # Now we check that this set S is exactly the set of all images of letters under pi_hat.  
    assert set(S_as_morphism._blocks)==set(pihat_list[i]._blocks),f'Proof of structure theorem failed at outer layer.  Returns to the given marker are not exactly the blocks of pihat_{i+1}.'

    print(f'These are exactly the blocks of pihat_{i+1}.')
    print('')
print('------ Outer Layer (Lemma 6.2) confirmed!  We have z=pihat_i(x) for some i in {1,2,....,7} and some infinite word x. ------')
print('')
outer_layer_end=time.time()
print(f'Total time taken for outer layers: {outer_layer_end-outer_layer_start}')
print('')
print('')



# INNER LAYERS (Lemma 6.3)

inner_layers_start=time.time()

print('------ Proof of Inner Layers (Lemma 6.3) ------')
print('')

for i in range(len(pi_list)):
    print(f'------ i={i+1} ------')
    print('')

    assert inner_layers(top,bottom,backtrack_length,pihat_list[i],phi,num_phi_iterates,max_tipping_point), f'Proof of structure theorem failed at inner layers in the case that i={i+1}.'
    print('')
    print(f'------ Inner Layers confirmed for i={i+1}! ------')
    print('')

print('------ Inner Layers (Lemma 6.3) confirmed! ------')
print('')

inner_layers_end=time.time()
print(f'Time taken for inner layers: {inner_layers_end-inner_layers_start}')
print('')
print(f'Total time taken: {inner_layers_end-outer_layer_start}')
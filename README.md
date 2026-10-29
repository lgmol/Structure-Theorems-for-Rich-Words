# Structure-Theorems-for-Rich-Words

This repository contains all of the code used to verify the claims in the paper "An automated approach to structure theorems for minimally repetitive rich words" by Dvořáková, Mol, and Pelantová [1].   Much of this code is written on top of the code written by Jarkko Peltomäki [2] for the paper "The repetition threshold for ternary rich words" by Currie, Mol, and Peltomaki [3].

Running the following files will verify the computational results described in [1].
- verify_examples.py: Run this file to complete the computations necessary for Examples 3.4, 3.5, 3.6, A.1, and A.2.
- verify_ternary_structure_theorem: Run this file to complete the computations necessary for the ternary structure theorem, i.e., Lemma 5.2 and 5.3 of.
- verify_quaternary_structure_theorem: Run this file to complete the computations necessary for the quaternary structure theorem, i.e., for Lemma 6.2 and 6.3.

The following auxiliary files are included:
- morphisms.py: Implements the `morphism` class, used to define and work with morphisms.
- eertree.py: Implements the `eertree` class of Rubinchik and Shur [4].
- backtrack.py: Implements the general backtracking algorithms `backtrack` and `ReturnWords`.
- conditions.py: Implements the various conditions enforced in the backtracking algorithms (e.g., richness, power-freeness, compatibility, persistent power-freeness)
- inner_layers.py: Implements a routine used to establish inner layers of the ternary and quaternary structure theorems.

[1] L'. Dvořáková, L. Mol, and E. Pelantová, arXiv preprint, 2026.\
[2] [GitHub Repository: Ternary Rich Words Verification](https://github.com/japeltom/ternary-rich-words-verification)\
[3] J. D. Currie, L. Mol, and J. Peltomäki, The repetition threshold for ternary rich words, *Electronic Journal of Combinatorics* **32**(2) (2025), article #P2.55. [DOI](https://doi.org/10.37236/13499)\
[4] M. Rubinchik and A. M. Shur, EERTREE: An efficient data structure for processing palindromes in strings, *European Journal of Combinatorics* **68** (2018), 249-265.

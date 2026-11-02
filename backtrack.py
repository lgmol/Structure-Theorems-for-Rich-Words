from conditions import *

def backtrack(n, k, preconditions, postconditions=None, morph=None, prefix='',quiet=False):
    """A backtracking algorithm that builds words u satisfying given
    precondition that maps to words v that satisfy postconditions.

    Args:
    n: Max length of u, guarantees termination.
    k: Alphabet size of u.
    preconditions: Conditions that u must satisfy..
    postconditions: Conditions that v must satisfy.
    morph: A morphism that maps u to v.
    prefix: An initial prefix for u to start with.
    quiet: Display progress or not.

    Returns:
    u: A word u of length n satisfying the conditions if it exists. None otherwise.
    len(u): The length of the longest word u satisfying the conditions, or None if the given prefix does not satisfy the conditions.
    largest_observed_tipping_point: The largest tipping point of a persistent power encountered in the search if PersistentCondition() was enforced.  None otherwise.
    """

    def config_conditions(conditions):
        if conditions is None:
            conditions = []
        if not isinstance(conditions, list):
            conditions = [conditions]
        # If a condition is a plain function, we assume that we can use
        # FunctionCondition.
        for i in range(len(conditions)):
            if not isinstance(conditions[i], Condition):
                conditions[i] = FunctionCondition(conditions[i])
        return conditions

    preconditions = config_conditions(preconditions)
    postconditions = config_conditions(postconditions)

    pop_lengths = [] # Pop lengths for the image.

    def pop(conditions, pop_lengths=None, limit=-1):
        """Calls the pop method of every condition. If limit != -1, then only
        the first limit pop methods are called. Returns the pop length."""

        if len(conditions) == 0:
            return 1

        pop_length = pop_lengths.pop() if pop_lengths is not None else 1

        for n, c in enumerate(conditions):
            if limit != -1 and n >= limit:
                break
            for _ in range(pop_length):
                c.pop()

        return pop_length

    def check_conditions(w, x, conditions, pop_lengths=None):
        """Checks that all conditions are satisfied for w + x. Returns the
        number of calls to add that were successful and the first nonsuccessful
        condition (None if it does not exist)."""

        failed = False
        n = -1
        flag=None
        for n, c in enumerate(conditions):
            z = ""
            for a in x:
                add_result=c.add(w + z, a)
                if add_result is not None:
                    flag=add_result
                    failed = True
                z += a
            if failed: break

        if pop_lengths is not None:
            pop_lengths.append(len(x))

        n_failed = n + 1 if not failed else n
        return n_failed, None if not failed else c,flag

    # Check that the provided prefix satisfies the given conditions.
    u = "" # preimage
    v = "" # image
    for a in prefix:
        x = a if morph is None else morph.apply(a)
        l_pre, c_pre, flag_pre = check_conditions(u, a, preconditions)
        if c_pre is not None:
            print(f"The prefix {u+a} does not satisfy precondition {str(c_pre)}.")
            print(flag_pre)
            return None,None,None
        l_post, c_post, flag_post = check_conditions(v, x, postconditions, pop_lengths=pop_lengths)
        if c_post is not None:
            print(f"The prefix {u+a} does not satisfy postcondition {str(c_post)}.")  
            print(f'The image of this prefix under the given morphism is {v+x}.')
            print(flag_post) 
            return None,None,None
        u += a
        v += x

    

    longest=prefix
    extensions='0'

    count=0
    
    while len(extensions) > 0:
        
        if not quiet:
            print('-----')
            print(prefix+extensions)
        a = extensions[-1]
        x = a if morph is None else morph.apply(a)

        l_pre, c_pre, flag_pre = check_conditions(u, a, preconditions)
        l_post, c_post, flag_post = check_conditions(v, x, postconditions, pop_lengths=pop_lengths)
        if l_pre == len(preconditions) and l_post == len(postconditions):
            # u + a and v + x are good
            u = u + a
            v = v + x

            count+=1
            # if count%10000000==0:
            #     print(len(u),u)

            if len(u) > len(longest):
                # Save (and uncomment to print) the new longest word.
                longest = u
                # if not quiet:
                #     print(len(u), u)

            if len(u) == n:
                # Terminate if we reach the given length.
                print(f"Found a word of length {n}.")
                for c in preconditions:
                    if c.__str__()[0:10]=="Persistent":
                        return u, len(u), c.largest_observed_tipping_point
                
                return u, len(u), None
            
            else:
                # Set the next extension letter to be 0.
                extensions += '0'
        else:
            # u + a or v + x is not good, backtrack
            # First, we pop only on those conditions for which add was called and it succeeded.
            if not quiet:
                if not c_pre==None:
                    print(f'Precondition: {str(c_pre)}')
                    print(flag_pre)
                else:
                    print(f'Postcondition: {str(c_post)}')
                    print(f'The image of this word under the given morphism is {v+x}.')
                    print(flag_post)
            pop(preconditions, limit=l_pre+1)
            pop(postconditions, pop_lengths=pop_lengths, limit=l_post+1)
            a = extensions[-1]
            extensions = extensions[:-1]

            # Continue backtracking until we can increment a letter or we reach the beginning.
            while len(extensions) > 0 and int(a) == k - 1:
                l_pre = pop(preconditions)
                l_post = pop(postconditions, pop_lengths=pop_lengths)
                a = extensions[-1]
                extensions = extensions[:-1]
                u = u[:-l_pre]
                v = v[:-l_post]

            if int(a) != k - 1:
                extensions += str(int(a) + 1)

    # if not quiet:
    #     print(f"There are only finitely many words satisfying the given conditions. The longest such word has length {len(longest)}.")

    for c in preconditions:
        if c.__str__()[0:10]=="Persistent":
            # print(f'Largest observed tipping point: {c.largest_observed_tipping_point}')
            return None, len(longest), c.largest_observed_tipping_point

    return None, len(longest), None







def ReturnWords(n, k, marker,preconditions, postconditions=None, morph=None, prefix="0", quiet=False):
    """A backtracking algorithm that finds all possible return words w to the given marker starting with the given prefix
    such that w satisfies the given preconditions and morph(w) satisfies the given postconditions

    Args:
    n: If a word of this length is encountered, return False.  (This guarantees termination.)
    k: Alphabet size
    preconditions: Conditions that w must satisfy
    postconditions: Conditions that morph(w) must satisfy
    morph: A morphism f
    prefix: An initial prefix that w must start with
    quiet: Display progress or not

    Returns:
    PossibleReturns, the set of all possible return words w satisfying the required conditions, or
    False if the given prefix does not satisfy the required conditions, or a word of length n is encountered.    
    """

    def config_conditions(conditions):
        if conditions is None:
            conditions = []
        if not isinstance(conditions, list):
            conditions = [conditions]
        # If a condition is a plain function, we assume that we can use
        # FunctionCondition.
        for i in range(len(conditions)):
            if not isinstance(conditions[i], Condition):
                conditions[i] = FunctionCondition(conditions[i])
        return conditions

    preconditions = config_conditions(preconditions)
    postconditions = config_conditions(postconditions)

    pop_lengths = [] # Pop lengths for the image.

    def pop(conditions, pop_lengths=None, limit=-1):
        """Calls the pop method of every condition. If limit != -1, then only
        the first limit pop methods are called. Returns the pop length."""

        if len(conditions) == 0:
            return 1

        pop_length = pop_lengths.pop() if pop_lengths is not None else 1

        for n, c in enumerate(conditions):
            if limit != -1 and n >= limit:
                break
            for _ in range(pop_length):
                c.pop()

        return pop_length

    def check_conditions(w, x, conditions, pop_lengths=None):
        """Checks that all conditions are satisfied for w + x. Returns the
        number of calls to add that were successful and the first nonsuccessful
        condition (None if it does not exist)."""

        failed = False
        n = -1
        flag=None
        for n, c in enumerate(conditions):
            z = ""
            for a in x:
                add_result=c.add(w + z, a)
                if add_result is not None:
                    flag=add_result
                    failed = True
                z += a
            if failed: break

        if pop_lengths is not None:
            pop_lengths.append(len(x))

        n_failed = n + 1 if not failed else n
        return n_failed, None if not failed else c,flag

    PossibleReturns=[]

    # Check that the provided prefix satisfies the given conditions.
    u = "" # preimage
    v = "" # image
    for a in prefix:
        x = a if morph is None else morph.apply(a)
        l_pre, c_pre, flag_pre = check_conditions(u, a, preconditions)
        if c_pre is not None:
            print(f"The prefix {u+a} does not satisfy precondition {str(c_pre)}.")
            print(flag_pre)
            return False
        l_post, c_post, flag_post = check_conditions(v, x, postconditions, pop_lengths=pop_lengths)
        if c_post is not None:
            print(f"The prefix {u+a} does not satisfy postcondition {str(c_post)}.")  
            print(f'The image of this prefix under the given morphism is {v+x}.')
            print(flag_post) 
            return False
        u += a
        v += x

    extensions = '0'
    while len(extensions) > 0:
        if not quiet:
            print('-----')
            print(prefix+extensions)
        
        a = extensions[-1]
        x = a if morph is None else morph.apply(a)

        l_pre, c_pre, flag_pre = check_conditions(u, a, preconditions)
        l_post, c_post, flag_post = check_conditions(v, x, postconditions, pop_lengths=pop_lengths)
        if l_pre == len(preconditions) and l_post == len(postconditions):
            # u + a and v + x are good
            u = u + a
            v = v + x
            # print(u,v)
            if len(u) == n:
                # Terminate if we reach the given length.
                print(f"Found a word of length {n}, so the search for returns did not finish.")
                return False

            elif u[-len(marker):]==marker:
                PossibleReturns.append(u[:-len(marker)])
                if not quiet:
                    print(f'New possible return to the marker: {u[:-len(marker)]}')

                pop(preconditions, limit=l_pre+1)
                pop(postconditions, pop_lengths=pop_lengths, limit=l_post+1)
                a = extensions[-1]
                extensions = extensions[:-1]
                u = u[:-1]
                v = v[:-len(x)]

                while len(extensions) > 0 and int(a) == k - 1:
                    l_pre = pop(preconditions)
                    l_post = pop(postconditions, pop_lengths=pop_lengths)
                    a = extensions[-1]
                    extensions = extensions[:-1]
                    u = u[:-l_pre]
                    v = v[:-l_post]

                if int(a) != k - 1:
                    extensions += str(int(a) + 1)    

            
            else:
                # Set the next extension letter to be 0.
                extensions += '0'
        else:
            # u + a or v + x is not good, backtrack
            # First, we pop only on those conditions for which add was called and it succeeded.
            if not quiet:
                if not c_pre==None:
                    print(f'Precondition: {str(c_pre)}')
                    print(flag_pre)
                else:
                    print(f'Postcondition: {str(c_post)}')
                    print(f'The image of this word under the given morphism is {v+x}.')
                    print(flag_post)
            pop(preconditions, limit=l_pre+1)
            pop(postconditions, pop_lengths=pop_lengths, limit=l_post+1)
            a = extensions[-1]
            extensions = extensions[:-1]

            # Continue backtracking until we can increment a letter or we reach
            # th beginning.
            while len(extensions) > 0 and int(a) == k - 1:
                l_pre = pop(preconditions)
                l_post = pop(postconditions, pop_lengths=pop_lengths)
                a = extensions[-1]
                extensions = extensions[:-1]
                u = u[:-l_pre]
                v = v[:-l_post]

            if int(a) != k - 1:
                extensions += str(int(a) + 1)

    return PossibleReturns
import numpy as np

def extend_by_blanks(seq, b):
    """Extend a label seq. by adding blanks at the beginning, end and in between each label."""
    res = [b]
    for s in seq:
        res.append(s)
        res.append(b)
    return res


def word_to_label_seq(w, chars):
    """Map a word (string of characters) to a sequence of labels (indices)."""
    res = [chars.index(c) for c in w]
    return res

def recursive_forward_probability(t, s, mat, labeling_with_blanks, blank, cache):
    """Recursively compute probability of labeling,
    save results of sub-problems in cache to avoid recalculating them."""

    # check index of labeling
    if s < 0:
        return 0.0

    # sub-problem already computed
    if cache[t][s] is not None:
        return cache[t][s]

    # initial values
    if t == 0:
        if s == 0:
            res = mat[0, blank]
        elif s == 1:
            res = mat[0, labeling_with_blanks[1]]
        else:
            res = 0.0

        cache[t][s] = res
        return res

    # recursion on s and t
    p1 = recursive_forward_probability(t - 1, s, mat, labeling_with_blanks, blank, cache)
    p2 = recursive_forward_probability(t - 1, s - 1, mat, labeling_with_blanks, blank, cache)
    res = (p1 + p2) * mat[t, labeling_with_blanks[s]]

    # in case of a blank or a repeated label, we only consider s and s-1 at t-1, so we're done
    if labeling_with_blanks[s] == blank or (s >= 2 and labeling_with_blanks[s - 2] == labeling_with_blanks[s]):
        cache[t][s] = res
        return res

    # otherwise, in case of a non-blank and non-repeated label, we additionally add s-2 at t-1
    p = recursive_forward_probability(t - 1, s - 2, mat, labeling_with_blanks, blank, cache)
    res += p * mat[t, labeling_with_blanks[s]]
    cache[t][s] = res
    return res

def recursive_backward_probability(t, s, mat, labeling_with_blanks, blank, cache):
    """Recursively compute backward probability of labeling,
    save results of sub-problems in cache to avoid recalculating them."""

    max_T, _ = mat.shape
    L = len(labeling_with_blanks)

    # Check for out-of-bounds indices
    if s >= L:
        return 0.0

    # Sub-problem already computed
    if cache[t][s] is not None:
        return cache[t][s]

    # Initial values at the last time step
    if t == max_T - 1:
        if s == L - 1:
            res = mat[t, blank]
        elif s == L - 2:
            res = mat[t, labeling_with_blanks[L - 2]]
        else:
            res = 0.0

        cache[t][s] = res
        return res

    # Recursion on s and t
    p1 = recursive_backward_probability(t + 1, s, mat, labeling_with_blanks, blank, cache)
    p2 = recursive_backward_probability(t + 1, s + 1, mat, labeling_with_blanks, blank, cache)
    res = (p1 + p2) * mat[t, labeling_with_blanks[s]]

    # In case of a blank or a repeated label, we only consider s and s+1 at t+1, so we're done
    if labeling_with_blanks[s] == blank or (s + 2 < L and labeling_with_blanks[s + 2] == labeling_with_blanks[s]):
        cache[t][s] = res
        return res

    # Otherwise, in case of a non-blank and non-repeated label, we additionally add s+2 at t+1
    p = recursive_backward_probability(t + 1, s + 2, mat, labeling_with_blanks, blank, cache)
    res += p * mat[t, labeling_with_blanks[s]]
    cache[t][s] = res
    return res

def empty_cache(max_T, labeling_with_blanks):
    """Create empty cache."""
    return [[None for _ in range(len(labeling_with_blanks))] for _ in range(max_T)]

def any_list_has_none(list_of_lists):
    """Check if any sublist contains None."""
    for sublist in list_of_lists:
        if None in sublist:
            return True
    return False

def probability(mat: np.ndarray, gt: str, chars: str) -> float:
    """Compute probability of ground truth text gt given neural network output mat.

    See the CTC Forward-Backward Algorithm in Graves paper.

    Args:
        mat: Output of neural network of shape TxC.
        gt: Ground truth text.
        chars: The set of characters the neural network can recognize, excluding the CTC-blank.

    Returns:
        The probability of the text given the neural network output.
    """

    max_T, _ = mat.shape  # size of input matrix
    blank = len(chars)  # index of blank label
    labeling_with_blanks = extend_by_blanks(word_to_label_seq(gt, chars), blank)
    cache = empty_cache(max_T, labeling_with_blanks)

    p1 = recursive_forward_probability(max_T - 1, len(labeling_with_blanks) - 1, mat, labeling_with_blanks, blank, cache)
    p2 = recursive_forward_probability(max_T - 1, len(labeling_with_blanks) - 2, mat, labeling_with_blanks, blank, cache)
    p = p1 + p2
    return p
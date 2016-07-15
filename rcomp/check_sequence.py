intab = "atgc"
outtab = "tacg"

def check_sequence(seq):
    """Check if a sequence is a valid FASTA format.
    Sequence header should start with a ">", should not contain any numbers or characters
    other than A,T,G,C.

    Args:
        seq: A list

    Returns:
        A string of nucleotide sequence. For example,
        if input was ['>sequence_1','ATGC','TTGAC'], return 'ATGCTTGAC'

    """
    if seq:
        header = seq.split('\r\n',maxsplit=1)[0]
        fasta = seq[len(header):]
        if header.startswith(">"):
            fasta_sequence = '\n'.join(fasta).replace('\n', '').replace('\r','').lower()
            if any(char.isdigit() for char in fasta_sequence) \
                    or not all(c in intab for c in fasta_sequence):
                return "Enter a valid sequence"
            else:
                return reverse_complement(fasta_sequence)
        if not header.startswith(">"):
            return "Enter a valid sequence"

def reverse_complement(fasta_sequence):

    """Find the reverse complement of a sequence

    Args:
        fasta_sequence: a string of nucleotide sequence

    Returns:
        a string of nucleotide sequence that is the reverse complement of input sequence
        For example, if the input was 'ATGCTT', return 'AAGCAT'
    """
    complement = fasta_sequence.translate(fasta_sequence.maketrans(intab, outtab))
    rev_comp = complement[::-1]
    #print("reverse complement is:", rev_comp)
    return rev_comp


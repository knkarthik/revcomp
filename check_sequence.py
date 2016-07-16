from django.core.exceptions import ValidationError
import io

intab = "atgc"
outtab = "tacg"
permitted = ["octet-stream", "text"]


def handle_uploaded_file(ufile, content):
    """Check if the uploaded file is text or octet-stream.
    InMemoryUploadedFile object has a 'content_type' that can be used to
    check the type of file. but additional checks are also encouraged.

        Args:
            ufile: A InMemoryUploadedFile object
            content: A TextIOWrapper object containing the contents of uploaded file

        Returns:
            A list of nucleotide sequence. For example,
            ['>sequence_1','ATGC','TTGAC']

        """

    if "text" not in ufile.content_type and \
                    "octet" not in ufile.content_type:
        return "Invalid file type."
    else:
        file = content.readlines()

    return check_sequence(file)


def check_sequence(seq):
    """Check if a sequence is a valid FASTA format.
    Sequence header should start with a ">", should not contain any numbers or characters
    other than A,T,G,C.

    Args:
        seq: A string when read from request.POST or a list when read from request.FILE

    Returns:
        A string of nucleotide sequence. For example,
        if input was ['>sequence_1','ATGC','TTGAC'], return 'ATGCTTGAC'

    """
    if seq:
        if type(seq) is list:
            try:
                header = seq[0]
                fasta = seq[1:]
                if header.startswith(">"):
                    fasta_sequence = '\n'.join(fasta).replace('\n', '').lower()
            except IndexError:
                return "Is the uploaded file empty?"

        elif type(seq) is str:
            header = seq.split('\r\n', maxsplit=1)[0]
            fasta = seq[len(header):].replace('\r\n', '')
            if header.startswith(">"):
                fasta_sequence = '\n'.join(fasta).replace('\n', '').replace('\r', '').lower()
            else:
                return "Enter a valid sequence"
        if any(char.isdigit() for char in fasta_sequence.strip()) \
                or not all(c in intab for c in fasta_sequence):
            return "Enter a valid sequence"

    return reverse_complement(fasta_sequence)


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
    return rev_comp

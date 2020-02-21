class Dna:

    def __init__(self, sequence: str):
        self.sequence = sequence
        self.length = len(self.sequence)
        self.complement_dict = {'A': 'T', 'G': 'C', 'T': 'A', 'C': 'G'}
        self.transcribe_dict = {'A': 'U', 'G': 'C', 'T': 'A', 'C': 'G'}
        self.index = 0

    def gc_content(self):
        self.c_count = self.sequence.count('C')
        self.g_count = self.sequence.count('G')
        return (self.c_count + self.g_count) / self.length

    def reverse_complementary(self):
        complement_seq = ''
        for x in self.sequence:
            complement_seq += self.complement_dict[x]
        return complement_seq[::-1]

    def __eq__(self, other):
        return self.sequence == other.sequence


    def __iter__(self):
        return self

    def next(self):
        if self.index == self.length:
            raise StopIteration
        self.index += 1
        return self.sequence[self.index]

    def transcribe(self):
        transcribed_seq = ''
        for x in self.sequence:
            transcribed_seq += self.transcribe_dict[x]
        return Rna(transcribed_seq)

class Rna(Dna):
    pass






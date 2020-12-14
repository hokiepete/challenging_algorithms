#python3

READS = 400
READ_LEN = 100

def read():
    reads = set()
    for _ in range(READS):
        reads.add(input().strip())
    return list(reads)

def optimal(reads, k):
    kmers = set()
    for read in reads:
        for i in range(READ_LEN - k + 1):
            kmers.add(read[i:i+k])

    pref = set()
    suff = set()
    for kmer in kmers:
        pref.add(kmer[:-1])
        suff.add(kmer[1:])
    # print(kmers)
    return pref == suff


reads = read()
for i in range(READ_LEN, 1, -1):
    val = optimal(reads, i)
    if val:
        print(i)
        break

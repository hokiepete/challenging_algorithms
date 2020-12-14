#python3

READS = 1618
READ_LEN = 100

def read():
    reads = set()
    for _ in range(READS):
        reads.add(input().strip())
    return list(reads)

def match_length(read1, read2):
    for i in range(READ_LEN):
        k = i
        j = 0
        while k < READ_LEN:
            if read1[k] != read2[j]:
                break
            k+=1
            j+=1
        if k == READ_LEN:
            return READ_LEN - i
    return 0

def ml(read1, read2, min_l = 1):
    start = 0
    while True:
        start = read1.find(read2[:min_l], start)
        if start == -1:
            return 0
        if read2.startswith(read1[start:]):
            return len(read1) - start
        start += 1


def overlap(reads, n):
    visited = [False] * n
    visited[0] = True
    v_n = 1
    
    current_read = 0
    genome = reads[current_read]
    
    while v_n < n:
        molap = 0
        other_read = -1
        for i in range(n):
            if not visited[i]:
                overlap = ml(
                    reads[current_read],
                    reads[i]
                    )
                if overlap > molap:
                    molap = overlap
                    other_read = i
        # print(genome)
        # print(reads[other_read])
        # print(reads[other_read][molap:])
        genome += reads[other_read][molap:]
        # print(genome)
        current_read = other_read
        visited[current_read] = True
        v_n += 1

    genome = genome[
        :len(genome) - ml(
            reads[current_read],
            reads[0]
        )
    ]

    return genome

reads = read()
# print(reads)
genome = overlap(reads, len(reads))
print(genome)

# print('ACGTTCGA')
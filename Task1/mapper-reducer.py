from random import randint, seed

DATA_FEATURES = 8193 #shingles_matrix space
PRIME = 105667
R = 10 # row per band
B = 50 # total band
S = 0.85

DATA_FEATURES = 8193 #shingles_matrix space
PRIME = 105667
R = 10 # row per band
B = 50 # total band
S = 0.85

def hashPermutation():
    seed(42)
    
    for _ in range(R * B):
        a = randint(1, DATA_FEATURES)
        b = randint(0, DATA_FEATURES- 1)
        yield lambda x: ((a * x + b) % PRIME) % DATA_FEATURES

def comb(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def mapper(key, value):
    key, values = value.split(' ', 1)

    key = int(key.replace("PAGE_", "")) #erase PAGE_
    values = [int(x) for x in values.split(' ')]

    minhash = [min(map(hash, values)) for hash in hashPermutation()] # 1/0 matrix reflect to random permutation hash func
    for index in range(0, R * B, R):  #go thorough band by band
        yield (str(minhash[index: index + R]), (key, values))   # hash the in page colum in each band to the bucket



def reducer(key, values):
    for a, b in comb(values, 2):
        key1, shingle1 = a #pageA
        key2, shingle2 = b #page B
        shingle1 = set(shingle1)
        shingle2 = set(shingle2)
        if float(len(shingle1.intersection(shingle2))) / len(shingle1.union(shingle2)) >= S:
            yield (min(key1, key2), max(key1, key2))

import siphash

def callhash(hashkey, inval):
    return siphash.SipHash_2_4(hashkey, inval).hash()


def ht_hash(hashkey, inval, htsize):
    return callhash(hashkey, inval) % htsize

#Put your collision-finding code here.
#Your function should output the colliding strings in a list.
def find_collisions(key, target_length):
    size = 2 ** 16
    ht = [None] * size

    max_bucket = []
    cnt = 0
    while len(max_bucket) < target_length:
        random_str = str(cnt).encode("utf-8")
        hashed_str = ht_hash(key, random_str, size)

        if ht[hashed_str] == None:
            ht[hashed_str] = [random_str]
        
        else:
            ht[hashed_str].append(random_str)
            if len(ht[hashed_str]) > len(max_bucket):
                print("current max list: ", len(ht[hashed_str]))
                max_bucket = ht[hashed_str]
        cnt += 1
    print(ht_hash(key, max_bucket[0], size))
    return max_bucket
    # table_size = 2 ** 16
    # third_of_table_size = int(table_size/3)

    # hash_table = [None] * table_size
    # buckets_cap = 0
    # half_target_collision = int(target_length / 2)

    # max_collided_bucket = []
    # count = 0
    # while len(max_collided_bucket) < target_length:
    #     # take the count variable, encode it, and then hash it
    #     random_string = str(count).encode("utf-8")
    #     hashed_string = ht_hash(key, random_string, table_size)

    #     if hash_table[hashed_string] is None and buckets_cap != third_of_table_size:
    #         hash_table[hashed_string] = [random_string]
    #     else:
    #         if buckets_cap != third_of_table_size or len(hash_table[hashed_string]) >= half_target_collision:
    #             hash_table[hashed_string].append(random_string)

    #         if len(hash_table[hashed_string]) == half_target_collision:
    #             buckets_cap += 1

    #         if len(hash_table[hashed_string]) > len(max_collided_bucket):
    #             print("current collided string #: ", len(max_collided_bucket))
    #             max_collided_bucket = hash_table[hashed_string]

    #     count += 1

    # return max_collided_bucket

#Implement this function, which takes the list of
#collisions and verifies they all have the same
#SipHash output under the given key.
def check_collisions(key, colls):
    size = 2 ** 16
    target = ht_hash(key, colls[0], size)

    for coll in colls:
        if ht_hash(key, coll, size) != target:
            return False
    return True

if __name__=='__main__':
    #Look in the source code of the app to
    #find the key used for hashing.
    key = b'\x00'*16
    colls = find_collisions(key, 20)
    # print(colls)
    print("Check Collision: ", check_collisions(key, colls))


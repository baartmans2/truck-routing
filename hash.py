# Space Complexity: O(N)
class DeliveriesHashTable:
    # Time Complexity: O(N)
    def __init__(self, initial_capacity=10):
        # if not specified, create 10 buckets for the hash table
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Time Complexity: O(1)
    # Space Complexity: O(N)
    def insert(self, id, address, city, state, zip, deadline, mass, specialNotes, status):
        # hash id to obtain bucket
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]
        # append object to bucket
        bucket_list.append(
            [id, [id, address, city, state, zip, deadline, mass, specialNotes, status]])

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def search(self, key):
        # hash id to obtain bucket
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # for each item in bucket, check if id matches. if match, return item
        for pair in bucket_list:
            if key == pair[0]:
                item_index = bucket_list.index(pair)
                return bucket_list[item_index][1]
        return None

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def update(self, key, item):
        # hash id to obtain bucket
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # for each item in bucket, check if id matches. if match, replace old item with new item
        for pair in bucket_list:
            if key == pair[0]:
                item_index = bucket_list.index(pair)
                bucket_list[item_index] = [key, item]

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def remove(self, key):
        # hash id to obtain bucket
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # for each item in bucket, check if id matches. if match, remove the item from the bucket
        for pair in bucket_list:
            if key == pair[0]:
                bucket_list.remove(pair)

    # Time Complexity: O(N)
    # Space Complexity: O(N)
    def getAllPackages(self):
        # retrieve all items stored in the hash table
        packages = []
        for bucket in self.table:
            for pair in bucket:
                packages.append(pair[1])
        return packages

# Name: Eugene Song
# OSU Email: songeu@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/2022
# Description: A Hash Map will be implemented using a Dynamic Array to store the hash table and will implement
#                   chaining for collision resolution using a singly linked list. Chains of key/value pairs
#                       will be stored in linked list nodes.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        -Updates the key/value pair in hash map. If given key already exists, its associated value must be replaced
        with the new value. If given key does not exist, a key/value pair must be added.

        Parameters:
            self(HashMap)
            key(str): the identifier
            value(object): the identifier's value

        Returns:
            None
        """

        # ******* 2-step Hash Function Computation --> find hash ***********
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()
        # *********************************************************************

        # gets LinkedList at bucket index position
        current_bucket = self._buckets.get_at_index(index)

        # if LinkedList len is 0 --> insert at start to avoid NoneType error
        if current_bucket.length() == 0:
            current_bucket.insert(key, value)
            self._size += 1
        else:
            # if LinkedList does not have key --> insert new Node(key, value) at the start
            if current_bucket.contains(key) is None:
                current_bucket.insert(key, value)
                self._size += 1
            # else LinkedList has key --> update its value
            else:
                current_bucket.contains(key).value = value

    def empty_buckets(self) -> int:
        """
        -Returns the number of empty "buckets" in the hash table.

        Parameters:
            self(HashMap)

        Returns:
            buckets(int): number of empty buckets
        """
        # get number of total buckets
        buckets = self.get_capacity()

        # iterate through all buckets --> if len is not 0, decrement
        for each in range(self.get_capacity()):
            if self._buckets.get_at_index(each).length() != 0:
                buckets -= 1
        return buckets

    def table_load(self) -> float:
        """
        -Returns the current hash table's load factor.
            "load factor" is the average number of elements in each bucket
                load factor = # of total elements in table / # of buckets
        Parameters:
            self(HashMap)

        Returns:
            factor(float): load factor for hash table
        """
        # init num of total elements and num of buckets
        total_elements = self.get_size()
        buckets = self.get_capacity()

        factor = total_elements / buckets
        return factor

    def clear(self) -> None:
        """
        -Clears the contents of hash map. Does not change the underlying hash table capacity.

        Parameters:
            self(HashMap)

        Returns:
            None
        """
        # iterate current buckets and replace each with empty LinkedList
        for each in range(self.get_capacity()):
            self._buckets.set_at_index(each, LinkedList())
        self._size = 0
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        -Changes the capacity of the internal hash table. All existing key/value pairs must remain and be rehashed
        into a new hash map. If new capacity is < 1 --> do nothing

        Parameters:
            self(HashMap)
            new_capacity(int): new internal capacity

        Returns:
            None
        """
        # corner case: when new capacity is less than 1
        if new_capacity < 1:
            return

        # create a new HashMap with new capacity
        new_map = HashMap(new_capacity, self._hash_function)

        # iterate buckets (capacity)
        for each in range(self._buckets.length()):
            # iterate the LinkedList
            for node in self._buckets.get_at_index(each):
                if node is not None:
                    new_map.put(node.key, node.value)

        # self = new_map <---- does not work, instead...
        # return         <----

        # set self._buckets to new._buckets and reinitialize capacity
        self._buckets = new_map._buckets
        self._capacity = new_capacity
        return

    def get(self, key: str) -> object:
        """
        -Returns the value associated with given key. If key does not exist --> return None

        Parameters:
            self(HashMap)
            key(str): key to search for

        Returns:
            val(object): return val associated with given key
        """
        # ******* 2-step Hash Function Computation --> find hash ***********
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()
        # *********************************************************************

        # gets LinkedList at bucket index position
        current_bucket = self._buckets.get_at_index(index)

        # iterate LinkedList using iterator
        for each in current_bucket:
            if each.key == key:
                return each.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        -Returns True if given key exists in the hash map, otherwise return False. If empty --> return False

        Parameters:
            self(HashMap)
            key(str): key to search for

        Returns:
            exist(bool): boolean whether key exists or not
        """
        # ******* 2-step Hash Function Computation --> find hash ***********
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()
        # *********************************************************************

        # gets LinkedList at bucket index position
        current_bucket = self._buckets.get_at_index(index)

        # Corner case 1) empty hash map --> return false
        if self.get_size == 0:
            return False

        # if at the hashed LinkedList, key exists --> return True
        if current_bucket.contains(key) is not None:
            return True

        # otherwise, return False
        return False

    def remove(self, key: str) -> None:
        """
        -Removes the given key and its associated value from the hash map. If key does not exist --> do nothing

        Parameters:
            self(HashMap)
            key(str): key to remove

        Returns:
            None
        """
        # ******* 2-step Hash Function Computation --> find hash ***********
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()
        # *********************************************************************

        # gets LinkedList at bucket index position
        current_bucket = self._buckets.get_at_index(index)

        # if LL.remove(key) returns True --> dec size of hashmap by 1
        if current_bucket.remove(key):
            self._size -= 1
            return

        return

    def get_keys(self) -> DynamicArray:
        """
        -Returns a DynamicArray that contains all the keys stored in the hash map. Order does not matter.

        Parameters:
            self(HashMap)

        Returns:
            keys(DynamicArray): Dynamic Array with all key entries
        """
        # init new DynamicArray to hold all keys
        keys = DynamicArray()

        # iterate through DynamicArray bucket
        for each in range(self.get_capacity()):
            # iter through each link in LinkedList
            for link in self._buckets.get_at_index(each):
                keys.append(link.key)
        return keys

    def get_buckets(self) -> DynamicArray:
        """
        -Helper function to return the underlying DynamicArray structure

        Parameters:
            self(HashMap)
        Returns:
            DynamicArray: dynamic array for passed HashMap
        """
        return self._buckets


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    -Returns a tuple containing
        1) DynamicArray that contains the mode value/s of the array
        2) integer that represents the highest frequency
    -Multiple values with the highest frequency is to be included in DA and order does not matter.
    -Need be implemented in o(n) time complexity

    Parameters:
        da(DynamicArray): array with all values

    Return:
        tuple (DynamicArray, int)
    """
    mode_array = DynamicArray()
    highest = 0

    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)

    # iterate given DA to hash each value
    for i in range(da.length()):
        # condition: if key DNE in map --> place key/value of 0 into map
        if not map.contains_key(da.get_at_index(i)):
            map.put(da.get_at_index(i), 1)
            if 1 > highest:
                highest = 1
        else:
            map.put(da.get_at_index(i), map.get(da.get_at_index(i)) + 1)
            if int(map.get(da.get_at_index(i))) + 1 > highest:
                highest = int(map.get(da.get_at_index(i)))

    # iterate capacity of HashMap (da.length // 3)
    for j in range(da.length() // 3):
        # iterate through each node in LinkedList --> call LinkedList using
        #       helper custom helper function, get_buckets() to retrieve DynamicArray
        for link in map.get_buckets().get_at_index(j):
            if link.value == highest:
                mode_array.append(link.key)

    return mode_array, highest

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    #
    # m.resize_table(1)
    # print(m.get_keys())
    #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
    #
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")

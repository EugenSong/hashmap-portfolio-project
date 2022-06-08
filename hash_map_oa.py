# Name: Eugene Song
# OSU Email: songeu@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/2022
# Description: A HashMap will be implemented using a Dynamic Array to store the hash table and implement Open
#                   Addressing with Quadratic Probing for collision resolution inside the Dynamic Array.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
            - remember, if the load factor is greater than or equal to 0.5,
                    resize the table before putting the new key/value pair

        Parameters:
            self(HashMap)
            key(str): the identifier
            value(object): the identifier's value

        Returns:
            None
        """
        # ------ PRE-PRECONDITION CHECK LOAD FACTOR BEFORE ANYTHING --> resize to optimize for future performance ---
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)
        # --------------------- 2-step Hash Function Computation --> find hash ---------------------------
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()  # <--- returns index in DynamicArray
        # -------------------------------------------------------------------------------
        # gets value at hashed index and init new hash entry (tombstone implemented)
        current_position = self._buckets.get_at_index(index)
        new_hash_entry = HashEntry(key, value)
        # -------------------------------------------------------------------------------
        # corner case 1) if current position is None (empty) --> insert hash entry
        if current_position is None:
            self._buckets.set_at_index(index, new_hash_entry)
            self._size += 1
        # corner case 2) if current position IS the key we want to insert --> update value
        elif current_position.key == key and current_position.is_tombstone is False:
            current_position.value = value
        # corner case 3) if current is a tombstone w/ the key --> update value and tombstone value
        elif current_position.key == key and current_position.is_tombstone is True:
            current_position.value = value
            current_position.is_tombstone = False
            self._size += 1
        # else if spot is not empty AND spot has different key (already occupied) --> execute quadratic probing
        else:
            # init probing counter for use in probing formula
            move_by = 1
            keepGoing = True
            # iterate through DA using perform quadratic probing and wrapping
            while keepGoing:
                probe = (index + move_by ** 2) % self.get_capacity()

                # if empty slot --> insert
                if self._buckets.get_at_index(probe) is None:
                    self._buckets.set_at_index(probe, new_hash_entry)
                    self._size += 1
                    keepGoing = False
                # if key already exists --> update HashEntry value
                elif self._buckets.get_at_index(probe).key == key and \
                        self._buckets.get_at_index(probe).is_tombstone is False:
                    self._buckets.get_at_index(probe).value = value
                    keepGoing = False
                    # if key exists but is a tombstone
                elif self._buckets.get_at_index(probe).key == key and self._buckets.get_at_index(probe).is_tombstone \
                        is True:
                    self._buckets.get_at_index(probe).value = value
                    self._buckets.get_at_index(probe).is_tombstone = False
                    self._size += 1
                    keepGoing = False
                    # if slot is filled by a different key
                else:
                    move_by += 1
        return

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
        total_capacity = self.get_capacity()

        factor = total_elements / total_capacity
        return factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets.
            algorithm: # of total buckets - # of elements
        Parameters:
            self(HashMap)

        Returns:
            int: number of empty buckets
        """
        return self.get_capacity() - self.get_size()

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
        # corner case: when new capacity is less than 1 OR less than the current # of elements in map
        if new_capacity < 1 or new_capacity < self.get_size():
            return

        # create a new HashMap with new capacity
        new_map = HashMap(new_capacity, self._hash_function)

        # iterate buckets (capacity)
        for each in range(self._buckets.length()):
            if self._buckets.get_at_index(each) is not None:
                if self._buckets.get_at_index(each).is_tombstone is False:
                    new_map.put(self._buckets.get_at_index(each).key, self._buckets.get_at_index(each).value)

        # set self._buckets to new map's buckets and reinitialize capacity to new map's capacity
        self._buckets = new_map._buckets
        self._capacity = new_map.get_capacity()

        return

    def get(self, key: str) -> object:
        """
        Returns value associated w/ given key. If key DNE --> return None

        Parameters:
            self(HashMap)
            key(str): key we are searching for

        Returns:
            object: value of searched key --> return None if DNE
        """

        # --------------------- 2-step Hash Function Computation --> find hash ---------------------------
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()  # <--- returns index in DynamicArray
        # -------------------------------------------------------------------------------
        # gets value at hashed index and init new hash entry (tombstone implemented)
        current_position = self._buckets.get_at_index(index)

        # init probing counter for use in probing formula
        move_by = 1
        keepGoing = True

        # if current == None --> value DNE
        if current_position is None:
            return None
        # if found
        elif current_position.is_tombstone is False and current_position.key == key:
            return current_position.value
        # if current is already taken by a different key
        else:
            # iterate through DA using perform quadratic probing and wrapping
            while keepGoing:
                probe = (index + move_by ** 2) % self.get_capacity()
                # again, if empty --> DNE
                if self._buckets.get_at_index(probe) is None:
                    return None
                # if key --> return val
                elif self._buckets.get_at_index(probe).key == key and \
                        self._buckets.get_at_index(probe).is_tombstone is False:
                    return self._buckets.get_at_index(probe).value
                # probe
                else:
                    move_by += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns a boolean based on whether desired key is in HashMap.

        Parameters:
            self(HashMap)
            key(str): key we are searching for

        Returns:
            bool:
                Exist --> True
                DNE --> False
        """
        # corner case) if empty --> return False
        if self.get_size() == 0:
            return False

        # --------------------- 2-step Hash Function Computation --> find hash ---------------------------
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()  # <--- returns index in DynamicArray
        # -------------------------------------------------------------------------------
        # gets value at hashed index and init new hash entry (tombstone implemented)
        current_position = self._buckets.get_at_index(index)

        # init probing counter for use in probing formula
        move_by = 1
        keepGoing = True

        # if current == None --> value DNE --> False
        if current_position is None:
            return False
        # if found --> return True
        elif current_position.is_tombstone is False and current_position.key == key:
            return True
        # if current is already taken by a different key
        else:
            # iterate through DA using perform quadratic probing and wrapping
            while keepGoing:
                probe = (index + move_by ** 2) % self.get_capacity()
                # again, if empty --> DNE --> False
                if self._buckets.get_at_index(probe) is None:
                    return False
                # if key --> return True
                elif self._buckets.get_at_index(probe).key == key and \
                        self._buckets.get_at_index(probe).is_tombstone is False:
                    return True
                # probe
                else:
                    move_by += 1

    def remove(self, key: str) -> None:
        """
        Removes given key and its associated value from HashMap --> "remove" by updating value of .is_tombstone

        Parameters:
            self(HashMap)
            key(str): key we are removing

        Returns:
            None
        """
        # --------------------- 2-step Hash Function Computation --> find hash ---------------------------
        hash_val = self._hash_function(key)
        index = hash_val % self.get_capacity()  # <--- returns index in DynamicArray
        # -------------------------------------------------------------------------------
        # gets value at hashed index and init new hash entry (tombstone implemented)
        current_position = self._buckets.get_at_index(index)

        # init probing counter for use in probing formula
        move_by = 1
        keepGoing = True

        # if None --> return
        if current_position is None:
            return
        # if immediately found --> make tombstone and dec size
        elif current_position.is_tombstone is False and current_position.key == key:
            current_position.is_tombstone = True
            self._size -= 1
            return
        # if current is already taken by a different key
        else:
            # iterate through DA using perform quadratic probing and wrapping
            while keepGoing:
                probe = (index + move_by ** 2) % self.get_capacity()
                # if key --> return val
                if self._buckets.get_at_index(probe) is None:
                    return
                elif self._buckets.get_at_index(probe).key == key and \
                        self._buckets.get_at_index(probe).is_tombstone is False:
                    self._buckets.get_at_index(probe).is_tombstone = True
                    self._size -= 1
                # probe
                else:
                    move_by += 1
        return

    def clear(self) -> None:
        """
        Clears contents of HashMap. Do not touch underlying hash table capacity.
            Don't forget to reset size.

        Parameters:
            self(HashMap)

        Returns:
            None
        """
        # set each bucket (value of each index) to null
        for each in range(self.get_capacity()):
            self._buckets.set_at_index(each, None)
        self._size = 0
        return

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys stored in the Hash Map. Order does not matter.

        Parameters:
            self(HashMap)

        Returns:
            da(DynamicArray): contains all valid keys in any order
        """
        da = DynamicArray()
        # iterate hashmap buckets and append any non-null keys to empty DA --> return da
        for each in range(self.get_capacity()):
            if self._buckets.get_at_index(each) is not None and self._buckets.get_at_index(each).is_tombstone is False:
                da.append(self._buckets.get_at_index(each).key)
        return da

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

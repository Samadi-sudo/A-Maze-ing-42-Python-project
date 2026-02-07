import random
data = {
    (0, 0): [(1, 0), (0, 1)],
    (1, 0): [(0, 0)]
}
print(data)
print()
key = random.choice(list(data))          # random key
value = random.choice(data[key])         # random value from its list

print(key, value)
print()

data[key].remove(value)                  # remove value

if not data[key]:                        # if list is empty
    del data[key]                        # remove key

# print(data)
cordoner = (2,3)
x, y = cordoner
data[cordoner] = [(x + dx, y + dy) for dx, dy in (
                (1, 0), (-1, 0), (0, 1), (0, -1)
                 )]
print(data)

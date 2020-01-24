import numpy as np

array = np.random.randint(1, 20, (3, 3))

sum = 0
r1 = []
r2 = []
r = 0
p = 0
for row in array:
    r += 1
    a = []
    for i, ii in enumerate(row):
        a.append([i, ii])

    r1 = r2
    r2 = sorted(a, key = lambda x: x[1])

    sumTest = None

    if len(r1) > 0 and len(r2) > 0:
        ss = None
        for r1val in r1:
            for r2val in r2:

                if r1val[0] == r2val[0]:
                    continue
                print(r, r1val[1], r2val[1], end="")
                if sumTest is None:
                    sumTest = r1val[1] + r2val[1]
                    ss = r1val[1]
                    print("None")
                else:
                    print("sumTest: {} {} {}".format(sumTest, r1val[1], r2val[1]))
                    if r1val[1] + r2val[1] < sumTest:
                        sumTest = r1val[1] + r2val[1]
                        ss = r1val[1]



        sum += ss
        if r == len(array):
            sum += min(row)

print(array)
print(sum)
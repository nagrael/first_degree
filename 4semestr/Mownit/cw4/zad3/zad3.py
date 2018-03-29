import math
import random
import os
import os.path
import matplotlib.pyplot as plt


def temp(T, n):
    return T * n


def calculate(arr):
    energy = 0
    for i in range(9):
        tmp = set()
        energy -= len(set(arr[i]))
        for j in range(9):
            tmp.add(arr[j][i])
        energy -= len((tmp))
    return energy


def simple_swap(arr, orig):
    new = [d[:] for d in arr]
    xb = random.randint(0, 2)
    yb = random.randint(0, 2)

    while ispossible(xb, yb, orig):
        xb = random.randint(0, 2)
        yb = random.randint(0, 2)

    ax = random.randint(xb * 3, xb * 3 + 2)
    ay = random.randint(yb * 3, yb * 3 + 2)

    while orig[ax][ay]:
        ax = random.randint(xb * 3, xb * 3 + 2)
        ay = random.randint(yb * 3, yb * 3 + 2)

    bx = random.randint(xb * 3, xb * 3 + 2)
    by = random.randint(yb * 3, yb * 3 + 2)

    while orig[bx][by] or (ax == bx and ay == by):
        bx = random.randint(xb * 3, xb * 3 + 2)
        by = random.randint(yb * 3, yb * 3 + 2)

    new[ax][ay], new[bx][by] = new[bx][by], new[ax][ay]
    return new


def ispossible(xb, yb, orig):
    count = 9
    for x in range(xb * 3, xb * 3 + 3):
        for y in range(yb * 3, yb * 3 + 3):
            if orig[x][y]:
                count -= 1
    return count <= 1


def sim_annealing(arr, orig, T, k):
    energy_val = []
    Temp =[]
    Poss = []
    current_solution = random_fill(arr)
    current_val = calculate(current_solution)
    best_solution = current_solution
    best_val = current_val
    for i in range(k):
        if best_val == -162:
            break
        neighbour = simple_swap(current_solution, orig)
        second_val = calculate(neighbour)
        if second_val < current_val:
            current_solution = neighbour
            current_val = second_val
        else:
            #print(math.exp((current_val - second_val) / T))
            if math.exp((current_val - second_val) / T) > random.random():
                current_solution = neighbour
                current_val = second_val
        if best_val > current_val:
            best_solution = current_solution
            best_val = current_val
        Temp.append(T)
        T = temp(T, 0.9993)
        energy_val.append(current_val)
        Poss.append(math.exp((current_val - second_val) / T))

    return best_solution, energy_val, best_val, Temp, Poss


def read_from_file(f):
    arr = []
    orig = []
    for line in f:
        c = line.replace("x", "0")
        if len(c.split()) !=1:
            c = [int(a) for a in c.split()]
        else:
            c = [int(a) for a in line if a != "\n"]
        d = [(0 != q) for q in c]
        arr.append(c)
        orig.append(d)
    return arr, orig

def generate(f, i):
    arr = []
    orig = []
    for line in f:
        c = line.replace("x", "0")
        if len(c.split()) !=1:
            c = [int(a) for a in c.split()]
        else:
            c = [int(a) for a in line if a != "\n"]
        d = [(0 != q) for q in c]
        arr.append(c)
        orig.append(d)
    for x in range(i):
        x = random.randrange(9)
        y = random.randrange(9)
        while arr[x][y] == 0:
            x = random.randrange(9)
            y = random.randrange(9)
        arr[x][y] = 0
        orig[x][y] = False
    return arr, orig

def write_to_file(f, solution):
    for i in range(9):
        for j in range(9):
            f.write(str(solution[i][j]))
        f.write('\n')


def random_fill(arr):
    new = [d[:] for d in arr]
    i = [k for k in range(1, 10)]
    random.shuffle(i)
    for xb in range(3):
        for yb in range(3):
            for x in range(xb * 3, xb * 3 + 3):
                for y in range(yb * 3, yb * 3 + 3):
                    if new[x][y] == 0:
                        for j in i:
                            if is_not_in_block(j, new, xb, yb):
                                new[x][y] = j
                                break
            random.shuffle(i)
    return new


def is_not_in_block(i, arr, xb, yb):
    for x in range(xb * 3, xb * 3 + 3):
        for y in range(yb * 3, yb * 3 + 3):
            if arr[x][y] == i:
                return False

    return True


def main():
    T = 100.0
    k = 10000
    i = 1
    m = 0

    kx =[]
    for name in os.listdir('./gen'):
        if os.path.isfile('./gen/' + name):
            for x in range(1,80):
                total = 0
                best_value = 0
                energy_val = []
                tempe = []
                poss =[]
                with open('./gen/' + name, 'r') as f:
                    arr, orig = generate(f, x)
                while best_value != -162 and m < 10:
                    m += 1
                    solution, energy_val1, best_value, tempe1, poss1 = sim_annealing(arr, orig, T, k)
                    energy_val.extend(energy_val1)
                    total += len(energy_val1)
                    k += 1000
                    T *= 1.23
                kx.append(total)
                print("Calculated val: " + str(best_value) + ", Solved should be -162. Solved in " + str(total)+" steps and "+str(m-1)+ " resets")
                k = 10000
                T = 100.0
                m = 0
    plt.plot(range(1,80), kx)
    plt.show()

    for name in os.listdir('./test'):
        if os.path.isfile('./test/' + name):
            best_value = 0
            energy_val = []
            tempe = []
            poss =[]
            print("Next one:\n")
            with open('./test/' + name, 'r') as f:
                arr, orig = read_from_file(f)
            for p in range(9):
                print(arr[p])
            while best_value != -162 and m < 15:
                m += 1
                k += 1000
                solution, energy_val1, best_value, tempe1, poss1 = sim_annealing(arr, orig, T, k)
                energy_val.extend(energy_val1)
                tempe.extend(tempe1)
                poss.extend(poss1)
                T *= 1.23
            print("Calculated val: " + str(best_value) + ", Solved should be -162. Solved in " + str(len(energy_val))+" steps and "+str(m-1)+ " resets")
            f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
            ax1.axis([0,len(energy_val),-162,-70])
            ax1.plot(range(len(energy_val)), energy_val)
            ax1.set_title('Energy')
            ax2.axis([0, len(energy_val), 0, T])
            ax2.plot(range(len(tempe)), tempe)
            ax2.set_title('Temperature')
            ax3.axis([0,len(energy_val),0,1])
            ax3.scatter(range(len(poss)), poss)
            ax3.set_title('Possibility')
            k = 10000
            T = 100.0
            m = 0
            with open(str(i) + "_solution.txt", 'w') as f:
                write_to_file(f, solution)
            i += 1
            for q in range(9):
                print(solution[q])
    plt.show()

if(__name__ =="__main__"):
    main()
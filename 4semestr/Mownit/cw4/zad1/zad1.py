import copy
import math
import random
import numpy as np
import matplotlib.pyplot as plt


def temp(T, n):
    return T * n


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def calculate(arr, n):
    energy = 0.0
    for i in range(n):
        energy += distance(arr[i][0], arr[i][1], arr[(i + 1) % n][0], arr[(i + 1) % n][1])
    return energy


def simple_swap(arr, n ,k):
    new = [d[:] for d in arr]
    first = random.randrange(n)
    second = random.randrange(n)
    while first == second:
        second = random.randrange(n)
    new[first], new[second] = new[second], new[first]
    return new


def advanced_swap(arr, n, k):
    new = [d[:] for d in arr]
    first = random.randrange(n)
    new[first], new[(first + k) % (n-1) + 1] = new[(first + k) % (n-1) + 1], new[first]
    return new


def insert_swap(arr, n, k):
    new = [d[:] for d in arr]
    first = random.randrange(n)
    second = random.randrange(n-1)
    while first == second:
        second = random.randrange(n-1)
    x = new.pop(first)
    new.insert(second,x)
    return new

def gen_four(n):
    sigma = 300
    mu = 500

    arr = list(sigma * np.random.randn(n, 2) + mu)
    return arr


def gen_nine(n):
    dx = n // 9
    b = n % 9
    z = random.randint(2,5)
    arr = []
    for a in range(dx):
        for y in range (3):
            for x in range(3):
                arr.append([random.uniform(x*dx+z,x*dx+2*z),random.uniform(y*dx+z,y*dx+2*z)])
                if b > 0:
                    arr.append([random.uniform(x*dx+z,x*dx+2*z),random.uniform(y*dx+z,y*dx+2*z)])
                    b -= 1
    random.shuffle(arr)
    return arr


def sim_annealing(swaping, arr, n, T, k):
    energy_val = []
    tem = []
    current_solution = copy.deepcopy(arr)
    current_val = calculate(current_solution, n)
    best_solution = current_solution
    best_val = current_val
    print("Beggining val: " + str(best_val) +" len: " + str(len(arr)))
    for i in range(k):
        neighbour = swaping(current_solution, n, i)
        second_val = calculate(neighbour, n)
        if second_val < current_val:
            current_solution = neighbour
            current_val = second_val
        else:
            if math.exp((current_val - second_val) / T) > random.random():
                current_solution = neighbour
                current_val = second_val
        if best_val > current_val:
            best_solution = current_solution
            best_val = current_val
        tem.append(T)
        T = temp(T, 0.99997)
        energy_val.append(current_val)
        if i % 1000 == 0:
            print("Calculated val: " + str(current_val) +"\tBest val: " + str(best_val) + "\t T is :" + str(T))
    print("Calculated val: " + str(best_val))
    return best_solution, energy_val, tem, best_val


def main():
    T = 100.0
    k = 200000
    n = 300
    #arr = [[random.randrange(100) for i in range(2)] for x in range(n)]
    arr = gen_four(n)
    f, (ax1, ax2, ax3) = plt.subplots(3)
    f, (bx1, bx2, bx3) = plt.subplots(3,sharex=True)
    f, (cx1, cx2, cx3) = plt.subplots(3,sharex=True)

    solution, energy, tem, best_val = sim_annealing(simple_swap, arr, n, T, k)
    bx1.plot(range(len(energy)),energy)
    cx1.set_title('Simple swap '+str(n))
    cx1.plot(range(len(tem)),tem)
    bx1.set_title('Simple swap '+str(n))
    ax1.set_title('Simple swap '+str(n)+ ".   Best energy " + str(best_val))
    ax1.plot([row[0] for row in solution] + [solution[0][0]], [row[1] for row in solution] + [solution[0][1]],
             marker="o")

    solution, energy, tem, best_val = sim_annealing(advanced_swap, arr, n, T, k)
    cx2.plot(range(len(tem)),tem)
    cx2.set_title('Advanced swap '+str(n))
    bx2.plot(range(len(energy)),energy)
    bx2.set_title('Advanced swap '+str(n))
    ax2.set_title('Advanced swap '+str(n)+ ".   Best energy " + str(best_val))
    ax2.plot([row[0] for row in solution] + [solution[0][0]], [row[1] for row in solution] + [solution[0][1]],
             marker="o")

    solution, energy, tem, best_val = sim_annealing(insert_swap, arr, n, T, k)
    bx3.plot(range(len(energy)),energy)
    bx3.set_title('Insert swap ' +str(n))
    cx3.plot(range(len(tem)),tem)
    cx3.set_title('Insert swap ' +str(n))
    ax3.set_title('Insert swap ' +str(n)+ ".   Best energy " + str(best_val))
    ax3.plot([row[0] for row in solution] + [solution[0][0]], [row[1] for row in solution] + [solution[0][1]],
             marker="o")

    plt.show()


if (__name__ == "__main__"):
    main()

import math
import random
import copy
import matplotlib.pyplot as plt


def temp(T, n):
    return T * n


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def neighbour1(x, y, arr, n):
    for x1 in range(x - 1, x + 2):
        if x1 != x:
            yield x1 % n, y, arr[x1 % n][y]
    for y1 in range(y - 1, y + 2):
        if y1 != y:
            yield x, y1 % n, arr[x][y % n]


def neighbour2(x, y, arr, n):
    for x1 in range(x - 1, x + 2):
        for y1 in range(y - 1, y + 2):
            if x1 != x or y1 != y:
                yield x1 % n, y1 % n, arr[x1 % n][y1 % n]


def neighbour3(x, y, arr, n):
    for x1 in range(x - 6, x + 7):
        for y1 in range(y - 6, y + 7):
            if x1 != x or y1 != y:
                yield x1 % n, y1 % n, arr[x1 % n][y1 % n]


def neighbour4(x, y, arr, n):
    for x1 in range(x - 8, x + 9):
        for y1 in range(y - 8, y + 9):
            if x1 != x or y1 != y:
                yield x1 % n, y1 % n, arr[x1 % n][y1 % n]


def energy1(neighbour, d, x, y, n):
    en = 0.0
    for x1, y1, p in neighbour:
        if d == 0:
            if y1 < n / 2:
                en -= 1
            else:
                en += 1
        else:
            if y1 < n / 2:
                en += 1
            else:
                en -= 1
    return en


def energy2(neighbour, d, x, y, n):
    en = 0.0
    mid = n / 2
    if d == 0:
            en += distance(mid, mid, x, y)
    return en


def energy3(neighbour, d, x, y, n):
    en = 0.0
    if d == 0:
        for x1, y1, p in neighbour:
            if p == 0:
                en -= 1
    return en


def energy4(neighbour, d, x, y, n):
    en = 0.0
    for x1, y1, p in neighbour:
        if d == p:
            en += 1
        else:
            en -= 1
    return en


def energy5(neighbour, d, x, y, n):
    en = 0.0
    for x1, y1, p in neighbour:
        if d == p:
            en -= 1
        else:
            en += 1
    return en


def energy6(neighbour, d, x, y, n):
    en = 0.0
    for x1, y1, p in neighbour:
        if d == p:
            if x <= x1:
                en -= 1
            else:
                en += 1
        else:
            if x <= x1:
                en += 1
            else:
                en -= 1
    return en


def energy_dif(x1, y1, x2, y2, arr, new, neig, energ, n):
    en = 0.0
    en += energ(neig(x1, y1, arr, n), arr[x1][y1], x1, y1, n)
    en += energ(neig(x2, y2, arr, n), arr[x2][y2], x2, y2, n)
    en -= energ(neig(x1, y1, new, n), new[x1][y1], x1, y1, n)
    en -= energ(neig(x2, y2, new, n), new[x2][y2], x2, y2, n)
    return 2 * en


def calculate(arr, n, neig, energys):
    e = 0.0
    for i in range(n):
        for j in range(n):
            e += energys(neig(i, j, arr, n), arr[i][j], i, j, n)
    return e


def simple_swap(arr, n):
    new = [d[:] for d in arr]

    x1 = random.randrange(n)
    y1 = random.randrange(n)

    x2 = random.randrange(n)
    y2 = random.randrange(n)

    while (x1 == x2 and y1 == y2) or new[x1][y1] == new[x2][y2]:
        x2 = random.randrange(n)
        y2 = random.randrange(n)

    new[x1][y1], new[x2][y2] = new[x2][y2], new[x1][y1]
    return new, x1, y1, x2, y2


def sim_annealing(arr, n, neig=neighbour4, energys=energy1, T=100.0, k=100000):
    energy_val = []
    temperatur = []
    current_solution = copy.deepcopy(arr)
    current_val = calculate(current_solution, n, neig, energys)
    best_solution = current_solution
    best_val = current_val
    for i in range(k):
        neighbour, x1, y1, x2, y2 = simple_swap(current_solution, n)
        second_val = current_val - energy_dif(x1, y1, x2, y2, current_solution, neighbour, neig, energys, n)
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
        temperatur.append(T)
        T = temp(T, 0.99998)
        energy_val.append(current_val)
        if i % 1000 == 0:
            print("Current val:" + str(current_val) + " Best so far: " + str(best_val) + " T: " + str(T))
    print("Calculated val: " + str(best_val))
    return best_solution, energy_val, temperatur


def main():
    T = 100.0
    k = 600000
    n = 500
    density = 0.5
    density = int(density * n ** 2)
    arr = [[1 for i in range(n)] for x in range(n)]
    for point in range(density):
        x = random.randrange(n)
        y = random.randrange(n)
        while arr[x][y] == 0:
            x = random.randrange(n)
            y = random.randrange(n)
        arr[x][y] = 0

    plt.figure(1)
    plt.imshow(arr, cmap=plt.get_cmap('gray'))
    solution, energy, temperature = sim_annealing(arr, n, neighbour1, energy1, T, k)
    plt.figure(2)
    plt.imshow(solution, cmap=plt.get_cmap('gray'))

    f, (ax1, ax2,) = plt.subplots(2, sharex=True)
    ax1.axis([0, len(energy), min(energy), max(energy)])
    ax1.plot(range(len(energy)), energy)
    ax1.set_title('Energy')
    ax2.axis([0, len(temperature), 0, int(T)])
    ax2.plot(range(len(temperature)), temperature)
    ax2.set_title('Temperature')

    plt.show()

if (__name__ == "__main__"):
    main()

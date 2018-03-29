# Author: Jan Tulowiecki, aka. wielomian
# Program: Random FramStick Generator
import random
import re


def get_number(probability):
    if probability > 0.9:
        return 10 + random.randint(0, 5)
    ans = 0
    while random.random() < probability:
        ans += 1
    return ans


class FramsticGenerator:
    def __init__(self):
        self.framstick = 'X'
        self.size = 1
        # BODY GENERATOR CONSTANTS
        self.coma = 0.4
        self.rotation = 0.3
        self.twist = 0.12
        self.curvedness = 0.12
        self.capital_l = 0.3
        self.lower_l = 0.4
        # NERVE SYSTEM GENERATOR CONSTANTS
        self.nerves = True
        self.neuron = 0.25
        # Signal generators
        self.generator = 0.45
        self.gyroscope = 5
        self.touch = 10
        self.smell = 10
        self.sin = 35
        self.constant = 15
        # Signal interpreters
        self.interpreter = 0.55
        self.bend_muscle = 35
        self.rotation_muscle = 15

    def make_nervous(self):
        framstick = self.framstick
        generators = []
        interpreters = []
        neurons = []
        for i in range(self.size):
            if random.random() < self.generator:
                generators.append(i)
            if random.random() < self.interpreter:
                interpreters.append(i)
            if random.random() < self.neuron:
                neurons.append(i)
        gen_sum = [0, self.gyroscope, self.touch, self.smell, self.sin, self.constant]
        gen_sum[2] += gen_sum[1]
        gen_sum[3] += gen_sum[2]
        gen_sum[4] += gen_sum[3]
        gen_sum[5] += gen_sum[4]
        gen_sum.reverse()
        int_sum = [0, self.bend_muscle, self.bend_muscle + self.rotation_muscle]
        int_sum.reverse()
        gen = []
        inter = []
        neu = []
        for sig in generators:
            value = random.randint(0, gen_sum[0] - 1)
            i = 0
            while value < gen_sum[i]:
                i += 1
            if i == 1:
                gen.append([sig, '[*', 'g'])
            if i == 2:
                gen.append([sig, '[Sin, f0:{0}'.format(random.randint(-1000, 1000) / 1000), 'g'])
            if i == 3:
                gen.append([sig, '[S', 'g'])
            if i == 4:
                gen.append([sig, '[T', 'g'])
            if i == 5:
                gen.append([sig, '[G', 'g'])
        for sig in interpreters:
            value = random.randint(0, int_sum[0] - 1)
            i = 0
            while value < int_sum[i]:
                i += 1
            if i == 1:
                inter.append([sig, '[@, p:{0}'.format(random.randint(1, 100) / 100), 'i'])
            if i == 2:
                inter.append([sig, '[|, p:{0}'.format(random.randint(1, 100) / 100), 'i'])
        for sig in neurons:
            neu.append(
                    [sig, '[N, in:{0}, fo:{1}'.format(random.randint(1, 100) / 100, random.randint(0, 100) / 100), 'n'])
        gen.append([2000000000])
        inter.append([2000000000])
        neu.append([2000000000])
        full_list = []
        i, j, k, pos = 0, 0, 0, 0
        while gen[i][0] != 2000000000 or inter[j][0] != 2000000000 or neu[k][0] != 2000000000:
            if gen[i][0] < inter[j][0]:
                if gen[i][0] < neu[k][0]:
                    full_list.append(gen[i])
                    gen[i] = pos
                    i += 1
                else:
                    full_list.append(neu[k])
                    neu[k] = pos
                    k += 1
            else:
                if inter[j][0] < neu[k][0]:
                    full_list.append(inter[j])
                    inter[j] = pos
                    j += 1
                else:
                    full_list.append(neu[k])
                    neu[k] = pos
                    k += 1
            pos += 1
        gen = gen[:-1]
        inter = inter[:-1]
        neu = neu[:-1]
        gen_neu = gen + neu
        int_neu = inter + neu
        used = []
        if not neu:
            if not gen:
                return
        for elem in int_neu:
            k = gen_neu[random.randint(0, len(gen_neu) - 1)]
            h = ', {0}:{1}'.format(k - elem, random.randint(10, 1000) / 100)
            full_list[elem][1] += h
            if not k in used:
                used.append(k)
        if neu:
            for elem in gen:
                if not elem in used:
                    k = neu[random.randint(0, len(neu) - 1)]
                    h = ', {0}:{1}'.format(elem - k, random.randint(10, 1000) / 100)
                    full_list[k][1] += h
        for i, elem in enumerate(full_list):
            full_list[i] = [elem[0], elem[1] + ']']
        framstick_constr = re.split('X', framstick)
        framstick = ''
        i = 0
        for part in framstick_constr[:-1]:
            part += 'X'
            help = [x for x in full_list if x[0] == i]
            help = [x[1] for x in help]
            part += ''.join(help)
            framstick += part
            i += 1
        framstick += framstick_constr[-1]
        self.framstick = framstick
        return

    def make_framstick_from_tree(self, tree, vertex=0):
        ans = 'X'
        if vertex == 0:
            ans = ''
        if not tree[vertex]:
            return ans
        if len(tree[vertex]) == 1:
            return '{0}{1}'.format(ans, self.make_framstick_from_tree(tree, tree[vertex][0]))
        return '{0}({1})'.format(ans, ','.join([self.make_framstick_from_tree(tree, i) for i in tree[vertex]]))

    def generate_framstick(self, seg=10):
        self.size = seg
        tree_generator = [-1]
        for edge in range(seg):
            tree_generator.append(random.randint(0, edge))
        tree = [[] for i in range(seg + 1)]
        for i in range(seg):
            tree[tree_generator[i + 1]].append(i + 1)
        framstick = self.make_framstick_from_tree(tree)
        # FRAMSTICK BODY
        # COMA
        framstick_constr = re.split(',', framstick)
        framstick = ''
        for part in framstick_constr[:-1]:
            part += ''.join([',' for i in range(get_number(self.coma) + 1)])
            framstick += part
        framstick += framstick_constr[-1]
        # ROTATION
        framstick_constr = re.split('X', framstick)
        framstick = ''
        for part in framstick_constr[:-1]:
            part += ''.join(['R' for i in range(get_number(self.rotation))])
            part += 'X'
            framstick += part
        framstick += framstick_constr[-1]
        # TWIST
        framstick_constr = re.split('X', framstick)
        framstick = ''
        for part in framstick_constr[:-1]:
            part += ''.join(['Q' for i in range(get_number(self.twist))])
            part += 'X'
            framstick += part
        framstick += framstick_constr[-1]
        # CURVEDNESS
        framstick_constr = re.split('X', framstick)
        framstick = ''
        for part in framstick_constr[:-1]:
            part += ''.join(['Q' for i in range(get_number(self.curvedness))])
            part += 'X'
            framstick += part
        framstick += framstick_constr[-1]
        # LENGTH
        framstick_constr = re.split('X', framstick)
        framstick = ''
        for part in framstick_constr[:-1]:
            length = get_number(self.capital_l) - get_number(self.lower_l)
            if length < 0:
                length *= -1
                part += ''.join(['l' for i in range(length)])
            else:
                part += ''.join(['L' for i in range(length)])
            part += 'X'
            framstick += part
        framstick += framstick_constr[-1]
        self.framstick = framstick
        if self.nerves:
            self.make_nervous()
        return self.framstick


if __name__ == '__main__':
    generator = FramsticGenerator()
    print(generator.generate_framstick())


import pyhop


def buy_ingredients(state, agent):
    state.time[agent] -= 30
    state.money[agent] -= 10
    return state


def actually_cook(state, agent):
    state.time[agent] -= 60
    state.fullness[agent] += 1.5
    return state


def burger(state, agent):
    state.time[agent] -= 20
    state.money[agent] -=15
    state.fullness[agent] += 0.5
    return state


def pizza(state, agent):
    state.time[agent] -= 60
    state.money[agent] -= 35
    state.fullness[agent] += 1.0
    return state


def chinese(state, agent):
    state.time[agent] -= 18
    state.money[agent] -= 25
    state.fullness[agent] += 0.6
    return state


pyhop.declare_operators(buy_ingredients, actually_cook, burger, pizza, chinese)
print '\n'
pyhop.print_operators()


def cook(state, agent, full):
    if state.time[agent] >= 90:
        if state.money[agent] >= 10:
            if state.fullness[agent] + 1.5 < full:
                return [('buy_ingredients', agent), ('actually_cook', agent), ("eating", agent, full)]
            else:
                return [('buy_ingredients', agent), ('actually_cook', agent)]

    return False


def order_burger(state, agent, full):
    if state.time[agent] >= 20:
        if state.money[agent] >= 15:
            if state.fullness[agent] + .5 < full:
                return [('burger', agent),("eating", agent, full)]
            else:
                return [('burger', agent)]

    return False


def order_pizza(state, agent, full):
    if state.time[agent] >= 60:
        if state.money[agent] >= 35:
            if state.fullness[agent] + 1.0 < full:
                return [('pizza', agent),("eating", agent, full)]
            else:
                return [('pizza', agent)]

    return False


def order_chinese(state, agent, full):
    if state.time[agent] >= 18:
        if state.money[agent] >= 25:
            if state.fullness[agent] + 0.6 < full:
                return [('chinese', agent),("eating", agent, full)]
            else:
                return [('chinese', agent)]

    return False


pyhop.declare_methods('eating',  order_pizza, order_burger, order_chinese, cook)
print '\n'
pyhop.print_methods()

person = pyhop.State('state')

person.fullness = {'me_friends': 0.0}
person.time = {'me_friends': 200}
person.money = {'me_friends': 80}
pyhop.pyhop(person, [('eating', 'me_friends', 3.0)], verbose=3)


person.fullness = {'me_friends': 0.0}
person.time = {'me_friends': 220}
person.money = {'me_friends': 100}
pyhop.pyhop(person, [('eating', 'me_friends', 3.0)], verbose=3)

person.fullness = {'me_friends': 0.0}
person.time = {'me_friends': 1000}
person.money = {'me_friends': 30}
pyhop.pyhop(person, [('eating', 'me_friends', 3.0)], verbose=3)

person.fullness = {'me_friends': 0.0}
person.time = {'me_friends': 110}
person.money = {'me_friends': 2000}
pyhop.pyhop(person, [('eating', 'me_friends', 3.0)], verbose=3)
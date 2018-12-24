"""
--- Part Two ---

Things aren't looking good for the reindeer. The man asks whether more milk and cookies would help you think.

If only you could give the reindeer's immune system a boost, you might be able to change the outcome of the combat.

A boost is an integer increase in immune system units' attack damage. For example, if you were to boost the above example's immune system's units by 1570, the armies would instead look like this:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 6077 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 1595 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4

With this boost, the combat proceeds differently:

Immune System:
Group 2 contains 989 units
Group 1 contains 17 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 2 185832 damage
Infection group 1 would deal defending group 1 185832 damage
Infection group 2 would deal defending group 1 53820 damage
Immune System group 2 would deal defending group 1 1577455 damage
Immune System group 2 would deal defending group 2 1577455 damage
Immune System group 1 would deal defending group 2 206618 damage

Infection group 2 attacks defending group 1, killing 9 units
Immune System group 2 attacks defending group 1, killing 335 units
Immune System group 1 attacks defending group 2, killing 32 units
Infection group 1 attacks defending group 2, killing 84 units

Immune System:
Group 2 contains 905 units
Group 1 contains 8 units
Infection:
Group 1 contains 466 units
Group 2 contains 4453 units

Infection group 1 would deal defending group 2 108112 damage
Infection group 1 would deal defending group 1 108112 damage
Infection group 2 would deal defending group 1 53436 damage
Immune System group 2 would deal defending group 1 1443475 damage
Immune System group 2 would deal defending group 2 1443475 damage
Immune System group 1 would deal defending group 2 97232 damage

Infection group 2 attacks defending group 1, killing 8 units
Immune System group 2 attacks defending group 1, killing 306 units
Infection group 1 attacks defending group 2, killing 29 units

Immune System:
Group 2 contains 876 units
Infection:
Group 2 contains 4453 units
Group 1 contains 160 units

Infection group 2 would deal defending group 2 106872 damage
Immune System group 2 would deal defending group 2 1397220 damage
Immune System group 2 would deal defending group 1 1397220 damage

Infection group 2 attacks defending group 2, killing 83 units
Immune System group 2 attacks defending group 2, killing 427 units

After a few fights...

Immune System:
Group 2 contains 64 units
Infection:
Group 2 contains 214 units
Group 1 contains 19 units

Infection group 2 would deal defending group 2 5136 damage
Immune System group 2 would deal defending group 2 102080 damage
Immune System group 2 would deal defending group 1 102080 damage

Infection group 2 attacks defending group 2, killing 4 units
Immune System group 2 attacks defending group 2, killing 32 units

Immune System:
Group 2 contains 60 units
Infection:
Group 1 contains 19 units
Group 2 contains 182 units

Infection group 1 would deal defending group 2 4408 damage
Immune System group 2 would deal defending group 1 95700 damage
Immune System group 2 would deal defending group 2 95700 damage

Immune System group 2 attacks defending group 1, killing 19 units

Immune System:
Group 2 contains 60 units
Infection:
Group 2 contains 182 units

Infection group 2 would deal defending group 2 4368 damage
Immune System group 2 would deal defending group 2 95700 damage

Infection group 2 attacks defending group 2, killing 3 units
Immune System group 2 attacks defending group 2, killing 30 units

After a few more fights...

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 40 units

Infection group 2 would deal defending group 2 960 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 27 units

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 13 units

Infection group 2 would deal defending group 2 312 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 13 units

Immune System:
Group 2 contains 51 units
Infection:
No groups remain.

This boost would allow the immune system's armies to win! It would be left with 51 units.

You don't even know how you could boost the reindeer's immune system or what effect it might have, so you need to be cautious and find the smallest boost that would allow the immune system to win.

How many units does the immune system have left after getting the smallest boost it needs to win?
"""
import re
from collections import OrderedDict
from typing import List, Tuple


class Army:
    def __init__(self, name: str) -> None:
        self.enemy = None  # type: Army
        self._groups = []  # type: List[Group]

        self.name = name

    @property
    def is_alive(self) -> bool:
        return any(g.is_alive for g in self._groups)

    @property
    def groups(self) -> List['Group']:
        return [g for g in self._groups if g.is_alive]

    def add_group(self, group: 'Group'):
        self._groups.append(group)
        group.id = len(self._groups)

    def reset(self) -> None:
        for g in self._groups:
            g.reset()

    def boost(self, ap: int) -> None:
        for g in self._groups:
            g.ap += ap

    def count(self) -> int:
        return sum(g.count for g in self.groups)

    def __str__(self) -> str:
        groups = "\n".join(str(g) for g in self.groups)
        return f'{self.name}:\n{groups}'


class Group:
    id_counter = 0

    def __init__(
            self,
            army: Army,
            count: int,
            hp: int,
            immunities: List[str],
            weaknesses: List[str],
            ap: int,
            dmg_type: str,
            initiative: int,
    ):
        self.id = None
        self.army = army
        self.weaknesses = weaknesses
        self.initiative = initiative
        self.dmg_type = dmg_type
        self.ap = ap
        self.immunities = immunities
        self.hp = hp
        self.count = count
        self.original_count = count

    @property
    def is_alive(self) -> bool:
        return self.count > 0

    @property
    def effective_ap(self) -> int:
        return self.ap * self.count

    def reset(self) -> None:
        self.count = self.original_count

    def __str__(self) -> str:
        return f'{self.army.name} Group {self.id}'


rexps = {
    'count': re.compile('(\d+) units'),
    'hp': re.compile('(\d+) hit points'),
    'immunities': re.compile('immune to ([\w, ]+)'),
    'weaknesses': re.compile('weak to ([\w, ]+)'),
    'ap': re.compile('with an attack that does (\d+)'),
    'dmg_type': re.compile('(\w+) damage'),
    'initiative': re.compile('at initiative (\d+)'),
}


def main():
    with open("input.txt") as f:
        data = f.read().splitlines()

        immune_system = None
        army = None
        for line in data:
            if line == 'Immune System:':
                army = Army(line.rstrip(':'))
            elif line == 'Infection:':
                immune_system = army
                army = Army(line.rstrip(':'))
            elif line:
                count = int(rexps['count'].findall(line)[0])
                hp = int(rexps['hp'].findall(line)[0])

                try:
                    immunities = rexps['immunities'].findall(line)[0].split(
                        ', ')
                except IndexError:
                    immunities = []

                try:
                    weaknesses = rexps['weaknesses'].findall(line)[0].split(
                        ', ')
                except IndexError:
                    weaknesses = []

                ap = int(rexps['ap'].findall(line)[0])
                dmg_type = rexps['dmg_type'].findall(line)[0]
                initiative = int(rexps['initiative'].findall(line)[0])

                group = Group(army, count, hp, immunities, weaknesses, ap,
                              dmg_type, initiative)

                army.add_group(group)

        infection = army
        infection.enemy = immune_system
        immune_system.enemy = infection

        step = 2 ** 20
        while True:
            infection.reset()
            immune_system.reset()

            immune_system.boost(step)

            while immune_system.is_alive and infection.is_alive:
                targeting = OrderedDict()  # type: OrderedDict[Group, Group]

                groups = sorted(
                    immune_system.groups + infection.groups,
                    key=lambda x: (-x.ap * x.count, -x.initiative)
                )

                for g in groups:
                    enemy_groups = sorted(
                        g.army.enemy.groups,
                        key=lambda x: (-x.ap * x.count, -x.initiative),
                    )

                    enemy_groups = [
                        eg for eg in enemy_groups if
                        eg not in targeting.values() and
                        g.dmg_type not in eg.immunities
                    ]

                    weak_groups = [
                        eg for eg in enemy_groups if
                        g.dmg_type in eg.weaknesses
                    ]

                    target = None
                    if weak_groups:
                        target = weak_groups[0]
                    elif enemy_groups:
                        target = enemy_groups[0]

                    if target:
                        targeting[g] = target

                attacks = sorted(
                    targeting.items(),
                    key=lambda x: -x[0].initiative
                )  # type: Tuple[Group, Group]

                immune_system_before = immune_system.count()
                infection_before = infection.count()
                for attacker, defender in attacks:
                    ap = attacker.effective_ap
                    if attacker.dmg_type in defender.weaknesses:
                        ap *= 2
                    casualties = min(ap // defender.hp, defender.count)
                    defender.count -= casualties
                if immune_system_before == immune_system.count() and \
                        infection_before == infection.count():
                    # It's a stalemate. Kill everything.
                    for g in groups:
                        g.count = 0

            if immune_system.is_alive:
                if step == 1:
                    break
                else:
                    immune_system.boost(-step)
                    step //= 2
                    print(step)

        print(max(sum(g.count for g in immune_system.groups),
                  sum(g.count for g in infection.groups)))


main()

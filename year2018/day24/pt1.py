"""
--- Day 24: Immune System Simulator 20XX ---

After a weird buzzing noise, you appear back at the man's cottage. He seems relieved to see his friend, but quickly notices that the little reindeer caught some kind of cold while out exploring.

The portly man explains that this reindeer's immune system isn't similar to regular reindeer immune systems:

The immune system and the infection each have an army made up of several groups; each group consists of one or more identical units. The armies repeatedly fight until only one army has units remaining.

Units within a group all have the same hit points (amount of damage a unit can take before it is destroyed), attack damage (the amount of damage each unit deals), an attack type, an initiative (higher initiative units attack first and win ties), and sometimes weaknesses or immunities. Here is an example group:

18 units each with 729 hit points (weak to fire; immune to cold, slashing)
 with an attack that does 8 radiation damage at initiative 10

Each group also has an effective power: the number of units in that group multiplied by their attack damage. The above group has an effective power of 18 * 8 = 144. Groups never have zero or negative units; instead, the group is removed from combat.

Each fight consists of two phases: target selection and attacking.

During the target selection phase, each group attempts to choose one target. In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher initiative chooses first. The attacking group chooses to target the group in the enemy army to which it would deal the most damage (after accounting for weaknesses and immunities, but not accounting for whether the defending group has enough units to actually receive all of that damage).

If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to target the defending group with the largest effective power; if there is still a tie, it chooses the defending group with the highest initiative. If it cannot deal any defending groups damage, it does not choose a target. Defending groups can only be chosen as a target by one attacking group.

At the end of the target selection phase, each group has selected zero or one groups to attack, and each group is being attacked by zero or one groups.

During the attacking phase, each group deals damage to the target it selected, if any. Groups attack in decreasing order of initiative, regardless of whether they are part of the infection or the immune system. (If a group contains no units, it cannot attack.)

The damage an attacking group deals to a defending group depends on the attacking group's attack type and the defending group's immunities and weaknesses. By default, an attacking group would deal damage equal to its effective power to the defending group. However, if the defending group is immune to the attacking group's attack type, the defending group instead takes no damage; if the defending group is weak to the attacking group's attack type, the defending group instead takes double damage.

The defending group only loses whole units from damage; damage is always dealt in such a way that it kills the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored. For example, if a defending group contains 10 units with 10 hit points each and receives 75 damage, it loses exactly 7 units and is left with 3 units at full health.

After the fight is over, if both armies still contain units, a new fight begins; combat only ends once one army has lost all of its units.

For example, consider the following armies:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4

If these armies were to enter combat, the following fights, including details during the target selection and attacking phases, would take place:

Immune System:
Group 1 contains 17 units
Group 2 contains 989 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 1 185832 damage
Infection group 1 would deal defending group 2 185832 damage
Infection group 2 would deal defending group 2 107640 damage
Immune System group 1 would deal defending group 1 76619 damage
Immune System group 1 would deal defending group 2 153238 damage
Immune System group 2 would deal defending group 1 24725 damage

Infection group 2 attacks defending group 2, killing 84 units
Immune System group 2 attacks defending group 1, killing 4 units
Immune System group 1 attacks defending group 2, killing 51 units
Infection group 1 attacks defending group 1, killing 17 units

Immune System:
Group 2 contains 905 units
Infection:
Group 1 contains 797 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 184904 damage
Immune System group 2 would deal defending group 1 22625 damage
Immune System group 2 would deal defending group 2 22625 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 144 units

Immune System:
Group 2 contains 761 units
Infection:
Group 1 contains 793 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183976 damage
Immune System group 2 would deal defending group 1 19025 damage
Immune System group 2 would deal defending group 2 19025 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 143 units

Immune System:
Group 2 contains 618 units
Infection:
Group 1 contains 789 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183048 damage
Immune System group 2 would deal defending group 1 15450 damage
Immune System group 2 would deal defending group 2 15450 damage

Immune System group 2 attacks defending group 1, killing 3 units
Infection group 1 attacks defending group 2, killing 143 units

Immune System:
Group 2 contains 475 units
Infection:
Group 1 contains 786 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 182352 damage
Immune System group 2 would deal defending group 1 11875 damage
Immune System group 2 would deal defending group 2 11875 damage

Immune System group 2 attacks defending group 1, killing 2 units
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 333 units
Infection:
Group 1 contains 784 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181888 damage
Immune System group 2 would deal defending group 1 8325 damage
Immune System group 2 would deal defending group 2 8325 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 191 units
Infection:
Group 1 contains 783 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181656 damage
Immune System group 2 would deal defending group 1 4775 damage
Immune System group 2 would deal defending group 2 4775 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 49 units
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181424 damage
Immune System group 2 would deal defending group 1 1225 damage
Immune System group 2 would deal defending group 2 1225 damage

Immune System group 2 attacks defending group 1, killing 0 units
Infection group 1 attacks defending group 2, killing 49 units

Immune System:
No groups remain.
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

In the example above, the winning army ends up with 782 + 4434 = 5216 units.

You scan the reindeer's condition (your puzzle input); the white-bearded man looks nervous. As it stands now, how many units would the winning army have?
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

    @property
    def is_alive(self) -> bool:
        return self.count > 0

    @property
    def effective_ap(self) -> int:
        return self.ap * self.count

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

            for attacker, defender in attacks:
                ap = attacker.effective_ap
                if attacker.dmg_type in defender.weaknesses:
                    ap *= 2
                casualties = min(ap // defender.hp, defender.count)
                # print(
                #     f'{attacker} -> {defender} for {ap} dmg, {casualties} dead'
                # )
                defender.count -= casualties

            # print('ROUND')

        # print(", ".join(str(g) for g in immune_system.groups))
        print(max(sum(g.count for g in immune_system.groups),
                  sum(g.count for g in infection.groups)))

        # print(", ".join(str(g) for g in infection.groups))


# 20406 too high
# 19837 too low
main()

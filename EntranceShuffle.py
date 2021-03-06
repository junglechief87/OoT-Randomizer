import random

def link_entrances(world):

    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname)

    # if we do not shuffle, set default connections
    if world.shuffle == 'vanilla':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)
        for exitname, regionname in default_dungeon_connections:
            connect_simple(world, exitname, regionname)
    elif world.shuffle == 'dungeonssimple':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)

        simple_shuffle_dungeons(world)
    elif world.shuffle == 'dungeonsfull':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)

        skull_woods_shuffle(world)

        dungeon_exits = list(Dungeon_Exits)
        lw_entrances = list(LW_Dungeon_Entrances)
        dw_entrances = list(DW_Dungeon_Entrances)

        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        else:
            dungeon_exits.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
        else:
            dw_entrances.append('Ganons Tower')
            dungeon_exits.append('Ganons Tower Exit')

        if world.mode == 'standard':
            # rest of hyrule castle must be in light world, so it has to be the one connected to east exit of desert
            connect_mandatory_exits(world, lw_entrances, [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')], list(LW_Dungeon_Entrances_Must_Exit))
        else:
            connect_mandatory_exits(world, lw_entrances, dungeon_exits, list(LW_Dungeon_Entrances_Must_Exit))
        connect_mandatory_exits(world, dw_entrances, dungeon_exits, list(DW_Dungeon_Entrances_Must_Exit))
        connect_caves(world, lw_entrances, dw_entrances, dungeon_exits)
    elif world.shuffle == 'simple':
        simple_shuffle_dungeons(world)

        old_man_entrances = list(Old_Man_Entrances)
        caves = list(Cave_Exits)
        three_exit_caves = list(Cave_Three_Exits)

        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # we shuffle all 2 entrance caves as pairs as a start
        # start with the ones that need to be directed
        two_door_caves = list(Two_Door_Caves_Directional)
        random.shuffle(two_door_caves)
        random.shuffle(caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1)
            connect_two_way(world, entrance2, exit2)

        # now the remaining pairs
        two_door_caves = list(Two_Door_Caves)
        random.shuffle(two_door_caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1)
            connect_two_way(world, entrance2, exit2)

        # at this point only Light World death mountain entrances remain
        # place old man, has limited options
        remaining_entrances = ['Old Man Cave (West)', 'Old Man House (Bottom)', 'Death Mountain Return Cave (West)', 'Paradox Cave (Bottom)', 'Paradox Cave (Middle)', 'Paradox Cave (Top)',
                               'Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave (Top)', 'Spiral Cave', 'Spiral Cave (Bottom)']
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        remaining_entrances.extend(old_man_entrances)
        random.shuffle(remaining_entrances)
        old_man_entrance = remaining_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')

        # add old man house to ensure it is alwayxs somewhere on light death mountain
        caves.append(('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)'))
        caves.extend(list(three_exit_caves))

        # connect rest
        connect_caves(world, remaining_entrances, [], caves)

        # scramble holes
        scramble_holes(world)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)
    elif world.shuffle == 'restricted':
        simple_shuffle_dungeons(world)

        lw_entrances = list(LW_Entrances + LW_Single_Cave_Doors + Old_Man_Entrances)
        dw_entrances = list(DW_Entrances + DW_Single_Cave_Doors)
        dw_must_exits = list(DW_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances)
        caves = list(Cave_Exits + Cave_Three_Exits)
        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # in restricted, the only mandatory exits are in dark world
        connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in lw_entrances]
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')
        lw_entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in all_entrances]
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        if blacksmith_hut in lw_entrances:
            lw_entrances.remove(blacksmith_hut)
        if blacksmith_hut in dw_entrances:
            dw_entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in all_entrances]
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        if bomb_shop in lw_entrances:
            lw_entrances.remove(bomb_shop)
        if bomb_shop in dw_entrances:
            dw_entrances.remove(bomb_shop)

        # place the old man cave's entrance somewhere in the light world
        random.shuffle(lw_entrances)
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')

        # place Old Man House in Light World
        connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')])

        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves)

        # scramble holes
        scramble_holes(world)

        doors = lw_entrances + dw_entrances

        # place remaining doors
        connect_doors(world, doors, door_targets)
    elif world.shuffle == 'restricted_legacy':
        simple_shuffle_dungeons(world)

        lw_entrances = list(LW_Entrances)
        dw_entrances = list(DW_Entrances)
        dw_must_exits = list(DW_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances)
        caves = list(Cave_Exits)
        three_exit_caves = list(Cave_Three_Exits)
        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # only use two exit caves to do mandatory dw connections
        connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
        # add three exit doors to pool for remainder
        caves.extend(three_exit_caves)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        lw_entrances.extend(old_man_entrances)
        random.shuffle(lw_entrances)
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')

        # place Old Man House in Light World
        connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')])

        # connect rest. There's 2 dw entrances remaining, so we will not run into parity issue placing caves
        connect_caves(world, lw_entrances, dw_entrances, caves)

        # scramble holes
        scramble_holes(world)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)
    elif world.shuffle == 'full':
        skull_woods_shuffle(world)

        lw_entrances = list(LW_Entrances + LW_Dungeon_Entrances + LW_Single_Cave_Doors + Old_Man_Entrances)
        dw_entrances = list(DW_Entrances + DW_Dungeon_Entrances + DW_Single_Cave_Doors)
        dw_must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit)
        lw_must_exits = list(LW_Dungeon_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances + ['Tower of Hera'])
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        else:
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
        else:
            dw_entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')

        # we randomize which world requirements we fulfill first so we get better dungeon distribution
        if random.randint(0, 1) == 0:
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits)
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
        else:
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits)
        if world.mode == 'standard':
            # rest of hyrule castle must be in light world
            connect_caves(world, lw_entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')])

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in lw_entrances]
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')
        lw_entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in all_entrances]
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        if blacksmith_hut in lw_entrances:
            lw_entrances.remove(blacksmith_hut)
        if blacksmith_hut in dw_entrances:
            dw_entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in all_entrances]
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        if bomb_shop in lw_entrances:
            lw_entrances.remove(bomb_shop)
        if bomb_shop in dw_entrances:
            dw_entrances.remove(bomb_shop)

        # place the old man cave's entrance somewhere in the light world
        random.shuffle(lw_entrances)
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')

        # place Old Man House in Light World
        connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')])

        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves)

        # scramble holes
        scramble_holes(world)

        doors = lw_entrances + dw_entrances

        # place remaining doors
        connect_doors(world, doors, door_targets)
    elif world.shuffle == 'crossed':
        skull_woods_shuffle(world)

        entrances = list(LW_Entrances + LW_Dungeon_Entrances + LW_Single_Cave_Doors + Old_Man_Entrances + DW_Entrances + DW_Dungeon_Entrances + DW_Single_Cave_Doors)
        must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + LW_Dungeon_Entrances_Must_Exit)

        old_man_entrances = list(Old_Man_Entrances + ['Tower of Hera'])
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        else:
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
        else:
            entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')

        connect_mandatory_exits(world, entrances, caves, must_exits)

        if world.mode == 'standard':
            # rest of hyrule castle must be dealt with
            connect_caves(world, entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')])

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in entrances]
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')
        entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in entrances]
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options

        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in entrances]
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        entrances.remove(bomb_shop)


        # place the old man cave's entrance somewhere
        random.shuffle(entrances)
        old_man_entrance = entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')

        # place Old Man House
        connect_caves(world, entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')])

        # now scramble the rest
        connect_caves(world, entrances, [], caves)

        # scramble holes
        scramble_holes(world)

        # place remaining doors
        connect_doors(world, entrances, door_targets)
    elif world.shuffle == 'full_legacy':
        skull_woods_shuffle(world)

        lw_entrances = list(LW_Entrances + LW_Dungeon_Entrances + Old_Man_Entrances)
        dw_entrances = list(DW_Entrances + DW_Dungeon_Entrances)
        dw_must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit)
        lw_must_exits = list(LW_Dungeon_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances + ['Tower of Hera'])
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        else:
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
        else:
            dw_entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')

        # we randomize which world requirements we fulfill first so we get better dungeon distribution
        if random.randint(0, 1) == 0:
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits)
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
        else:
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits)
        if world.mode == 'standard':
            # rest of hyrule castle must be in light world
            connect_caves(world, lw_entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')])

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in lw_entrances]
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        lw_entrances.remove(old_man_exit)

        random.shuffle(lw_entrances)
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')

        # place Old Man House in Light World
        connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')])

        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves)

        # scramble holes
        scramble_holes(world)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)
    elif world.shuffle == 'madness_legacy':
        # here lie dragons, connections are no longer two way
        lw_entrances = list(LW_Entrances + LW_Dungeon_Entrances + Old_Man_Entrances)
        dw_entrances = list(DW_Entrances + DW_Dungeon_Entrances)
        dw_entrances_must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit)

        lw_doors = list(LW_Entrances + LW_Dungeon_Entrances + LW_Dungeon_Entrances_Must_Exit) + ['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump',
                                                                                                 'Lumberjack Tree Cave', 'Hyrule Castle Secret Entrance Stairs'] + list(Old_Man_Entrances)
        dw_doors = list(DW_Entrances + DW_Dungeon_Entrances + DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit) + ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)']

        random.shuffle(lw_doors)
        random.shuffle(dw_doors)

        dw_entrances_must_exits.append('Skull Woods Second Section Door (West)')
        dw_entrances.append('Skull Woods Second Section Door (East)')
        dw_entrances.append('Skull Woods First Section Door')

        lw_entrances.extend(['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Entrance (South)'])

        lw_entrances_must_exits = list(LW_Dungeon_Entrances_Must_Exit)

        old_man_entrances = list(Old_Man_Entrances) + ['Tower of Hera']

        mandatory_light_world = ['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)']
        mandatory_dark_world = []
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)

        # shuffle up holes

        lw_hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave']
        dw_hole_entrances = ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = [('Kakariko Well Exit', 'Kakariko Well (top)'),
                        ('Bat Cave Exit', 'Bat Cave (right)'),
                        ('North Fairy Cave Exit', 'North Fairy Cave'),
                        ('Lost Woods Hideout Exit', 'Lost Woods Hideout (top)'),
                        ('Lumberjack Tree Exit', 'Lumberjack Tree (top)'),
                        (('Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)'), 'Skull Woods Second Section (Drop)')]

        if world.mode == 'standard':
            # cannot move uncle cave
            connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance')
            connect_exit(world, 'Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance Stairs')
            connect_entrance(world, lw_doors.pop(), 'Hyrule Castle Secret Entrance Exit')
        else:
            lw_hole_entrances.append('Hyrule Castle Secret Entrance Drop')
            hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))
            lw_entrances.append('Hyrule Castle Secret Entrance Stairs')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
            connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit')
            connect_entrance(world, 'Pyramid Hole', 'Pyramid')
        else:
            dw_entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')
            dw_hole_entrances.append('Pyramid Hole')
            hole_targets.append(('Pyramid Exit', 'Pyramid'))
            dw_entrances_must_exits.append('Pyramid Entrance')
            dw_doors.extend(['Ganons Tower', 'Pyramid Entrance'])

        random.shuffle(lw_hole_entrances)
        random.shuffle(dw_hole_entrances)
        random.shuffle(hole_targets)

        # decide if skull woods first section should be in light or dark world
        sw_light = random.randint(0, 1) == 0
        if sw_light:
            sw_hole_pool = lw_hole_entrances
            mandatory_light_world.append('Skull Woods First Section Exit')
        else:
            sw_hole_pool = dw_hole_entrances
            mandatory_dark_world.append('Skull Woods First Section Exit')
        for target in ['Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)']:
            connect_entrance(world, sw_hole_pool.pop(), target)

        # sanctuary has to be in light world
        connect_entrance(world, lw_hole_entrances.pop(), 'Sewer Drop')
        mandatory_light_world.append('Sanctuary Exit')

        # fill up remaining holes
        for hole in dw_hole_entrances:
            exits, target = hole_targets.pop()
            mandatory_dark_world.append(exits)
            connect_entrance(world, hole, target)

        for hole in lw_hole_entrances:
            exits, target = hole_targets.pop()
            mandatory_light_world.append(exits)
            connect_entrance(world, hole, target)

        # hyrule castle handling
        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_entrance(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
            random.shuffle(lw_entrances)
            connect_exit(world, 'Hyrule Castle Exit (South)', lw_entrances.pop())
            mandatory_light_world.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            lw_doors.append('Hyrule Castle Entrance (South)')
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        # now let's deal with mandatory reachable stuff
        def extract_reachable_exit(cavelist):
            random.shuffle(cavelist)
            candidate = None
            for cave in cavelist:
                if isinstance(cave, tuple) and len(cave) > 1:
                    # special handling: TRock and Spectracle Rock cave have two entries that we should consider entrance only
                    # ToDo this should be handled in a more sensible manner
                    if cave[0] in ['Turtle Rock Exit (Front)', 'Spectacle Rock Cave Exit (Peak)'] and len(cave) == 2:
                        continue
                    candidate = cave
                    break
            if candidate is None:
                raise RuntimeError('No suitable cave.')
            cavelist.remove(candidate)
            return candidate

        def connect_reachable_exit(entrance, general, worldspecific, worldoors):
            # select which one is the primary option
            if random.randint(0, 1) == 0:
                primary = general
                secondary = worldspecific
            else:
                primary = worldspecific
                secondary = general

            try:
                cave = extract_reachable_exit(primary)
            except RuntimeError:
                cave = extract_reachable_exit(secondary)

            exit = cave[-1]
            cave = cave[:-1]
            connect_exit(world, exit, entrance)
            connect_entrance(world, worldoors.pop(), exit)
            # rest of cave now is forced to be in this world
            worldspecific.append(cave)

        # we randomize which world requirements we fulfill first so we get better dungeon distribution
        if random.randint(0, 1) == 0:
            for entrance in lw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_light_world, lw_doors)
            for entrance in dw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_dark_world, dw_doors)
        else:
            for entrance in dw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_dark_world, dw_doors)
            for entrance in lw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_light_world, lw_doors)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [entrance for entrance in old_man_entrances if entrance in lw_entrances]
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        lw_entrances.remove(old_man_exit)

        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit)
        connect_entrance(world, lw_doors.pop(), 'Old Man Cave Exit (East)')
        mandatory_light_world.append('Old Man Cave Exit (West)')

        # we connect up the mandatory associations we have found
        for mandatory in mandatory_light_world:
            if not isinstance(mandatory, tuple):
                mandatory = (mandatory,)
            for exit in mandatory:
                # point out somewhere
                connect_exit(world, exit, lw_entrances.pop())
                # point in from somewhere
                connect_entrance(world, lw_doors.pop(), exit)

        for mandatory in mandatory_dark_world:
            if not isinstance(mandatory, tuple):
                mandatory = (mandatory,)
            for exit in mandatory:
                # point out somewhere
                connect_exit(world, exit, dw_entrances.pop())
                # point in from somewhere
                connect_entrance(world, dw_doors.pop(), exit)

        # handle remaining caves
        while caves:
            # connect highest exit count caves first, prevent issue where we have 2 or 3 exits accross worlds left to fill
            cave_candidate = (None, 0)
            for i, cave in enumerate(caves):
                if isinstance(cave, str):
                    cave = (cave,)
                if len(cave) > cave_candidate[1]:
                    cave_candidate = (i, len(cave))
            cave = caves.pop(cave_candidate[0])

            place_lightworld = random.randint(0, 1) == 0
            if place_lightworld:
                target_doors = lw_doors
                target_entrances = lw_entrances
            else:
                target_doors = dw_doors
                target_entrances = dw_entrances

            if isinstance(cave, str):
                cave = (cave,)

            # check if we can still fit the cave into our target group
            if len(target_doors) < len(cave):
                if not place_lightworld:
                    target_doors = lw_doors
                    target_entrances = lw_entrances
                else:
                    target_doors = dw_doors
                    target_entrances = dw_entrances

            for exit in cave:
                connect_exit(world, exit, target_entrances.pop())
                connect_entrance(world, target_doors.pop(), exit)

        # handle simple doors

        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)
    elif world.shuffle == 'insanity':
        # beware ye who enter here

        entrances = LW_Entrances + LW_Dungeon_Entrances + DW_Entrances + DW_Dungeon_Entrances + Old_Man_Entrances + ['Skull Woods Second Section Door (East)', 'Skull Woods First Section Door', 'Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Entrance (South)']
        entrances_must_exits = DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + LW_Dungeon_Entrances_Must_Exit + ['Skull Woods Second Section Door (West)']

        doors = LW_Entrances + LW_Dungeon_Entrances + LW_Dungeon_Entrances_Must_Exit + ['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Secret Entrance Stairs'] + Old_Man_Entrances +\
                DW_Entrances + DW_Dungeon_Entrances + DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'] +\
                LW_Single_Cave_Doors + DW_Single_Cave_Doors

        # TODO: there are other possible entrances we could support here by way of exiting from a connector,
        # and rentering to find bomb shop. However appended list here is all those that we currently have
        # bomb shop logic for.
        # Specifically we could potentially add: 'Dark Death Mountain Ledge (East)' and doors associated with pits
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors+['Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Entrance', 'Bumper Cave (Top)', 'Hookshot Cave Back Entrance'])
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        random.shuffle(doors)

        old_man_entrances = list(Old_Man_Entrances) + ['Tower of Hera']

        caves = Cave_Exits + Dungeon_Exits + Cave_Three_Exits + ['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)', 'Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)',
                                                                 'Kakariko Well Exit', 'Bat Cave Exit', 'North Fairy Cave Exit', 'Lost Woods Hideout Exit', 'Lumberjack Tree Exit', 'Sanctuary Exit']


        # shuffle up holes

        hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave',
                          'Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = ['Kakariko Well (top)', 'Bat Cave (right)', 'North Fairy Cave', 'Lost Woods Hideout (top)', 'Lumberjack Tree (top)', 'Sewer Drop', 'Skull Woods Second Section (Drop)',
                        'Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)']

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        if world.mode == 'standard':
            # cannot move uncle cave
            connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance')
            connect_exit(world, 'Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance Stairs')
            connect_entrance(world, doors.pop(), 'Hyrule Castle Secret Entrance Exit')
        else:
            hole_entrances.append('Hyrule Castle Secret Entrance Drop')
            hole_targets.append('Hyrule Castle Secret Entrance')
            entrances.append('Hyrule Castle Secret Entrance Stairs')
            caves.append('Hyrule Castle Secret Entrance Exit')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
            connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit')
            connect_entrance(world, 'Pyramid Hole', 'Pyramid')
        else:
            entrances.append('Ganons Tower')
            caves.extend(['Ganons Tower Exit', 'Pyramid Exit'])
            hole_entrances.append('Pyramid Hole')
            hole_targets.append('Pyramid')
            entrances_must_exits.append('Pyramid Entrance')
            doors.extend(['Ganons Tower', 'Pyramid Entrance'])

        random.shuffle(hole_entrances)
        random.shuffle(hole_targets)
        random.shuffle(entrances)

        # fill up holes
        for hole in hole_entrances:
            connect_entrance(world, hole, hole_targets.pop())

        # hyrule castle handling
        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_entrance(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
            connect_exit(world, 'Hyrule Castle Exit (South)', entrances.pop())
            caves.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            doors.append('Hyrule Castle Entrance (South)')
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        # now let's deal with mandatory reachable stuff
        def extract_reachable_exit(cavelist):
            random.shuffle(cavelist)
            candidate = None
            for cave in cavelist:
                if isinstance(cave, tuple) and len(cave) > 1:
                    # special handling: TRock has two entries that we should consider entrance only
                    # ToDo this should be handled in a more sensible manner
                    if cave[0] in ['Turtle Rock Exit (Front)', 'Spectacle Rock Cave Exit (Peak)'] and len(cave) == 2:
                        continue
                    candidate = cave
                    break
            if candidate is None:
                raise RuntimeError('No suitable cave.')
            cavelist.remove(candidate)
            return candidate

        def connect_reachable_exit(entrance, caves, doors):
            cave = extract_reachable_exit(caves)

            exit = cave[-1]
            cave = cave[:-1]
            connect_exit(world, exit, entrance)
            connect_entrance(world, doors.pop(), exit)
            # rest of cave now is forced to be in this world
            caves.append(cave)

        # connect mandatory exits
        for entrance in entrances_must_exits:
            connect_reachable_exit(entrance, caves, doors)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [entrance for entrance in old_man_entrances if entrance in entrances]
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        entrances.remove(old_man_exit)

        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit)
        connect_entrance(world, doors.pop(), 'Old Man Cave Exit (East)')
        caves.append('Old Man Cave Exit (West)')

        # place blacksmith, has limited options
        blacksmith_doors = [door for door in blacksmith_doors if door in doors]
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        doors.remove(blacksmith_hut)

        # place dam and pyramid fairy, have limited options
        bomb_shop_doors = [door for door in bomb_shop_doors if door in doors]
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        doors.remove(bomb_shop)

        # handle remaining caves
        for cave in caves:
            if isinstance(cave, str):
                cave = (cave,)

            for exit in cave:
                connect_exit(world, exit, entrances.pop())
                connect_entrance(world, doors.pop(), exit)

        # place remaining doors
        connect_doors(world, doors, door_targets)
    elif world.shuffle == 'insanity_legacy':
        world.fix_fake_world = False
        # beware ye who enter here

        entrances = LW_Entrances + LW_Dungeon_Entrances + DW_Entrances + DW_Dungeon_Entrances + Old_Man_Entrances + ['Skull Woods Second Section Door (East)', 'Skull Woods First Section Door', 'Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Entrance (South)']
        entrances_must_exits = DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + LW_Dungeon_Entrances_Must_Exit + ['Skull Woods Second Section Door (West)']

        doors = LW_Entrances + LW_Dungeon_Entrances + LW_Dungeon_Entrances_Must_Exit + ['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Secret Entrance Stairs'] + Old_Man_Entrances +\
                DW_Entrances + DW_Dungeon_Entrances + DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)']

        random.shuffle(doors)

        old_man_entrances = list(Old_Man_Entrances) + ['Tower of Hera']

        caves = Cave_Exits + Dungeon_Exits + Cave_Three_Exits + ['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)', 'Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)',
                                                                 'Kakariko Well Exit', 'Bat Cave Exit', 'North Fairy Cave Exit', 'Lost Woods Hideout Exit', 'Lumberjack Tree Exit', 'Sanctuary Exit']

        # shuffle up holes

        hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave',
                          'Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = ['Kakariko Well (top)', 'Bat Cave (right)', 'North Fairy Cave', 'Lost Woods Hideout (top)', 'Lumberjack Tree (top)', 'Sewer Drop', 'Skull Woods Second Section (Drop)',
                        'Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)']

        if world.mode == 'standard':
            # cannot move uncle cave
            connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance')
            connect_exit(world, 'Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance Stairs')
            connect_entrance(world, doors.pop(), 'Hyrule Castle Secret Entrance Exit')
        else:
            hole_entrances.append('Hyrule Castle Secret Entrance Drop')
            hole_targets.append('Hyrule Castle Secret Entrance')
            entrances.append('Hyrule Castle Secret Entrance Stairs')
            caves.append('Hyrule Castle Secret Entrance Exit')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
            connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit')
            connect_entrance(world, 'Pyramid Hole', 'Pyramid')
        else:
            entrances.append('Ganons Tower')
            caves.extend(['Ganons Tower Exit', 'Pyramid Exit'])
            hole_entrances.append('Pyramid Hole')
            hole_targets.append('Pyramid')
            entrances_must_exits.append('Pyramid Entrance')
            doors.extend(['Ganons Tower', 'Pyramid Entrance'])

        random.shuffle(hole_entrances)
        random.shuffle(hole_targets)
        random.shuffle(entrances)

        # fill up holes
        for hole in hole_entrances:
            connect_entrance(world, hole, hole_targets.pop())

        # hyrule castle handling
        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_entrance(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
            connect_exit(world, 'Hyrule Castle Exit (South)', entrances.pop())
            caves.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            doors.append('Hyrule Castle Entrance (South)')
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        # now let's deal with mandatory reachable stuff
        def extract_reachable_exit(cavelist):
            random.shuffle(cavelist)
            candidate = None
            for cave in cavelist:
                if isinstance(cave, tuple) and len(cave) > 1:
                    # special handling: TRock has two entries that we should consider entrance only
                    # ToDo this should be handled in a more sensible manner
                    if cave[0] in ['Turtle Rock Exit (Front)', 'Spectacle Rock Cave Exit (Peak)'] and len(cave) == 2:
                        continue
                    candidate = cave
                    break
            if candidate is None:
                raise RuntimeError('No suitable cave.')
            cavelist.remove(candidate)
            return candidate

        def connect_reachable_exit(entrance, caves, doors):
            cave = extract_reachable_exit(caves)

            exit = cave[-1]
            cave = cave[:-1]
            connect_exit(world, exit, entrance)
            connect_entrance(world, doors.pop(), exit)
            # rest of cave now is forced to be in this world
            caves.append(cave)

        # connect mandatory exits
        for entrance in entrances_must_exits:
            connect_reachable_exit(entrance, caves, doors)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [entrance for entrance in old_man_entrances if entrance in entrances]
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        entrances.remove(old_man_exit)

        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit)
        connect_entrance(world, doors.pop(), 'Old Man Cave Exit (East)')
        caves.append('Old Man Cave Exit (West)')

        # handle remaining caves
        for cave in caves:
            if isinstance(cave, str):
                cave = (cave,)

            for exit in cave:
                connect_exit(world, exit, entrances.pop())
                connect_entrance(world, doors.pop(), exit)

        # handle simple doors

        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)
    else:
        raise NotImplementedError('Shuffling not supported yet')


def connect_simple(world, exitname, regionname):
    world.get_entrance(exitname).connect(world.get_region(regionname))


def connect_entrance(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    # check if we got an entrance or a region to connect to
    try:
        region = world.get_region(exitname)
        exit = None
    except RuntimeError:
        exit = world.get_entrance(exitname)
        region = exit.parent_region

    # if this was already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)

    target = exit_ids[exit.name][0] if exit is not None else exit_ids.get(region.name, None)
    addresses = door_addresses[entrance.name][0]

    entrance.connect(region, addresses, target)
    world.spoiler.set_entrance(entrance.name, exit.name if exit is not None else region.name, 'entrance')


def connect_exit(world, exitname, entrancename):
    entrance = world.get_entrance(entrancename)
    exit = world.get_entrance(exitname)

    # if this was already connected somewhere, remove the backreference
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'exit')


def connect_two_way(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    exit = world.get_entrance(exitname)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    entrance.connect(exit.parent_region, door_addresses[entrance.name][0], exit_ids[exit.name][0])
    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'both')


def scramble_holes(world):
    hole_entrances = [('Kakariko Well Cave', 'Kakariko Well Drop'),
                      ('Bat Cave Cave', 'Bat Cave Drop'),
                      ('North Fairy Cave', 'North Fairy Cave Drop'),
                      ('Lost Woods Hideout Stump', 'Lost Woods Hideout Drop'),
                      ('Lumberjack Tree Cave', 'Lumberjack Tree Tree'),
                      ('Sanctuary', 'Sanctuary Grave')]

    hole_targets = [('Kakariko Well Exit', 'Kakariko Well (top)'),
                    ('Bat Cave Exit', 'Bat Cave (right)'),
                    ('North Fairy Cave Exit', 'North Fairy Cave'),
                    ('Lost Woods Hideout Exit', 'Lost Woods Hideout (top)'),
                    ('Lumberjack Tree Exit', 'Lumberjack Tree (top)')]

    if not world.shuffle_ganon:
        connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit')
        connect_entrance(world, 'Pyramid Hole', 'Pyramid')
    else:
        hole_targets.append(('Pyramid Exit', 'Pyramid'))

    if world.mode == 'standard':
        # cannot move uncle cave
        connect_two_way(world, 'Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit')
        connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance')
    else:
        hole_entrances.append(('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Drop'))
        hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))

    # do not shuffle sanctuary into pyramid hole unless shuffle is crossed
    if world.shuffle == 'crossed':
        hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))
    if world.shuffle_ganon:
        random.shuffle(hole_targets)
        exit, target = hole_targets.pop()
        connect_two_way(world, 'Pyramid Entrance', exit)
        connect_entrance(world, 'Pyramid Hole', target)
    if world.shuffle != 'crossed':
        hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))

    random.shuffle(hole_targets)
    for entrance, drop in hole_entrances:
        exit, target = hole_targets.pop()
        connect_two_way(world, entrance, exit)
        connect_entrance(world, drop, target)


def connect_random(world, exitlist, targetlist, two_way=False):
    targetlist = list(targetlist)
    random.shuffle(targetlist)

    for exit, target in zip(exitlist, targetlist):
        if two_way:
            connect_two_way(world, exit, target)
        else:
            connect_entrance(world, exit, target)


def connect_mandatory_exits(world, entrances, caves, must_be_exits):
    """This works inplace"""
    random.shuffle(entrances)
    random.shuffle(caves)
    while must_be_exits:
        exit = must_be_exits.pop()
        # find multi exit cave
        cave = None
        for candidate in caves:
            if not isinstance(candidate, str):
                cave = candidate
                break

        if cave is None:
            raise RuntimeError('No more caves left. Should not happen!')
        else:
            caves.remove(cave)
        # all caves are sorted so that the last exit is always reachable
        for i in range(len(cave) - 1):
            entrance = entrances.pop()

            # ToDo Better solution, this is a hot fix. Do not connect both sides of trock ledge to each other
            if entrance == 'Dark Death Mountain Ledge (West)':
                new_entrance = entrances.pop()
                entrances.append(entrance)
                entrance = new_entrance

            connect_two_way(world, entrance, cave[i])
        connect_two_way(world, exit, cave[-1])


def connect_caves(world, lw_entrances, dw_entrances, caves):
    """This works inplace"""
    random.shuffle(lw_entrances)
    random.shuffle(dw_entrances)
    random.shuffle(caves)
    while caves:
        # connect highest exit count caves first, prevent issue where we have 2 or 3 exits accross worlds left to fill
        cave_candidate = (None, 0)
        for i, cave in enumerate(caves):
            if isinstance(cave, str):
                cave = (cave,)
            if len(cave) > cave_candidate[1]:
                cave_candidate = (i, len(cave))
        cave = caves.pop(cave_candidate[0])

        target = lw_entrances if random.randint(0, 1) == 0 else dw_entrances
        if isinstance(cave, str):
            cave = (cave,)

        # check if we can still fit the cave into our target group
        if len(target) < len(cave):
            # need to use other set
            target = lw_entrances if target is dw_entrances else dw_entrances

        for exit in cave:
            connect_two_way(world, target.pop(), exit)


def connect_doors(world, doors, targets):
    """This works inplace"""
    random.shuffle(doors)
    random.shuffle(targets)
    while doors:
        door = doors.pop()
        target = targets.pop()
        connect_entrance(world, door, target)


def skull_woods_shuffle(world):
    connect_random(world, ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole'],
                   ['Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)', 'Skull Woods Second Section (Drop)'])
    connect_random(world, ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'],
                   ['Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)'], True)


def simple_shuffle_dungeons(world):
    skull_woods_shuffle(world)

    dungeon_entrances = ['Eastern Palace', 'Tower of Hera', 'Thieves Town', 'Skull Woods Final Section', 'Palace of Darkness', 'Ice Palace', 'Misery Mire', 'Swamp Palace']
    dungeon_exits = ['Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit', 'Skull Woods Final Section Exit', 'Palace of Darkness Exit', 'Ice Palace Exit', 'Misery Mire Exit', 'Swamp Palace Exit']

    if not world.shuffle_ganon:
        connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
    else:
        dungeon_entrances.append('Ganons Tower')
        dungeon_exits.append('Ganons Tower Exit')

    # shuffle up single entrance dungeons
    connect_random(world, dungeon_entrances, dungeon_exits, True)

    # mix up 4 door dungeons
    multi_dungeons = ['Desert', 'Turtle Rock']
    if world.mode == 'open':
        multi_dungeons.append('Hyrule Castle')
    random.shuffle(multi_dungeons)

    dp_target = multi_dungeons[0]
    tr_target = multi_dungeons[1]
    if world.mode != 'open':
        # place hyrule castle as intended
        hc_target = 'Hyrule Castle'
    else:
        hc_target = multi_dungeons[2]

    # ToDo improve this?
    if hc_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Hyrule Castle Exit (East)')
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Hyrule Castle Exit (West)')
        connect_two_way(world, 'Agahnims Tower', 'Agahnims Tower Exit')
    elif hc_target == 'Desert':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Hyrule Castle Exit (South)')
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Hyrule Castle Exit (East)')
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Hyrule Castle Exit (West)')
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Agahnims Tower Exit')
    elif hc_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Hyrule Castle Exit (South)')
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Hyrule Castle Exit (East)')
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Hyrule Castle Exit (West)')
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Agahnims Tower Exit')

    if dp_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Desert Palace Exit (South)')
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Desert Palace Exit (East)')
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Desert Palace Exit (West)')
        connect_two_way(world, 'Agahnims Tower', 'Desert Palace Exit (North)')
    elif dp_target == 'Desert':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Desert Palace Exit (South)')
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Desert Palace Exit (East)')
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Desert Palace Exit (West)')
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Desert Palace Exit (North)')
    elif dp_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Desert Palace Exit (South)')
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Desert Palace Exit (East)')
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Desert Palace Exit (West)')
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Desert Palace Exit (North)')

    if tr_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Turtle Rock Exit (Front)')
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Turtle Rock Ledge Exit (East)')
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Turtle Rock Ledge Exit (West)')
        connect_two_way(world, 'Agahnims Tower', 'Turtle Rock Isolated Ledge Exit')
    elif tr_target == 'Desert':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Turtle Rock Exit (Front)')
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Turtle Rock Ledge Exit (East)')
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Turtle Rock Ledge Exit (West)')
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Exit')
    elif tr_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Turtle Rock Exit (Front)')
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Turtle Rock Isolated Ledge Exit')
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Turtle Rock Ledge Exit (West)')
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Turtle Rock Ledge Exit (East)')


LW_Dungeon_Entrances = ['Desert Palace Entrance (South)',
                        'Desert Palace Entrance (West)',
                        'Desert Palace Entrance (North)',
                        'Eastern Palace',
                        'Tower of Hera',
                        'Hyrule Castle Entrance (West)',
                        'Hyrule Castle Entrance (East)',
                        'Agahnims Tower']

LW_Dungeon_Entrances_Must_Exit = ['Desert Palace Entrance (East)']

DW_Dungeon_Entrances = ['Thieves Town',
                        'Skull Woods Final Section',
                        'Ice Palace',
                        'Misery Mire',
                        'Palace of Darkness',
                        'Swamp Palace',
                        'Turtle Rock',
                        'Dark Death Mountain Ledge (West)']

DW_Dungeon_Entrances_Must_Exit = ['Dark Death Mountain Ledge (East)',
                                  'Turtle Rock Isolated Ledge Entrance']

Dungeon_Exits = [('Desert Palace Exit (South)', 'Desert Palace Exit (West)', 'Desert Palace Exit (East)'),
                 'Desert Palace Exit (North)',
                 'Eastern Palace Exit',
                 'Tower of Hera Exit',
                 'Thieves Town Exit',
                 'Skull Woods Final Section Exit',
                 'Ice Palace Exit',
                 'Misery Mire Exit',
                 'Palace of Darkness Exit',
                 'Swamp Palace Exit',
                 'Agahnims Tower Exit',
                 ('Turtle Rock Exit (Front)', 'Turtle Rock Ledge Exit (East)', 'Turtle Rock Ledge Exit (West)', 'Turtle Rock Isolated Ledge Exit')]

DW_Entrances_Must_Exit = ['Bumper Cave (Top)', 'Hookshot Cave Back Entrance']

Two_Door_Caves_Directional = [('Bumper Cave (Bottom)', 'Bumper Cave (Top)'),
                              ('Hookshot Cave', 'Hookshot Cave Back Entrance')]

Two_Door_Caves = [('Elder House (East)', 'Elder House (West)'),
                  ('Two Brothers House (East)', 'Two Brothers House (West)'),
                  ('Superbunny Cave (Bottom)', 'Superbunny Cave (Top)')]

Old_Man_Entrances = ['Old Man Cave (East)',
                     'Old Man House (Top)',
                     'Death Mountain Return Cave (East)',
                     'Spectacle Rock Cave',
                     'Spectacle Rock Cave Peak',
                     'Spectacle Rock Cave (Bottom)']

Cave_Exits = [('Elder House Exit (East)', 'Elder House Exit (West)'),
              ('Two Brothers House Exit (East)', 'Two Brothers House Exit (West)'),
              ('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave Exit (East)'),
              ('Fairy Ascension Cave Exit (Bottom)', 'Fairy Ascension Cave Exit (Top)'),
              ('Spiral Cave Exit (Top)', 'Spiral Cave Exit'),
              ('Bumper Cave Exit (Top)', 'Bumper Cave Exit (Bottom)'),
              ('Superbunny Cave Exit (Bottom)', 'Superbunny Cave Exit (Top)'),
              ('Hookshot Cave Exit (South)', 'Hookshot Cave Exit (North)')]

Cave_Three_Exits = [('Spectacle Rock Cave Exit (Peak)', 'Spectacle Rock Cave Exit (Top)', 'Spectacle Rock Cave Exit'),
                    ('Paradox Cave Exit (Top)', 'Paradox Cave Exit (Middle)', 'Paradox Cave Exit (Bottom)')]

LW_Entrances = ['Elder House (East)',
                'Elder House (West)',
                'Two Brothers House (East)',
                'Two Brothers House (West)',
                'Old Man Cave (West)',
                'Old Man House (Bottom)',
                'Death Mountain Return Cave (West)',
                'Paradox Cave (Bottom)',
                'Paradox Cave (Middle)',
                'Paradox Cave (Top)',
                'Fairy Ascension Cave (Bottom)',
                'Fairy Ascension Cave (Top)',
                'Spiral Cave',
                'Spiral Cave (Bottom)']

DW_Entrances = ['Bumper Cave (Bottom)',
                'Superbunny Cave (Top)',
                'Superbunny Cave (Bottom)',
                'Hookshot Cave']

Bomb_Shop_Multi_Cave_Doors = ['Hyrule Castle Entrance (South)',
                              'Misery Mire',
                              'Thieves Town',
                              'Bumper Cave (Bottom)',
                              'Swamp Palace',
                              'Hyrule Castle Secret Entrance Stairs',
                              'Skull Woods First Section Door',
                              'Skull Woods Second Section Door (East)',
                              'Skull Woods Second Section Door (West)',
                              'Skull Woods Final Section',
                              'Ice Palace',
                              'Turtle Rock',
                              'Dark Death Mountain Ledge (West)',
                              'Dark Death Mountain Ledge (East)',
                              'Superbunny Cave (Top)',
                              'Superbunny Cave (Bottom)',
                              'Hookshot Cave',
                              'Ganons Tower',
                              'Desert Palace Entrance (South)',
                              'Tower of Hera',
                              'Two Brothers House (West)',
                              'Old Man Cave (East)',
                              'Old Man House (Bottom)',
                              'Old Man House (Top)',
                              'Death Mountain Return Cave (East)',
                              'Death Mountain Return Cave (West)',
                              'Spectacle Rock Cave Peak',
                              'Spectacle Rock Cave',
                              'Spectacle Rock Cave (Bottom)',
                              'Paradox Cave (Bottom)',
                              'Paradox Cave (Middle)',
                              'Paradox Cave (Top)',
                              'Fairy Ascension Cave (Bottom)',
                              'Fairy Ascension Cave (Top)',
                              'Spiral Cave',
                              'Spiral Cave (Bottom)',
                              'Palace of Darkness',
                              'Hyrule Castle Entrance (West)',
                              'Hyrule Castle Entrance (East)',
                              'Agahnims Tower',
                              'Desert Palace Entrance (West)',
                              'Desert Palace Entrance (North)'
                              # all entrances below this line would be possible for blacksmith_hut
                              # if it were not for dwarf checking multi-entrance caves
                              ]

Blacksmith_Multi_Cave_Doors = ['Eastern Palace',
                               'Elder House (East)',
                               'Elder House (West)',
                               'Two Brothers House (East)',
                               'Old Man Cave (West)',
                               'Sanctuary',
                               'Lumberjack Tree Cave',
                               'Lost Woods Hideout Stump',
                               'North Fairy Cave',
                               'Bat Cave Cave',
                               'Kakariko Well Cave']

LW_Single_Cave_Doors = ['Blinds Hideout',
                        'Lake Hylia Fairy',
                        'Light Hype Fairy',
                        'Desert Fairy',
                        'Chicken House',
                        'Aginahs Cave',
                        'Sahasrahlas Hut',
                        'Cave Shop (Lake Hylia)',
                        'Blacksmiths Hut',
                        'Sick Kids House',
                        'Lost Woods Gamble',
                        'Fortune Teller (Light)',
                        'Snitch Lady (East)',
                        'Snitch Lady (West)',
                        'Bush Covered House',
                        'Tavern (Front)',
                        'Light World Bomb Hut',
                        'Kakariko Shop',
                        'Mini Moldorm Cave',
                        'Long Fairy Cave',
                        'Good Bee Cave',
                        '20 Rupee Cave',
                        '50 Rupee Cave',
                        'Ice Rod Cave',
                        'Library',
                        'Potion Shop',
                        'Dam',
                        'Lumberjack House',
                        'Lake Hylia Fortune Teller',
                        'Kakariko Gamble Game',
                        'Waterfall of Wishing',
                        'Capacity Upgrade',
                        'Bonk Rock Cave',
                        'Graveyard Cave',
                        'Checkerboard Cave',
                        'Cave 45',
                        'Kings Grave',
                        'Bonk Fairy (Light)',
                        'Hookshot Fairy',
                        'Mimic Cave']

DW_Single_Cave_Doors = ['Bonk Fairy (Dark)',
                        'Dark Sanctuary Hint',
                        'Dark Lake Hylia Fairy',
                        'C-Shaped House',
                        'Big Bomb Shop',
                        'Dark Death Mountain Fairy',
                        'Dark Lake Hylia Shop',
                        'Dark World Shop',
                        'Red Shield Shop',
                        'Mire Shed',
                        'East Dark World Hint',
                        'Dark Desert Hint',
                        'Spike Cave',
                        'Palace of Darkness Hint',
                        'Dark Lake Hylia Ledge Spike Cave',
                        'Cave Shop (Dark Death Mountain)',
                        'Dark World Potion Shop',
                        'Pyramid Fairy',
                        'Archery Game',
                        'Dark World Lumberjack Shop',
                        'Hype Cave',
                        'Brewery',
                        'Dark Lake Hylia Ledge Hint',
                        'Chest Game',
                        'Dark Desert Fairy',
                        'Dark Lake Hylia Ledge Fairy',
                        'Fortune Teller (Dark)',
                        'Dark World Hammer Peg Cave']

Blacksmith_Single_Cave_Doors = ['Blinds Hideout',
                                'Lake Hylia Fairy',
                                'Light Hype Fairy',
                                'Desert Fairy',
                                'Chicken House',
                                'Aginahs Cave',
                                'Sahasrahlas Hut',
                                'Cave Shop (Lake Hylia)',
                                'Blacksmiths Hut',
                                'Sick Kids House',
                                'Lost Woods Gamble',
                                'Fortune Teller (Light)',
                                'Snitch Lady (East)',
                                'Snitch Lady (West)',
                                'Bush Covered House',
                                'Tavern (Front)',
                                'Light World Bomb Hut',
                                'Kakariko Shop',
                                'Mini Moldorm Cave',
                                'Long Fairy Cave',
                                'Good Bee Cave',
                                '20 Rupee Cave',
                                '50 Rupee Cave',
                                'Ice Rod Cave',
                                'Library',
                                'Potion Shop',
                                'Dam',
                                'Lumberjack House',
                                'Lake Hylia Fortune Teller',
                                'Kakariko Gamble Game']

Bomb_Shop_Single_Cave_Doors = ['Waterfall of Wishing',
                               'Capacity Upgrade',
                               'Bonk Rock Cave',
                               'Graveyard Cave',
                               'Checkerboard Cave',
                               'Cave 45',
                               'Kings Grave',
                               'Bonk Fairy (Light)',
                               'Hookshot Fairy',
                               'East Dark World Hint',
                               'Palace of Darkness Hint',
                               'Dark Lake Hylia Fairy',
                               'Dark Lake Hylia Ledge Fairy',
                               'Dark Lake Hylia Ledge Spike Cave',
                               'Dark Lake Hylia Ledge Hint',
                               'Hype Cave',
                               'Bonk Fairy (Dark)',
                               'Brewery',
                               'C-Shaped House',
                               'Chest Game',
                               'Dark World Hammer Peg Cave',
                               'Red Shield Shop',
                               'Dark Sanctuary Hint',
                               'Fortune Teller (Dark)',
                               'Dark World Shop',
                               'Dark World Lumberjack Shop',
                               'Dark World Potion Shop',
                               'Archery Game',
                               'Mire Shed',
                               'Dark Desert Hint',
                               'Dark Desert Fairy',
                               'Spike Cave',
                               'Cave Shop (Dark Death Mountain)',
                               'Dark Death Mountain Fairy',
                               'Mimic Cave',
                               'Big Bomb Shop',
                               'Dark Lake Hylia Shop']

Single_Cave_Doors = ['Pyramid Fairy']

Single_Cave_Targets = ['Blinds Hideout',
                       'Bonk Fairy (Light)',
                       'Lake Hylia Healer Fairy',
                       'Swamp Healer Fairy',
                       'Desert Healer Fairy',
                       'Kings Grave',
                       'Chicken House',
                       'Aginahs Cave',
                       'Sahasrahlas Hut',
                       'Cave Shop (Lake Hylia)',
                       'Sick Kids House',
                       'Lost Woods Gamble',
                       'Fortune Teller (Light)',
                       'Snitch Lady (East)',
                       'Snitch Lady (West)',
                       'Bush Covered House',
                       'Tavern (Front)',
                       'Light World Bomb Hut',
                       'Kakariko Shop',
                       'Cave 45',
                       'Graveyard Cave',
                       'Checkerboard Cave',
                       'Mini Moldorm Cave',
                       'Long Fairy Cave',
                       'Good Bee Cave',
                       '20 Rupee Cave',
                       '50 Rupee Cave',
                       'Ice Rod Cave',
                       'Bonk Rock Cave',
                       'Library',
                       'Potion Shop',
                       'Hookshot Fairy',
                       'Waterfall of Wishing',
                       'Capacity Upgrade',
                       'Pyramid Fairy',
                       'East Dark World Hint',
                       'Palace of Darkness Hint',
                       'Dark Lake Hylia Healer Fairy',
                       'Dark Lake Hylia Ledge Healer Fairy',
                       'Dark Lake Hylia Ledge Spike Cave',
                       'Dark Lake Hylia Ledge Hint',
                       'Hype Cave',
                       'Bonk Fairy (Dark)',
                       'Brewery',
                       'C-Shaped House',
                       'Chest Game',
                       'Dark World Hammer Peg Cave',
                       'Red Shield Shop',
                       'Dark Sanctuary Hint',
                       'Fortune Teller (Dark)',
                       'Village of Outcasts Shop',
                       'Dark Lake Hylia Shop',
                       'Dark World Lumberjack Shop',
                       'Archery Game',
                       'Mire Shed',
                       'Dark Desert Hint',
                       'Dark Desert Healer Fairy',
                       'Spike Cave',
                       'Cave Shop (Dark Death Mountain)',
                       'Dark Death Mountain Healer Fairy',
                       'Mimic Cave',
                       'Dark World Potion Shop',
                       'Lumberjack House',
                       'Lake Hylia Fortune Teller',
                       'Kakariko Gamble Game',
                       'Dam']

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [('Adult Forest Warp Pad', 'Forest Temple Entry Area'),
                         ('Child Forest Warp Pad', 'Sacred Forest Meadow'),
                         ('Temple Warp Pad', 'Temple of Time'),
                         ('Crater Warp Pad', 'Death Mountain Crater Central'),
                         ('Lake Warp Pad', 'Lake Hylia'),
                         ('Graveyard Warp Pad', 'Shadow Temple Warp Region'),
                         ('Colossus Warp Pad', 'Desert Colossus'),
                         ('Lost Woods', 'Lost Woods'),
                         ('Lost Woods Front', 'Kokiri Forest'),
                         ('Woods to Goron City', 'Goron City Woods Warp'),
                         ('Goron City to Woods', 'Lost Woods'),
                         ('Goron City from Woods', 'Goron City'),
                         ('Goron City Bomb Wall', 'Goron City Woods Warp'),
                         ('Lost Woods Dive Warp', 'Zora River Top'),
                         ('Zora River Dive Warp', 'Lost Woods'),
                         ('Meadow Entrance', 'Sacred Forest Meadow Entryway'),
                         ('Meadow Exit', 'Lost Woods'),
                         ('Meadow Gate', 'Sacred Forest Meadow'),
                         ('Meadow Gate Exit', 'Sacred Forest Meadow Entryway'),
                         ('Adult Meadow Access', 'Forest Temple Entry Area'),
                         ('Adult Meadow Exit', 'Lost Woods'),
                         ('Lost Woods Bridge', 'Lost Woods Bridge'),
                         ('Kokiri Forest Entrance', 'Kokiri Forest'),
                         ('Field to Forest', 'Lost Woods Bridge'),
                         ('Forest Exit', 'Hyrule Field'),
                         ('Field to Lake', 'Lake Hylia'),
                         ('Lake Hylia Dive Warp', 'Zoras Domain'),
                         ('Zoras Domain Dive Warp', 'Lake Hylia'),
                         ('Lake Exit', 'Hyrule Field'),
                         ('Field to Valley', 'Gerudo Valley'),
                         ('Valley Exit', 'Hyrule Field'),
                         ('Valley River', 'Lake Hylia'),
                         ('Bridge Crossing', 'Gerudo Valley Far Side'),
                         ('Fortress Entrance', 'Gerudo Fortress'),
                         ('Haunted Wasteland Entrance', 'Haunted Wasteland'),
                         ('Haunted Wasteland Crossing', 'Desert Colossus'),
                         ('Field to Castle Town', 'Castle Town'),
                         ('Castle Town Exit', 'Hyrule Field'),
                         ('Hyrule Castle Grounds', 'Hyrule Castle Grounds'),
                         ('Hyrule Castle Grounds Exit', 'Castle Town'),
                         ('Hyrule Castle Garden', 'Hyrule Castle Garden'),
                         ('Hyrule Castle Garden Exit', 'Hyrule Castle Grounds'),
                         ('Ganons Castle Grounds', 'Ganons Castle Grounds'),
                         ('Ganons Castle Grounds Exit', 'Castle Town'),
                         ('Field to Kakariko', 'Kakariko Village'),
                         ('Kakariko Exit', 'Hyrule Field'),
                         ('Graveyard Entrance', 'Graveyard'),
                         ('Graveyard Exit', 'Kakariko Village'),
                         ('Drop to Graveyard', 'Graveyard'),
                         ('Death Mountain Entrance', 'Death Mountain'),
                         ('Death Mountain Exit', 'Kakariko Village'),
                         ('Goron City Entrance', 'Goron City'),
                         ('Goron City Exit', 'Death Mountain'),
                         ('Darunias Chamber', 'Darunias Chamber'),
                         ('Darunias Chamber Exit', 'Goron City'),
                         ('Mountain Crater Entrance', 'Death Mountain Crater Upper'),
                         ('Crater Exit', 'Death Mountain'),
                         ('Crater Hover Boots', 'Death Mountain Crater Lower'),
                         ('Crater Ascent', 'Death Mountain Crater Upper'),
                         ('Crater Scarecrow', 'Death Mountain Crater Central'),
                         ('Crater Bridge', 'Death Mountain Crater Central'),
                         ('Crater Bridge Reverse', 'Death Mountain Crater Lower'),
                         ('Crater to City', 'Goron City'),
                         ('Crater Access', 'Death Mountain Crater Lower'),
                         ('Dodongos Cavern Rocks', 'Dodongos Cavern Entryway'),
                         ('Mountain Access from Behind Rock', 'Death Mountain'),
                         ('Field to Zora River', 'Zora River Bottom'),
                         ('Zora River Exit', 'Hyrule Field'),
                         ('Zora River Rocks', 'Zora River Top'),
                         ('Zora River Downstream', 'Zora River Bottom'),
                         ('Zora River Waterfall', 'Zoras Domain'),
                         ('Zoras Domain Exit', 'Zora River Top'),
                         ('Behind King Zora', 'Zoras Fountain'),
                         ('Zoras Fountain Exit', 'Zoras Domain'),
                         ('Zora River Adult', 'Zora River Adult'),
                         ('Zoras Domain Adult Access', 'Zoras Domain Frozen'),
                         ('Zoras Fountain Adult Access', 'Outside Ice Cavern'),
                         ('Lon Lon Rance Entrance', 'Lon Lon Ranch'),
                         ('Lon Lon Exit', 'Hyrule Field'),
                         ('Deku Tree Slingshot Passage', 'Deku Tree Slingshot Room'),
                         ('Deku Tree Slingshot Exit', 'Deku Tree Lobby'),
                         ('Deku Tree Basement Path', 'Deku Tree Boss Room'),
                         ('Deku Tree Basement Vines', 'Deku Tree Lobby'),
                         ('Dodongos Cavern Lobby', 'Dodongos Cavern Lobby'),
                         ('Dodongos Cavern Retreat', 'Dodongos Cavern Beginning'),
                         ('Dodongos Cavern Left Door', 'Dodongos Cavern Climb'),
                         ('Dodongos Cavern Bridge Fall', 'Dodongos Cavern Lobby'),
                         ('Dodongos Cavern Slingshot Target', 'Dodongos Cavern Far Bridge'),
                         ('Dodongos Cavern Bridge Fall 2', 'Dodongos Cavern Lobby'),
                         ('Dodongos Cavern Bomb Drop', 'Dodongos Cavern Boss Area'),
                         ('Dodongos Cavern Exit Skull', 'Dodongos Cavern Lobby'),
                         ('Jabu Jabus Belly Ceiling Switch', 'Jabu Jabus Belly Main'),
                         ('Jabu Jabus Belly Retreat', 'Jabu Jabus Belly Beginning'),
                         ('Jabu Jabus Belly Tentacles', 'Jabu Jabus Belly Depths'),
                         ('Jabu Jabus Belly Elevator', 'Jabu Jabus Belly Main'),
                         ('Jabu Jabus Belly Octopus', 'Jabu Jabus Belly Boss Area'),
                         ('Jabu Jabus Belly Final Backtrack', 'Jabu Jabus Belly Main'),
                         ('Forest Temple Song of Time Block', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Lobby Eyeball Switch', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Lobby Locked Door', 'Forest Temple Block Push Room'),
                         ('Forest Temple Through Map Room', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Well Connection', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Outside to Lobby', 'Forest Temple Lobby'),
                         ('Forest Temple Scarecrows Song', 'Forest Temple Falling Room'),
                         ('Forest Temple Falling Room Exit', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Elevator', 'Forest Temple Boss Region'),
                         ('Forest Temple Outside Backdoor', 'Forest Temple Outside Upper Ledge'),
                         ('Forest Temple Twisted Hall', 'Forest Temple Bow Region'),
                         ('Forest Temple Straightened Hall', 'Forest Temple Straightened Hall'),
                         ('Forest Temple Boss Key Chest Drop', 'Forest Temple Outside Upper Ledge'),
                         ('Forest Temple Outside Ledge Drop', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Drop to Falling Room', 'Forest Temple Falling Room'),
                         ('Fire Temple Early Climb', 'Fire Temple Middle'),
                         ('Fire Temple Fire Maze Escape', 'Fire Temple Upper'),
                         ('Water Temple Central Pillar', 'Water Temple Middle Water Level'),
                         ('Water Temple Upper Locked Door', 'Water Temple Dark Link Region'),
                         ('Shadow Temple First Pit', 'Shadow Temple First Beamos'),
                         ('Shadow Temple Bomb Wall', 'Shadow Temple Huge Pit'),
                         ('Shadow Temple Hookshot Target', 'Shadow Temple Wind Tunnel'),
                         ('Shadow Temple Boat', 'Shadow Temple Beyond Boat'),
                         ('Gerudo Training Ground Left Silver Rupees', 'Gerudo Training Grounds Heavy Block Room'),
                         ('Gerudo Training Ground Beamos', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Ground Central Door', 'Gerudo Training Grounds Central Maze'),
                         ('Gerudo Training Grounds Right Locked Doors', 'Gerudo Training Grounds Central Maze Right'),
                         ('Gerudo Training Grounds Maze Exit', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Grounds Maze Ledge', 'Gerudo Training Grounds Central Maze Right'),
                         ('Gerudo Training Grounds Right Hookshot Target', 'Gerudo Training Grounds Hammer Room'),
                         ('Gerudo Training Grounds Hammer Target', 'Gerudo Training Grounds Eye Statue Lower'),
                         ('Gerudo Training Grounds Hammer Room Clear', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Grounds Eye Statue Exit', 'Gerudo Training Grounds Hammer Room'),
                         ('Gerudo Training Grounds Eye Statue Drop', 'Gerudo Training Grounds Eye Statue Lower'),
                         ('Gerudo Training Grounds Hidden Hookshot Target', 'Gerudo Training Grounds Eye Statue Upper'),
                         ('Spirit Temple Crawl Passage', 'Child Spirit Temple'),
                         ('Spirit Temple Silver Block', 'Early Adult Spirit Temple'),
                         ('Child Spirit Temple Passthrough', 'Spirit Temple Central Chamber'),
                         ('Adult Spirit Temple Passthrough', 'Spirit Temple Central Chamber'),
                         ('Spirit Temple to Hands', 'Spirit Temple Outdoor Hands'),
                         ('Spirit Temple Central Locked Door', 'Spirit Temple Beyond Central Locked Door'),
                         ('Spirit Temple Final Locked Door', 'Spirit Temple Beyond Final Locked Door'),
                         ('Ganons Castle Forest Trial', 'Ganons Castle Forest Trial'),
                         ('Ganons Castle Fire Trial', 'Ganons Castle Fire Trial'),
                         ('Ganons Castle Water Trial', 'Ganons Castle Water Trial'),
                         ('Ganons Castle Shadow Trial', 'Ganons Castle Shadow Trial'),
                         ('Ganons Castle Spirit Trial', 'Ganons Castle Spirit Trial'),
                         ('Ganons Castle Light Trial', 'Ganons Castle Light Trial'),
                         ('Ganons Castle Tower', 'Ganons Castle Tower')
                        ]

# non-shuffled entrance links
default_connections = [('Links House Exit', 'Kokiri Forest'),
                       ('Links House', 'Links House'),
                       ('Mido House Exit', 'Kokiri Forest'),
                       ('Mido House', 'Mido House'),
                       ('Saria House Exit', 'Kokiri Forest'),
                       ('Saria House', 'Saria House'),
                       ('House of Twins Exit', 'Kokiri Forest'),
                       ('House of Twins', 'House of Twins'),
                       ('Know It All House Exit', 'Kokiri Forest'),
                       ('Know It All House', 'Know It All House'),
                       ('Kokiri Shop Exit', 'Kokiri Forest'),
                       ('Kokiri Shop', 'Kokiri Shop'),
                       ('Lake Hylia Lab', 'Lake Hylia Lab'),
                       ('Fishing Hole', 'Fishing Hole'),
                       ('Colossus Fairy', 'Colossus Fairy'),
                       ('Temple of Time', 'Temple of Time'),
                       ('Temple of Time Exit', 'Castle Town'),
                       ('Door of Time', 'Beyond Door of Time'),
                       ('Emerge as Adult', 'Temple of Time'),
                       ('Hyrule Castle Fairy', 'Hyrule Castle Fairy'),
                       ('Ganons Castle Fairy', 'Ganons Castle Fairy'),
                       ('Castle Town Rupee Room', 'Castle Town Rupee Room'),
                       ('Castle Town Bazaar', 'Castle Town Bazaar'),
                       ('Castle Town Mask Shop', 'Castle Town Mask Shop'),
                       ('Castle Town Shooting Gallery', 'Castle Town Shooting Gallery'),
                       ('Castle Town Bombchu Bowling', 'Castle Town Bombchu Bowling'),
                       ('Castle Town Potion Shop', 'Castle Town Potion Shop'),
                       ('Castle Town Treasure Chest Game', 'Castle Town Treasure Chest Game'),
                       ('Castle Town Bombchu Shop', 'Castle Town Bombchu Shop'),
                       ('Castle Town Dog Lady', 'Castle Town Dog Lady'),
                       ('Castle Town Man in Green House', 'Castle Town Man in Green House'),
                       ('Carpenter Boss House', 'Carpenter Boss House'),
                       ('House of Skulltulla', 'House of Skulltulla'),
                       ('Impas House', 'Impas House'),
                       ('Impas House Back', 'Impas House Back'),
                       ('Windmill', 'Windmill'),
                       ('Kakariko Bazaar', 'Kakariko Bazaar'),
                       ('Kakariko Shooting Gallery', 'Kakariko Shooting Gallery'),
                       ('Kakariko Potion Shop Front', 'Kakariko Potion Shop Front'),
                       ('Kakariko Potion Shop Back', 'Kakariko Potion Shop Back'),
                       ('Odd Medicine Building', 'Odd Medicine Building'),
                       ('Shield Grave', 'Shield Grave'),
                       ('Heart Piece Grave', 'Heart Piece Grave'),
                       ('Composer Grave', 'Composer Grave'),
                       ('Dampes Grave', 'Dampes Grave'),
                       ('Crater Fairy', 'Crater Fairy'),
                       ('Mountain Summit Fairy', 'Mountain Summit Fairy'),
                       ('Dampes House', 'Dampes House'),
                       ('Talon House', 'Talon House'),
                       ('Ingo Barn', 'Ingo Barn'),
                       ('Lon Lon Corner Tower', 'Lon Lon Corner Tower'),
                       ('Zora Shop', 'Zora Shop'),
                       ('Zoras Fountain Fairy', 'Zoras Fountain Fairy'),
                       ('Forest Generic Grotto', 'Forest Generic Grotto'),
                       ('Deku Theater', 'Deku Theater'),
                       ('Forest Sales Grotto', 'Forest Sales Grotto'),
                       ('Meadow Fairy Grotto', 'Meadow Fairy Grotto'),
                       ('Front of Meadow Grotto', 'Front of Meadow Grotto'),
                       ('Lon Lon Grotto', 'Lon Lon Grotto'),
                       ('Remote Southern Grotto', 'Remote Southern Grotto'),
                       ('Field Near Lake Outside Fence Grotto', 'Field Near Lake Outside Fence Grotto'),
                       ('Field Near Lake Inside Fence Grotto', 'Field Near Lake Inside Fence Grotto'),
                       ('Field Valley Grotto', 'Field Valley Grotto'),
                       ('Field West Castle Town Grotto', 'Field West Castle Town Grotto'),
                       ('Field Far West Castle Town Grotto', 'Field Far West Castle Town Grotto'),
                       ('Field Kakariko Grotto', 'Field Kakariko Grotto'),
                       ('Kakariko Bombable Grotto', 'Kakariko Bombable Grotto'),
                       ('Kakariko Back Grotto', 'Kakariko Back Grotto'),
                       ('Mountain Bombable Grotto', 'Mountain Bombable Grotto'),
                       ('Top of Crater Grotto', 'Top of Crater Grotto'),
                       ('Field North Lon Lon Grotto', 'Field North Lon Lon Grotto'),
                       ('Castle Storms Grotto', 'Castle Storms Grotto'),
                       ('Zora River Plateau Open Grotto', 'Zora River Plateau Open Grotto'),
                       ('Zora River Plateau Bombable Grotto', 'Zora River Plateau Bombable Grotto'),
                       ('Lake Hylia Grotto', 'Lake Hylia Grotto')
                      ]

# non shuffled dungeons
default_dungeon_connections = [('Deku Tree', 'Deku Tree Lobby'),
                               ('Deku Tree Exit', 'Kokiri Forest'),
                               ('Dodongos Cavern', 'Dodongos Cavern Beginning'),
                               ('Dodongos Cavern Exit', 'Dodongos Cavern Entryway'),
                               ('Jabu Jabus Belly', 'Jabu Jabus Belly Beginning'),
                               ('Jabu Jabus Belly Exit', 'Zoras Fountain'),
                               ('Forest Temple Entrance', 'Forest Temple Lobby'),
                               ('Forest Temple Exit', 'Forest Temple Entry Area'),
                               ('Bottom of the Well', 'Bottom of the Well'),
                               ('Bottom of the Well Exit', 'Kakariko Village'),
                               ('Fire Temple Entrance', 'Fire Temple Lower'),
                               ('Fire Temple Exit', 'Death Mountain Crater Central'),
                               ('Ice Cavern Entrance', 'Ice Cavern'),
                               ('Ice Cavern Exit', 'Outside Ice Cavern'),
                               ('Water Temple Entrance', 'Water Temple Lobby'),
                               ('Water Temple Exit', 'Lake Hylia'),
                               ('Shadow Temple Entrance', 'Shadow Temple Beginning'),
                               ('Shadow Temple Exit', 'Shadow Temple Warp Region'),
                               ('Gerudo Training Grounds Entrance', 'Gerudo Training Grounds Lobby'),
                               ('Gerudo Training Grounds Exit', 'Gerudo Fortress'),
                               ('Spirit Temple Entrance', 'Spirit Temple Lobby'),
                               ('Spirit Temple Exit', 'Desert Colossus'),
                               ('Rainbow Bridge', 'Ganons Castle Lobby'),
                               ('Ganons Castle Exit', 'Ganons Castle Grounds')
                              ]


# format:
# Key=Name
# addr = (door_index, exitdata) # multiexit
#       | ([addr], None)  # holes
# exitdata = (room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2)

# ToDo somehow merge this with creation of the locations
door_addresses = {'Links House': (0x00, (0x0104, 0x2c, 0x0506, 0x0a9a, 0x0832, 0x0ae8, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfe, 0x0816, 0x0000)),
                  'Desert Palace Entrance (South)': (0x08, (0x0084, 0x30, 0x0314, 0x0c56, 0x00a6, 0x0ca8, 0x0128, 0x0cc3, 0x0133, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Desert Palace Entrance (West)': (0x0A, (0x0083, 0x30, 0x0280, 0x0c46, 0x0003, 0x0c98, 0x0088, 0x0cb3, 0x0090, 0x0a, 0xfd, 0x0000, 0x0000)),
                  'Desert Palace Entrance (North)': (0x0B, (0x0063, 0x30, 0x0016, 0x0c00, 0x00a2, 0x0c28, 0x0128, 0x0c6d, 0x012f, 0x00, 0x0e, 0x0000, 0x0000)),
                  'Desert Palace Entrance (East)': (0x09, (0x0085, 0x30, 0x02a8, 0x0c4a, 0x0142, 0x0c98, 0x01c8, 0x0cb7, 0x01cf, 0x06, 0xfe, 0x0000, 0x0000)),
                  'Eastern Palace': (0x07, (0x00c9, 0x1e, 0x005a, 0x0600, 0x0ed6, 0x0618, 0x0f50, 0x066d, 0x0f5b, 0x00, 0xfa, 0x0000, 0x0000)),
                  'Tower of Hera': (0x32, (0x0077, 0x03, 0x0050, 0x0014, 0x087c, 0x0068, 0x08f0, 0x0083, 0x08fb, 0x0a, 0xf4, 0x0000, 0x0000)),
                  'Hyrule Castle Entrance (South)': (0x03, (0x0061, 0x1b, 0x0530, 0x0692, 0x0784, 0x06cc, 0x07f8, 0x06ff, 0x0803, 0x0e, 0xfa, 0x0000, 0x87be)),
                  'Hyrule Castle Entrance (West)': (0x02, (0x0060, 0x1b, 0x0016, 0x0600, 0x06ae, 0x0604, 0x0728, 0x066d, 0x0733, 0x00, 0x02, 0x0000, 0x8124)),
                  'Hyrule Castle Entrance (East)': (0x04, (0x0062, 0x1b, 0x004a, 0x0600, 0x0856, 0x0604, 0x08c8, 0x066d, 0x08d3, 0x00, 0xfa, 0x0000, 0x8158)),
                  'Agahnims Tower': (0x23, (0x00e0, 0x1b, 0x0032, 0x0600, 0x0784, 0x0634, 0x07f8, 0x066d, 0x0803, 0x00, 0x0a, 0x0000, 0x82be)),
                  'Thieves Town': (0x33, (0x00db, 0x58, 0x0b2e, 0x075a, 0x0176, 0x07a8, 0x01f8, 0x07c7, 0x0203, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Skull Woods First Section Door': (0x29, (0x0058, 0x40, 0x0f4c, 0x01f6, 0x0262, 0x0248, 0x02e8, 0x0263, 0x02ef, 0x0a, 0xfe, 0x0000, 0x0000)),
                  'Skull Woods Second Section Door (East)': (0x28, (0x0057, 0x40, 0x0eb8, 0x01e6, 0x01c2, 0x0238, 0x0248, 0x0253, 0x024f, 0x0a, 0xfe, 0x0000, 0x0000)),
                  'Skull Woods Second Section Door (West)': (0x27, (0x0056, 0x40, 0x0c8e, 0x01a6, 0x0062, 0x01f8, 0x00e8, 0x0213, 0x00ef, 0x0a, 0x0e, 0x0000, 0x0000)),
                  'Skull Woods Final Section': (0x2A, (0x0059, 0x40, 0x0282, 0x0066, 0x0016, 0x00b8, 0x0098, 0x00d3, 0x00a3, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Ice Palace': (0x2C, (0x000e, 0x75, 0x0bc6, 0x0d6a, 0x0c3e, 0x0db8, 0x0cb8, 0x0dd7, 0x0cc3, 0x06, 0xf2, 0x0000, 0x0000)),
                  'Misery Mire': (0x26, (0x0098, 0x70, 0x0414, 0x0c79, 0x00a6, 0x0cc7, 0x0128, 0x0ce6, 0x0133, 0x07, 0xfa, 0x0000, 0x0000)),
                  'Palace of Darkness': (0x25, (0x004a, 0x5e, 0x005a, 0x0600, 0x0ed6, 0x0628, 0x0f50, 0x066d, 0x0f5b, 0x00, 0xfa, 0x0000, 0x0000)),
                  'Swamp Palace': (0x24, (0x0028, 0x7b, 0x049e, 0x0e8c, 0x06f2, 0x0ed8, 0x0778, 0x0ef9, 0x077f, 0x04, 0xfe, 0x0000, 0x0000)),
                  'Turtle Rock': (0x34, (0x00d6, 0x47, 0x0712, 0x00da, 0x0e96, 0x0128, 0x0f08, 0x0147, 0x0f13, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Dark Death Mountain Ledge (West)': (0x14, (0x0023, 0x45, 0x07ca, 0x0103, 0x0c46, 0x0157, 0x0cb8, 0x0172, 0x0cc3, 0x0b, 0x0a, 0x0000, 0x0000)),
                  'Dark Death Mountain Ledge (East)': (0x18, (0x0024, 0x45, 0x07e0, 0x0103, 0x0d00, 0x0157, 0x0d78, 0x0172, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Turtle Rock Isolated Ledge Entrance': (0x17, (0x00d5, 0x45, 0x0ad4, 0x0164, 0x0ca6, 0x01b8, 0x0d18, 0x01d3, 0x0d23, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Hyrule Castle Secret Entrance Stairs': (0x31, (0x0055, 0x1b, 0x044a, 0x067a, 0x0854, 0x06c8, 0x08c8, 0x06e7, 0x08d3, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Kakariko Well Cave': (0x38, (0x002f, 0x18, 0x0386, 0x0665, 0x0032, 0x06b7, 0x00b8, 0x06d2, 0x00bf, 0x0b, 0xfe, 0x0000, 0x0000)),
                  'Bat Cave Cave': (0x10, (0x00e3, 0x22, 0x0412, 0x087a, 0x048e, 0x08c8, 0x0508, 0x08e7, 0x0513, 0x06, 0x02, 0x0000, 0x0000)),
                  'Elder House (East)': (0x0D, (0x00f3, 0x18, 0x02c4, 0x064a, 0x0222, 0x0698, 0x02a8, 0x06b7, 0x02af, 0x06, 0xfe, 0x05d4, 0x0000)),
                  'Elder House (West)': (0x0C, (0x00f2, 0x18, 0x02bc, 0x064c, 0x01e2, 0x0698, 0x0268, 0x06b9, 0x026f, 0x04, 0xfe, 0x05cc, 0x0000)),
                  'North Fairy Cave': (0x37, (0x0008, 0x15, 0x0088, 0x0400, 0x0a36, 0x0448, 0x0aa8, 0x046f, 0x0ab3, 0x00, 0x0a, 0x0000, 0x0000)),
                  'Lost Woods Hideout Stump': (0x2B, (0x00e1, 0x00, 0x0f4e, 0x01f6, 0x0262, 0x0248, 0x02e8, 0x0263, 0x02ef, 0x0a, 0x0e, 0x0000, 0x0000)),
                  'Lumberjack Tree Cave': (0x11, (0x00e2, 0x02, 0x0118, 0x0015, 0x04c6, 0x0067, 0x0548, 0x0082, 0x0553, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Two Brothers House (East)': (0x0F, (0x00f5, 0x29, 0x0880, 0x0b07, 0x0200, 0x0b58, 0x0238, 0x0b74, 0x028d, 0x09, 0x00, 0x0b86, 0x0000)),
                  'Two Brothers House (West)': (0x0E, (0x00f4, 0x28, 0x08a0, 0x0b06, 0x0100, 0x0b58, 0x01b8, 0x0b73, 0x018d, 0x0a, 0x00, 0x0bb6, 0x0000)),
                  'Sanctuary': (0x01, (0x0012, 0x13, 0x001c, 0x0400, 0x06de, 0x0414, 0x0758, 0x046d, 0x0763, 0x00, 0x02, 0x0000, 0x01aa)),
                  'Old Man Cave (West)': (0x05, (0x00f0, 0x0a, 0x03a0, 0x0264, 0x0500, 0x02b8, 0x05a8, 0x02d3, 0x058d, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Old Man Cave (East)': (0x06, (0x00f1, 0x03, 0x1402, 0x0294, 0x0604, 0x02e8, 0x0678, 0x0303, 0x0683, 0x0a, 0xfc, 0x0000, 0x0000)),
                  'Old Man House (Bottom)': (0x2F, (0x00e4, 0x03, 0x181a, 0x031e, 0x06b4, 0x03a7, 0x0728, 0x038d, 0x0733, 0x00, 0x0c, 0x0000, 0x0000)),
                  'Old Man House (Top)': (0x30, (0x00e5, 0x03, 0x10c6, 0x0224, 0x0814, 0x0278, 0x0888, 0x0293, 0x0893, 0x0a, 0x0c, 0x0000, 0x0000)),
                  'Death Mountain Return Cave (East)': (0x2E, (0x00e7, 0x03, 0x0d82, 0x01c4, 0x0600, 0x0218, 0x0648, 0x0233, 0x067f, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Death Mountain Return Cave (West)': (0x2D, (0x00e6, 0x0a, 0x00a0, 0x0205, 0x0500, 0x0257, 0x05b8, 0x0272, 0x058d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Spectacle Rock Cave Peak': (0x22, (0x00ea, 0x03, 0x092c, 0x0133, 0x0754, 0x0187, 0x07c8, 0x01a2, 0x07d3, 0x0b, 0xfc, 0x0000, 0x0000)),
                  'Spectacle Rock Cave': (0x21, (0x00fa, 0x03, 0x0eac, 0x01e3, 0x0754, 0x0237, 0x07c8, 0x0252, 0x07d3, 0x0b, 0xfc, 0x0000, 0x0000)),
                  'Spectacle Rock Cave (Bottom)': (0x20, (0x00f9, 0x03, 0x0d9c, 0x01c3, 0x06d4, 0x0217, 0x0748, 0x0232, 0x0753, 0x0b, 0xfc, 0x0000, 0x0000)),
                  'Paradox Cave (Bottom)': (0x1D, (0x00ff, 0x05, 0x0ee0, 0x01e3, 0x0d00, 0x0237, 0x0da8, 0x0252, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Paradox Cave (Middle)': (0x1E, (0x00ef, 0x05, 0x17e0, 0x0304, 0x0d00, 0x0358, 0x0dc8, 0x0373, 0x0d7d, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Paradox Cave (Top)': (0x1F, (0x00df, 0x05, 0x0460, 0x0093, 0x0d00, 0x00e7, 0x0db8, 0x0102, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Fairy Ascension Cave (Bottom)': (0x19, (0x00fd, 0x05, 0x0dd4, 0x01c4, 0x0ca6, 0x0218, 0x0d18, 0x0233, 0x0d23, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Fairy Ascension Cave (Top)': (0x1A, (0x00ed, 0x05, 0x0ad4, 0x0163, 0x0ca6, 0x01b7, 0x0d18, 0x01d2, 0x0d23, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Spiral Cave': (0x1C, (0x00ee, 0x05, 0x07c8, 0x0108, 0x0c46, 0x0158, 0x0cb8, 0x0177, 0x0cc3, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Spiral Cave (Bottom)': (0x1B, (0x00fe, 0x05, 0x0cca, 0x01a3, 0x0c56, 0x01f7, 0x0cc8, 0x0212, 0x0cd3, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Bumper Cave (Bottom)': (0x15, (0x00fb, 0x4a, 0x03a0, 0x0263, 0x0500, 0x02b7, 0x05a8, 0x02d2, 0x058d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Bumper Cave (Top)': (0x16, (0x00eb, 0x4a, 0x00a0, 0x020a, 0x0500, 0x0258, 0x05b8, 0x0277, 0x058d, 0x06, 0x00, 0x0000, 0x0000)),
                  'Superbunny Cave (Top)': (0x13, (0x00e8, 0x45, 0x0460, 0x0093, 0x0d00, 0x00e7, 0x0db8, 0x0102, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Superbunny Cave (Bottom)': (0x12, (0x00f8, 0x45, 0x0ee0, 0x01e4, 0x0d00, 0x0238, 0x0d78, 0x0253, 0x0d7d, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Hookshot Cave': (0x39, (0x003c, 0x45, 0x04da, 0x00a3, 0x0cd6, 0x0107, 0x0d48, 0x0112, 0x0d53, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Hookshot Cave Back Entrance': (0x3A, (0x002c, 0x45, 0x004c, 0x0000, 0x0c56, 0x0038, 0x0cc8, 0x006f, 0x0cd3, 0x00, 0x0a, 0x0000, 0x0000)),
                  'Ganons Tower': (0x36, (0x000c, 0x43, 0x0052, 0x0000, 0x0884, 0x0028, 0x08f8, 0x006f, 0x0903, 0x00, 0xfc, 0x0000, 0x0000)),
                  'Pyramid Entrance': (0x35, (0x0010, 0x5b, 0x0b0e, 0x075a, 0x0674, 0x07a8, 0x06e8, 0x07c7, 0x06f3, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Skull Woods First Section Hole (West)': ([0xDB84D, 0xDB84E], None),
                  'Skull Woods First Section Hole (East)': ([0xDB84F, 0xDB850], None),
                  'Skull Woods First Section Hole (North)': ([0xDB84C], None),
                  'Skull Woods Second Section Hole': ([0xDB851, 0xDB852], None),
                  'Pyramid Hole': ([0xDB854, 0xDB855, 0xDB856], None),
                  'Waterfall of Wishing': (0x5B, (0x0114, 0x0f, 0x0080, 0x0200, 0x0e00, 0x0207, 0x0e60, 0x026f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000)),
                  'Dam': (0x4D, (0x010b, 0x3b, 0x04a0, 0x0e8a, 0x06fa, 0x0ed8, 0x0778, 0x0ef7, 0x077f, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Blinds Hideout': (0x60, (0x0119, 0x18, 0x02b2, 0x064a, 0x0186, 0x0697, 0x0208, 0x06b7, 0x0213, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Hyrule Castle Secret Entrance Drop': ([0xDB858], None),
                  'Bonk Fairy (Light)': (0x76, (0x0126, 0x2b, 0x00a0, 0x0a0a, 0x0700, 0x0a67, 0x0788, 0x0a77, 0x0785, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Lake Hylia Fairy': (0x5D, (0x0115, 0x2e, 0x0016, 0x0a00, 0x0cb6, 0x0a37, 0x0d28, 0x0a6d, 0x0d33, 0x00, 0x00, 0x0000, 0x0000)),
                  'Light Hype Fairy': (0x6B, (0x0115, 0x34, 0x00a0, 0x0c04, 0x0900, 0x0c58, 0x0988, 0x0c73, 0x0985, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Desert Fairy': (0x71, (0x0115, 0x3a, 0x0000, 0x0e00, 0x0400, 0x0e26, 0x0468, 0x0e6d, 0x0485, 0x00, 0x00, 0x0000, 0x0000)),
                  'Kings Grave': (0x5A, (0x0113, 0x14, 0x0320, 0x0456, 0x0900, 0x04a6, 0x0998, 0x04c3, 0x097d, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Tavern North': (0x42, (0x0103, 0x18, 0x1440, 0x08a7, 0x0206, 0x08f9, 0x0288, 0x0914, 0x0293, 0xf7, 0x09, 0xFFFF, 0x0000)),  # do not use, buggy
                  'Chicken House': (0x4A, (0x0108, 0x18, 0x1120, 0x0837, 0x0106, 0x0888, 0x0188, 0x08a4, 0x0193, 0x07, 0xf9, 0x1530, 0x0000)),
                  'Aginahs Cave': (0x70, (0x010a, 0x30, 0x0656, 0x0cc6, 0x02aa, 0x0d18, 0x0328, 0x0d33, 0x032f, 0x08, 0xf8, 0x0000, 0x0000)),
                  'Sahasrahlas Hut': (0x44, (0x0105, 0x1e, 0x0610, 0x06d4, 0x0c76, 0x0727, 0x0cf0, 0x0743, 0x0cfb, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Cave Shop (Lake Hylia)': (0x57, (0x0112, 0x35, 0x0022, 0x0c00, 0x0b1a, 0x0c26, 0x0b98, 0x0c6d, 0x0b9f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Capacity Upgrade': (0x5C, (0x0115, 0x35, 0x0a46, 0x0d36, 0x0c2a, 0x0d88, 0x0ca8, 0x0da3, 0x0caf, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Kakariko Well Drop': ([0xDB85C, 0xDB85D], None),
                  'Blacksmiths Hut': (0x63, (0x0121, 0x22, 0x010c, 0x081a, 0x0466, 0x0868, 0x04d8, 0x0887, 0x04e3, 0x06, 0xfa, 0x041A, 0x0000)),
                  'Bat Cave Drop': ([0xDB859, 0xDB85A], None),
                  'Sick Kids House': (0x3F, (0x0102, 0x18, 0x10be, 0x0826, 0x01f6, 0x0877, 0x0278, 0x0893, 0x0283, 0x08, 0xf8, 0x14CE, 0x0000)),
                  'North Fairy Cave Drop': ([0xDB857], None),
                  'Lost Woods Gamble': (0x3B, (0x0100, 0x00, 0x004e, 0x0000, 0x0272, 0x0008, 0x02f0, 0x006f, 0x02f7, 0x00, 0x00, 0x0000, 0x0000)),
                  'Fortune Teller (Light)': (0x64, (0x0122, 0x11, 0x060e, 0x04b4, 0x027d, 0x0508, 0x02f8, 0x0523, 0x0302, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Snitch Lady (East)': (0x3D, (0x0101, 0x18, 0x0ad8, 0x074a, 0x02c6, 0x0798, 0x0348, 0x07b7, 0x0353, 0x06, 0xfa, 0x0DE8, 0x0000)),
                  'Snitch Lady (West)': (0x3E, (0x0101, 0x18, 0x0788, 0x0706, 0x0046, 0x0758, 0x00c8, 0x0773, 0x00d3, 0x08, 0xf8, 0x0B98, 0x0000)),
                  'Bush Covered House': (0x43, (0x0103, 0x18, 0x1156, 0x081a, 0x02b6, 0x0868, 0x0338, 0x0887, 0x0343, 0x06, 0xfa, 0x1466, 0x0000)),
                  'Tavern (Front)': (0x41, (0x0103, 0x18, 0x1842, 0x0916, 0x0206, 0x0967, 0x0288, 0x0983, 0x0293, 0x08, 0xf8, 0x1C50, 0x0000)),
                  'Light World Bomb Hut': (0x49, (0x0107, 0x18, 0x1800, 0x0916, 0x0000, 0x0967, 0x0068, 0x0983, 0x008d, 0x08, 0xf8, 0x9C0C, 0x0000)),
                  'Kakariko Shop': (0x45, (0x011f, 0x18, 0x16a8, 0x08e7, 0x0136, 0x0937, 0x01b8, 0x0954, 0x01c3, 0x07, 0xf9, 0x1AB6, 0x0000)),
                  'Lost Woods Hideout Drop': ([0xDB853], None),
                  'Lumberjack Tree Tree': ([0xDB85B], None),
                  'Cave 45': (0x50, (0x011b, 0x32, 0x0680, 0x0cc9, 0x0400, 0x0d16, 0x0438, 0x0d36, 0x0485, 0x07, 0xf9, 0x0000, 0x0000)),
                  'Graveyard Cave': (0x51, (0x011b, 0x14, 0x0016, 0x0400, 0x08a2, 0x0446, 0x0918, 0x046d, 0x091f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Checkerboard Cave': (0x7D, (0x0126, 0x30, 0x00c8, 0x0c0a, 0x024a, 0x0c67, 0x02c8, 0x0c77, 0x02cf, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Mini Moldorm Cave': (0x7C, (0x0123, 0x35, 0x1480, 0x0e96, 0x0a00, 0x0ee8, 0x0a68, 0x0f03, 0x0a85, 0x08, 0xf8, 0x0000, 0x0000)),
                  'Long Fairy Cave': (0x54, (0x011e, 0x2f, 0x06a0, 0x0aca, 0x0f00, 0x0b18, 0x0fa8, 0x0b37, 0x0f85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Good Bee Cave': (0x6A, (0x0120, 0x37, 0x0084, 0x0c00, 0x0e26, 0x0c36, 0x0e98, 0x0c6f, 0x0ea3, 0x00, 0x00, 0x0000, 0x0000)),
                  '20 Rupee Cave': (0x7A, (0x0125, 0x37, 0x0200, 0x0c23, 0x0e00, 0x0c86, 0x0e68, 0x0c92, 0x0e7d, 0x0d, 0xf3, 0x0000, 0x0000)),
                  '50 Rupee Cave': (0x78, (0x0124, 0x3a, 0x0790, 0x0eea, 0x047a, 0x0f47, 0x04f8, 0x0f57, 0x04ff, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Ice Rod Cave': (0x7F, (0x0120, 0x37, 0x0080, 0x0c00, 0x0e00, 0x0c37, 0x0e48, 0x0c6f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000)),
                  'Bonk Rock Cave': (0x79, (0x0124, 0x13, 0x0280, 0x044a, 0x0600, 0x04a7, 0x0638, 0x04b7, 0x067d, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Library': (0x48, (0x0107, 0x29, 0x0100, 0x0a14, 0x0200, 0x0a67, 0x0278, 0x0a83, 0x0285, 0x0a, 0xf6, 0x040E, 0x0000)),
                  'Potion Shop': (0x4B, (0x0109, 0x16, 0x070a, 0x04e6, 0x0c56, 0x0538, 0x0cc8, 0x0553, 0x0cd3, 0x08, 0xf8, 0x0A98, 0x0000)),
                  'Sanctuary Grave': ([0xDB85E], None),
                  'Hookshot Fairy': (0x4F, (0x010c, 0x05, 0x0ee0, 0x01e3, 0x0d00, 0x0236, 0x0d78, 0x0252, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Pyramid Fairy': (0x62, (0x0116, 0x5b, 0x0b1e, 0x0754, 0x06fa, 0x07a7, 0x0778, 0x07c3, 0x077f, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'East Dark World Hint': (0x68, (0x010e, 0x6f, 0x06a0, 0x0aca, 0x0f00, 0x0b18, 0x0fa8, 0x0b37, 0x0f85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Palace of Darkness Hint': (0x67, (0x011a, 0x5e, 0x0c24, 0x0794, 0x0d12, 0x07e8, 0x0d90, 0x0803, 0x0d97, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Dark Lake Hylia Fairy': (0x6C, (0x0115, 0x6e, 0x0016, 0x0a00, 0x0cb6, 0x0a36, 0x0d28, 0x0a6d, 0x0d33, 0x00, 0x00, 0x0000, 0x0000)),
                  'Dark Lake Hylia Ledge Fairy': (0x80, (0x0115, 0x77, 0x0080, 0x0c00, 0x0e00, 0x0c37, 0x0e48, 0x0c6f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000)),
                  'Dark Lake Hylia Ledge Spike Cave': (0x7B, (0x0125, 0x77, 0x0200, 0x0c27, 0x0e00, 0x0c86, 0x0e68, 0x0c96, 0x0e7d, 0x09, 0xf7, 0x0000, 0x0000)),
                  'Dark Lake Hylia Ledge Hint': (0x69, (0x010e, 0x77, 0x0084, 0x0c00, 0x0e26, 0x0c36, 0x0e98, 0x0c6f, 0x0ea3, 0x00, 0x00, 0x0000, 0x0000)),
                  'Hype Cave': (0x3C, (0x011e, 0x74, 0x00a0, 0x0c0a, 0x0900, 0x0c58, 0x0988, 0x0c77, 0x097d, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Bonk Fairy (Dark)': (0x77, (0x0126, 0x6b, 0x00a0, 0x0a05, 0x0700, 0x0a66, 0x0788, 0x0a72, 0x0785, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Brewery': (0x47, (0x0106, 0x58, 0x16a8, 0x08e4, 0x013e, 0x0938, 0x01b8, 0x0953, 0x01c3, 0x0a, 0xf6, 0x1AB6, 0x0000)),
                  'C-Shaped House': (0x53, (0x011c, 0x58, 0x09d8, 0x0744, 0x02ce, 0x0797, 0x0348, 0x07b3, 0x0353, 0x0a, 0xf6, 0x0DE8, 0x0000)),
                  'Chest Game': (0x46, (0x0106, 0x58, 0x078a, 0x0705, 0x004e, 0x0758, 0x00c8, 0x0774, 0x00d3, 0x09, 0xf7, 0x0B98, 0x0000)),
                  'Dark World Hammer Peg Cave': (0x7E, (0x0127, 0x62, 0x0894, 0x091e, 0x0492, 0x09a6, 0x0508, 0x098b, 0x050f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Red Shield Shop': (0x74, (0x0110, 0x5a, 0x079a, 0x06e8, 0x04d6, 0x0738, 0x0548, 0x0755, 0x0553, 0x08, 0xf8, 0x0AA8, 0x0000)),
                  'Dark Sanctuary Hint': (0x59, (0x0112, 0x53, 0x001e, 0x0400, 0x06e2, 0x0446, 0x0758, 0x046d, 0x075f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Fortune Teller (Dark)': (0x65, (0x0122, 0x51, 0x0610, 0x04b4, 0x027e, 0x0507, 0x02f8, 0x0523, 0x0303, 0x0a, 0xf6, 0x091E, 0x0000)),
                  'Dark World Shop': (0x5F, (0x010f, 0x58, 0x1058, 0x0814, 0x02be, 0x0868, 0x0338, 0x0883, 0x0343, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Dark World Lumberjack Shop': (0x56, (0x010f, 0x42, 0x041c, 0x0074, 0x04e2, 0x00c7, 0x0558, 0x00e3, 0x055f, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Dark World Potion Shop': (0x6E, (0x010f, 0x56, 0x080e, 0x04f4, 0x0c66, 0x0548, 0x0cd8, 0x0563, 0x0ce3, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Archery Game': (0x58, (0x0111, 0x69, 0x069e, 0x0ac4, 0x02ea, 0x0b18, 0x0368, 0x0b33, 0x036f, 0x0a, 0xf6, 0x09AC, 0x0000)),
                  'Mire Shed': (0x5E, (0x010d, 0x70, 0x0384, 0x0c69, 0x001e, 0x0cb6, 0x0098, 0x0cd6, 0x00a3, 0x07, 0xf9, 0x0000, 0x0000)),
                  'Dark Desert Hint': (0x61, (0x0114, 0x70, 0x0654, 0x0cc5, 0x02aa, 0x0d16, 0x0328, 0x0d32, 0x032f, 0x09, 0xf7, 0x0000, 0x0000)),
                  'Dark Desert Fairy': (0x55, (0x0115, 0x70, 0x03a8, 0x0c6a, 0x013a, 0x0cb7, 0x01b8, 0x0cd7, 0x01bf, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Spike Cave': (0x40, (0x0117, 0x43, 0x0ed4, 0x01e4, 0x08aa, 0x0236, 0x0928, 0x0253, 0x092f, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Cave Shop (Dark Death Mountain)': (0x6D, (0x0112, 0x45, 0x0ee0, 0x01e3, 0x0d00, 0x0236, 0x0daa, 0x0252, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Dark Death Mountain Fairy': (0x6F, (0x0115, 0x43, 0x1400, 0x0294, 0x0600, 0x02e8, 0x0678, 0x0303, 0x0685, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Mimic Cave': (0x4E, (0x010c, 0x05, 0x07e0, 0x0103, 0x0d00, 0x0156, 0x0d78, 0x0172, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Big Bomb Shop': (0x52, (0x011c, 0x6c, 0x0506, 0x0a9a, 0x0832, 0x0ae7, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfa, 0x0816, 0x0000)),
                  'Dark Lake Hylia Shop': (0x73, (0x010f, 0x75, 0x0380, 0x0c6a, 0x0a00, 0x0cb8, 0x0a58, 0x0cd7, 0x0a85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Lumberjack House': (0x75, (0x011f, 0x02, 0x049c, 0x0088, 0x04e6, 0x00d8, 0x0558, 0x00f7, 0x0563, 0x08, 0xf8, 0x07AA, 0x0000)),
                  'Lake Hylia Fortune Teller': (0x72, (0x0122, 0x35, 0x0380, 0x0c6a, 0x0a00, 0x0cb8, 0x0a58, 0x0cd7, 0x0a85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Kakariko Gamble Game': (0x66, (0x0118, 0x29, 0x069e, 0x0ac4, 0x02ea, 0x0b18, 0x0368, 0x0b33, 0x036f, 0x0a, 0xf6, 0x09AC, 0x0000))}

# format:
# Key=Name
# value = entrance #
#        | (entrance #, exit #)
exit_ids = {'Links House Exit': (0x01, 0x00),
            'Chris Houlihan Room Exit': (None, 0x3D),
            'Desert Palace Exit (South)': (0x09, 0x0A),
            'Desert Palace Exit (West)': (0x0B, 0x0C),
            'Desert Palace Exit (East)': (0x0A, 0x0B),
            'Desert Palace Exit (North)': (0x0C, 0x0D),
            'Eastern Palace Exit': (0x08, 0x09),
            'Tower of Hera Exit': (0x33, 0x2D),
            'Hyrule Castle Exit (South)': (0x04, 0x03),
            'Hyrule Castle Exit (West)': (0x03, 0x02),
            'Hyrule Castle Exit (East)': (0x05, 0x04),
            'Agahnims Tower Exit': (0x24, 0x25),
            'Thieves Town Exit': (0x34, 0x35),
            'Skull Woods First Section Exit': (0x2A, 0x2B),
            'Skull Woods Second Section Exit (East)': (0x29, 0x2A),
            'Skull Woods Second Section Exit (West)': (0x28, 0x29),
            'Skull Woods Final Section Exit': (0x2B, 0x2C),
            'Ice Palace Exit': (0x2D, 0x2E),
            'Misery Mire Exit': (0x27, 0x28),
            'Palace of Darkness Exit': (0x26, 0x27),
            'Swamp Palace Exit': (0x25, 0x26),
            'Turtle Rock Exit (Front)': (0x35, 0x34),
            'Turtle Rock Ledge Exit (West)': (0x15, 0x16),
            'Turtle Rock Ledge Exit (East)': (0x19, 0x1A),
            'Turtle Rock Isolated Ledge Exit': (0x18, 0x19),
            'Hyrule Castle Secret Entrance Exit': (0x32, 0x33),
            'Kakariko Well Exit': (0x39, 0x3A),
            'Bat Cave Exit': (0x11, 0x12),
            'Elder House Exit (East)': (0x0E, 0x0F),
            'Elder House Exit (West)': (0x0D, 0x0E),
            'North Fairy Cave Exit': (0x38, 0x39),
            'Lost Woods Hideout Exit': (0x2C, 0x36),
            'Lumberjack Tree Exit': (0x12, 0x13),
            'Two Brothers House Exit (East)': (0x10, 0x11),
            'Two Brothers House Exit (West)': (0x0F, 0x10),
            'Sanctuary Exit': (0x02, 0x01),
            'Old Man Cave Exit (East)': (0x07, 0x08),
            'Old Man Cave Exit (West)': (0x06, 0x07),
            'Old Man House Exit (Bottom)': (0x30, 0x31),
            'Old Man House Exit (Top)': (0x31, 0x32),
            'Death Mountain Return Cave Exit (West)': (0x2E, 0x2F),
            'Death Mountain Return Cave Exit (East)': (0x2F, 0x30),
            'Spectacle Rock Cave Exit': (0x21, 0x22),
            'Spectacle Rock Cave Exit (Top)': (0x22, 0x23),
            'Spectacle Rock Cave Exit (Peak)': (0x23, 0x24),
            'Paradox Cave Exit (Bottom)': (0x1E, 0x1F),
            'Paradox Cave Exit (Middle)': (0x1F, 0x20),
            'Paradox Cave Exit (Top)': (0x20, 0x21),
            'Fairy Ascension Cave Exit (Bottom)': (0x1A, 0x1B),
            'Fairy Ascension Cave Exit (Top)': (0x1B, 0x1C),
            'Spiral Cave Exit': (0x1C, 0x1D),
            'Spiral Cave Exit (Top)': (0x1D, 0x1E),
            'Bumper Cave Exit (Top)': (0x17, 0x18),
            'Bumper Cave Exit (Bottom)': (0x16, 0x17),
            'Superbunny Cave Exit (Top)': (0x14, 0x15),
            'Superbunny Cave Exit (Bottom)': (0x13, 0x14),
            'Hookshot Cave Exit (South)': (0x3A, 0x3B),
            'Hookshot Cave Exit (North)': (0x3B, 0x3C),
            'Ganons Tower Exit': (0x37, 0x38),
            'Pyramid Exit': (0x36, 0x37),
            'Waterfall of Wishing': 0x5C,
            'Dam': 0x4E,
            'Blinds Hideout': 0x61,
            'Lumberjack House': 0x6B,
            'Bonk Fairy (Light)': 0x71,
            'Bonk Fairy (Dark)': 0x71,
            'Lake Hylia Healer Fairy': 0x5E,
            'Swamp Healer Fairy': 0x5E,
            'Desert Healer Fairy': 0x5E,
            'Dark Lake Hylia Healer Fairy': 0x5E,
            'Dark Lake Hylia Ledge Healer Fairy': 0x5E,
            'Dark Desert Healer Fairy': 0x5E,
            'Dark Death Mountain Healer Fairy': 0x5E,
            'Fortune Teller (Light)': 0x65,
            'Lake Hylia Fortune Teller': 0x65,
            'Kings Grave': 0x5B,
            'Tavern': 0x43,
            'Chicken House': 0x4B,
            'Aginahs Cave': 0x4D,
            'Sahasrahlas Hut': 0x45,
            'Cave Shop (Lake Hylia)': 0x58,
            'Cave Shop (Dark Death Mountain)': 0x58,
            'Capacity Upgrade': 0x5D,
            'Blacksmiths Hut': 0x64,
            'Sick Kids House': 0x40,
            'Lost Woods Gamble': 0x3C,
            'Snitch Lady (East)': 0x3E,
            'Snitch Lady (West)': 0x3F,
            'Bush Covered House': 0x44,
            'Tavern (Front)': 0x42,
            'Light World Bomb Hut': 0x4A,
            'Kakariko Shop': 0x46,
            'Cave 45': 0x51,
            'Graveyard Cave': 0x52,
            'Checkerboard Cave': 0x72,
            'Mini Moldorm Cave': 0x6C,
            'Long Fairy Cave': 0x55,
            'Good Bee Cave': 0x56,
            '20 Rupee Cave': 0x6F,
            '50 Rupee Cave': 0x6D,
            'Ice Rod Cave': 0x84,
            'Bonk Rock Cave': 0x6E,
            'Library': 0x49,
            'Kakariko Gamble Game': 0x67,
            'Potion Shop': 0x4C,
            'Hookshot Fairy': 0x50,
            'Pyramid Fairy': 0x63,
            'East Dark World Hint': 0x69,
            'Palace of Darkness Hint': 0x68,
            'Big Bomb Shop': 0x53,
            'Village of Outcasts Shop': 0x60,
            'Dark Lake Hylia Shop': 0x60,
            'Dark World Lumberjack Shop': 0x60,
            'Dark World Potion Shop': 0x60,
            'Dark Lake Hylia Ledge Spike Cave': 0x70,
            'Dark Lake Hylia Ledge Hint': 0x6A,
            'Hype Cave': 0x3D,
            'Brewery': 0x48,
            'C-Shaped House': 0x54,
            'Chest Game': 0x47,
            'Dark World Hammer Peg Cave': 0x83,
            'Red Shield Shop': 0x57,
            'Dark Sanctuary Hint': 0x5A,
            'Fortune Teller (Dark)': 0x66,
            'Archery Game': 0x59,
            'Mire Shed': 0x5F,
            'Dark Desert Hint': 0x62,
            'Spike Cave': 0x41,
            'Mimic Cave': 0x4F,
            'Kakariko Well (top)': 0x80,
            'Hyrule Castle Secret Entrance': 0x7D,
            'Bat Cave (right)': 0x7E,
            'North Fairy Cave': 0x7C,
            'Lost Woods Hideout (top)': 0x7A,
            'Lumberjack Tree (top)': 0x7F,
            'Sewer Drop': 0x81,
            'Skull Woods Second Section (Drop)': 0x79,
            'Skull Woods First Section (Left)': 0x77,
            'Skull Woods First Section (Right)': 0x78,
            'Skull Woods First Section (Top)': 0x76,
            'Pyramid': 0x7B}

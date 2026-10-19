import json

def build_perfect_layout():
    with open('map_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    plots = data['plots']
    nodes = data['nodes']
    edges = data['edges']
    amenities = data['amenities']

    PW = 42
    PH_NORTH = 22
    PH_MID = 19
    PH_SOUTH = 19

    # 1. Update Road Nodes coordinates
    node_coords = {
        'gate_1':          (70, 336),
        'gate_1_entry':    (135, 336),
        
        # North perimeter road at y=172
        'ast_n':           (188, 172),
        'blu_n':           (306, 172),
        'car_n':           (424, 172),
        'dha_n':           (542, 172),
        'exo_n':           (660, 172),
        'flo_n':           (778, 172),
        'gar_n':           (896, 172),
        'east_park_n':     (1018, 172),

        # Main road at y=336
        'ast_main':        (188, 336),
        'blu_main':        (306, 336),
        'car_main':        (424, 336),
        'dha_main':        (542, 336),
        'exo_main':        (660, 336),
        'flo_gate2_x':     (778, 336),
        'gate_2_entry':    (896, 336),
        'gate_2':          (940, 336),
        'east_gate2':      (988, 336),
        'east_ne_turn':    (1018, 336),

        # Middle avenue midpoints at y=482
        'ast_mid':         (188, 482),
        'blu_mid':         (306, 482),
        'car_mid':         (424, 482),
        'dha_mid':         (542, 482),
        'exo_mid':         (660, 482),
        'flo_mid':         (778, 482),
        'gar_mid':         (896, 482),

        # Central Road at y=626
        'ast_s':           (188, 626),
        'blu_s':           (306, 626),
        'car_garden':      (424, 626),
        'dha_garden':      (542, 626),
        'exo_garden':      (660, 626),
        'flo_garden':      (778, 626),
        'gar_s':           (896, 626),

        # South Central Road at y=702
        'car_s_garden':    (424, 702),
        'dha_s_garden':    (542, 702),
        'exo_s_garden':    (660, 702),
        'flo_s_garden':    (778, 702),

        # South avenue midpoints at y=805
        'car_s_mid':       (424, 805),
        'dha_s_mid':       (542, 805),
        'exo_s_mid':       (660, 805),
        'flo_s_mid':       (778, 805),

        # South Perimeter Road at y=925
        'car_s_end':       (424, 925),
        'dha_s_end':       (542, 925),
        'exo_s_end':       (660, 925),
        'flo_s_end':       (778, 925),

        # West utility nodes
        'ast_sw_corner':   (188, 685),
        'ast_temple':      (60, 685),
        'ast_wtp':         (60, 520),

        # East Sector nodes
        'east_mid':        (988, 440),
        'east_s':          (988, 560),

        # Hibiscus nodes
        'hib_top_w':       (60, 715),
        'hib_top_m':       (180, 715),
        'hib_top_e':       (306, 715),
        'hib_inner_lane':  (180, 785),
        'hib_main_s1':     (306, 780),
        'hib_main_s2':     (306, 850),
        'hib_se_corner':   (306, 925),
        'hib_sw_bottom':   (60, 880),
        'hib_s_perimeter': (230, 925),
    }

    for nid, (nx, ny) in node_coords.items():
        if nid not in nodes:
            nodes[nid] = {'id': nid, 'label': nid}
        nodes[nid]['x'] = nx
        nodes[nid]['y'] = ny

    # Clean edges: remove edges that cut through house blocks
    valid_edges = []
    forbidden_pairs = {
        ('ast_mid', 'ast_wtp'), ('ast_wtp', 'ast_mid'),
        ('ast_s', 'ast_temple'), ('ast_temple', 'ast_s'),
        ('flo_garden', 'gar_s'), ('gar_s', 'flo_garden'),
        ('hib_top_m', 'hib_inner_lane'), ('hib_inner_lane', 'hib_top_m'),
        ('hib_inner_lane', 'hib_s_perimeter'), ('hib_s_perimeter', 'hib_inner_lane'),
        ('hib_main_s2', 'car_s_garden'), ('car_s_garden', 'hib_main_s2'),
        ('hib_s_perimeter', 'hib_main_s2'), ('hib_main_s2', 'hib_s_perimeter'),
        ('east_park_n', 'east_gate2'), ('east_gate2', 'east_park_n')
    }

    for e in edges:
        pair = (e['u'], e['v'])
        if pair in forbidden_pairs:
            continue
        valid_edges.append(e)

    # Add correct clean connections
    clean_connections = [
        ('ast_s', 'ast_sw_corner', 'secondary'),
        ('ast_sw_corner', 'ast_temple', 'secondary'),
        ('ast_temple', 'ast_wtp', 'secondary'),
        ('ast_temple', 'hib_top_w', 'secondary'),
        ('blu_s', 'hib_top_e', 'secondary'),
        ('hib_top_e', 'hib_main_s1', 'secondary'),
        ('hib_main_s1', 'hib_main_s2', 'secondary'),
        ('hib_main_s2', 'hib_se_corner', 'secondary'),
        ('hib_se_corner', 'hib_s_perimeter', 'secondary'),
        ('hib_s_perimeter', 'car_s_end', 'secondary'),
        ('hib_top_w', 'hib_top_m', 'secondary'),
        ('hib_top_m', 'hib_top_e', 'secondary'),
        ('hib_top_w', 'hib_sw_bottom', 'secondary'),
        ('hib_sw_bottom', 'hib_s_perimeter', 'secondary'),
        ('east_gate2', 'east_ne_turn', 'secondary'),
        ('east_ne_turn', 'east_park_n', 'secondary'),
    ]
    for u, v, t in clean_connections:
        if not any((e['u'] == u and e['v'] == v) or (e['u'] == v and e['v'] == u) for e in valid_edges):
            valid_edges.append({'u': u, 'v': v, 'type': t})

    data['edges'] = valid_edges

    # Helper function to place a vertical column of plots
    def place_col(plot_list, x, start_y, pitch, height, facing, road_node, block_name, width=PW):
        for i, pid in enumerate(plot_list):
            if pid not in plots:
                print(f"Warning: plot {pid} not found!")
                continue
            p = plots[pid]
            p['x'] = x
            p['y'] = start_y + i * pitch
            p['w'] = width
            p['h'] = height
            p['facing'] = facing
            p['roadNode'] = road_node
            p['block'] = block_name

    # 2. Aster West
    place_col(['1C', '1B', '1A'], 130, 248, 24, PH_NORTH, 'East', 'ast_n', 'Aster North')
    aster_mid = ['1', '2', '3', '5', '6', '7', '8', '9', '10', '11', '12', '12B', '14', '15', '16']
    place_col(aster_mid, 130, 356, 20, 18, 'East', 'ast_mid', 'Aster South')

    # West temple plots
    if '97' in plots:
        plots['97'].update({'x': 90, 'y': 620, 'w': 24, 'h': 18, 'facing': 'East', 'roadNode': 'ast_temple', 'block': 'West Sector'})
    if '96' in plots:
        plots['96'].update({'x': 90, 'y': 642, 'w': 24, 'h': 18, 'facing': 'East', 'roadNode': 'ast_temple', 'block': 'West Sector'})

    # 3. Block 1 (between Aster and Bluebell)
    place_col(['33', '32', '31', '30', '29'], 204, 200, 24, PH_NORTH, 'West', 'ast_n', 'Aster North')
    place_col(['35/36', '37', '38', '39', '40'], 248, 200, 24, PH_NORTH, 'East', 'blu_n', 'Bluebell North')

    b1_s_left = ['28', '27', '26', '25', '24', '23', '22', '21', '20', '19', '18', '17']
    b1_s_right = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52']
    place_col(b1_s_left, 204, 356, 21, PH_MID, 'West', 'ast_mid', 'Aster South')
    place_col(b1_s_right, 248, 356, 21, PH_MID, 'East', 'blu_mid', 'Bluebell Mid')

    # 4. Block 2 (between Bluebell and Carnation)
    place_col(['78', '77', '76', '75', '74'], 322, 200, 24, PH_NORTH, 'West', 'blu_n', 'Bluebell North')
    place_col(['79', '80', '81', '82', '83'], 366, 200, 24, PH_NORTH, 'East', 'car_n', 'Carnation North')

    b2_s_left = ['73', '72', '71', '70', '69', '68', '67', '66', '65', '64', '63', '62']
    b2_s_right = ['84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95']
    place_col(b2_s_left, 322, 356, 21, PH_MID, 'West', 'blu_mid', 'Bluebell Mid')
    place_col(b2_s_right, 366, 356, 21, PH_MID, 'East', 'car_mid', 'Carnation Mid')

    # 5. Block 3 (between Carnation and Dhalia)
    place_col(['112', '111', '110', '109', '108'], 440, 200, 24, PH_NORTH, 'West', 'car_n', 'Carnation North')
    place_col(['113', '114', '115', '116', '117'], 484, 200, 24, PH_NORTH, 'East', 'dha_n', 'Dhalia North')

    b3_s_left = ['107', '106', '105', '104', '103', '102', '101', '100', '99', '98', '240', '239']
    b3_s_right = ['118', '119', '120', '121', '122', '123', '124', '234', '235', '236', '237', '238']
    place_col(b3_s_left, 440, 356, 21, PH_MID, 'West', 'car_mid', 'Carnation Mid')
    place_col(b3_s_right, 484, 356, 21, PH_MID, 'East', 'dha_mid', 'Dhalia Mid')

    # 6. Block 4 (between Dhalia and Exotica)
    place_col(['135', '134', '133', '132'], 558, 224, 24, PH_NORTH, 'West', 'dha_n', 'Dhalia North')
    place_col(['136', '137', '138', '139'], 602, 224, 24, PH_NORTH, 'East', 'exo_n', 'Exotica North')

    b4_s_left = ['131', '130', '129', '128', '127', '126', '233', '232', '231', '230', '229', '228']
    b4_s_right = ['140', '141', '142', '143', '144', '145', '222', '223', '224', '225', '226', '227']
    place_col(b4_s_left, 558, 356, 21, PH_MID, 'West', 'dha_mid', 'Dhalia Mid')
    place_col(b4_s_right, 602, 356, 21, PH_MID, 'East', 'exo_mid', 'Exotica Mid')

    # 7. Block 5 (between Exotica and Florentine)
    place_col(['156', '155', '154', '153'], 676, 224, 24, PH_NORTH, 'West', 'exo_n', 'Exotica North')
    place_col(['157', '158', '159', '160'], 720, 224, 24, PH_NORTH, 'East', 'flo_n', 'Florentine North')

    b5_s_left = ['152', '151', '150', '149', '148', '147', '221', '220', '219', '218', '217', '216']
    b5_s_right = ['161', '162', '163', '164', '165', '166', '210', '211', '212', '213', '214', '215']
    place_col(b5_s_left, 676, 356, 21, PH_MID, 'West', 'exo_mid', 'Exotica Mid')
    place_col(b5_s_right, 720, 356, 21, PH_MID, 'East', 'flo_mid', 'Florentine Mid')

    # 8. Block 6 (between Florentine and Gardenia)
    place_col(['175', '174', '173', '172'], 794, 224, 24, PH_NORTH, 'West', 'flo_n', 'Florentine North')
    place_col(['176', '177', '178', '179'], 838, 224, 24, PH_NORTH, 'East', 'gar_n', 'Gardenia North')

    b6_s_left = ['171', '170', '169', '168', '167', '209', '208', '207', '206', '205', '204', '203', '340', '341']
    b6_s_right = ['180', '181', '182', '183', '184', '196', '197', '198', '199', '200', '201', '202', '344', '342', '343']
    place_col(b6_s_left, 794, 356, 21, PH_MID, 'West', 'flo_mid', 'Florentine Mid')
    place_col(b6_s_right, 838, 356, 21, PH_MID, 'East', 'gar_mid', 'Gardenia Mid')

    # 9. Gate 2 Precinct & East Area
    place_col(['192', '191', '190'], 918, 248, 24, PH_NORTH, 'West', 'gar_n', 'Gardenia North', width=38)
    place_col(['332', '331', '330'], 960, 248, 24, PH_NORTH, 'East', 'east_park_n', 'East Park North', width=38)
    # North East Corner
    place_col(['333', '334', '335'], 1040, 200, 24, PH_NORTH, 'West', 'east_park_n', 'North East Sector', width=36)
    place_col(['338', '337', '336'], 1080, 200, 24, PH_NORTH, 'East', 'east_park_n', 'North East Sector', width=36)
    
    # South of Gate 2:
    place_col(['322', '323', '329'], 918, 356, 24, PH_MID, 'West', 'gate_2_entry', 'East Sector', width=38)

    # Far East Plots
    for idx, pid in enumerate(['351', '350', '349', '348B']):
        plots[pid].update({'x': 1010 + idx * 34, 'y': 356, 'w': 32, 'h': 21, 'facing': 'West', 'roadNode': 'east_mid', 'block': 'East Sector'})
    for idx, pid in enumerate(['352', '353', '360']):
        plots[pid].update({'x': 1010 + idx * 46, 'y': 382, 'w': 44, 'h': 21, 'facing': 'West', 'roadNode': 'east_mid', 'block': 'East Sector'})
    for idx, pid in enumerate(['355', '354', '358']):
        plots[pid].update({'x': 1010 + idx * 46, 'y': 416, 'w': 44, 'h': 21, 'facing': 'West', 'roadNode': 'east_mid', 'block': 'East Sector'})
    for idx, pid in enumerate(['356', '359']):
        plots[pid].update({'x': 1010 + idx * 46, 'y': 442, 'w': 44, 'h': 21, 'facing': 'West', 'roadNode': 'east_s', 'block': 'East Sector'})
    plots['357'].update({'x': 1056, 'y': 468, 'w': 44, 'h': 21, 'facing': 'West', 'roadNode': 'east_s', 'block': 'East Sector'})

    # 10. South Sector
    place_col(['286', '287', '288', '289', '290', '291'], 440, 720, 21, PH_SOUTH, 'West', 'car_s_mid', 'Carnation South')
    place_col(['285', '284', '283', '282', '281', '280', '279'], 484, 720, 21, PH_SOUTH, 'East', 'dha_s_mid', 'Carnation South')

    place_col(['272', '273', '274', '275', '276', '277', '278'], 558, 720, 21, PH_SOUTH, 'West', 'dha_s_mid', 'Dhalia South')
    place_col(['271', '270', '269', '268', '267', '266', '265', '265/B'], 602, 720, 21, PH_SOUTH, 'East', 'exo_s_mid', 'Dhalia South')

    place_col(['257', '258', '259', '260', '261', '262', '263', '264'], 676, 720, 21, PH_SOUTH, 'West', 'exo_s_mid', 'Exotica South')
    place_col(['256', '255', '254', '253', '252', '251', '250', '249', '248'], 720, 720, 21, PH_SOUTH, 'East', 'flo_s_mid', 'Exotica South')

    # Florentine South-East Block
    for idx, pid in enumerate(['345', '346', '347', '348']):
        plots[pid].update({'x': 796 + idx * 25, 'y': 720, 'w': 23, 'h': 20, 'facing': 'North', 'roadNode': 'flo_s_garden'})
    for idx, pid in enumerate(['247', '246', '245']):
        plots[pid].update({'x': 796 + idx * 33, 'y': 744, 'w': 31, 'h': 20, 'facing': 'North', 'roadNode': 'flo_s_mid'})
    for idx, pid in enumerate(['243', '244']):
        plots[pid].update({'x': 796 + idx * 50, 'y': 768, 'w': 48, 'h': 20, 'facing': 'North', 'roadNode': 'flo_s_mid'})
    plots['242'].update({'x': 796, 'y': 792, 'w': 50, 'h': 20, 'facing': 'North', 'roadNode': 'flo_s_mid'})
    plots['241'].update({'x': 796, 'y': 816, 'w': 50, 'h': 20, 'facing': 'North', 'roadNode': 'flo_s_end'})

    # 11. Far West South (Hibiscus Area)
    # Angled top row: 53..60
    for idx, pid in enumerate(['53', '54', '55', '56', '57', '58', '59', '60']):
        plots[pid].update({'x': 85 + idx * 24, 'y': 730, 'w': 22, 'h': 20, 'facing': 'North', 'roadNode': 'hib_top_m', 'block': 'Hibiscus North'})
    # Mid row: 318..321
    for idx, pid in enumerate(['318', '319', '320', '321']):
        plots[pid].update({'x': 85 + idx * 24, 'y': 760, 'w': 22, 'h': 20, 'facing': 'North', 'roadNode': 'hib_inner_lane', 'block': 'Hibiscus Mid'})
    
    # Hibiscus inner lane: 306, 303 / 307, 304 / 305
    plots['306'].update({'x': 214, 'y': 758, 'w': 24, 'h': 19, 'facing': 'East', 'roadNode': 'hib_inner_lane', 'block': 'Hibiscus Lane'})
    plots['303'].update({'x': 242, 'y': 758, 'w': 24, 'h': 19, 'facing': 'West', 'roadNode': 'hib_inner_lane', 'block': 'Hibiscus Lane'})
    plots['307'].update({'x': 214, 'y': 780, 'w': 24, 'h': 19, 'facing': 'East', 'roadNode': 'hib_inner_lane', 'block': 'Hibiscus Lane'})
    plots['304'].update({'x': 242, 'y': 780, 'w': 24, 'h': 19, 'facing': 'West', 'roadNode': 'hib_inner_lane', 'block': 'Hibiscus Lane'})
    plots['305'].update({'x': 228, 'y': 802, 'w': 38, 'h': 19, 'facing': 'East', 'roadNode': 'hib_inner_lane', 'block': 'Hibiscus Lane'})

    # Bottom row: 317..310
    for idx, pid in enumerate(['317', '316', '315', '314', '313', '312', '311', '310']):
        plots[pid].update({'x': 85 + idx * 25, 'y': 840, 'w': 23, 'h': 20, 'facing': 'South', 'roadNode': 'hib_s_perimeter', 'block': 'Hibiscus South'})

    # Hibiscus vertical column: 298..302 (left) and 297..292, 309 (right)
    place_col(['298', '299', '300', '301', '302'], 322, 730, 22, 20, 'West', 'hib_main_s1', 'Hibiscus East')
    place_col(['297', '296', '295', '294', '293', '292', '309'], 366, 730, 22, 20, 'East', 'car_s_mid', 'Hibiscus East')

    # 12. Update amenities positions
    for am in amenities:
        aid = am['id']
        if aid == 'gate_1':
            am.update({'x': 70, 'y': 336})
        elif aid == 'gate_2':
            am.update({'x': 940, 'y': 336})
        elif aid == 'school_bus':
            am.update({'x': 188, 'y': 356})
        elif aid == 'wtp_sump':
            am.update({'x': 45, 'y': 520})
        elif aid == 'temple_west':
            am.update({'x': 45, 'y': 685})
        elif aid == 'children_play':
            am.update({'x': 260, 'y': 660})
        elif aid == 'auditorium':
            am.update({'x': 366, 'y': 660})
        elif aid == 'temple_central':
            am.update({'x': 542, 'y': 660})
        elif aid == 'shopping':
            am.update({'x': 50, 'y': 220})
        elif aid == 'stp_plant':
            am.update({'x': 940, 'y': 175})
        elif aid == 'atm':
            am.update({'x': 940, 'y': 660})
        elif aid == 'dry_waste':
            am.update({'x': 45, 'y': 710})

    # Collision Check between plots
    plot_items = list(plots.items())
    collisions = []
    for i in range(len(plot_items)):
        id1, p1 = plot_items[i]
        r1 = (p1['x'], p1['y'], p1['x'] + p1['w'], p1['y'] + p1['h'])
        for j in range(i + 1, len(plot_items)):
            id2, p2 = plot_items[j]
            r2 = (p2['x'], p2['y'], p2['x'] + p2['w'], p2['y'] + p2['h'])
            if not (r1[2] <= r2[0] + 0.1 or r1[0] >= r2[2] - 0.1 or r1[3] <= r2[1] + 0.1 or r1[1] >= r2[3] - 0.1):
                collisions.append((id1, id2))

    print(f"Total plots placed: {len(plots)} / 344")
    print(f"Plot collisions: {len(collisions)}")

    # Check road-plot collisions
    road_collisions = []
    for e in valid_edges:
        u = nodes[e['u']]
        v = nodes[e['v']]
        x1, y1, x2, y2 = u['x'], u['y'], v['x'], v['y']
        for pid, p in plots.items():
            px, py, pw, ph = p['x'], p['y'], p['w'], p['h']
            length = max(1, int(((x2-x1)**2 + (y2-y1)**2)**0.5))
            for step in range(0, length + 1, 4):
                sx = x1 + (x2 - x1) * step / length
                sy = y1 + (y2 - y1) * step / length
                if (px - 10 <= sx <= px + pw + 10) and (py - 10 <= sy <= py + ph + 10):
                    road_collisions.append((e['u'], e['v'], pid))
                    break

    print(f"Road-plot overlaps: {len(road_collisions)}")
    if road_collisions:
        for c in road_collisions[:15]:
            print("Road collision:", c)

    # Save to map_data.json
    with open('map_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Save to map_data.js
    with open('map_data.js', 'w', encoding='utf-8') as f:
        f.write("window.HIMAGIRI_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")

    print("SUCCESS: map_data.json and map_data.js successfully written!")

build_perfect_layout()

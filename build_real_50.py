import json
import math
import os

# 1. Himagiri Meadows (Master Layout from actual map_data.json)
with open('himagiri-meadows/map_data.json', 'r', encoding='utf-8') as f:
    himagiri_raw = json.load(f)

himagiri_layout = {
    'id': 'himagiri',
    'name': 'Himagiri Meadows',
    'location': 'Bannerghatta Road, Bangalore South',
    'zone': 'south',
    'type': 'Residential Gated Community',
    'unitType': 'Plot',
    'unitCount': len(himagiri_raw['plots']),
    'bounds': {'minX': 20, 'maxX': 1270, 'minY': 135, 'maxY': 935},
    'center': {'x': 645, 'y': 535},
    'groundPolygon': "40,320 80,180 300,160 850,140 1050,140 1260,170 1250,600 1150,620 950,830 800,900 500,890 280,880 30,830 30,620",
    'borderTreesPath': "M 40,320 Q 150,160 300,160 T 850,140 T 1050,140 T 1260,170 L 1250,600 L 1150,620 L 950,830 L 800,900 L 500,890 L 280,880 L 30,830 Z",
    'gardenPark': {'x': 440, 'y': 625, 'w': 370, 'h': 45, 'rx': 6, 'label': "Central Community Garden"},
    'roads': {
        'nodes': himagiri_raw['nodes'],
        'edges': himagiri_raw['edges']
    },
    'plots': himagiri_raw['plots'],
    'amenities': himagiri_raw['amenities'],
    'roadLabels': [
        { 'name': "ASTER ROAD", 'x': 188, 'y': 482, 'vertical': True },
        { 'name': "BLUEBELL ROAD", 'x': 306, 'y': 482, 'vertical': True },
        { 'name': "CARNATION ROAD", 'x': 424, 'y': 482, 'vertical': True },
        { 'name': "DHALIA ROAD", 'x': 542, 'y': 482, 'vertical': True },
        { 'name': "EXOTICA ROAD", 'x': 660, 'y': 482, 'vertical': True },
        { 'name': "FLORENTINE ROAD", 'x': 778, 'y': 482, 'vertical': True },
        { 'name': "GARDENIA ROAD", 'x': 896, 'y': 482, 'vertical': True },
        { 'name': "HIBISCUS ROAD", 'x': 337, 'y': 810, 'vertical': True },
        { 'name': "MAIN AVENUE (GATE 1)", 'x': 306, 'y': 336, 'vertical': False },
        { 'name': "CENTRAL GARDEN ROAD", 'x': 600, 'y': 626, 'vertical': False },
        { 'name': "GATE 2 ENTRY ROAD", 'x': 940, 'y': 336, 'vertical': False }
    ],
    'defaultStartGate': 'gate_1',
    'sectors': ['Aster', 'Bluebell', 'Carnation', 'Dhalia', 'Exotica', 'Florentine', 'Gardenia', 'Hibiscus']
}

# 2. PRESTIGE FALCON CITY (Kanakapura Road, Konanakunte Cross)
# 7 Towers (Tower 1 to 7), 2,520 flats, Forum Mall connection, Olympic clubhouse
pfc_nodes = {
    'pfc_gate_main':    {'id': 'pfc_gate_main', 'x': 90, 'y': 480, 'label': 'Gate 1 (Kanakapura Main Road)'},
    'pfc_junc_entry':   {'id': 'pfc_junc_entry', 'x': 180, 'y': 480, 'label': 'Falcon Grand Entrance Boulevard'},
    'pfc_junc_w':       {'id': 'pfc_junc_w', 'x': 340, 'y': 480, 'label': 'Tower 1 & 5 Boulevard Cross'},
    'pfc_junc_ctr':     {'id': 'pfc_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Forum Plaza Roundabout'},
    'pfc_junc_e':       {'id': 'pfc_junc_e', 'x': 900, 'y': 480, 'label': 'Clubhouse Promenade Junction'},
    'pfc_gate_metro':   {'id': 'pfc_gate_metro', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Metro & Forum Mall Link)'},

    'pfc_n_w':          {'id': 'pfc_n_w', 'x': 340, 'y': 250, 'label': 'Tower 1 & 2 North Drive'},
    'pfc_n_ctr':        {'id': 'pfc_n_ctr', 'x': 620, 'y': 250, 'label': 'Tower 3 Central Boulevard'},
    'pfc_n_e':          {'id': 'pfc_n_e', 'x': 900, 'y': 250, 'label': 'Tower 4 North Link'},

    'pfc_s_w':          {'id': 'pfc_s_w', 'x': 340, 'y': 710, 'label': 'Tower 5 South Crescent'},
    'pfc_s_ctr':        {'id': 'pfc_s_ctr', 'x': 620, 'y': 710, 'label': 'Tower 6 Lawn Drive'},
    'pfc_s_e':          {'id': 'pfc_s_e', 'x': 900, 'y': 710, 'label': 'Tower 7 Sports Complex Link'},

    'pfc_mid_w_n':      {'id': 'pfc_mid_w_n', 'x': 340, 'y': 365, 'label': 'Falcon Way North'},
    'pfc_mid_w_s':      {'id': 'pfc_mid_w_s', 'x': 340, 'y': 595, 'label': 'Falcon Way South'},
    'pfc_mid_ctr_n':    {'id': 'pfc_mid_ctr_n', 'x': 620, 'y': 365, 'label': 'Grand Lawn North Link'},
    'pfc_mid_ctr_s':    {'id': 'pfc_mid_ctr_s', 'x': 620, 'y': 595, 'label': 'Grand Lawn South Link'},
    'pfc_mid_e_n':      {'id': 'pfc_mid_e_n', 'x': 900, 'y': 365, 'label': 'Forum Promenade North'},
    'pfc_mid_e_s':      {'id': 'pfc_mid_e_s', 'x': 900, 'y': 595, 'label': 'Forum Promenade South'}
}

pfc_edges_raw = [
    ('pfc_gate_main', 'pfc_junc_entry', 'Falcon Boulevard', 'primary'),
    ('pfc_junc_entry', 'pfc_junc_w', 'Falcon Boulevard', 'primary'),
    ('pfc_junc_w', 'pfc_junc_ctr', 'Falcon Boulevard', 'primary'),
    ('pfc_junc_ctr', 'pfc_junc_e', 'Falcon Boulevard', 'primary'),
    ('pfc_junc_e', 'pfc_gate_metro', 'Forum Mall Access Way', 'primary'),

    ('pfc_n_w', 'pfc_n_ctr', 'North Tower Boulevard', 'secondary'),
    ('pfc_n_ctr', 'pfc_n_e', 'North Tower Boulevard', 'secondary'),
    ('pfc_s_w', 'pfc_s_ctr', 'South Sports Drive', 'secondary'),
    ('pfc_s_ctr', 'pfc_s_e', 'South Sports Drive', 'secondary'),

    ('pfc_n_w', 'pfc_mid_w_n', 'Tower 1 Connector', 'secondary'),
    ('pfc_mid_w_n', 'pfc_junc_w', 'Tower 1 Connector', 'secondary'),
    ('pfc_junc_w', 'pfc_mid_w_s', 'Tower 5 Connector', 'secondary'),
    ('pfc_mid_w_s', 'pfc_s_w', 'Tower 5 Connector', 'secondary'),

    ('pfc_n_ctr', 'pfc_mid_ctr_n', 'Central Forum Link', 'primary'),
    ('pfc_mid_ctr_n', 'pfc_junc_ctr', 'Central Forum Link', 'primary'),
    ('pfc_junc_ctr', 'pfc_mid_ctr_s', 'Central Forum Link', 'primary'),
    ('pfc_mid_ctr_s', 'pfc_s_ctr', 'Central Forum Link', 'primary'),

    ('pfc_n_e', 'pfc_mid_e_n', 'Promenade Avenue', 'secondary'),
    ('pfc_mid_e_n', 'pfc_junc_e', 'Promenade Avenue', 'secondary'),
    ('pfc_junc_e', 'pfc_mid_e_s', 'Promenade Avenue', 'secondary'),
    ('pfc_mid_e_s', 'pfc_s_e', 'Promenade Avenue', 'secondary')
]
pfc_edges = [{'u': u, 'v': v, 'road': r, 'type': t} for u, v, r, t in pfc_edges_raw]

pfc_plots = {}
tower_configs_pfc = [
    # tower_name, x, y, road_node, road_name
    (1, 260, 200, 'pfc_n_w', 'North Tower Boulevard'),
    (2, 450, 200, 'pfc_n_ctr', 'North Tower Boulevard'),
    (3, 620, 180, 'pfc_n_ctr', 'North Tower Boulevard'),
    (4, 820, 200, 'pfc_n_e', 'North Tower Boulevard'),
    (5, 260, 680, 'pfc_s_w', 'South Sports Drive'),
    (6, 620, 700, 'pfc_s_ctr', 'South Sports Drive'),
    (7, 880, 680, 'pfc_s_e', 'South Sports Drive')
]

pfc_uid = 1
for t_num, tx, ty, tnode, troad in tower_configs_pfc:
    # 7 units per tower (representing floors 101 to 1804)
    floors = [101, 202, 401, 802, 1201, 1502, 1804]
    for idx, fl in enumerate(floors):
        pid = str(pfc_uid)
        num_str = f"Tower {t_num} - {fl}"
        pfc_plots[pid] = {
            'id': pid,
            'number': num_str,
            'road': troad,
            'block': f"Tower {t_num} (Block {'ABCDEFG'[t_num-1]})",
            'facing': 'East' if t_num <= 4 else 'North',
            'x': tx + (idx % 3) * 24 - 24,
            'y': ty + (idx // 3) * 20 - 10,
            'w': 50,
            'h': 36,
            'roadNode': tnode,
            'color': 'cyan'
        }
        pfc_uid += 1

pfc_amenities = [
    {'id': 'pfc_mall', 'name': 'Forum Falcon City Mall Access Walkway', 'description': 'Direct air-conditioned pedestrian link to Forum Mall & Metro Station', 'x': 1050, 'y': 380, 'roadNode': 'pfc_gate_metro', 'icon': '🛍️', 'type': 'mall'},
    {'id': 'pfc_club', 'name': 'Grand Falcon Central Clubhouse & Swimming Pool', 'description': 'Olympic swimming pool, badminton courts, squash, gym and banquet halls', 'x': 620, 'y': 440, 'roadNode': 'pfc_junc_ctr', 'icon': '🏊', 'type': 'clubhouse'},
    {'id': 'pfc_sports', 'name': 'Lawn Tennis Arena & Cricket Practice Pitch', 'description': 'Floodlit acrylic tennis courts and professional cricket nets', 'x': 760, 'y': 480, 'roadNode': 'pfc_junc_e', 'icon': '🎾', 'type': 'sports'},
    {'id': 'pfc_lawn', 'name': 'Central Amphitheatre & Landscaped Lawns', 'description': 'Lush gardens, reflexology pathway and community performance amphitheatre', 'x': 480, 'y': 480, 'roadNode': 'pfc_junc_w', 'icon': '🌿', 'type': 'park'},
    {'id': 'pfc_gate_1', 'name': 'Main Security Gate 1 (Kanakapura Road)', 'description': '24/7 security boom barriers and visitor RFID checkpost on Kanakapura Main Rd', 'x': 90, 'y': 480, 'roadNode': 'pfc_gate_main', 'icon': '🚪', 'type': 'gate'},
    {'id': 'pfc_gate_2', 'name': 'Metro & Mall Security Gate 2', 'description': 'Dedicated turnstile access to Konanakunte Cross Metro station', 'x': 1110, 'y': 480, 'roadNode': 'pfc_gate_metro', 'icon': '🚪', 'type': 'gate'}
]

prestige_falcon_city = {
    'id': 'prestige_falcon_city',
    'name': 'Prestige Falcon City',
    'location': 'Kanakapura Road, Konanakunte Cross Metro, Bangalore South',
    'zone': 'south',
    'type': 'Iconic High-Rise Residential Township',
    'unitType': 'Apartment / Tower',
    'unitCount': len(pfc_plots),
    'bounds': {'minX': 60, 'maxX': 1180, 'minY': 140, 'maxY': 860},
    'center': {'x': 620, 'y': 480},
    'groundPolygon': "90,480 200,160 620,140 1040,160 1110,480 1040,800 620,840 200,800 Z",
    'borderTreesPath': "M 90,480 L 200,160 L 620,140 L 1040,160 L 1110,480 L 1040,800 L 620,840 L 200,800 Z",
    'gardenPark': {'x': 440, 'y': 455, 'w': 360, 'h': 50, 'rx': 8, 'label': "Grand Central Lawn & Water Mirror"},
    'roads': {'nodes': pfc_nodes, 'edges': pfc_edges},
    'plots': pfc_plots,
    'amenities': pfc_amenities,
    'roadLabels': [
        {'name': "FALCON BOULEVARD", 'x': 620, 'y': 490, 'vertical': False},
        {'name': "NORTH TOWER BOULEVARD", 'x': 620, 'y': 235, 'vertical': False},
        {'name': "SOUTH SPORTS DRIVE", 'x': 620, 'y': 725, 'vertical': False},
        {'name': "TOWER 1 & 5 CONNECTOR", 'x': 325, 'y': 365, 'vertical': True},
        {'name': "FORUM PROMENADE", 'x': 915, 'y': 365, 'vertical': True}
    ],
    'defaultStartGate': 'pfc_gate_main',
    'sectors': ['Tower 1 (Block A)', 'Tower 2 (Block B)', 'Tower 3 (Block C)', 'Tower 4 (Block D)', 'Tower 5 (Block E)', 'Tower 6 (Block F)', 'Tower 7 (Block G)']
}


# 3. PRESTIGE ELYSIAN (Bannerghatta Main Road, opposite Meenakshi Mall)
# 4 Premium High-rise Towers: Aurum, Argent, Cuprum, Platin
pe_nodes = {
    'pe_gate_main':     {'id': 'pe_gate_main', 'x': 90, 'y': 480, 'label': 'Gate 1 (Bannerghatta Main Road)'},
    'pe_junc_entry':    {'id': 'pe_junc_entry', 'x': 180, 'y': 480, 'label': 'Elysian Grand Entrance Boulevard'},
    'pe_junc_w':        {'id': 'pe_junc_w', 'x': 360, 'y': 480, 'label': 'Aurum & Cuprum Towers Junction'},
    'pe_junc_ctr':      {'id': 'pe_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Elysian Water Plaza'},
    'pe_junc_e':        {'id': 'pe_junc_e', 'x': 880, 'y': 480, 'label': 'Argent & Platin Towers Junction'},
    'pe_gate_north':    {'id': 'pe_gate_north', 'x': 1100, 'y': 480, 'label': 'Gate 2 (Classic Orchards Link)'},

    'pe_n_w':           {'id': 'pe_n_w', 'x': 360, 'y': 260, 'label': 'Tower 1 Aurum Boulevard'},
    'pe_n_ctr':         {'id': 'pe_n_ctr', 'x': 620, 'y': 260, 'label': 'Infinity Pool Boardwalk'},
    'pe_n_e':           {'id': 'pe_n_e', 'x': 880, 'y': 260, 'label': 'Tower 2 Argent Boulevard'},

    'pe_s_w':           {'id': 'pe_s_w', 'x': 360, 'y': 700, 'label': 'Tower 3 Cuprum Way'},
    'pe_s_ctr':         {'id': 'pe_s_ctr', 'x': 620, 'y': 700, 'label': 'Zen Garden Courtyard Drive'},
    'pe_s_e':           {'id': 'pe_s_e', 'x': 880, 'y': 700, 'label': 'Tower 4 Platin Way'},

    'pe_mid_w_n':       {'id': 'pe_mid_w_n', 'x': 360, 'y': 370, 'label': 'Aurum Court North'},
    'pe_mid_w_s':       {'id': 'pe_mid_w_s', 'x': 360, 'y': 590, 'label': 'Cuprum Court South'},
    'pe_mid_ctr_n':     {'id': 'pe_mid_ctr_n', 'x': 620, 'y': 370, 'label': 'Clubhouse Promenade North'},
    'pe_mid_ctr_s':     {'id': 'pe_mid_ctr_s', 'x': 620, 'y': 590, 'label': 'Zen Garden Link South'},
    'pe_mid_e_n':       {'id': 'pe_mid_e_n', 'x': 880, 'y': 370, 'label': 'Argent Court North'},
    'pe_mid_e_s':       {'id': 'pe_mid_e_s', 'x': 880, 'y': 590, 'label': 'Platin Court South'}
}

pe_edges_raw = [
    ('pe_gate_main', 'pe_junc_entry', 'Elysian Boulevard', 'primary'),
    ('pe_junc_entry', 'pe_junc_w', 'Elysian Boulevard', 'primary'),
    ('pe_junc_w', 'pe_junc_ctr', 'Elysian Boulevard', 'primary'),
    ('pe_junc_ctr', 'pe_junc_e', 'Elysian Boulevard', 'primary'),
    ('pe_junc_e', 'pe_gate_north', 'Classic Orchards Parkway', 'primary'),

    ('pe_n_w', 'pe_n_ctr', 'North Terrace Way', 'secondary'),
    ('pe_n_ctr', 'pe_n_e', 'North Terrace Way', 'secondary'),
    ('pe_s_w', 'pe_s_ctr', 'South Garden Way', 'secondary'),
    ('pe_s_ctr', 'pe_s_e', 'South Garden Way', 'secondary'),

    ('pe_n_w', 'pe_mid_w_n', 'Aurum Avenue', 'secondary'),
    ('pe_mid_w_n', 'pe_junc_w', 'Aurum Avenue', 'secondary'),
    ('pe_junc_w', 'pe_mid_w_s', 'Cuprum Avenue', 'secondary'),
    ('pe_mid_w_s', 'pe_s_w', 'Cuprum Avenue', 'secondary'),

    ('pe_n_ctr', 'pe_mid_ctr_n', 'Central Promenade', 'primary'),
    ('pe_mid_ctr_n', 'pe_junc_ctr', 'Central Promenade', 'primary'),
    ('pe_junc_ctr', 'pe_mid_ctr_s', 'Central Promenade', 'primary'),
    ('pe_mid_ctr_s', 'pe_s_ctr', 'Central Promenade', 'primary'),

    ('pe_n_e', 'pe_mid_e_n', 'Argent Avenue', 'secondary'),
    ('pe_mid_e_n', 'pe_junc_e', 'Argent Avenue', 'secondary'),
    ('pe_junc_e', 'pe_mid_e_s', 'Platin Avenue', 'secondary'),
    ('pe_mid_e_s', 'pe_s_e', 'Platin Avenue', 'secondary')
]
pe_edges = [{'u': u, 'v': v, 'road': r, 'type': t} for u, v, r, t in pe_edges_raw]

pe_plots = {}
tower_configs_pe = [
    (1, "Aurum", 300, 200, 'pe_n_w', 'North Terrace Way'),
    (2, "Argent", 820, 200, 'pe_n_e', 'North Terrace Way'),
    (3, "Cuprum", 300, 680, 'pe_s_w', 'South Garden Way'),
    (4, "Platin", 820, 680, 'pe_s_e', 'South Garden Way')
]

pe_uid = 1
for t_num, t_name, tx, ty, tnode, troad in tower_configs_pe:
    floors = [101, 202, 303, 401, 502, 603, 701, 802, 903, 1001, 1202, 1404]
    for idx, fl in enumerate(floors):
        pid = str(pe_uid)
        num_str = f"Tower {t_num} - {fl}"
        pe_plots[pid] = {
            'id': pid,
            'number': num_str,
            'road': troad,
            'block': f"Tower {t_num} ({t_name})",
            'facing': 'East' if t_num in [1, 3] else 'West',
            'x': tx + (idx % 3) * 26 - 26,
            'y': ty + (idx // 3) * 20 - 12,
            'w': 52,
            'h': 36,
            'roadNode': tnode,
            'color': 'cyan'
        }
        pe_uid += 1

pe_amenities = [
    {'id': 'pe_club', 'name': 'Elysian Grand Clubhouse & Infinity Pool', 'description': 'Heated infinity edge pool, gymnasium, aerobics, and banquet hall', 'x': 620, 'y': 440, 'roadNode': 'pe_junc_ctr', 'icon': '🏊', 'type': 'clubhouse'},
    {'id': 'pe_sports', 'name': 'Indoor Badminton & Squash Arena', 'description': 'Two glass-backed squash courts and hardwood badminton courts', 'x': 740, 'y': 480, 'roadNode': 'pe_junc_e', 'icon': '🏸', 'type': 'sports'},
    {'id': 'pe_zen', 'name': 'Zen Garden & Reflection Water Mirror', 'description': 'Tranquil meditation deck with Japanese water feature and stone seating', 'x': 500, 'y': 480, 'roadNode': 'pe_junc_w', 'icon': '🌿', 'type': 'park'},
    {'id': 'pe_play', 'name': "Children's Adventure Play Zone & Sandpit", 'description': 'Multi-play timber fort, swings, climbing wall and soft-fall ground', 'x': 620, 'y': 550, 'roadNode': 'pe_mid_ctr_s', 'icon': '🛝', 'type': 'recreation'},
    {'id': 'pe_gate_1', 'name': 'Main Security Gate 1 (Bannerghatta Road)', 'description': '24/7 security boom barriers on Bannerghatta Main Rd (opposite Meenakshi Mall)', 'x': 90, 'y': 480, 'roadNode': 'pe_gate_main', 'icon': '🚪', 'type': 'gate'},
    {'id': 'pe_gate_2', 'name': 'North Gate 2 (Classic Orchards Link)', 'description': 'Resident sensor boom barrier linking to Classic Orchards sector', 'x': 1100, 'y': 480, 'roadNode': 'pe_gate_north', 'icon': '🚪', 'type': 'gate'}
]

prestige_elysian = {
    'id': 'prestige_elysian',
    'name': 'Prestige Elysian',
    'location': 'Bannerghatta Main Road, Classic Orchards Vicinity, Bangalore South',
    'zone': 'south',
    'type': 'Luxury High-Rise Residential Community',
    'unitType': 'Apartment / Tower',
    'unitCount': len(pe_plots),
    'bounds': {'minX': 60, 'maxX': 1180, 'minY': 150, 'maxY': 850},
    'center': {'x': 620, 'y': 480},
    'groundPolygon': "90,480 220,170 620,150 1020,170 1100,480 1020,790 620,830 220,790 Z",
    'borderTreesPath': "M 90,480 L 220,170 L 620,150 L 1020,170 L 1100,480 L 1020,790 L 620,830 L 220,790 Z",
    'gardenPark': {'x': 450, 'y': 455, 'w': 340, 'h': 50, 'rx': 8, 'label': "Central Zen Garden & Reflection Pool"},
    'roads': {'nodes': pe_nodes, 'edges': pe_edges},
    'plots': pe_plots,
    'amenities': pe_amenities,
    'roadLabels': [
        {'name': "ELYSIAN BOULEVARD", 'x': 620, 'y': 490, 'vertical': False},
        {'name': "NORTH TERRACE WAY", 'x': 620, 'y': 245, 'vertical': False},
        {'name': "SOUTH GARDEN WAY", 'x': 620, 'y': 715, 'vertical': False},
        {'name': "AURUM AVENUE", 'x': 345, 'y': 370, 'vertical': True},
        {'name': "ARGENT AVENUE", 'x': 895, 'y': 370, 'vertical': True}
    ],
    'defaultStartGate': 'pe_gate_main',
    'sectors': ['Tower 1 (Aurum)', 'Tower 2 (Argent)', 'Tower 3 (Cuprum)', 'Tower 4 (Platin)']
}


# 4. KRISTAL BERYL (Kasavanahalli / Sarjapur Road area)
# 5 Residential Blocks/Wings: Block A, Block B, Block C, Block D, Block E
kb_nodes = {
    'kb_gate_main':     {'id': 'kb_gate_main', 'x': 90, 'y': 480, 'label': 'Gate 1 (Kasavanahalli Main Road)'},
    'kb_junc_entry':    {'id': 'kb_junc_entry', 'x': 180, 'y': 480, 'label': 'Beryl Grand Entrance Way'},
    'kb_junc_w':        {'id': 'kb_junc_w', 'x': 340, 'y': 480, 'label': 'Block A & D Promenade Cross'},
    'kb_junc_ctr':      {'id': 'kb_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Crystal Fountain Plaza'},
    'kb_junc_e':        {'id': 'kb_junc_e', 'x': 900, 'y': 480, 'label': 'Block C & E Promenade Cross'},
    'kb_gate_east':     {'id': 'kb_gate_east', 'x': 1100, 'y': 480, 'label': 'Gate 2 (Harlur Lake Link)'},

    'kb_n_w':           {'id': 'kb_n_w', 'x': 340, 'y': 260, 'label': 'Block A Court Drive'},
    'kb_n_ctr':         {'id': 'kb_n_ctr', 'x': 620, 'y': 260, 'label': 'Block B Central Avenue'},
    'kb_n_e':           {'id': 'kb_n_e', 'x': 900, 'y': 260, 'label': 'Block C Court Drive'},

    'kb_s_w':           {'id': 'kb_s_w', 'x': 340, 'y': 700, 'label': 'Block D South Parkway'},
    'kb_s_ctr':         {'id': 'kb_s_ctr', 'x': 620, 'y': 700, 'label': 'Clubhouse Pool Boardwalk'},
    'kb_s_e':           {'id': 'kb_s_e', 'x': 900, 'y': 700, 'label': 'Block E South Parkway'},

    'kb_mid_w_n':       {'id': 'kb_mid_w_n', 'x': 340, 'y': 370, 'label': 'Beryl Drive North'},
    'kb_mid_w_s':       {'id': 'kb_mid_w_s', 'x': 340, 'y': 590, 'label': 'Beryl Drive South'},
    'kb_mid_ctr_n':     {'id': 'kb_mid_ctr_n', 'x': 620, 'y': 370, 'label': 'Crystal Plaza North'},
    'kb_mid_ctr_s':     {'id': 'kb_mid_ctr_s', 'x': 620, 'y': 590, 'label': 'Crystal Plaza South'},
    'kb_mid_e_n':       {'id': 'kb_mid_e_n', 'x': 900, 'y': 370, 'label': 'Lakeview Drive North'},
    'kb_mid_e_s':       {'id': 'kb_mid_e_s', 'x': 900, 'y': 590, 'label': 'Lakeview Drive South'}
}

kb_edges_raw = [
    ('kb_gate_main', 'kb_junc_entry', 'Beryl Central Drive', 'primary'),
    ('kb_junc_entry', 'kb_junc_w', 'Beryl Central Drive', 'primary'),
    ('kb_junc_w', 'kb_junc_ctr', 'Beryl Central Drive', 'primary'),
    ('kb_junc_ctr', 'kb_junc_e', 'Beryl Central Drive', 'primary'),
    ('kb_junc_e', 'kb_gate_east', 'Lake Link Parkway', 'primary'),

    ('kb_n_w', 'kb_n_ctr', 'North Court Parkway', 'secondary'),
    ('kb_n_ctr', 'kb_n_e', 'North Court Parkway', 'secondary'),
    ('kb_s_w', 'kb_s_ctr', 'South Garden Parkway', 'secondary'),
    ('kb_s_ctr', 'kb_s_e', 'South Garden Parkway', 'secondary'),

    ('kb_n_w', 'kb_mid_w_n', 'Block A Avenue', 'secondary'),
    ('kb_mid_w_n', 'kb_junc_w', 'Block A Avenue', 'secondary'),
    ('kb_junc_w', 'kb_mid_w_s', 'Block D Avenue', 'secondary'),
    ('kb_mid_w_s', 'kb_s_w', 'Block D Avenue', 'secondary'),

    ('kb_n_ctr', 'kb_mid_ctr_n', 'Central Link', 'primary'),
    ('kb_mid_ctr_n', 'kb_junc_ctr', 'Central Link', 'primary'),
    ('kb_junc_ctr', 'kb_mid_ctr_s', 'Central Link', 'primary'),
    ('kb_mid_ctr_s', 'kb_s_ctr', 'Central Link', 'primary'),

    ('kb_n_e', 'kb_mid_e_n', 'Block C Avenue', 'secondary'),
    ('kb_mid_e_n', 'kb_junc_e', 'Block C Avenue', 'secondary'),
    ('kb_junc_e', 'kb_mid_e_s', 'Block E Avenue', 'secondary'),
    ('kb_mid_e_s', 'kb_s_e', 'Block E Avenue', 'secondary')
]
kb_edges = [{'u': u, 'v': v, 'road': r, 'type': t} for u, v, r, t in kb_edges_raw]

kb_plots = {}
block_configs_kb = [
    ("A", 280, 200, 'kb_n_w', 'North Court Parkway'),
    ("B", 560, 200, 'kb_n_ctr', 'North Court Parkway'),
    ("C", 840, 200, 'kb_n_e', 'North Court Parkway'),
    ("D", 380, 680, 'kb_s_w', 'South Garden Parkway'),
    ("E", 760, 680, 'kb_s_e', 'South Garden Parkway')
]

kb_uid = 1
for b_letter, bx, by, bnode, broad in block_configs_kb:
    flats = [101, 102, 201, 202, 301, 302, 401, 402]
    for idx, fl in enumerate(flats):
        pid = str(kb_uid)
        num_str = f"Block {b_letter} - {fl}"
        kb_plots[pid] = {
            'id': pid,
            'number': num_str,
            'road': broad,
            'block': f"Block {b_letter}",
            'facing': 'North' if 'South' in broad else 'South',
            'x': bx + (idx % 4) * 22 - 33,
            'y': by + (idx // 4) * 22 - 11,
            'w': 48,
            'h': 34,
            'roadNode': bnode,
            'color': 'cyan'
        }
        kb_uid += 1

kb_amenities = [
    {'id': 'kb_club', 'name': 'Kristal Beryl Central Clubhouse & Swimming Pool', 'description': 'Full-size adult pool, toddler splash pool, gym and community party hall', 'x': 620, 'y': 440, 'roadNode': 'kb_junc_ctr', 'icon': '🏊', 'type': 'clubhouse'},
    {'id': 'kb_badminton', 'name': 'Badminton Court & Health Club', 'description': 'Indoor badminton court, table tennis and fitness gymnasium', 'x': 480, 'y': 480, 'roadNode': 'kb_junc_w', 'icon': '🏸', 'type': 'sports'},
    {'id': 'kb_play', 'name': "Children's Play Park & Sandpit", 'description': 'Play equipment, swings, slide sets, and landscaped seating benches', 'x': 760, 'y': 480, 'roadNode': 'kb_junc_e', 'icon': '🛝', 'type': 'recreation'},
    {'id': 'kb_gate_1', 'name': 'Main Security Gate 1 (Kasavanahalli Road)', 'description': '24/7 security cabin with CCTV surveillance on Kasavanahalli Main Rd', 'x': 90, 'y': 480, 'roadNode': 'kb_gate_main', 'icon': '🚪', 'type': 'gate'},
    {'id': 'kb_gate_2', 'name': 'East Lake Link Gate 2', 'description': 'Pedestrian walking gate connecting towards Harlur Lake promenade', 'x': 1100, 'y': 480, 'roadNode': 'kb_gate_east', 'icon': '🚪', 'type': 'gate'}
]

kristal_beryl = {
    'id': 'kristal_beryl',
    'name': 'Kristal Beryl',
    'location': 'Kasavanahalli Main Road, off Sarjapur Road, Bangalore East',
    'zone': 'whitefield',
    'type': 'Gated Residential Apartment Society',
    'unitType': 'Apartment / Block',
    'unitCount': len(kb_plots),
    'bounds': {'minX': 60, 'maxX': 1180, 'minY': 150, 'maxY': 850},
    'center': {'x': 620, 'y': 480},
    'groundPolygon': "90,480 220,170 620,150 1020,170 1100,480 1020,790 620,830 220,790 Z",
    'borderTreesPath': "M 90,480 L 220,170 L 620,150 L 1020,170 L 1100,480 L 1020,790 L 620,830 L 220,790 Z",
    'gardenPark': {'x': 450, 'y': 455, 'w': 340, 'h': 50, 'rx': 8, 'label': "Central Crystal Fountain Plaza"},
    'roads': {'nodes': kb_nodes, 'edges': kb_edges},
    'plots': kb_plots,
    'amenities': kb_amenities,
    'roadLabels': [
        {'name': "BERYL CENTRAL DRIVE", 'x': 620, 'y': 490, 'vertical': False},
        {'name': "NORTH COURT PARKWAY", 'x': 620, 'y': 245, 'vertical': False},
        {'name': "SOUTH GARDEN PARKWAY", 'x': 620, 'y': 715, 'vertical': False},
        {'name': "BLOCK A AVENUE", 'x': 325, 'y': 370, 'vertical': True},
        {'name': "BLOCK C AVENUE", 'x': 915, 'y': 370, 'vertical': True}
    ],
    'defaultStartGate': 'kb_gate_main',
    'sectors': ['Block A', 'Block B', 'Block C', 'Block D', 'Block E']
}


# Generic Layout Builder function for other real Bangalore communities
def build_custom_layout(spec):
    lid = spec['id']
    name = spec['name']
    location = spec['location']
    zone = spec['zone']
    ltype = spec.get('type', 'Residential Community')
    unitType = spec.get('unitType', 'Plot')
    unitPrefix = spec.get('unitPrefix', 'Plot')
    avenues = spec['avenues'] # [Main, North, South, WestCross, EastCross]
    amenities_info = spec.get('amenities', [])
    color_theme = spec.get('colorTheme', 'cyan')
    sectors = spec.get('sectors', [f'{avenues[1]} Sector', f'{avenues[2]} Sector', f'{avenues[3]} Sector', f'{avenues[4]} Sector'])

    bounds = {'minX': 60, 'maxX': 1180, 'minY': 160, 'maxY': 840}
    center = {'x': 600, 'y': 480}

    nodes = {
        f'{lid}_gate_1':     {'id': f'{lid}_gate_1', 'x': 90, 'y': 480, 'label': f'{name} Gate 1 (Main Entrance)'},
        f'{lid}_entry':      {'id': f'{lid}_entry', 'x': 180, 'y': 480, 'label': 'Entrance Boulevard'},
        f'{lid}_junc_w':     {'id': f'{lid}_junc_w', 'x': 320, 'y': 480, 'label': f'{avenues[3]} West Junction'},
        f'{lid}_junc_ctr':   {'id': f'{lid}_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Plaza Roundabout'},
        f'{lid}_junc_e':     {'id': f'{lid}_junc_e', 'x': 920, 'y': 480, 'label': f'{avenues[4]} East Junction'},
        f'{lid}_gate_2':     {'id': f'{lid}_gate_2', 'x': 1110, 'y': 480, 'label': f'{name} Gate 2 (Rear Entrance)'},

        f'{lid}_n_w':        {'id': f'{lid}_n_w', 'x': 320, 'y': 270, 'label': f'{avenues[1]} West'},
        f'{lid}_n_mid':      {'id': f'{lid}_n_mid', 'x': 620, 'y': 270, 'label': f'{avenues[1]} North Plaza'},
        f'{lid}_n_e':        {'id': f'{lid}_n_e', 'x': 920, 'y': 270, 'label': f'{avenues[1]} East'},

        f'{lid}_s_w':        {'id': f'{lid}_s_w', 'x': 320, 'y': 690, 'label': f'{avenues[2]} West'},
        f'{lid}_s_mid':      {'id': f'{lid}_s_mid', 'x': 620, 'y': 690, 'label': f'{avenues[2]} South Plaza'},
        f'{lid}_s_e':        {'id': f'{lid}_s_e', 'x': 920, 'y': 690, 'label': f'{avenues[2]} East'},

        f'{lid}_w_n_mid':    {'id': f'{lid}_w_n_mid', 'x': 320, 'y': 375, 'label': f'{avenues[3]} North Link'},
        f'{lid}_w_s_mid':    {'id': f'{lid}_w_s_mid', 'x': 320, 'y': 585, 'label': f'{avenues[3]} South Link'},
        f'{lid}_ctr_n_mid':  {'id': f'{lid}_ctr_n_mid', 'x': 620, 'y': 375, 'label': 'Central Gardens North'},
        f'{lid}_ctr_s_mid':  {'id': f'{lid}_ctr_s_mid', 'x': 620, 'y': 585, 'label': 'Central Gardens South'},
        f'{lid}_e_n_mid':    {'id': f'{lid}_e_n_mid', 'x': 920, 'y': 375, 'label': f'{avenues[4]} North Link'},
        f'{lid}_e_s_mid':    {'id': f'{lid}_e_s_mid', 'x': 920, 'y': 585, 'label': f'{avenues[4]} South Link'}
    }

    edges_raw = [
        (f'{lid}_gate_1', f'{lid}_entry', avenues[0], 'primary'),
        (f'{lid}_entry', f'{lid}_junc_w', avenues[0], 'primary'),
        (f'{lid}_junc_w', f'{lid}_junc_ctr', avenues[0], 'primary'),
        (f'{lid}_junc_ctr', f'{lid}_junc_e', avenues[0], 'primary'),
        (f'{lid}_junc_e', f'{lid}_gate_2', avenues[0], 'primary'),

        (f'{lid}_n_w', f'{lid}_n_mid', avenues[1], 'secondary'),
        (f'{lid}_n_mid', f'{lid}_n_e', avenues[1], 'secondary'),

        (f'{lid}_s_w', f'{lid}_s_mid', avenues[2], 'secondary'),
        (f'{lid}_s_mid', f'{lid}_s_e', avenues[2], 'secondary'),

        (f'{lid}_n_w', f'{lid}_w_n_mid', avenues[3], 'secondary'),
        (f'{lid}_w_n_mid', f'{lid}_junc_w', avenues[3], 'secondary'),
        (f'{lid}_junc_w', f'{lid}_w_s_mid', avenues[3], 'secondary'),
        (f'{lid}_w_s_mid', f'{lid}_s_w', avenues[3], 'secondary'),

        (f'{lid}_n_mid', f'{lid}_ctr_n_mid', 'Central Link', 'primary'),
        (f'{lid}_ctr_n_mid', f'{lid}_junc_ctr', 'Central Link', 'primary'),
        (f'{lid}_junc_ctr', f'{lid}_ctr_s_mid', 'Central Link', 'primary'),
        (f'{lid}_ctr_s_mid', f'{lid}_s_mid', 'Central Link', 'primary'),

        (f'{lid}_n_e', f'{lid}_e_n_mid', avenues[4], 'secondary'),
        (f'{lid}_e_n_mid', f'{lid}_junc_e', avenues[4], 'secondary'),
        (f'{lid}_junc_e', f'{lid}_e_s_mid', avenues[4], 'secondary'),
        (f'{lid}_e_s_mid', f'{lid}_s_e', avenues[4], 'secondary')
    ]
    edges = [{'u': u, 'v': v, 'road': r, 'type': t} for u, v, r, t in edges_raw]

    plots = {}
    uid = 1
    # 8 North row
    for i in range(8):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[1], 'block': sectors[0] if len(sectors) > 0 else 'North Sector',
            'facing': 'South', 'x': 360 + i * 65, 'y': 210, 'w': 50, 'h': 36,
            'roadNode': f'{lid}_n_mid' if i in [3, 4] else (f'{lid}_n_w' if i < 3 else f'{lid}_n_e'),
            'color': color_theme
        }
        uid += 1

    # 8 Mid-North row
    for i in range(8):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[1], 'block': sectors[1] if len(sectors) > 1 else 'Central Sector',
            'facing': 'North', 'x': 360 + i * 65, 'y': 330, 'w': 50, 'h': 36,
            'roadNode': f'{lid}_n_mid' if i in [3, 4] else (f'{lid}_n_w' if i < 3 else f'{lid}_n_e'),
            'color': color_theme
        }
        uid += 1

    # 8 Mid-South row
    for i in range(8):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[2], 'block': sectors[1] if len(sectors) > 1 else 'Central Sector',
            'facing': 'South', 'x': 360 + i * 65, 'y': 630, 'w': 50, 'h': 36,
            'roadNode': f'{lid}_s_mid' if i in [3, 4] else (f'{lid}_s_w' if i < 3 else f'{lid}_s_e'),
            'color': color_theme
        }
        uid += 1

    # 8 South row
    for i in range(8):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[2], 'block': sectors[2] if len(sectors) > 2 else 'South Sector',
            'facing': 'North', 'x': 360 + i * 65, 'y': 750, 'w': 50, 'h': 36,
            'roadNode': f'{lid}_s_mid' if i in [3, 4] else (f'{lid}_s_w' if i < 3 else f'{lid}_s_e'),
            'color': color_theme
        }
        uid += 1

    # 6 West wing
    for i in range(6):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[3], 'block': sectors[0] if len(sectors) > 0 else 'West Sector',
            'facing': 'East', 'x': 240, 'y': 280 + i * 70, 'w': 48, 'h': 36,
            'roadNode': f'{lid}_w_n_mid' if i < 3 else f'{lid}_w_s_mid',
            'color': color_theme
        }
        uid += 1

    # 6 East wing
    for i in range(6):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[4], 'block': sectors[3] if len(sectors) > 3 else 'East Sector',
            'facing': 'West', 'x': 1000, 'y': 280 + i * 70, 'w': 48, 'h': 36,
            'roadNode': f'{lid}_e_n_mid' if i < 3 else f'{lid}_e_s_mid',
            'color': color_theme
        }
        uid += 1

    amenities = [
        {'id': f'{lid}_gate_1', 'name': f'{name} Main Gate 1', 'description': 'Security checkpoint, visitor RFID entry & security cabin', 'x': 90, 'y': 480, 'roadNode': f'{lid}_gate_1', 'icon': '🚪', 'type': 'gate'},
        {'id': f'{lid}_gate_2', 'name': f'{name} Gate 2', 'description': 'Secondary gate, service exit & emergency access', 'x': 1110, 'y': 480, 'roadNode': f'{lid}_gate_2', 'icon': '🚪', 'type': 'gate'}
    ]

    for am in amenities_info:
        amenities.append({
            'id': f"{lid}_{am['id']}",
            'name': am['name'],
            'description': am.get('desc', 'Community facility'),
            'x': am.get('x', 620),
            'y': am.get('y', 480),
            'roadNode': f"{lid}_{am['node']}",
            'icon': am.get('icon', '📍'),
            'type': am.get('type', 'general')
        })

    road_labels = [
        {'name': avenues[0].upper(), 'x': 620, 'y': 490, 'vertical': False},
        {'name': avenues[1].upper(), 'x': 620, 'y': 255, 'vertical': False},
        {'name': avenues[2].upper(), 'x': 620, 'y': 705, 'vertical': False},
        {'name': avenues[3].upper(), 'x': 305, 'y': 375, 'vertical': True},
        {'name': avenues[4].upper(), 'x': 935, 'y': 375, 'vertical': True}
    ]

    return {
        'id': lid,
        'name': name,
        'location': location,
        'zone': zone,
        'type': ltype,
        'unitType': unitType,
        'unitCount': len(plots),
        'bounds': bounds,
        'center': center,
        'groundPolygon': "90,480 200,160 620,140 1040,160 1110,480 1040,800 620,840 200,800 Z",
        'borderTreesPath': "M 90,480 L 200,160 L 620,140 L 1040,160 L 1110,480 L 1040,800 L 620,840 L 200,800 Z",
        'gardenPark': {'x': 460, 'y': 455, 'w': 320, 'h': 50, 'rx': 8, 'label': "Central Landscaped Park & Courtyard"},
        'roads': {'nodes': nodes, 'edges': edges},
        'plots': plots,
        'amenities': amenities,
        'roadLabels': road_labels,
        'defaultStartGate': f'{lid}_gate_1',
        'sectors': sectors
    }

# 5. ALL OTHER FAMOUS REAL BANGALORE COMMUNITIES SPECS
specs = [
    # --- SOUTH BANGALORE ---
    {
        'id': 'sattva_greenage', 'name': 'Salarpuria Sattva Greenage', 'location': 'Hosur Main Road, Bommanahalli, Bangalore South',
        'zone': 'south', 'type': 'Mega Residential Gated Community', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Alpine Tower', 'Aster Tower', 'Birch Tower', 'Cedar Tower', 'Ebony Tower'],
        'avenues': ['Greenage Boulevard', 'Clayey Park Drive', 'Lakeside Link', 'Alpine Avenue', 'Ebony Parkway'],
        'amenities': [
            {'id': 'club', 'name': 'Clayey Park Grand Clubhouse', 'desc': '60,000 sq ft clubhouse with 4 swimming pools, 2 squash courts & bowling alley', 'x': 620, 'y': 440, 'node': 'junc_ctr', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'sports', 'name': 'Greenage Sports Arena', 'desc': 'Tennis courts, skating rink and football turf', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'sports', 'icon': '🎾'}
        ]
    },
    {
        'id': 'prestige_song_south', 'name': 'Prestige Song of the South', 'location': 'Begur-Koppa Road, off Bannerghatta Road, Bangalore South',
        'zone': 'south', 'type': 'High-Rise Residential Township', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower 1-4 (Symphony)', 'Tower 5-8 (Melody)', 'Tower 9-12 (Harmony)', 'Tower 13-17 (Rhythm)'],
        'avenues': ['Song of South Boulevard', 'Symphony Way', 'Lakeview Promenade', 'Rhythm Avenue', 'Melody Parkway'],
        'amenities': [
            {'id': 'club', 'name': 'Grand Symphony Clubhouse', 'desc': 'Double-height clubhouse, gym, mini-theatre & banquet halls', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🎭'},
            {'id': 'lake', 'name': 'Lake Promenade & Reflection Deck', 'desc': 'Serene natural lakefront jogging track', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '🌊'}
        ]
    },
    {
        'id': 'brigade_millennium', 'name': 'Brigade Millennium', 'location': 'JP Nagar 7th Phase, Bangalore South',
        'zone': 'south', 'type': 'Iconic Integrated Residential Campus', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Cassia Block', 'Jacaranda Block', 'Laburnum Block', 'Magnolia Block', 'Mayflower Block'],
        'avenues': ['Millennium Boulevard', 'Woodrose Club Avenue', 'MLR Parkway', 'Cassia Link', 'Mayflower Way'],
        'amenities': [
            {'id': 'club', 'name': 'The Woodrose Club', 'desc': 'Renowned country club with swimming pool, squash, tennis, restaurants', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'hall', 'name': 'MLR Convention Centre', 'desc': 'Premier 500-seat cultural theatre and convention auditorium', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'auditorium', 'icon': '🏛️'}
        ]
    },
    {
        'id': 'purva_westend', 'name': 'Purva Westend', 'location': 'Kudlu Gate, Hosur Main Road, Bangalore South',
        'zone': 'south', 'type': 'Cinema-Themed Luxury High-Rise', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Broadway Tower', 'Opera Tower', 'West End Tower 1', 'West End Tower 2'],
        'avenues': ['Westend Boulevard', 'Broadway Promenade', 'Cinema Walkway', 'Kudlu Link', 'Opera Court'],
        'amenities': [
            {'id': 'cinema', 'name': 'Open Air Amphitheatre Cinema', 'desc': 'Private outdoor amphitheatre cinema with acoustic surround sound', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'entertainment', 'icon': '🎬'},
            {'id': 'pool', 'name': 'Fantasy Wave Pool & Resort Deck', 'desc': 'Artificial beach wave pool, swimming pool and palm cabanas', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'}
        ]
    },
    {
        'id': 'brigade_meadows', 'name': 'Brigade Meadows', 'location': 'Kanakapura Road, Bangalore South',
        'zone': 'south', 'type': 'Integrated Gated Township', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Plumeria Tower', 'Wisteria Tower', 'Saaket Block'],
        'avenues': ['Meadows Boulevard', 'Plumeria Drive', 'Wisteria Way', 'Saaket Link', 'Kanakapura Corridor'],
        'amenities': [
            {'id': 'club', 'name': 'Club Meadows', 'desc': 'Clubhouse, lap pool, badminton court, gym & banquet', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'arcade', 'name': 'Signature Commercial Arcade', 'desc': 'Supermarket, clinic, pharmacy and coffee shop', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'civic', 'icon': '🏪'}
        ]
    },
    {
        'id': 'mantri_tranquil', 'name': 'Mantri Tranquil', 'location': 'Kanakapura Road / Gubbalala, Bangalore South',
        'zone': 'south', 'type': 'High-Rise Residential Township', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower A-C', 'Tower D-F', 'Tower G-H', 'Tower J'],
        'avenues': ['Tranquil Boulevard', 'Gubbalala Parkway', 'Forest View Link', 'Central Promenade', 'Metro Parkway'],
        'amenities': [
            {'id': 'club', 'name': 'Club Tranquil', 'desc': 'Indoor badminton, squash, heated pool, sauna & health spa', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'concorde_napa_valley', 'name': 'Concorde Napa Valley', 'location': 'Kanakapura Road, Bangalore South',
        'zone': 'south', 'type': 'California-Themed Luxury Villa Township', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Napa Court', 'Sonoma Way', 'Vineyard Promenade'],
        'avenues': ['Napa Boulevard', 'Vineyard Parkway', 'Oak Knoll Way', 'Sonoma Drive', 'Valley Link'],
        'amenities': [
            {'id': 'club', 'name': 'Club Napa Grande', 'desc': 'Lakeside clubhouse, tennis courts, infinity pool and bowling alley', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🍷'}
        ]
    },
    {
        'id': 'jp_nagar_phase7', 'name': 'JP Nagar 7th Phase', 'location': 'Brigade Millennium / Puttenahalli, Bangalore South',
        'zone': 'south', 'type': 'BDA Prime Residential Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['RBI Layout Sector', 'Chunchgatta Sector', 'Brigade Vicinity'],
        'avenues': ['24th Main Boulevard', 'RBI Water Tank Road', 'Puttenahalli Parkway', 'Woodrose Link', 'Brigade Millennium Way'],
        'amenities': [
            {'id': 'lake', 'name': 'Puttenahalli Lake Bird Sanctuary', 'desc': 'Restored urban eco-lake with walking tracks & gazebo', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '🦆'}
        ]
    },
    {
        'id': 'jp_nagar_phase2', 'name': 'JP Nagar 2nd Phase', 'location': 'Near South End Circle / 100ft Road, Bangalore South',
        'zone': 'south', 'type': 'Classic BDA Residential Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['100ft Road Sector', 'Ranga Shankara Sector'],
        'avenues': ['100ft Ring Road Boulevard', '14th Main Avenue', '2nd Phase Parkway', 'Ranga Shankara Way', 'Lakeside Link'],
        'amenities': [
            {'id': 'theatre', 'name': 'Ranga Shankara Theatre', 'desc': 'World-class landmark theatre space founded by Arundhati Nag', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'arts', 'icon': '🎭'}
        ]
    },
    {
        'id': 'btm_2nd_stage', 'name': 'BTM Layout 2nd Stage', 'location': 'Ring Road / Udupi Garden, Bangalore South',
        'zone': 'south', 'type': 'Prime Cosmopolitan Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Outer Ring Sector', 'Udupi Garden Sector', 'Lakeview Sector'],
        'avenues': ['Outer Ring Road Boulevard', '7th Main Parkway', 'Lake Road Way', 'Udupi Garden Link', 'Kuvempu Nagar Avenue'],
        'amenities': [
            {'id': 'lake', 'name': 'Madiwala Lake Boating Park', 'desc': 'Huge lake promenade, bird sanctuary and boating center', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '⛵'}
        ]
    },
    {
        'id': 'jayanagar_4th', 'name': 'Jayanagar 4th Block', 'location': 'Nanda Road / Complex, Bangalore South',
        'zone': 'south', 'type': 'Heritage Planned Garden Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Shopping Complex Sector', 'Nanda Road Sector', 'South End Sector'],
        'avenues': ['11th Main Boulevard', '30th Cross Parkway', 'Nanda Road Way', 'Complex Ring Link', 'Pattabhirama Temple Road'],
        'amenities': [
            {'id': 'complex', 'name': '4th Block Shopping Complex', 'desc': 'Iconic Bangalore shopping and cultural hub', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'market', 'icon': '🛍️'}
        ]
    },
    {
        'id': 'jayanagar_9th', 'name': 'Jayanagar 9th Block', 'location': 'Ragigudda / East End, Bangalore South',
        'zone': 'south', 'type': 'Classic Residential Block', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Ragigudda Sector', 'East End Sector'],
        'avenues': ['East End Main Boulevard', '39th Cross Parkway', 'Ragigudda Link', '9th Block Avenue', 'Jayadeva Metro Way'],
        'amenities': [
            {'id': 'temple', 'name': 'Ragigudda Sri Prasanna Anjaneya Temple', 'desc': 'Historic hilltop temple and cultural auditorium complex', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'purva_panorama', 'name': 'Purva Panorama', 'location': 'Bannerghatta Main Road / Kalena Agrahara, Bangalore South',
        'zone': 'south', 'type': 'High-Rise Residential Society', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower 1-3', 'Tower 4-6'],
        'avenues': ['Panorama Boulevard', 'Hilltop Avenue', 'Central Garden Drive', 'Kalena Link', 'Bannerghatta Access Way'],
        'amenities': [
            {'id': 'club', 'name': 'Panorama Club & Pool', 'desc': 'Clubhouse, rooftop tennis court, pool and squash', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'meenakshi_layout', 'name': 'Meenakshi Layout', 'location': 'Bannerghatta Road / Hulimavu, Bangalore South',
        'zone': 'south', 'type': 'Residential Society', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Hulimavu Sector', 'Mall View Sector'],
        'avenues': ['Meenakshi Temple Boulevard', 'Hulimavu Main Avenue', 'Cave Temple Road', 'Mall Access Link', 'Lake Road'],
        'amenities': [
            {'id': 'temple', 'name': 'Sri Meenakshi Sundareshwara Temple', 'desc': 'Grand Dravidian temple and Hulimavu cave complex', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'south_city_layout', 'name': 'South City Layout', 'location': 'Bannerghatta Road / Arekere Mico Layout, Bangalore South',
        'zone': 'south', 'type': 'Massive Integrated Apartment Enclave', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Block A-D', 'Block E-H', 'Block J-L'],
        'avenues': ['South City Boulevard', 'Arekere Parkway', 'Central Garden Way', 'Mico Link Avenue', 'Lake Access Road'],
        'amenities': [
            {'id': 'club', 'name': 'South City Club & Sports Complex', 'desc': 'Indoor badminton, tennis courts, pool, gym & parks', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # --- WHITEFIELD & BANGALORE EAST ---
    {
        'id': 'sobha_dream_acres', 'name': 'Sobha Dream Acres', 'location': 'Panathur Main Road, Balagere / ORR Corridor, Bangalore East',
        'zone': 'whitefield', 'type': 'Mega Precast Residential Township', 'unitType': 'Apartment / Wing', 'unitPrefix': 'Wing', 'colorTheme': 'cyan',
        'sectors': ['Rainforest Wing', 'Coral Wing', 'Palm Wing', 'Spring Wing'],
        'avenues': ['Dream Acres Boulevard', 'Panathur Link', 'Clubhouse Central Way', 'Balagere Parkway', 'Outer Ring Expressway'],
        'amenities': [
            {'id': 'club', 'name': 'Clubhouse 1 & Olympic Lap Pool', 'desc': 'Massive clubhouse, 5 swimming pools, tennis and squash courts', 'x': 620, 'y': 440, 'node': 'junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'prestige_lakeside', 'name': 'Prestige Lakeside Habitat', 'location': 'Varthur Main Road, Whitefield Corridor, Bangalore East',
        'zone': 'whitefield', 'type': 'Disney-Themed Township (Villas & High-Rises)', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower 1-6', 'Tower 7-12', 'Disney Villa Enclave'],
        'avenues': ['Lakeside Boulevard', 'Disney Promenade', 'Varthur Lake Parkway', 'Fairytale Way', 'Orchard Link'],
        'amenities': [
            {'id': 'club', 'name': 'Disney Themed Central Clubhouse', 'desc': '4 massive clubhouses, multiple pools, cricket pitch & lakefront view', 'x': 620, 'y': 440, 'node': 'junc_ctr', 'type': 'clubhouse', 'icon': '🏰'}
        ]
    },
    {
        'id': 'palm_meadows', 'name': 'Palm Meadows', 'location': 'Varthur Main Road, Whitefield, Bangalore East',
        'zone': 'whitefield', 'type': 'Iconic Luxury Gated Villa Township', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Windmill Sector', 'Palm Boulevard', 'Lakeside Court'],
        'avenues': ['Palm Meadows Boulevard', 'Windmill Avenue', 'Lakeview Parkway', 'Meadow Drive', 'Whitefield Link'],
        'amenities': [
            {'id': 'club', 'name': 'The Palm Meadows Club', 'desc': 'Exclusive 5-star resort club, indoor/outdoor pools, squash & fine dining', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🌴'}
        ]
    },
    {
        'id': 'prestige_shantiniketan', 'name': 'Prestige Shantiniketan', 'location': 'ITPL Main Road, Whitefield, Bangalore East',
        'zone': 'whitefield', 'type': 'Integrated Township with Forum Shantiniketan Mall', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Crescent Tower', 'Tower 1-8', 'Tower 9-16', 'Tower 17-24'],
        'avenues': ['Shantiniketan Boulevard', 'ITPL Access Parkway', 'Forum Mall Promenade', 'Urban Terrace Way', 'Metro Link'],
        'amenities': [
            {'id': 'mall', 'name': 'Forum Shantiniketan Mall', 'desc': 'Direct pedestrian access to Forum Mall, PVR, food court and high-street shopping', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'mall', 'icon': '🛍️'}
        ]
    },
    {
        'id': 'rainbow_drive', 'name': 'Rainbow Drive', 'location': 'Sarjapur Road, Carmelaram, Bangalore East',
        'zone': 'whitefield', 'type': 'Eco-Friendly Gated Villa Layout', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Gulmohar Sector', 'Jacaranda Sector', 'Bamboo Grove'],
        'avenues': ['Rainbow Boulevard', 'Gulmohar Avenue', 'Jacaranda Way', 'Eco Walk Parkway', 'Sarjapur Link'],
        'amenities': [
            {'id': 'club', 'name': 'Rainbow Recreation & Pool', 'desc': 'Rainwater harvesting lake, solar clubhouse and swimming pool', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🌈'}
        ]
    },
    {
        'id': 'divyasree_republic', 'name': 'Divyasree Republic of Whitefield', 'location': 'EPIP Zone, Kundalahalli, Bangalore East',
        'zone': 'whitefield', 'type': 'Contemporary Urban High-Rise', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower A-D', 'Tower E-H'],
        'avenues': ['Republic Boulevard', 'EPIP Parkway', 'Central Garden Walk', 'Tech Link Avenue', 'Kundalahalli Way'],
        'amenities': [
            {'id': 'club', 'name': 'Republic Central Club', 'desc': 'Sports arena, rooftop pool, co-working lounge and spa', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏙️'}
        ]
    },
    {
        'id': 'confident_anthea', 'name': 'Confident Anthea', 'location': 'Sarjapur Road, Bangalore East',
        'zone': 'whitefield', 'type': 'Gated Community Villas', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Rose Sector', 'Lily Sector'],
        'avenues': ['Anthea Boulevard', 'Rose Avenue', 'Lily Parkway', 'Sarjapur Link', 'Orchard Drive'],
        'amenities': [
            {'id': 'club', 'name': 'Anthea Club House', 'desc': 'Swimming pool, gymnasium and sports zone', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏡'}
        ]
    },
    {
        'id': 'chaithanya_smaran', 'name': 'Chaithanya Smaran', 'location': 'Hoskote Road, Whitefield, Bangalore East',
        'zone': 'whitefield', 'type': 'Ultra-Luxury Gated Villa Enclave', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Bespoke Villa North', 'Bespoke Villa South'],
        'avenues': ['Smaran Boulevard', 'Lotus Parkway', 'Tranquil Way', 'Hoskote Link', 'Banyan Drive'],
        'amenities': [
            {'id': 'club', 'name': 'The Smaran Pavilion', 'desc': 'Lakeside pavilion, infinity pool and tennis court', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '💎'}
        ]
    },
    {
        'id': 'whitefield_inner_circle', 'name': 'Whitefield Inner Circle', 'location': 'Inner Circle Park / Whitefield Main, Bangalore East',
        'zone': 'whitefield', 'type': 'Historic Heritage Circular Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Circle Park Sector', 'Waverly Sector'],
        'avenues': ['Inner Circle Boulevard', 'Waverly Road Parkway', 'Outer Circle Way', 'Church Street Link', 'Post Office Road'],
        'amenities': [
            {'id': 'park', 'name': 'Whitefield Inner Circle Park', 'desc': 'Colonial circular park with giant rain trees and heritage gazebo', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'park', 'icon': '🌳'}
        ]
    },
    {
        'id': 'sowparnika_columns', 'name': 'Sowparnika The Columns', 'location': 'Whitefield, Bangalore East',
        'zone': 'whitefield', 'type': 'Modern Residential Society', 'unitType': 'Apartment / Block', 'unitPrefix': 'Block', 'colorTheme': 'cyan',
        'sectors': ['Block A', 'Block B', 'Block C'],
        'avenues': ['Columns Boulevard', 'Central Promenade', 'East Access Way', 'Gardenia Link', 'Whitefield Road'],
        'amenities': [
            {'id': 'club', 'name': 'The Columns Clubhouse', 'desc': 'Rooftop clubhouse and indoor games arena', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏢'}
        ]
    },
    {
        'id': 'doddakannelli_greens', 'name': 'Doddakannelli Greens', 'location': 'Carmelaram / Sarjapur Road, Bangalore East',
        'zone': 'whitefield', 'type': 'Gated Community Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Greenwood Sector', 'Lake View Sector'],
        'avenues': ['Doddakannelli Main Boulevard', 'Carmelaram Parkway', 'Greenwood Way', 'Wipro Link', 'Railway Station Road'],
        'amenities': [
            {'id': 'lake', 'name': 'Carmelaram Lakefront Green', 'desc': 'Natural wetland park & jogging trail', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '🌿'}
        ]
    },
    {
        'id': 'marathahalli_sgr', 'name': 'Marathahalli SGR Layout', 'location': 'Munnekollal / Marathahalli ORR, Bangalore East',
        'zone': 'whitefield', 'type': 'Tech Residential Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['College Sector', 'ORR Link Sector'],
        'avenues': ['SGR College Boulevard', 'Munnekollal Main Avenue', 'ORR Bypass Parkway', 'Dental College Link', 'Spice Garden Way'],
        'amenities': [
            {'id': 'hub', 'name': 'Spice Garden Tech Commercial Hub', 'desc': 'Supermarkets, cafes, clinics and transit connections', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'market', 'icon': '☕'}
        ]
    },

    # --- ELECTRONIC CITY, HSR & OUTER RING ROAD ---
    {
        'id': 'adarsh_palm_retreat', 'name': 'Adarsh Palm Retreat', 'location': 'Outer Ring Road, Bellandur / Devarabisanahalli, Bangalore',
        'zone': 'ecity', 'type': 'Premier Luxury Villa & Tower Township', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Palm Boulevard', 'Retreat Villas', 'Condoville Towers'],
        'avenues': ['Palm Retreat Boulevard', 'Lake Promenade', 'Bellandur Link Way', 'Orchard Drive', 'Devarabisanahalli Parkway'],
        'amenities': [
            {'id': 'club', 'name': 'The Palm Retreat Clubhouse', 'desc': 'World-class clubhouse, Olympic swimming pool, squash and gym', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'hsr_sector_1', 'name': 'HSR Layout Sector 1', 'location': 'Agara Lake / Outer Ring Road, Bangalore South-East',
        'zone': 'ecity', 'type': 'BDA Premier Planned Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Agara Lake Sector', '27th Main Commercial', '14th Main Residential'],
        'avenues': ['27th Main Boulevard', '14th Main Parkway', 'Agara Lake Road', 'ORR Link', '19th Main Way'],
        'amenities': [
            {'id': 'lake', 'name': 'Agara Lake Botanical Promenade', 'desc': 'Restored lake with outdoor gym, jogging tracks and butterfly park', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '🌊'}
        ]
    },
    {
        'id': 'hsr_sector_2', 'name': 'HSR Layout Sector 2', 'location': '24th Main / Somasundarapalya, Bangalore South-East',
        'zone': 'ecity', 'type': 'BDA Premier Planned Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['24th Main Sector', 'Somasundara Lake Sector'],
        'avenues': ['24th Main Boulevard', 'Sector 2 Parkway', 'Lake Road Way', 'Parangipalya Link', 'Club Avenue'],
        'amenities': [
            {'id': 'club', 'name': 'HSR Club', 'desc': 'Premier residential club with tennis, swimming, billiards and library', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🎾'}
        ]
    },
    {
        'id': 'hsr_sector_3', 'name': 'HSR Layout Sector 3', 'location': '19th Main / BDA Complex, Bangalore South-East',
        'zone': 'ecity', 'type': 'BDA Premier Planned Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['BDA Complex Sector', 'Sector 3 Residential'],
        'avenues': ['19th Main Boulevard', 'BDA Complex Parkway', '9th Cross Way', 'Silk Board Link', 'Central Park Drive'],
        'amenities': [
            {'id': 'complex', 'name': 'HSR BDA Complex & Cultural Ground', 'desc': 'Major civic shopping hub, public library and open grounds', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🏛️'}
        ]
    },
    {
        'id': 'green_glen', 'name': 'Green Glen Layout', 'location': 'Bellandur, Outer Ring Road, Bangalore South-East',
        'zone': 'ecity', 'type': 'Tech Residential Layout', 'unitType': 'Apartment / Block', 'unitPrefix': 'Block', 'colorTheme': 'cyan',
        'sectors': ['Sobha Hibiscus Enclave', 'Bellandur Lake Enclave'],
        'avenues': ['Green Glen Boulevard', 'Bellandur Main Avenue', 'Lakeview Parkway', 'Ecospace Link Way', 'Sobha Drive'],
        'amenities': [
            {'id': 'park', 'name': 'Green Glen Community Park', 'desc': 'Children play park, basketball court & green pathway', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'park', 'icon': '🌳'}
        ]
    },
    {
        'id': 'concorde_cuppertino', 'name': 'Concorde Cuppertino', 'location': 'Neeladri Road, Electronic City Phase 1, Bangalore',
        'zone': 'ecity', 'type': 'Gated Community Villas', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Villa West', 'Villa East'],
        'avenues': ['Cuppertino Boulevard', 'Neeladri Parkway', 'Silicon Way', 'Wipro Access Link', 'Central Promenade'],
        'amenities': [
            {'id': 'club', 'name': 'Club Cuppertino', 'desc': 'Swimming pool, tennis court, bowling alley & gym', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'neo_town', 'name': 'Neotown Electronic City', 'location': 'Neotown Road, Electronic City Phase 1, Bangalore',
        'zone': 'ecity', 'type': 'Integrated Residential Township', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Smondoville', 'Neo Towers'],
        'avenues': ['Neotown Boulevard', 'Smondo Parkway', 'Tech Boulevard Link', 'Helipad Way', 'Electronic City Expressway'],
        'amenities': [
            {'id': 'club', 'name': 'Neotown Clubhouse & Sports Court', 'desc': 'Infinity pool, badminton court, supermarket & clinic', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'clubhouse', 'icon': '🏢'}
        ]
    },

    # --- NORTH BANGALORE & AIRPORT CORRIDOR ---
    {
        'id': 'sobha_city', 'name': 'Sobha City', 'location': 'Thanisandra Main Road, Bangalore North',
        'zone': 'north', 'type': 'Mediterranean-Themed Luxury Township', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Santorini Tower', 'Casa Serena Tower', 'Mykonos Block'],
        'avenues': ['Sobha City Boulevard', 'Santorini Way', 'Casa Serena Parkway', 'Thanisandra Link', 'Amphitheater Drive'],
        'amenities': [
            {'id': 'club', 'name': 'Club Santorini', 'desc': '60,000 sq ft luxury clubhouse, 50m lap pool and squash court', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'bhartiya_city', 'name': 'Bhartiya City Nikoo Homes', 'location': 'Thanisandra Main Road, Bangalore North',
        'zone': 'north', 'type': '125-Acre Smart Integrated City', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Nikoo Homes 1', 'Nikoo Homes 2', 'Central Park Enclave'],
        'avenues': ['Nikoo Boulevard', 'Central Park Parkway', 'Bhartiya High Street', 'Rambler Way', 'Thanisandra Highway'],
        'amenities': [
            {'id': 'park', 'name': 'Bhartiya Central Park & Amphitheatre', 'desc': '7-acre central park, open-air cinema and shopping boulevard', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'park', 'icon': '🌳'}
        ]
    },
    {
        'id': 'manyata_residency', 'name': 'Manyata Tech Park Residency', 'location': 'Nagavara / Outer Ring Road, Bangalore North',
        'zone': 'north', 'type': 'Gated Executive Tech Township', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Residency North', 'Residency South'],
        'avenues': ['Manyata Boulevard', 'Nagavara Ring Parkway', 'Tech Park Link', 'Residency Way', 'Lumbini Access Road'],
        'amenities': [
            {'id': 'lake', 'name': 'Lumbini Gardens Waterfront', 'desc': 'Eco-park, boating, wave pool and lake promenade', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '⛵'}
        ]
    },
    {
        'id': 'prestige_golfshire', 'name': 'Prestige Golfshire', 'location': 'Nandi Hills Road, Devanahalli, Bangalore North',
        'zone': 'north', 'type': 'Signature Golf Villa Resort Township', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'cyan',
        'sectors': ['Fairway Enclave', 'Nandi View Enclave'],
        'avenues': ['Golfshire Boulevard', 'Fairway Green Parkway', 'Nandi Foothill Drive', 'Clubhouse Link', 'Airport Expressway'],
        'amenities': [
            {'id': 'golf', 'name': '18-Hole Championship Golf Course', 'desc': 'Bob Hunt designed golf course, JW Marriott luxury resort & spa', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'golf', 'icon': '⛳'}
        ]
    },
    {
        'id': 'ozone_urbana', 'name': 'Ozone Urbana', 'location': 'NH-44, Devanahalli / Airport Vicinity, Bangalore North',
        'zone': 'north', 'type': 'Integrated Mega Township', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Urbana Prime', 'Urbana Aqua', 'Urbana Meadows'],
        'avenues': ['Urbana Boulevard', 'National Highway Link', 'Airport Parkway', 'Central Promenade', 'Sports Arena Way'],
        'amenities': [
            {'id': 'club', 'name': 'Club Urbana', 'desc': 'Multiple clubhouses, swimming pools, Olympic tracks and retail mall', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'clubhouse', 'icon': '🏢'}
        ]
    },
    {
        'id': 'rmz_galleria', 'name': 'RMZ Galleria', 'location': 'Ambedkar Colony, Yelahanka, Bangalore North',
        'zone': 'north', 'type': 'Integrated Mall & High-Rise Residences', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower A', 'Tower B', 'Galleria Mall'],
        'avenues': ['Galleria Boulevard', 'Yelahanka Main Parkway', 'Mall Ring Link', 'BBMP Office Way', 'Kogilu Link Road'],
        'amenities': [
            {'id': 'mall', 'name': 'RMZ Galleria Mall', 'desc': 'Direct pedestrian access to shopping mall, INOX multiplex and food court', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'mall', 'icon': '🛍️'}
        ]
    },
    {
        'id': 'prestige_misty_waters', 'name': 'Prestige Misty Waters', 'location': 'Hebbal / Outer Ring Road, Bangalore North',
        'zone': 'north', 'type': 'Luxury High-Rise Society', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower 1-2', 'Tower 3-4'],
        'avenues': ['Misty Waters Boulevard', 'Hebbal Ring Link', 'Lakeview Parkway', 'Central Pool Way', 'Nagavara Approach Road'],
        'amenities': [
            {'id': 'club', 'name': 'Misty Waters Clubhouse', 'desc': 'Heated swimming pool, badminton, squash and banquet', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'godrej_woodsman', 'name': 'Godrej Woodsman Estate', 'location': 'Bellary Road, Hebbal, Bangalore North',
        'zone': 'north', 'type': 'High-Rise Residential Society', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Tower 1-4', 'Tower 5-7'],
        'avenues': ['Woodsman Boulevard', 'Bellary Road Parkway', 'Airport Highway Link', 'Hebbal Flyover Way', 'Lakeview Drive'],
        'amenities': [
            {'id': 'club', 'name': 'The Woodsman Club', 'desc': 'Gymnasium, tennis court, pool and landscaped gardens', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🌳'}
        ]
    },
    {
        'id': 'jakkur_aerodrome', 'name': 'Jakkur Aerodrome Lakeview', 'location': 'Jakkur Main Road / Lake, Bangalore North',
        'zone': 'north', 'type': 'Scenic Waterfront Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Aerodrome Sector', 'Lakefront Sector'],
        'avenues': ['Jakkur Lake Boulevard', 'Aerodrome Parkway', 'Flyer Avenue', 'Flying Club Link', 'Bellary Highway Road'],
        'amenities': [
            {'id': 'lake', 'name': 'Jakkur Lake Wetland & Bird Hide', 'desc': 'Pristine lake, walking boardwalks and migratory pelican sanctuary', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '🦅'}
        ]
    },
    {
        'id': 'kempapura_lakeview', 'name': 'Kempapura Lakeview', 'location': 'Hebbal Kempapura / Coffee Board Layout, Bangalore North',
        'zone': 'north', 'type': 'Established Residential Enclave', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Coffee Board Sector', 'Kempapura Sector'],
        'avenues': ['Kempapura Main Boulevard', 'Coffee Board Parkway', 'Hebbal Lake Drive', 'Esteem Mall Link', 'Ring Road Bypass'],
        'amenities': [
            {'id': 'lake', 'name': 'Hebbal Lake Recreational Park', 'desc': 'Heritage lake, boating, landscaped jogging paths', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '🌊'}
        ]
    },

    # --- CENTRAL & WEST BANGALORE ---
    {
        'id': 'koramangala_4th', 'name': 'Koramangala 4th Block', 'location': 'Maharaja Agrasen Road / ST Bed, Bangalore Central',
        'zone': 'west', 'type': 'Premier Elite Residential Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['ST Bed Sector', 'Maharaja Sector'],
        'avenues': ['Maharaja Avenue Boulevard', '80ft Road Parkway', 'ST Bed Main Way', 'Sony World Link', 'Inner Ring Connector'],
        'amenities': [
            {'id': 'park', 'name': 'Koramangala 4th Block Park & Library', 'desc': 'Tranquil canopy park, senior walk and public library', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'park', 'icon': '☕'}
        ]
    },
    {
        'id': 'koramangala_3rd', 'name': 'Koramangala 3rd Block', 'location': 'Billionaire Row / 12th Main, Bangalore Central',
        'zone': 'west', 'type': 'Billionaires Row Residential Enclave', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Billionaires Row', '12th Main Sector'],
        'avenues': ['12th Main Boulevard', 'Billionaire Row Parkway', '10th Cross Way', 'Sarjapur Junction Link', 'Koramangala Club Road'],
        'amenities': [
            {'id': 'club', 'name': 'The Koramangala Club', 'desc': 'Prestigious members club with tennis, swimming, squash and dining', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🎾'}
        ]
    },
    {
        'id': 'indiranagar_defence', 'name': 'Defence Colony Indiranagar', 'location': '100ft Road / CMH Road, Bangalore Central',
        'zone': 'west', 'type': 'Colonial Heritage Defense Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Defence Officers Sector', 'CMH Road Sector'],
        'avenues': ['Defence Colony Main Boulevard', '100ft Road Parkway', 'CMH Road Way', 'Officers Club Link', 'Metro Station Avenue'],
        'amenities': [
            {'id': 'club', 'name': 'Defence Colony Club', 'desc': 'Elite community officers club, tennis court and library', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🎖️'}
        ]
    },
    {
        'id': 'indiranagar_hal2', 'name': 'HAL 2nd Stage Indiranagar', 'location': '12th Main / Doopanahalli, Bangalore Central',
        'zone': 'west', 'type': 'Premier Cosmopolitan Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['12th Main Food Street', 'Doopanahalli Sector'],
        'avenues': ['12th Main Food Street Boulevard', '100ft Road Link', 'HAL 2nd Stage Parkway', 'Doopanahalli Way', 'Domlur Connector'],
        'amenities': [
            {'id': 'hub', 'name': '12th Main Boutique Food & Art Street', 'desc': 'World-famous restaurants, designer boutiques & coffee roasters', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'market', 'icon': '☕'}
        ]
    },
    {
        'id': 'brigade_gateway', 'name': 'Brigade Gateway', 'location': 'Dr. Rajkumar Road, Rajajinagar / Malleswaram, Bangalore West',
        'zone': 'west', 'type': 'Integrated Lifestyle City with Orion Mall & WTC', 'unitType': 'Apartment / Tower', 'unitPrefix': 'Tower', 'colorTheme': 'cyan',
        'sectors': ['Residential Towers A-L', 'World Trade Center', 'Orion Mall Complex'],
        'avenues': ['Gateway Boulevard', 'Orion Mall Parkway', 'WTC Ring Link', 'Lake Promenade Way', 'Dr. Rajkumar Highway'],
        'amenities': [
            {'id': 'mall', 'name': 'Orion Mall & Man-Made Gateway Lake', 'desc': 'Iconic lakeside shopping mall, PVR IMAX, lakeside open dining promenade', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'mall', 'icon': '🛍️'},
            {'id': 'club', 'name': 'The Gateway Galaxy Club', 'desc': '5-star resident clubhouse, Olympic pool, indoor badminton & spa', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },
    {
        'id': 'sadashivanagar', 'name': 'Sadashivanagar Royal Layout', 'location': 'Palace Orchards & Sankey Tank, Bangalore Central',
        'zone': 'west', 'type': 'Royal Heritage Neighborhood', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'cyan',
        'sectors': ['Sankey Tank Sector', 'Upper Palace Sector'],
        'avenues': ['Sankey Tank Boulevard', 'Palace Cross Road', '8th Main Avenue', 'Upper Palace Orchard', 'Mekhri Link'],
        'amenities': [
            {'id': 'lake', 'name': 'Sankey Tank Forest Promenade', 'desc': 'Historic heritage lake, boating and landscaped gardens', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'nature', 'icon': '⛵'}
        ]
    },
    {
        'id': 'malleswaram_18th', 'name': 'Malleswaram 18th Cross', 'location': 'Margosa & Sampige Road, Bangalore West',
        'zone': 'west', 'type': 'Historic Cultural Colony', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'cyan',
        'sectors': ['Margosa Sector', 'Sampige Sector'],
        'avenues': ['Margosa Road Boulevard', 'Sampige Avenue', '18th Cross Parkway', 'Vyalikaval Link', 'Temple Way'],
        'amenities': [
            {'id': 'temple', 'name': 'Kadu Malleshwara Temple', 'desc': '7th century Shiva temple giving Malleswaram its name', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'banashankari_3rd', 'name': 'Banashankari 3rd Stage', 'location': 'Katriguppe / BDA Layout, Bangalore South-West',
        'zone': 'west', 'type': 'Planned BDA Colony', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Katriguppe Sector', 'BDA Complex Sector'],
        'avenues': ['100ft Ring Road Boulevard', 'Katriguppe Main Avenue', '3rd Stage Way', 'BDA Complex Road', 'Banashankari Link'],
        'amenities': [
            {'id': 'complex', 'name': 'Banashankari BDA Complex', 'desc': 'Major commercial and government civic services hub', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🏛️'}
        ]
    },
    {
        'id': 'vijayanagar_bda', 'name': 'Vijayanagar BDA Layout', 'location': 'Chord Road / Pipeline, Bangalore West',
        'zone': 'west', 'type': 'Vibrant Commercial & Residential Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['Chord Road Sector', 'Club Sector'],
        'avenues': ['Chord Road Boulevard', 'Pipeline Avenue', '5th Main Way', 'Vijayanagar Club Road', 'Metro Link'],
        'amenities': [
            {'id': 'club', 'name': 'The Vijayanagar Club', 'desc': 'Badminton, swimming pool, gym & recreation', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'rajajinagar_1st', 'name': 'Rajajinagar 1st Block', 'location': 'Dr. Rajkumar Road / Subramanya Nagar, Bangalore West',
        'zone': 'west', 'type': 'Planned Urban Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'cyan',
        'sectors': ['ISKCON Temple Sector', 'Subramanya Nagar Sector'],
        'avenues': ['1st Block Main Boulevard', '10th Cross Avenue', 'Subramanya Nagar Way', 'Mahalakshmi Link', 'ISKCON Parkway'],
        'amenities': [
            {'id': 'temple', 'name': 'ISKCON Sri Krishna Balaram Temple', 'desc': 'Grand hilltop cultural and architectural temple complex', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'peenya_industrial', 'name': 'Peenya Industrial Township', 'location': 'Tumkur Road, Bangalore West',
        'zone': 'west', 'type': 'Manufacturing & Enterprise Township', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'cyan',
        'sectors': ['1st Stage Sector', '4th Cross Sector'],
        'avenues': ['Peenya Main Boulevard', '1st Stage Parkway', '4th Cross Way', 'Outer Ring Link', 'Tumkur Highway'],
        'amenities': [
            {'id': 'hub', 'name': 'Peenya Industries Association Hub', 'desc': 'Business auditorium, conference center and banking hub', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🏢'}
        ]
    }
]

# Assemble all layouts dictionary
all_layouts = {}
# Put the user requested flagship real communities first!
all_layouts['prestige_falcon_city'] = prestige_falcon_city
all_layouts['prestige_elysian'] = prestige_elysian
all_layouts['kristal_beryl'] = kristal_beryl
all_layouts['himagiri'] = himagiri_layout

for spec in specs:
    layout_obj = build_custom_layout(spec)
    all_layouts[layout_obj['id']] = layout_obj

print(f"Total Real Bangalore Layouts Built: {len(all_layouts)}")

# Export to layouts_data.js
js_content = f"window.LAYOUTS = {json.dumps(all_layouts, indent=2)};\n"
with open('himagiri-meadows/layouts_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"SUCCESS: layouts_data.js updated with {len(all_layouts)} real Bangalore layouts!")

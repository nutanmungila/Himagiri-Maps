import json
import math
import os

# 1. Himagiri Meadows (Master Layout)
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

# 2. Existing Greenwood Orchards
gw_nodes = {
    'gw_gate_main':    {'id': 'gw_gate_main', 'x': 80, 'y': 480, 'label': 'Grand Arch Main Gate (West)'},
    'gw_junc_entry':   {'id': 'gw_junc_entry', 'x': 160, 'y': 480, 'label': 'Entrance Boulevard'},
    'gw_junc_pine':    {'id': 'gw_junc_pine', 'x': 280, 'y': 480, 'label': 'Pine Court Junction'},
    'gw_junc_center':  {'id': 'gw_junc_center', 'x': 580, 'y': 480, 'label': 'Central Plaza Roundabout'},
    'gw_junc_palm':    {'id': 'gw_junc_palm', 'x': 880, 'y': 480, 'label': 'Palm Drive Junction'},
    'gw_gate_east':    {'id': 'gw_gate_east', 'x': 1100, 'y': 480, 'label': 'East Forest Gate'},
    'gw_mag_w':        {'id': 'gw_mag_w', 'x': 280, 'y': 260, 'label': 'Magnolia West'},
    'gw_mag_m':        {'id': 'gw_mag_m', 'x': 580, 'y': 260, 'label': 'Magnolia Club Roundabout'},
    'gw_mag_e':        {'id': 'gw_mag_e', 'x': 880, 'y': 260, 'label': 'Magnolia East'},
    'gw_ced_w':        {'id': 'gw_ced_w', 'x': 280, 'y': 700, 'label': 'Cedar West'},
    'gw_ced_m':        {'id': 'gw_ced_m', 'x': 580, 'y': 700, 'label': 'Cedar Lake Roundabout'},
    'gw_ced_e':        {'id': 'gw_ced_e', 'x': 880, 'y': 700, 'label': 'Cedar East'},
    'gw_pine_n_mid':   {'id': 'gw_pine_n_mid', 'x': 280, 'y': 370, 'label': 'Pine North Mid'},
    'gw_pine_s_mid':   {'id': 'gw_pine_s_mid', 'x': 280, 'y': 590, 'label': 'Pine South Mid'},
    'gw_palm_n_mid':   {'id': 'gw_palm_n_mid', 'x': 880, 'y': 370, 'label': 'Palm North Mid'},
    'gw_palm_s_mid':   {'id': 'gw_palm_s_mid', 'x': 880, 'y': 590, 'label': 'Palm South Mid'},
    'gw_club_n':       {'id': 'gw_club_n', 'x': 580, 'y': 370, 'label': 'Clubhouse Promenade'},
    'gw_lake_s':       {'id': 'gw_lake_s', 'x': 580, 'y': 590, 'label': 'Lakeside Boardwalk'}
}
gw_edges_raw = [
    ('gw_gate_main', 'gw_junc_entry', 'Orchard Boulevard', 'primary'),
    ('gw_junc_entry', 'gw_junc_pine', 'Orchard Boulevard', 'primary'),
    ('gw_junc_pine', 'gw_junc_center', 'Orchard Boulevard', 'primary'),
    ('gw_junc_center', 'gw_junc_palm', 'Orchard Boulevard', 'primary'),
    ('gw_junc_palm', 'gw_gate_east', 'Orchard Boulevard', 'primary'),
    ('gw_mag_w', 'gw_mag_m', 'Magnolia Avenue', 'secondary'),
    ('gw_mag_m', 'gw_mag_e', 'Magnolia Avenue', 'secondary'),
    ('gw_ced_w', 'gw_ced_m', 'Cedar Way', 'secondary'),
    ('gw_ced_m', 'gw_ced_e', 'Cedar Way', 'secondary'),
    ('gw_mag_w', 'gw_pine_n_mid', 'Pine Court', 'secondary'),
    ('gw_pine_n_mid', 'gw_junc_pine', 'Pine Court', 'secondary'),
    ('gw_junc_pine', 'gw_pine_s_mid', 'Pine Court', 'secondary'),
    ('gw_pine_s_mid', 'gw_ced_w', 'Pine Court', 'secondary'),
    ('gw_mag_m', 'gw_club_n', 'Central Promenade', 'primary'),
    ('gw_club_n', 'gw_junc_center', 'Central Promenade', 'primary'),
    ('gw_junc_center', 'gw_lake_s', 'Lakeside Link', 'primary'),
    ('gw_lake_s', 'gw_ced_m', 'Lakeside Link', 'primary'),
    ('gw_mag_e', 'gw_palm_n_mid', 'Palm Drive', 'secondary'),
    ('gw_palm_n_mid', 'gw_junc_palm', 'Palm Drive', 'secondary'),
    ('gw_junc_palm', 'gw_palm_s_mid', 'Palm Drive', 'secondary'),
    ('gw_palm_s_mid', 'gw_ced_e', 'Palm Drive', 'secondary'),
]
gw_edges = [{'u': u, 'v': v, 'road': r, 'type': t} for u, v, r, t in gw_edges_raw]

gw_plots = {}
def add_gw_villa(vid, vnum, road, block, facing, x, y, roadNode, color="green"):
    gw_plots[str(vid)] = {
        'id': str(vid),
        'number': f"Villa {vnum}",
        'road': road,
        'block': block,
        'facing': facing,
        'x': x,
        'y': y,
        'w': 48,
        'h': 30,
        'roadNode': roadNode,
        'color': color
    }
for i in range(5):
    add_gw_villa(i + 1, i + 1, "Pine Court", "Pine North Block", "East", 216, 275 + i * 38, "gw_pine_n_mid", "green")
for i in range(5):
    add_gw_villa(i + 6, i + 6, "Pine Court", "Pine South Block", "East", 216, 505 + i * 38, "gw_pine_s_mid", "green")
for i in range(10):
    add_gw_villa(i + 11, i + 11, "Magnolia Avenue", "Magnolia Central Block", "South", 330 + i * 52, 205, "gw_mag_m" if i in [4, 5] else ("gw_mag_w" if i < 4 else "gw_mag_e"), "green")
for i in range(10):
    add_gw_villa(i + 21, i + 21, "Magnolia Avenue", "Magnolia South Block", "North", 330 + i * 52, 305, "gw_mag_m" if i in [4, 5] else ("gw_mag_w" if i < 4 else "gw_mag_e"), "yellow")
for i in range(5):
    add_gw_villa(i + 31, i + 31, "Palm Drive", "Palm North Block", "West", 896, 275 + i * 38, "gw_palm_n_mid", "green")
for i in range(5):
    add_gw_villa(i + 36, i + 36, "Palm Drive", "Palm South Block", "West", 896, 505 + i * 38, "gw_palm_s_mid", "green")
for i in range(10):
    add_gw_villa(i + 41, i + 41, "Cedar Way", "Cedar North Block", "South", 330 + i * 52, 645, "gw_ced_m" if i in [4, 5] else ("gw_ced_w" if i < 4 else "gw_ced_e"), "yellow")
for i in range(10):
    add_gw_villa(i + 51, i + 51, "Cedar Way", "Cedar Lakeview Block", "North", 330 + i * 52, 745, "gw_ced_m" if i in [4, 5] else ("gw_ced_w" if i < 4 else "gw_ced_e"), "green")

gw_amenities = [
    {'id': 'gw_gate_main', 'name': 'Grand Arch Main Gate (West)', 'description': 'Main security gate, visitor registration & RFID barrier', 'x': 80, 'y': 480, 'roadNode': 'gw_gate_main', 'icon': '🚪', 'type': 'gate'},
    {'id': 'gw_clubhouse', 'name': 'Grand Country Club & Spa', 'description': '25,000 sq ft luxury clubhouse with indoor badminton & sauna', 'x': 580, 'y': 220, 'roadNode': 'gw_mag_m', 'icon': '🏊', 'type': 'sports'},
    {'id': 'gw_pool', 'name': 'Infinity Swimming Pool', 'description': 'Temperature-controlled lap pool & kids splash deck', 'x': 650, 'y': 220, 'roadNode': 'gw_mag_m', 'icon': '🏊', 'type': 'sports'},
    {'id': 'gw_tennis', 'name': 'Championship Tennis Court', 'description': 'Dual synthetic floodlit tennis courts with coach pavilion', 'x': 320, 'y': 430, 'roadNode': 'gw_junc_pine', 'icon': '🎾', 'type': 'sports'},
    {'id': 'gw_lake_park', 'name': 'Lakeside Park & Promenade', 'description': '4-acre scenic natural lake, walking boardwalk & duck pond', 'x': 580, 'y': 740, 'roadNode': 'gw_ced_m', 'icon': '🌊', 'type': 'recreation'},
    {'id': 'gw_jogging', 'name': 'Tree-Lined Jogging Track', 'description': '1.8 km cushioned rubberized track through fruit orchards', 'x': 840, 'y': 430, 'roadNode': 'gw_junc_palm', 'icon': '🏃', 'type': 'recreation'},
    {'id': 'gw_children', 'name': 'Adventure Playground', 'description': 'Kids wooden fortress, sandpit, and rope climbing web', 'x': 450, 'y': 440, 'roadNode': 'gw_junc_center', 'icon': '🛝', 'type': 'recreation'},
    {'id': 'gw_gate_east', 'name': 'East Forest Gate (Gate 2)', 'description': 'Access gate toward Carmelaram railway station & green belt', 'x': 1100, 'y': 480, 'roadNode': 'gw_gate_east', 'icon': '🚪', 'type': 'gate'},
]

greenwood_layout = {
    'id': 'greenwood',
    'name': 'Greenwood Orchards',
    'location': 'Sarjapur Road / Carmelaram, Bangalore East',
    'zone': 'east',
    'type': 'Luxury Gated Villa Township',
    'unitType': 'Villa',
    'unitCount': len(gw_plots),
    'bounds': {'minX': 40, 'maxX': 1180, 'minY': 160, 'maxY': 840},
    'center': {'x': 600, 'y': 480},
    'groundPolygon': "60,480 140,240 300,160 880,160 1080,240 1140,480 1080,720 880,820 300,820 140,720 Z",
    'borderTreesPath': "M 60,480 L 140,240 L 300,160 L 880,160 L 1080,240 L 1140,480 L 1080,720 L 880,820 L 300,820 L 140,720 Z",
    'gardenPark': {'x': 460, 'y': 455, 'w': 240, 'h': 50, 'rx': 8, 'label': "Orchard Central Park"},
    'roads': {'nodes': gw_nodes, 'edges': gw_edges},
    'plots': gw_plots,
    'amenities': gw_amenities,
    'roadLabels': [
        {'name': "ORCHARD BOULEVARD", 'x': 420, 'y': 480, 'vertical': False},
        {'name': "MAGNOLIA AVENUE", 'x': 420, 'y': 260, 'vertical': False},
        {'name': "CEDAR WAY", 'x': 420, 'y': 700, 'vertical': False},
        {'name': "PINE COURT", 'x': 280, 'y': 370, 'vertical': True},
        {'name': "PALM DRIVE", 'x': 880, 'y': 370, 'vertical': True}
    ],
    'defaultStartGate': 'gw_gate_main',
    'sectors': ['Orchard Boulevard', 'Magnolia Avenue', 'Pine Court', 'Palm Drive', 'Cedar Way']
}

# 3. Existing Tech Horizon Campus
th_nodes = {
    'th_gate_main':      {'id': 'th_gate_main', 'x': 580, 'y': 820, 'label': 'Main Gate 1 (South Entrance)'},
    'th_south_link':     {'id': 'th_south_link', 'x': 580, 'y': 680, 'label': 'South Boulevard Cross'},
    'th_center_plaza':   {'id': 'th_center_plaza', 'x': 580, 'y': 480, 'label': 'Innovation Central Plaza'},
    'th_north_link':     {'id': 'th_north_link', 'x': 580, 'y': 280, 'label': 'North Boulevard Cross'},
    'th_gate_north':     {'id': 'th_gate_north', 'x': 580, 'y': 150, 'label': 'Cargo & Shuttle Gate 2 (North)'},
    'th_west_s':         {'id': 'th_west_s', 'x': 260, 'y': 680, 'label': 'Silicon Avenue South'},
    'th_west_mid_link':  {'id': 'th_west_mid_link', 'x': 260, 'y': 480, 'label': 'Silicon Avenue Central'},
    'th_west_n':         {'id': 'th_west_n', 'x': 260, 'y': 280, 'label': 'Silicon Avenue North'},
    'th_east_s':         {'id': 'th_east_s', 'x': 900, 'y': 680, 'label': 'Cyber Boulevard South'},
    'th_east_mid_link':  {'id': 'th_east_mid_link', 'x': 900, 'y': 480, 'label': 'Cyber Boulevard Central'},
    'th_east_n':         {'id': 'th_east_n', 'x': 900, 'y': 280, 'label': 'Cyber Boulevard North'},
    'th_west_m':         {'id': 'th_west_m', 'x': 260, 'y': 380, 'label': 'Towers A & B Hub'},
    'th_east_m':         {'id': 'th_east_m', 'x': 900, 'y': 380, 'label': 'Towers C & D Hub'},
}
th_edges_raw = [
    ('th_gate_main', 'th_south_link', 'Innovation Boulevard', 'primary'),
    ('th_south_link', 'th_center_plaza', 'Innovation Boulevard', 'primary'),
    ('th_center_plaza', 'th_north_link', 'Innovation Boulevard', 'primary'),
    ('th_north_link', 'th_gate_north', 'Innovation Boulevard', 'primary'),
    ('th_west_n', 'th_north_link', 'Quantum Way', 'secondary'),
    ('th_north_link', 'th_east_n', 'Quantum Way', 'secondary'),
    ('th_west_mid_link', 'th_center_plaza', 'Alpha Link', 'primary'),
    ('th_center_plaza', 'th_east_mid_link', 'Alpha Link', 'primary'),
    ('th_west_s', 'th_south_link', 'Beta Link', 'secondary'),
    ('th_south_link', 'th_east_s', 'Beta Link', 'secondary'),
    ('th_west_n', 'th_west_m', 'Silicon Avenue', 'secondary'),
    ('th_west_m', 'th_west_mid_link', 'Silicon Avenue', 'secondary'),
    ('th_west_mid_link', 'th_west_s', 'Silicon Avenue', 'secondary'),
    ('th_east_n', 'th_east_m', 'Cyber Boulevard', 'secondary'),
    ('th_east_m', 'th_east_mid_link', 'Cyber Boulevard', 'secondary'),
    ('th_east_mid_link', 'th_east_s', 'Cyber Boulevard', 'secondary')
]
th_edges = [{'u': u, 'v': v, 'road': r, 'type': t} for u, v, r, t in th_edges_raw]

th_plots = {}
def add_th_block(bid, bname, road, block, facing, x, y, w, h, roadNode, color="blue"):
    th_plots[str(bid)] = {
        'id': str(bid),
        'number': bname,
        'road': road,
        'block': block,
        'facing': facing,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'roadNode': roadNode,
        'color': color
    }
for i in range(4):
    add_th_block(f"T-A{i+1}", f"Tower A{i+1}", "Silicon Avenue", "Global Technology Center", "East", 185, 310 + i * 44, 60, 36, "th_west_m", "blue")
    add_th_block(f"T-B{i+1}", f"Tower B{i+1}", "Silicon Avenue", "Engineering Innovation Block", "West", 285, 310 + i * 44, 60, 36, "th_west_m", "green")
for i in range(6):
    add_th_block(f"10{i+1}", f"Block 10{i+1}", "Silicon Avenue", "Silicon West Labs", "East", 185, 510 + i * 36, 60, 30, "th_west_s", "yellow")
for i in range(4):
    add_th_block(f"T-C{i+1}", f"Tower C{i+1}", "Cyber Boulevard", "Cloud & AI Labs", "East", 825, 310 + i * 44, 60, 36, "th_east_m", "green")
    add_th_block(f"T-D{i+1}", f"Tower D{i+1}", "Cyber Boulevard", "Data Systems Hub", "West", 925, 310 + i * 44, 60, 36, "th_east_m", "yellow")
for i in range(6):
    add_th_block(f"30{i+1}", f"Block 30{i+1}", "Cyber Boulevard", "Cyber Enterprise Park", "East", 825, 510 + i * 36, 60, 30, "th_east_s", "yellow")

th_amenities = [
    {'id': 'th_gate_main', 'name': 'Main Security Gate 1 (South)', 'description': 'Visitor badge pass counter & automated vehicle barrier', 'x': 580, 'y': 820, 'roadNode': 'th_gate_main', 'icon': '🚪', 'type': 'gate'},
    {'id': 'th_food_court', 'name': 'Central Cafeteria & Food Plaza', 'description': '40,000 sq ft multi-cuisine food court, cafes & bakery', 'x': 580, 'y': 480, 'roadNode': 'th_center_plaza', 'icon': '🍽️', 'type': 'civic'},
    {'id': 'th_convention', 'name': 'Auditorium & Convention Hall', 'description': '800-seat amphitheater & executive briefing center', 'x': 420, 'y': 480, 'roadNode': 'th_west_mid_link', 'icon': '🏛️', 'type': 'civic'},
    {'id': 'th_mlcp', 'name': 'Multi-Level Car Parking (MLCP)', 'description': '6-level automated parking garage with 2,500 bays', 'x': 180, 'y': 680, 'roadNode': 'th_west_s', 'icon': '🅿️', 'type': 'utility'},
    {'id': 'th_ev_bay', 'name': 'Supercharger EV Charging Bay', 'description': 'Fast-charging stations for 30 electric cars and two-wheelers', 'x': 980, 'y': 680, 'roadNode': 'th_east_s', 'icon': '⚡', 'type': 'utility'},
    {'id': 'th_sports', 'name': 'Sports Arena & Gymnasium', 'description': 'Indoor badminton, basketball court, and state-of-the-art gym', 'x': 180, 'y': 280, 'roadNode': 'th_west_n', 'icon': '🏀', 'type': 'sports'},
    {'id': 'th_gate_north', 'name': 'Express Cargo Gate 2 (North)', 'description': 'Delivery logistics & employee shuttle bus bay', 'x': 580, 'y': 150, 'roadNode': 'th_gate_north', 'icon': '🚪', 'type': 'gate'}
]

tech_horizon_layout = {
    'id': 'tech_horizon',
    'name': 'Tech Horizon Campus',
    'location': 'Electronic City Phase 1, Bangalore',
    'zone': 'ecity',
    'type': 'Enterprise Tech Park',
    'unitType': 'Tower/Block',
    'unitCount': len(th_plots),
    'bounds': {'minX': 100, 'maxX': 1100, 'minY': 120, 'maxY': 860},
    'center': {'x': 580, 'y': 480},
    'groundPolygon': "580,120 980,180 1080,480 980,780 580,850 180,780 80,480 180,180 Z",
    'borderTreesPath': "M 580,120 L 980,180 L 1080,480 L 980,780 L 580,850 L 180,780 L 80,480 L 180,180 Z",
    'gardenPark': {'x': 420, 'y': 460, 'w': 320, 'h': 40, 'rx': 6, 'label': "Central Plaza Green"},
    'roads': {'nodes': th_nodes, 'edges': th_edges},
    'plots': th_plots,
    'amenities': th_amenities,
    'roadLabels': [
        {'name': "INNOVATION BOULEVARD", 'x': 580, 'y': 380, 'vertical': True},
        {'name': "SILICON AVENUE", 'x': 260, 'y': 380, 'vertical': True},
        {'name': "CYBER BOULEVARD", 'x': 900, 'y': 380, 'vertical': True},
        {'name': "QUANTUM WAY", 'x': 420, 'y': 280, 'vertical': False},
        {'name': "ALPHA LINK", 'x': 420, 'y': 480, 'vertical': False}
    ],
    'defaultStartGate': 'th_gate_main',
    'sectors': ['Innovation Boulevard', 'Silicon Avenue', 'Cyber Boulevard', 'Quantum Way', 'Alpha Link']
}

# Generic Layout Builder function
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
    color_theme = spec.get('colorTheme', 'green')
    unit_count = spec.get('unitCount', 44)

    bounds = {'minX': 60, 'maxX': 1180, 'minY': 160, 'maxY': 840}
    center = {'x': 600, 'y': 480}

    nodes = {
        f'{lid}_gate_1':     {'id': f'{lid}_gate_1', 'x': 90, 'y': 480, 'label': f'{name} Gate 1 (West Entrance)'},
        f'{lid}_entry':      {'id': f'{lid}_entry', 'x': 180, 'y': 480, 'label': 'Entrance Boulevard'},
        f'{lid}_junc_w':     {'id': f'{lid}_junc_w', 'x': 320, 'y': 480, 'label': f'{avenues[3]} West Junction'},
        f'{lid}_junc_ctr':   {'id': f'{lid}_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Plaza Roundabout'},
        f'{lid}_junc_e':     {'id': f'{lid}_junc_e', 'x': 920, 'y': 480, 'label': f'{avenues[4]} East Junction'},
        f'{lid}_gate_2':     {'id': f'{lid}_gate_2', 'x': 1110, 'y': 480, 'label': f'{name} Gate 2 (East Entrance)'},

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
            'id': pid, 'number': num_str, 'road': avenues[1], 'block': 'North Crest Sector',
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
            'id': pid, 'number': num_str, 'road': avenues[1], 'block': 'Central Greens Sector',
            'facing': 'North', 'x': 360 + i * 65, 'y': 310, 'w': 50, 'h': 36,
            'roadNode': f'{lid}_n_mid' if i in [3, 4] else (f'{lid}_n_w' if i < 3 else f'{lid}_n_e'),
            'color': 'yellow' if color_theme != 'yellow' else 'green'
        }
        uid += 1

    # 6 West cross
    for i in range(6):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[3], 'block': 'West Avenue Enclave',
            'facing': 'East', 'x': 245, 'y': 290 + i * 65, 'w': 52, 'h': 38,
            'roadNode': f'{lid}_w_n_mid' if i < 3 else f'{lid}_w_s_mid',
            'color': color_theme
        }
        uid += 1

    # 6 East cross
    for i in range(6):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[4], 'block': 'East Avenue Enclave',
            'facing': 'West', 'x': 945, 'y': 290 + i * 65, 'w': 52, 'h': 38,
            'roadNode': f'{lid}_e_n_mid' if i < 3 else f'{lid}_e_s_mid',
            'color': color_theme
        }
        uid += 1

    # 8 Mid-South row
    for i in range(8):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[2], 'block': 'Lake Promenade Block',
            'facing': 'South', 'x': 360 + i * 65, 'y': 535, 'w': 50, 'h': 36,
            'roadNode': f'{lid}_s_mid' if i in [3, 4] else (f'{lid}_s_w' if i < 3 else f'{lid}_s_e'),
            'color': 'yellow' if color_theme != 'yellow' else 'green'
        }
        uid += 1

    # 8 South row
    for i in range(8):
        pid = str(uid)
        num_str = f"{unitPrefix} {uid}" if unitPrefix != 'House' else f"{uid}"
        plots[pid] = {
            'id': pid, 'number': num_str, 'road': avenues[2], 'block': 'South Parkland Sector',
            'facing': 'North', 'x': 360 + i * 65, 'y': 735, 'w': 50, 'h': 36,
            'roadNode': f'{lid}_s_mid' if i in [3, 4] else (f'{lid}_s_w' if i < 3 else f'{lid}_s_e'),
            'color': color_theme
        }
        uid += 1

    amenities = [
        {'id': f'{lid}_gate_1', 'name': f'{name} Gate 1 (Main Entrance)', 'description': 'Security verification post & RFID barrier', 'x': 90, 'y': 480, 'roadNode': f'{lid}_gate_1', 'type': 'gate', 'icon': '🚪'},
        {'id': f'{lid}_gate_2', 'name': f'{name} Gate 2 (East Entrance)', 'description': 'Express resident entry & visitor parking', 'x': 1110, 'y': 480, 'roadNode': f'{lid}_gate_2', 'type': 'gate', 'icon': '🚪'}
    ]

    for am in amenities_info:
        amenities.append({
            'id': f"{lid}_{am['id']}",
            'name': am['name'],
            'description': am.get('desc', 'Society landmark'),
            'x': am.get('x', 620),
            'y': am.get('y', 480),
            'roadNode': f"{lid}_{am.get('node', 'junc_ctr')}",
            'type': am.get('type', 'recreation'),
            'icon': am.get('icon', '★')
        })

    roadLabels = [
        {'name': avenues[0].upper(), 'x': 500, 'y': 480, 'vertical': False},
        {'name': avenues[1].upper(), 'x': 500, 'y': 270, 'vertical': False},
        {'name': avenues[2].upper(), 'x': 500, 'y': 690, 'vertical': False},
        {'name': avenues[3].upper(), 'x': 320, 'y': 400, 'vertical': True},
        {'name': avenues[4].upper(), 'x': 920, 'y': 400, 'vertical': True}
    ]

    # Verify Dijkstra
    graph = {nid: [] for nid in nodes}
    for e in edges:
        graph[e['u']].append(e['v'])
        graph[e['v']].append(e['u'])

    visited = set()
    queue = [f'{lid}_gate_1']
    visited.add(f'{lid}_gate_1')
    while queue:
        curr = queue.pop(0)
        for nxt in graph[curr]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)

    unreachable = set(nodes.keys()) - visited
    if unreachable:
        raise ValueError(f"Unreachable in {lid}: {unreachable}")

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
        'groundPolygon': "70,480 180,210 400,160 850,160 1080,210 1140,480 1080,750 850,810 400,810 180,750 Z",
        'borderTreesPath': "M 70,480 L 180,210 L 400,160 L 850,160 L 1080,210 L 1140,480 L 1080,750 L 850,810 L 400,810 L 180,750 Z",
        'gardenPark': {'x': 480, 'y': 455, 'w': 280, 'h': 50, 'rx': 8, 'label': f"{name} Central Garden"},
        'roads': {'nodes': nodes, 'edges': edges},
        'plots': plots,
        'amenities': amenities,
        'roadLabels': roadLabels,
        'defaultStartGate': f'{lid}_gate_1',
        'sectors': avenues
    }

# 47 New Layout Specs across all Bangalore Zones
specs = [
    # --- EAST BANGALORE & WHITEFIELD ---
    {
        'id': 'palm_meadows', 'name': 'Palm Meadows', 'location': 'Varthur Main Road, Whitefield, Bangalore East',
        'zone': 'whitefield', 'type': 'Ultra-Luxury Gated Villa Township', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Palm Drive Boulevard', 'Windmill Avenue', 'Lakeview Crescent', 'Orchard Way', 'Boulevard Road'],
        'amenities': [
            {'id': 'club', 'name': 'The Club at Palm Meadows', 'desc': 'Olympic pool, squash, multi-cuisine dining & spa', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'lake', 'name': 'Windmill Lake Promenade', 'desc': 'Natural fresh water lake with shaded walking deck', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'}
        ]
    },
    {
        'id': 'prestige_lakeside', 'name': 'Prestige Lakeside Habitat', 'location': 'Varthur Lake, Whitefield East',
        'zone': 'whitefield', 'type': 'Integrated Township & Villa Enclave', 'unitType': 'Tower/Villa', 'unitPrefix': 'Unit', 'colorTheme': 'blue',
        'avenues': ['Disney Boulevard', 'Lakeside Parkway', 'Castle Avenue', 'Boardwalk Way', 'Promenade Drive'],
        'amenities': [
            {'id': 'club', 'name': 'Lake Habitat Grand Club', 'desc': '4 massive clubhouses, 4 swimming pools, skating rink', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'promenade', 'name': 'Varthur Lake Viewpoint', 'desc': 'Panoramic lakeside viewing promenade & gazebo', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'}
        ]
    },
    {
        'id': 'rainbow_drive', 'name': 'Rainbow Drive Layout', 'location': 'Sarjapur Road / Doddakannelli, Bangalore East',
        'zone': 'east', 'type': 'Gated Villa & Tree-Lined Community', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Rainbow Boulevard', 'Gulmohar Avenue', 'Jacaranda Way', 'Silver Oak Lane', 'Cassia Drive'],
        'amenities': [
            {'id': 'park', 'name': 'Rainbow Central Garden & Lake', 'desc': 'Rainwater harvesting lake & lush bird habitat', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'recreation', 'icon': '🌳'},
            {'id': 'sports', 'name': 'Community Tennis & Badminton', 'desc': 'Floodlit tennis court & community hall', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🎾'}
        ]
    },
    {
        'id': 'divyasree_republic', 'name': 'Republic of Whitefield', 'location': 'EPIP Zone, Whitefield, Bangalore East',
        'zone': 'whitefield', 'type': 'Modern Urban Township', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'yellow',
        'avenues': ['Innovation Boulevard', 'Cyber Parkway', 'Technopolis Way', 'Vanguard Avenue', 'Metro Link'],
        'amenities': [
            {'id': 'hub', 'name': 'Republic Central Plaza', 'desc': 'Amphitheater, shopping arcade & cafe promenade', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🏛️'},
            {'id': 'sports', 'name': 'Olympic Sports Complex', 'desc': 'Full-size football turf, swimming pool & gym', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '⚽'}
        ]
    },
    {
        'id': 'prestige_shantiniketan', 'name': 'Prestige Shantiniketan', 'location': 'ITPL Main Road, Whitefield, Bangalore East',
        'zone': 'whitefield', 'type': 'Integrated Megacity Township', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'purple',
        'avenues': ['Shantiniketan Boulevard', 'Crescent Walk', 'Forum Parkway', 'Tower Way', 'Harmony Drive'],
        'amenities': [
            {'id': 'mall', 'name': 'Forum Shantiniketan Link', 'desc': 'Direct pedestrian walkway to shopping & IMAX', 'x': 920, 'y': 480, 'node': 'junc_e', 'type': 'civic', 'icon': '🛍️'},
            {'id': 'club', 'name': 'The Crescent Club', 'desc': 'Infinity pool, bowling alley, gym & banquet halls', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'confident_anthea', 'name': 'Confident Anthea', 'location': 'Sarjapur Town / Bilapura, Bangalore East',
        'zone': 'east', 'type': 'Gated Luxury Villa Community', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Anthea Boulevard', 'Orchid Way', 'Jasmine Crescent', 'Tulip Avenue', 'Rose Court'],
        'amenities': [
            {'id': 'club', 'name': 'Anthea Country Club', 'desc': 'Tennis court, swimming pool & fitness pavilion', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'park', 'name': 'Botanical Fragrance Park', 'desc': 'Landscaped floral gardens and children play area', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌺'}
        ]
    },
    {
        'id': 'chaithanya_smaran', 'name': 'Chaithanya Smaran', 'location': 'Budigere Cross, Whitefield North, Bangalore',
        'zone': 'whitefield', 'type': 'Bespoke Luxury Villa Enclave', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Smaran Boulevard', 'Zen Parkway', 'Lotus Court', 'Bamboo Grove', 'Banyan Avenue'],
        'amenities': [
            {'id': 'zen', 'name': 'Zen Water Pavilion & Club', 'desc': 'Reflecting lily ponds, spa, and meditation gazebo', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'recreation', 'icon': '🧘'},
            {'id': 'temple', 'name': 'Heritage Meditation Shrine', 'desc': 'Serene open-air sanctuary', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'whitefield_inner_circle', 'name': 'Whitefield Inner Circle', 'location': 'Whitefield Heritage Colony, Bangalore East',
        'zone': 'whitefield', 'type': 'Colonial Heritage Colony', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'yellow',
        'avenues': ['Inner Circle Road', 'Waverly Way', 'Memorial Avenue', 'Colonial Drive', 'Church Walk'],
        'amenities': [
            {'id': 'club', 'name': 'The Historic Whitefield Club', 'desc': 'Colonial heritage sports and social club founded 1905', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'civic', 'icon': '🏛️'},
            {'id': 'church', 'name': 'CSI Memorial Church Garden', 'desc': 'Victorian stone church and community garden', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'worship', 'icon': '⛪'}
        ]
    },
    {
        'id': 'sowparnika_columns', 'name': 'Sowparnika The Columns', 'location': 'Whitefield East / Hope Farm, Bangalore',
        'zone': 'whitefield', 'type': 'Modern Residential Community', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'yellow',
        'avenues': ['Columns Boulevard', 'Royal Palm Avenue', 'Harmony Way', 'Symphony Lane', 'Metro Link'],
        'amenities': [
            {'id': 'club', 'name': 'Columns Central Club', 'desc': 'Rooftop infinity pool and health club', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'doddakannelli_greens', 'name': 'Greenwood Regency', 'location': 'Doddakannelli, Sarjapur Link, Bangalore East',
        'zone': 'east', 'type': 'Private Gated Community', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Regency Boulevard', 'Maple Way', 'Cedar Court', 'Willow Crescent', 'Pine Drive'],
        'amenities': [
            {'id': 'sports', 'name': 'Regency Sports Pavilion', 'desc': 'Squash court, gym, and table tennis', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏸'},
            {'id': 'park', 'name': 'Regency Children Park', 'desc': 'Lush lawn and play fortress', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🛝'}
        ]
    },
    {
        'id': 'marathahalli_sgr', 'name': 'SGR Dental College Layout', 'location': 'Munnekollal, Marathahalli, Bangalore East',
        'zone': 'east', 'type': 'Residential Colony', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['SGR Main Boulevard', 'Lakeview 1st Cross', 'Park Road', 'Temple Link', 'Avenue 2'],
        'amenities': [
            {'id': 'lake', 'name': 'Munnekollal Lake Promenade', 'desc': 'Restored freshwater lake and jogging track', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'}
        ]
    },

    # --- SOUTH BANGALORE ---
    {
        'id': 'brigade_meadows', 'name': 'Brigade Meadows', 'location': 'Kanakapura Road / Saalu Hunase, Bangalore South',
        'zone': 'south', 'type': 'Integrated Green Township', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'green',
        'avenues': ['Meadow Boulevard', 'Plumeria Way', 'Wisteria Avenue', 'Rosewood Drive', 'Arcade Parkway'],
        'amenities': [
            {'id': 'club', 'name': 'Meadows Clubhouse & Pool', 'desc': 'Full gymnasium, indoor badminton & pool', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'arcade', 'name': 'The Arcade Shopping Center', 'desc': 'Supermarket, medical clinic, cafes & retail', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🛍️'}
        ]
    },
    {
        'id': 'mantri_tranquil', 'name': 'Mantri Tranquil', 'location': 'Gubbalala, Kanakapura Road, Bangalore South',
        'zone': 'south', 'type': 'Hilltop Gated Community', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'blue',
        'avenues': ['Tranquil Boulevard', 'Hilltop Avenue', 'Pine Valley Drive', 'Breeze Way', 'Temple Road'],
        'amenities': [
            {'id': 'club', 'name': 'Tranquil Grand Club', 'desc': 'Heated indoor swimming pool, amphitheater & gym', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'temple', 'name': 'Sri Anjaneya Swamy Temple', 'desc': 'Hilltop community temple and prayer hall', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'concorde_napa_valley', 'name': 'Concorde Napa Valley', 'location': 'Kaggalipura, Kanakapura Road, Bangalore South',
        'zone': 'south', 'type': 'Vineyard-Themed Luxury Villa Estate', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Napa Boulevard', 'Sonoma Drive', 'Cabernet Court', 'Merlot Way', 'Vineyard Link'],
        'amenities': [
            {'id': 'club', 'name': 'The Napa Grand Resort Club', 'desc': 'Wine tasting lounge, infinity pool, tennis & spa', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'lake', 'name': 'Private Lake & Boating Deck', 'desc': 'Scenic lake with wooden dock and waterfront trail', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '⛵'}
        ]
    },
    {
        'id': 'jp_nagar_phase7', 'name': 'JP Nagar 7th Phase', 'location': 'Brigade Millennium Enclave, Bangalore South',
        'zone': 'south', 'type': 'Prime Residential Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['Millennium Boulevard', 'Cassia Avenue', 'Woodrose Link', 'Puttenahalli Way', 'Elita Avenue'],
        'amenities': [
            {'id': 'club', 'name': 'The Woodrose Club', 'desc': 'Renowned sporting & dining club with pool and squash', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'lake', 'name': 'Puttenahalli Bird Sanctuary Lake', 'desc': 'Beautiful natural urban bird watching reserve', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🦆'}
        ]
    },
    {
        'id': 'jp_nagar_phase2', 'name': 'JP Nagar 2nd Phase', 'location': 'Aurobindo Marg / Mini Forest, Bangalore South',
        'zone': 'south', 'type': 'Heritage Tree-Lined Layout', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'green',
        'avenues': ['Aurobindo Boulevard', 'Mini Forest Avenue', '14th Main Road', '6th Cross Way', 'Ring Road Link'],
        'amenities': [
            {'id': 'forest', 'name': 'JP Nagar Mini Forest Park', 'desc': '32-acre dense urban forest, walking trails & butterfly park', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'recreation', 'icon': '🌳'},
            {'id': 'temple', 'name': 'Sri Rama Temple', 'desc': 'Prominent cultural landmark and prayer sanctum', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'btm_2nd_stage', 'name': 'BTM Layout 2nd Stage', 'location': 'Mico Layout / 7th Main, Bangalore South',
        'zone': 'south', 'type': 'Urban High-Density Colony', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['7th Main Boulevard', '16th Cross Avenue', 'Mico Layout Road', 'Tavarekere Parkway', 'Ring Road Access'],
        'amenities': [
            {'id': 'lake', 'name': 'BTM Lake Park & Boating', 'desc': 'Recreational lake with jogging track & outdoor gym', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'},
            {'id': 'park', 'name': 'BTM Children Play Park', 'desc': 'Community park with basketball court and seating', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'recreation', 'icon': '🏀'}
        ]
    },
    {
        'id': 'jayanagar_4th', 'name': 'Jayanagar 4th Block', 'location': '10th Main & Ashoka Pillar, Bangalore South',
        'zone': 'south', 'type': 'Heritage Planned Garden City Layout', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'green',
        'avenues': ['10th Main Boulevard', 'Ashoka Pillar Avenue', '32nd Cross Way', 'Nanda Theatre Road', 'Shopping Complex Link'],
        'amenities': [
            {'id': 'park', 'name': 'Madhavan Park & Playground', 'desc': 'Historic multi-acre sports ground and garden', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'recreation', 'icon': '🌳'},
            {'id': 'complex', 'name': 'Jayanagar BDA Shopping Complex', 'desc': 'Iconic 4th block commercial shopping plaza', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'civic', 'icon': '🛍️'}
        ]
    },
    {
        'id': 'jayanagar_9th', 'name': 'Jayanagar 9th Block', 'location': 'Ragigudda & East End, Bangalore South',
        'zone': 'south', 'type': 'Quiet Residential Colony', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['East End Boulevard', 'Ragigudda Avenue', '39th Cross', '18th Main Way', 'Marenahalli Link'],
        'amenities': [
            {'id': 'temple', 'name': 'Sri Prasanna Veeranjaneya Temple', 'desc': 'Famous Ragigudda hilltop temple and fairground', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'purva_panorama', 'name': 'Purva Panorama', 'location': 'Kalena Agrahara, Bannerghatta Road, Bangalore South',
        'zone': 'south', 'type': 'Hilltop Luxury Enclave', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'purple',
        'avenues': ['Panorama Boulevard', 'Hillview Crescent', 'Summit Drive', 'Breeze Avenue', 'Green Link'],
        'amenities': [
            {'id': 'club', 'name': 'Panorama Clubhouse & Deck', 'desc': 'Infinity pool overlooking Meenakshi temple hills', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'meenakshi_layout', 'name': 'Meenakshi Layout', 'location': 'Hulimavu, Bannerghatta Road, Bangalore South',
        'zone': 'south', 'type': 'Residential Lakeview Community', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['Meenakshi Temple Boulevard', 'Hulimavu Lake Road', '4th Cross Way', 'Royal Avenue', 'Temple Crescent'],
        'amenities': [
            {'id': 'temple', 'name': 'Meenakshi Sundareswarar Temple', 'desc': 'Grand Dravidian temple and cultural hall', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'},
            {'id': 'lake', 'name': 'Hulimavu Lake Boardwalk', 'desc': 'Freshwater walking and fitness trail', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'}
        ]
    },
    {
        'id': 'south_city_layout', 'name': 'South City Enclave', 'location': 'Arekere Mico Layout, Bannerghatta Road, Bangalore',
        'zone': 'south', 'type': 'Master-Planned Gated Township', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'green',
        'avenues': ['South City Boulevard', 'Pine Crest Way', 'Central Garden Avenue', 'Sports Link', 'Valley Drive'],
        'amenities': [
            {'id': 'club', 'name': 'South City Club', 'desc': 'Multi-court tennis, Olympic pool & restaurant', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },

    # --- SOUTH-EAST & ELECTRONIC CITY / BELLANDUR ---
    {
        'id': 'adarsh_palm_retreat', 'name': 'Adarsh Palm Retreat', 'location': 'Outer Ring Road, Bellandur, Bangalore',
        'zone': 'ecity', 'type': 'Red-Brick Victorian Villa Township', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Retreat Boulevard', 'Red Wood Drive', 'Silver Oak Way', 'Palm Court', 'Lakeside Parkway'],
        'amenities': [
            {'id': 'club', 'name': 'The Palm Retreat Clubhouse', 'desc': '45,000 sq ft luxury club, squash, pool & restaurants', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'lake', 'name': 'Retreat Lake & Waterfall', 'desc': 'Private landscaped water body and jogging loop', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'}
        ]
    },
    {
        'id': 'hsr_sector_1', 'name': 'HSR Layout Sector 1', 'location': 'Agara Lake Enclave, Bangalore South-East',
        'zone': 'ecity', 'type': 'Modern BDA Residential Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['27th Main Boulevard', 'Agara Lake Parkway', '14th Cross Avenue', 'Green Avenue', 'ORR Link'],
        'amenities': [
            {'id': 'lake', 'name': 'Agara Lake Nature Park', 'desc': '140-acre wetland park, boardwalk, and bird tower', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🦆'},
            {'id': 'park', 'name': 'Sector 1 BDA Park', 'desc': 'Multi-sport park with synthetic jogging track', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'recreation', 'icon': '🏃'}
        ]
    },
    {
        'id': 'hsr_sector_2', 'name': 'HSR Layout Sector 2', 'location': '24th Main & Parangi Palya, HSR Layout',
        'zone': 'ecity', 'type': 'Prime Residential Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['24th Main Boulevard', '19th Main Avenue', '5th Cross Road', 'Central Parkway', 'Metro Way'],
        'amenities': [
            {'id': 'park', 'name': 'Sector 2 Central BDA Park', 'desc': 'Children play fortress, yoga deck and lawn', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'recreation', 'icon': '🌳'}
        ]
    },
    {
        'id': 'hsr_sector_3', 'name': 'HSR Layout Sector 3', 'location': 'Teachers Colony & 17th Cross, HSR Layout',
        'zone': 'ecity', 'type': 'Quiet Residential Colony', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['17th Cross Boulevard', 'Teachers Colony Avenue', '9th Main Road', 'Sector 3 Link', 'Parkview Way'],
        'amenities': [
            {'id': 'park', 'name': 'Sector 3 Children Play Garden', 'desc': 'Shaded trees, badminton court & library', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'recreation', 'icon': '🛝'}
        ]
    },
    {
        'id': 'green_glen', 'name': 'Green Glen Layout', 'location': 'Bellandur / Outer Ring Road, Bangalore',
        'zone': 'ecity', 'type': 'High-Rise Residential Enclave', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'blue',
        'avenues': ['Green Glen Boulevard', 'Sobha Lake Link', '2nd Cross Way', 'Park Avenue', 'ORR Access'],
        'amenities': [
            {'id': 'park', 'name': 'Green Glen Community Park', 'desc': 'Community managed organic park and sports arena', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'recreation', 'icon': '🌳'}
        ]
    },
    {
        'id': 'concorde_cuppertino', 'name': 'Concorde Cuppertino', 'location': 'Neeladri Road, Electronic City Phase 1',
        'zone': 'ecity', 'type': 'Gated Tech-Villa Community', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Cuppertino Boulevard', 'Silicon Way', 'Apple Court', 'Neeladri Link', 'Wipro Way'],
        'amenities': [
            {'id': 'club', 'name': 'Cuppertino Clubhouse', 'desc': 'Swimming pool, tennis court & indoor recreation', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'neo_town', 'name': 'Neotown Township', 'location': 'Begur Road / Electronic City Phase 1, Bangalore',
        'zone': 'ecity', 'type': 'Integrated City Township', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'purple',
        'avenues': ['Neotown Boulevard', 'South Parkway', 'Tech Link Road', 'Town Plaza Way', 'Expressway Access'],
        'amenities': [
            {'id': 'mall', 'name': 'Neotown Mall & Arena', 'desc': 'Shopping, bowling, food court and multiplex', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🛍️'}
        ]
    },

    # --- NORTH BANGALORE & AIRPORT CORRIDOR ---
    {
        'id': 'sobha_city', 'name': 'Sobha City', 'location': 'Thanisandra Main Road, Bangalore North',
        'zone': 'north', 'type': 'Luxury Mediterranean Township', 'unitType': 'Tower/Villa', 'unitPrefix': 'Unit', 'colorTheme': 'blue',
        'avenues': ['Emerald Boulevard', 'Santorini Way', 'Casablanca Crescent', 'Greek Amphitheater Way', 'Lakeview Drive'],
        'amenities': [
            {'id': 'club', 'name': 'The Sobha City Club', 'desc': 'Palatial 50,000 sq ft clubhouse with indoor Olympic pool', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'lake', 'name': '24-Acre Lakefront Promenade', 'desc': 'Private lagoon, sailing dock & jogging boardwalk', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '⛵'}
        ]
    },
    {
        'id': 'bhartiya_city', 'name': 'Bhartiya City Nikoo Homes', 'location': 'Thanisandra Main Road, Bangalore North',
        'zone': 'north', 'type': 'Smart City Township', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'purple',
        'avenues': ['Nikoo Boulevard', 'Central Park Avenue', 'High Street Parkway', 'Campus Way', 'Airport Link'],
        'amenities': [
            {'id': 'mall', 'name': 'Bhartiya Mall of Bengaluru', 'desc': '1 million sq ft luxury shopping, dining and cinema', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🛍️'},
            {'id': 'park', 'name': 'The 7-Acre Central Park', 'desc': 'Vast green lawns, amphitheater and sports courts', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'recreation', 'icon': '🌳'}
        ]
    },
    {
        'id': 'manyata_residency', 'name': 'Manyata Tech Park Residency', 'location': 'Nagavara / Hebbal, Bangalore North',
        'zone': 'north', 'type': 'Corporate Residency Layout', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'yellow',
        'avenues': ['Residency Boulevard', 'Tech View Road', 'Green Park Way', 'Outer Ring Road Link', 'Nagavara Parkway'],
        'amenities': [
            {'id': 'club', 'name': 'Manyata Residency Sports Club', 'desc': 'Tennis court, gym, pool & banquet hall', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'lake', 'name': 'Nagavara Lakefront Garden', 'desc': 'Scenic lake viewpoint and landscaped trail', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌊'}
        ]
    },
    {
        'id': 'prestige_golfshire', 'name': 'Prestige Golfshire', 'location': 'Nandi Hills Road, Devanahalli, Bangalore North',
        'zone': 'north', 'type': 'PGA Golf Course Ultra-Luxury Estate', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Golfshire Boulevard', 'Fairway Drive', 'Falcon Crescent', 'Green View Way', 'Nandi Vista Road'],
        'amenities': [
            {'id': 'golf', 'name': '18-Hole Championship PGA Golf Course', 'desc': 'World-class golf course designed by Bob Hunt', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'sports', 'icon': '⛳'},
            {'id': 'club', 'name': 'Falcon Country Club', 'desc': 'Helipad, luxury spa, heated pool & clubhouse', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'ozone_urbana', 'name': 'Ozone Urbana', 'location': 'Kannamangala, Devanahalli, Bangalore North',
        'zone': 'north', 'type': 'Integrated Mega Township', 'unitType': 'Tower/Villa', 'unitPrefix': 'Unit', 'colorTheme': 'green',
        'avenues': ['Urbana Boulevard', 'Pavilion Way', 'Green Meadows Avenue', 'School Parkway', 'Airport Expressway'],
        'amenities': [
            {'id': 'club', 'name': 'The Urbana Club & Bowling Alley', 'desc': '60,000 sq ft mega clubhouse with 4 pools', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🎳'},
            {'id': 'school', 'name': 'National Public School Link', 'desc': 'Campus sports field and auditorium', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'civic', 'icon': '🏫'}
        ]
    },
    {
        'id': 'rmz_galleria', 'name': 'RMZ Galleria Layout', 'location': 'Yelahanka New Town, Bangalore North',
        'zone': 'north', 'type': 'Premium Urban Enclave', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'blue',
        'avenues': ['Galleria Boulevard', 'Yelahanka Lake Road', '5th Cross Avenue', 'North Parkway', 'Highway Access'],
        'amenities': [
            {'id': 'mall', 'name': 'RMZ Galleria Mall', 'desc': 'Direct pedestrian access to shopping & dining', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🛍️'}
        ]
    },
    {
        'id': 'prestige_misty_waters', 'name': 'Prestige Misty Waters', 'location': 'Hebbal / Kempapura, Bangalore North',
        'zone': 'north', 'type': 'High-Rise Lakeside Community', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'blue',
        'avenues': ['Misty Waters Boulevard', 'Vista Avenue', 'Lake Breeze Way', 'North Crest Road', 'ORR Link'],
        'amenities': [
            {'id': 'club', 'name': 'Misty Waters Clubhouse', 'desc': 'Rooftop party deck, pool and squash court', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'godrej_woodsman', 'name': 'Godrej Woodsman Estate', 'location': 'Bellary Road, Hebbal, Bangalore North',
        'zone': 'north', 'type': 'Modern Forest Estate', 'unitType': 'Tower', 'unitPrefix': 'Tower', 'colorTheme': 'green',
        'avenues': ['Woodsman Boulevard', 'Pine Crest Avenue', 'Royal Palm Parkway', 'Hebbal Flyover Link', 'Airport Road'],
        'amenities': [
            {'id': 'club', 'name': 'Woodsman Country Club', 'desc': 'Heated pool, fitness center, library & salon', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'jakkur_aerodrome', 'name': 'Jakkur Lakeview Enclave', 'location': 'Jakkur Plantation, Bangalore North',
        'zone': 'north', 'type': 'Lakefront Villa Community', 'unitType': 'Villa', 'unitPrefix': 'Villa', 'colorTheme': 'green',
        'avenues': ['Aerodrome Boulevard', 'Flight Path Avenue', 'Lakeview Crescent', 'Plantation Way', 'Bellary Link'],
        'amenities': [
            {'id': 'lake', 'name': 'Jakkur Lake Bird Boardwalk', 'desc': 'Island bird sanctuary and fresh air walkway', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🦆'}
        ]
    },
    {
        'id': 'kempapura_lakeview', 'name': 'Kempapura Coffee Board Layout', 'location': 'Hebbal / Kempapura, Bangalore North',
        'zone': 'north', 'type': 'Residential Colony', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['Coffee Board Boulevard', 'Lakeview 1st Main', '4th Cross Way', 'Ring Road Parkway', 'Hebbal Link'],
        'amenities': [
            {'id': 'park', 'name': 'Hebbal Lakefront Park', 'desc': 'Vast garden bordering Hebbal Lake', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌳'}
        ]
    },

    # --- CENTRAL & WEST BANGALORE ---
    {
        'id': 'koramangala_4th', 'name': 'Koramangala 4th Block', 'location': 'ST Bed & Maharaja Enclave, Bangalore Central',
        'zone': 'central', 'type': 'Affluent Tree-Lined Residential Colony', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'green',
        'avenues': ['80ft Road Boulevard', 'Maharaja Avenue', 'ST Bed Parkway', '1st Main Road', 'Sony World Link'],
        'amenities': [
            {'id': 'club', 'name': 'The Koramangala Club', 'desc': 'Elite social, tennis and sports club founded 1976', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🎾'},
            {'id': 'park', 'name': 'ST Bed Botanical Park', 'desc': 'Lush neighborhood park with outdoor gym', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌳'}
        ]
    },
    {
        'id': 'koramangala_3rd', 'name': 'Koramangala 3rd Block', 'location': "Millionaire's Row, 12th Main, Bangalore Central",
        'zone': 'central', 'type': 'Ultra-Prime Residential Enclave', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'green',
        'avenues': ['12th Main Boulevard', '3rd Block Cross Road', 'Sarjapur Link Way', 'IIMB Enclave Road', 'Parkview Crescent'],
        'amenities': [
            {'id': 'park', 'name': 'Koramangala 3rd Block Park', 'desc': 'Manicured lawns, jogging path & flowering trees', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'recreation', 'icon': '🌳'}
        ]
    },
    {
        'id': 'indiranagar_defence', 'name': 'Defence Colony Indiranagar', 'location': '100 Feet Road, Indiranagar, Bangalore Central',
        'zone': 'central', 'type': 'Elite Planned Military Officers Colony', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'green',
        'avenues': ['Defence Colony Boulevard', 'Officers Avenue', '1st Cross Road', '100ft Road Access', 'Park Lane'],
        'amenities': [
            {'id': 'club', 'name': 'Defence Colony Club', 'desc': 'Private club, swimming pool, library and tennis court', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'park', 'name': 'Defence Colony Memorial Children Park', 'desc': 'Children play fortress and shaded gazebos', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🛝'}
        ]
    },
    {
        'id': 'indiranagar_hal2', 'name': 'HAL 2nd Stage Indiranagar', 'location': '12th Main & Doopanahalli, Bangalore Central',
        'zone': 'central', 'type': 'Vibrant Garden City Enclave', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'yellow',
        'avenues': ['12th Main Boulevard', '80ft Road Parkway', 'Doopanahalli Cross', 'Indiranagar Club Link', 'Metro Way'],
        'amenities': [
            {'id': 'club', 'name': 'The Indiranagar Club', 'desc': 'Premier recreation, Olympic swimming pool & dining', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'},
            {'id': 'park', 'name': 'Doopanahalli Central Park', 'desc': 'Walking trail and open green garden', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '🌳'}
        ]
    },
    {
        'id': 'brigade_gateway', 'name': 'Brigade Gateway Campus', 'location': 'Dr. Rajkumar Road, Rajajinagar / West',
        'zone': 'west', 'type': 'Integrated City & Lifestyle Campus', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'blue',
        'avenues': ['Gateway Boulevard', 'Orion Promenade', 'WTC Parkway', 'Columbia Asia Link', 'Metro Corridor'],
        'amenities': [
            {'id': 'mall', 'name': 'Orion Mall & Lake Walkway', 'desc': 'World-class waterfront mall, dining & multiplex', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🛍️'},
            {'id': 'wtc', 'name': 'World Trade Center (WTC)', 'desc': '32-story corporate landmark and observation deck', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'civic', 'icon': '🏢'}
        ]
    },
    {
        'id': 'sadashivanagar', 'name': 'Sadashivanagar Royal Layout', 'location': 'Palace Orchards & Sankey Tank, Bangalore',
        'zone': 'central', 'type': 'Royal Heritage Neighborhood', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'green',
        'avenues': ['Sankey Tank Boulevard', 'Palace Cross Road', '8th Main Avenue', 'Upper Palace Orchard', 'Mekhri Link'],
        'amenities': [
            {'id': 'lake', 'name': 'Sankey Tank Forest Promenade', 'desc': 'Historic heritage lake, boating and landscaped gardens', 'x': 620, 'y': 690, 'node': 's_mid', 'type': 'recreation', 'icon': '⛵'},
            {'id': 'club', 'name': 'The Sadashivanagar Club', 'desc': 'Billiards, tennis courts and members lounge', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🎾'}
        ]
    },
    {
        'id': 'malleswaram_18th', 'name': 'Malleswaram 18th Cross', 'location': 'Margosa & Sampige Road, Bangalore West',
        'zone': 'west', 'type': 'Historic Cultural Colony', 'unitType': 'House', 'unitPrefix': 'House', 'colorTheme': 'yellow',
        'avenues': ['Margosa Road Boulevard', 'Sampige Avenue', '18th Cross Parkway', 'Vyalikaval Link', 'Temple Way'],
        'amenities': [
            {'id': 'temple', 'name': 'Kadu Malleshwara Temple', 'desc': '7th century Shiva temple giving Malleswaram its name', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'banashankari_3rd', 'name': 'Banashankari 3rd Stage', 'location': 'Katriguppe / BDA Layout, Bangalore South-West',
        'zone': 'west', 'type': 'Planned BDA Colony', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['100ft Ring Road Boulevard', 'Katriguppe Main Avenue', '3rd Stage Way', 'BDA Complex Road', 'Banashankari Link'],
        'amenities': [
            {'id': 'complex', 'name': 'Banashankari BDA Complex', 'desc': 'Major commercial and government civic services hub', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🏛️'}
        ]
    },
    {
        'id': 'vijayanagar_bda', 'name': 'Vijayanagar BDA Layout', 'location': 'Chord Road / Pipeline, Bangalore West',
        'zone': 'west', 'type': 'Vibrant Commercial & Residential Layout', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['Chord Road Boulevard', 'Pipeline Avenue', '5th Main Way', 'Vijayanagar Club Road', 'Metro Link'],
        'amenities': [
            {'id': 'club', 'name': 'The Vijayanagar Club', 'desc': 'Badminton, swimming pool, gym & recreation', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'sports', 'icon': '🏊'}
        ]
    },
    {
        'id': 'rajajinagar_1st', 'name': 'Rajajinagar 1st Block', 'location': 'Dr. Rajkumar Road / Subramanya Nagar, West',
        'zone': 'west', 'type': 'Planned Urban Sector', 'unitType': 'Plot', 'unitPrefix': 'Plot', 'colorTheme': 'yellow',
        'avenues': ['1st Block Main Boulevard', '10th Cross Avenue', 'Subramanya Nagar Way', 'Mahalakshmi Link', 'ISKCON Parkway'],
        'amenities': [
            {'id': 'temple', 'name': 'ISKCON Sri Krishna Balaram Temple', 'desc': 'Grand hilltop cultural and architectural temple complex', 'x': 620, 'y': 270, 'node': 'n_mid', 'type': 'worship', 'icon': '🛕'}
        ]
    },
    {
        'id': 'peenya_industrial', 'name': 'Peenya Industrial Township', 'location': 'Tumkur Road, Bangalore West',
        'zone': 'west', 'type': 'Manufacturing & Enterprise Township', 'unitType': 'Block', 'unitPrefix': 'Block', 'colorTheme': 'yellow',
        'avenues': ['Peenya Main Boulevard', '1st Stage Parkway', '4th Cross Way', 'Outer Ring Link', 'Tumkur Highway'],
        'amenities': [
            {'id': 'hub', 'name': 'Peenya Industries Association Hub', 'desc': 'Business auditorium, conference center and banking hub', 'x': 620, 'y': 480, 'node': 'junc_ctr', 'type': 'civic', 'icon': '🏢'}
        ]
    }
]

# Build all 50 layouts
all_layouts = {}
all_layouts['himagiri'] = himagiri_layout
all_layouts['greenwood'] = greenwood_layout
all_layouts['tech_horizon'] = tech_horizon_layout

for spec in specs:
    layout_obj = build_custom_layout(spec)
    all_layouts[layout_obj['id']] = layout_obj

print(f"Total Layouts Built: {len(all_layouts)}")

# Export to layouts_data.js
js_content = f"window.LAYOUTS = {json.dumps(all_layouts, indent=2)};\n"
with open('himagiri-meadows/layouts_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"SUCCESS: layouts_data.js updated with {len(all_layouts)} layouts!")

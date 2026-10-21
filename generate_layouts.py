import json
import math

# 1. Load Himagiri Layout from map_data.json
with open('map_data.json', 'r', encoding='utf-8') as f:
    himagiri_raw = json.load(f)

himagiri_layout = {
    'id': 'himagiri',
    'name': 'Himagiri Meadows',
    'location': 'Bannerghatta Road, Bangalore South',
    'type': 'Residential Gated Community',
    'unitType': 'Plot',
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
    'gates': [
        { 'id': 'gate_1', 'label': 'Gate 1 (Main Entrance - West)', 'nodeId': 'gate_1' },
        { 'id': 'gate_2', 'label': 'Gate 2 (East Entrance)', 'nodeId': 'gate_2' }
    ],
    'sectors': ['Aster', 'Bluebell', 'Carnation', 'Dhalia', 'Exotica', 'Florentine', 'Gardenia', 'Hibiscus']
}

# 2. Build Greenwood Orchards Layout
gw_nodes = {
    'gw_gate_main':    {'id': 'gw_gate_main', 'x': 80, 'y': 480, 'label': 'Grand Arch Main Gate (West)'},
    'gw_junc_entry':   {'id': 'gw_junc_entry', 'x': 160, 'y': 480, 'label': 'Entrance Boulevard'},
    'gw_junc_pine':    {'id': 'gw_junc_pine', 'x': 280, 'y': 480, 'label': 'Pine Court Junction'},
    'gw_junc_center':  {'id': 'gw_junc_center', 'x': 580, 'y': 480, 'label': 'Central Plaza Roundabout'},
    'gw_junc_palm':    {'id': 'gw_junc_palm', 'x': 880, 'y': 480, 'label': 'Palm Drive Junction'},
    'gw_gate_east':    {'id': 'gw_gate_east', 'x': 1100, 'y': 480, 'label': 'East Forest Gate'},
    
    # North Loop (Magnolia Avenue at y=260)
    'gw_mag_w':        {'id': 'gw_mag_w', 'x': 280, 'y': 260, 'label': 'Magnolia West'},
    'gw_mag_m':        {'id': 'gw_mag_m', 'x': 580, 'y': 260, 'label': 'Magnolia Club Roundabout'},
    'gw_mag_e':        {'id': 'gw_mag_e', 'x': 880, 'y': 260, 'label': 'Magnolia East'},

    # South Loop (Cedar Way at y=700)
    'gw_ced_w':        {'id': 'gw_ced_w', 'x': 280, 'y': 700, 'label': 'Cedar West'},
    'gw_ced_m':        {'id': 'gw_ced_m', 'x': 580, 'y': 700, 'label': 'Cedar Lake Roundabout'},
    'gw_ced_e':        {'id': 'gw_ced_e', 'x': 880, 'y': 700, 'label': 'Cedar East'},

    # Mid Avenue stops
    'gw_pine_n_mid':   {'id': 'gw_pine_n_mid', 'x': 280, 'y': 370, 'label': 'Pine North Mid'},
    'gw_pine_s_mid':   {'id': 'gw_pine_s_mid', 'x': 280, 'y': 590, 'label': 'Pine South Mid'},
    'gw_palm_n_mid':   {'id': 'gw_palm_n_mid', 'x': 880, 'y': 370, 'label': 'Palm North Mid'},
    'gw_palm_s_mid':   {'id': 'gw_palm_s_mid', 'x': 880, 'y': 590, 'label': 'Palm South Mid'},
    'gw_club_n':       {'id': 'gw_club_n', 'x': 580, 'y': 370, 'label': 'Clubhouse Promenade'},
    'gw_lake_s':       {'id': 'gw_lake_s', 'x': 580, 'y': 590, 'label': 'Lakeside Boardwalk'}
}

gw_edges_raw = [
    # Main Central Boulevard (East-West at y=480)
    ('gw_gate_main', 'gw_junc_entry', 'Orchard Boulevard', 'primary'),
    ('gw_junc_entry', 'gw_junc_pine', 'Orchard Boulevard', 'primary'),
    ('gw_junc_pine', 'gw_junc_center', 'Orchard Boulevard', 'primary'),
    ('gw_junc_center', 'gw_junc_palm', 'Orchard Boulevard', 'primary'),
    ('gw_junc_palm', 'gw_gate_east', 'Orchard Boulevard', 'primary'),

    # Magnolia Avenue (North Loop at y=260)
    ('gw_mag_w', 'gw_mag_m', 'Magnolia Avenue', 'secondary'),
    ('gw_mag_m', 'gw_mag_e', 'Magnolia Avenue', 'secondary'),

    # Cedar Way (South Loop at y=700)
    ('gw_ced_w', 'gw_ced_m', 'Cedar Way', 'secondary'),
    ('gw_ced_m', 'gw_ced_e', 'Cedar Way', 'secondary'),

    # Pine Court (Vertical at x=280)
    ('gw_mag_w', 'gw_pine_n_mid', 'Pine Court', 'secondary'),
    ('gw_pine_n_mid', 'gw_junc_pine', 'Pine Court', 'secondary'),
    ('gw_junc_pine', 'gw_pine_s_mid', 'Pine Court', 'secondary'),
    ('gw_pine_s_mid', 'gw_ced_w', 'Pine Court', 'secondary'),

    # Club & Lake Central Link (Vertical at x=580)
    ('gw_mag_m', 'gw_club_n', 'Central Promenade', 'primary'),
    ('gw_club_n', 'gw_junc_center', 'Central Promenade', 'primary'),
    ('gw_junc_center', 'gw_lake_s', 'Lakeside Link', 'primary'),
    ('gw_lake_s', 'gw_ced_m', 'Lakeside Link', 'primary'),

    # Palm Drive (Vertical at x=880)
    ('gw_mag_e', 'gw_palm_n_mid', 'Palm Drive', 'secondary'),
    ('gw_palm_n_mid', 'gw_junc_palm', 'Palm Drive', 'secondary'),
    ('gw_junc_palm', 'gw_palm_s_mid', 'Palm Drive', 'secondary'),
    ('gw_palm_s_mid', 'gw_ced_e', 'Palm Drive', 'secondary'),
]

gw_edges = []
for u, v, road, rtype in gw_edges_raw:
    gw_edges.append({'u': u, 'v': v, 'road': road, 'type': rtype})
    gw_edges.append({'u': v, 'v': u, 'road': road, 'type': rtype})

# Generate 60 Luxury Villas for Greenwood Orchards
gw_plots = {}

def add_villa(vid, vnum, road, block, facing, x, y, w, h, node, color='green'):
    gw_plots[str(vid)] = {
        'id': str(vid),
        'number': str(vnum),
        'road': road,
        'block': block,
        'facing': facing,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'roadNode': node,
        'color': color
    }

# Block 1: Pine Court North (Villas 1 to 10)
for i in range(5):
    # Left column (facing East to x=280)
    add_villa(i + 1, f"Villa {i+1}", "Pine Court", "Pine North Block", "East", 216, 275 + i * 38, 48, 30, "gw_pine_n_mid", "green")
    # Right column (facing West to x=280)
    add_villa(i + 6, f"Villa {i+6}", "Pine Court", "Pine North Block", "West", 296, 275 + i * 38, 48, 30, "gw_pine_n_mid", "yellow")

# Block 2: Magnolia Central Villas (Villas 11 to 20)
for i in range(5):
    # Top row (facing South to Magnolia at y=260)
    add_villa(i + 11, f"Villa {i+11}", "Magnolia Avenue", "Magnolia Central", "South", 380 + i * 75, 212, 58, 34, "gw_mag_m", "yellow")
    # Bottom row (facing North to Magnolia at y=260)
    add_villa(i + 16, f"Villa {i+16}", "Magnolia Avenue", "Magnolia Central", "North", 380 + i * 75, 276, 58, 34, "gw_mag_m", "green")

# Block 3: Palm Drive North (Villas 21 to 30)
for i in range(5):
    add_villa(i + 21, f"Villa {i+21}", "Palm Drive", "Palm North Block", "East", 816, 275 + i * 38, 48, 30, "gw_palm_n_mid", "green")
    add_villa(i + 26, f"Villa {i+26}", "Palm Drive", "Palm North Block", "West", 896, 275 + i * 38, 48, 30, "gw_palm_n_mid", "yellow")

# Block 4: Pine Court South (Villas 31 to 40)
for i in range(5):
    add_villa(i + 31, f"Villa {i+31}", "Pine Court", "Pine South Block", "East", 216, 515 + i * 36, 48, 28, "gw_pine_s_mid", "yellow")
    add_villa(i + 36, f"Villa {i+36}", "Pine Court", "Pine South Block", "West", 296, 515 + i * 36, 48, 28, "gw_pine_s_mid", "green")

# Block 5: Cedar Lakeside Villas (Villas 41 to 50)
for i in range(5):
    add_villa(i + 41, f"Villa {i+41}", "Cedar Way", "Cedar Lake Block", "North", 380 + i * 75, 650, 58, 34, "gw_ced_m", "green")
    add_villa(i + 46, f"Villa {i+46}", "Cedar Way", "Cedar Lake Block", "South", 380 + i * 75, 716, 58, 34, "gw_ced_m", "yellow")

# Block 6: Palm Drive South (Villas 51 to 60)
for i in range(5):
    add_villa(i + 51, f"Villa {i+51}", "Palm Drive", "Palm South Block", "East", 816, 515 + i * 36, 48, 28, "gw_palm_s_mid", "yellow")
    add_villa(i + 56, f"Villa {i+56}", "Palm Drive", "Palm South Block", "West", 896, 515 + i * 36, 48, 28, "gw_palm_s_mid", "green")

gw_amenities = [
    {'id': 'gw_gate_main', 'name': 'Grand Arch Main Gate (West)', 'desc': 'Primary security entry and visitor registration', 'x': 80, 'y': 480, 'roadNode': 'gw_gate_main', 'icon': '🚪', 'color': '#059669'},
    {'id': 'gw_clubhouse', 'name': 'Grand Clubhouse & Swimming Pool', 'desc': '3-story luxury clubhouse, Olympic pool, indoor squash & lounge', 'x': 580, 'y': 345, 'roadNode': 'gw_club_n', 'icon': '🏊', 'color': '#2563eb'},
    {'id': 'gw_tennis', 'name': 'Tennis & Pickleball Courts', 'desc': 'All-weather floodlit courts and sports gazebo', 'x': 980, 'y': 260, 'roadNode': 'gw_mag_e', 'icon': '🎾', 'color': '#f59e0b'},
    {'id': 'gw_lake', 'name': 'Lakeside Promenade & Deck', 'desc': 'Scenic freshwater lake with wooden jogging boardwalk and gazebos', 'x': 580, 'y': 780, 'roadNode': 'gw_ced_m', 'icon': '🌊', 'color': '#06b6d4'},
    {'id': 'gw_park', 'name': "Children's Nature Park", 'desc': 'Treehouse, sensory play zones, and zip-line for kids', 'x': 200, 'y': 370, 'roadNode': 'gw_pine_n_mid', 'icon': '🛝', 'color': '#16a34a'},
    {'id': 'gw_garden', 'name': 'Organic Community Garden', 'desc': 'Hydroponic herbs, flowering orchards, and butterfly zone', 'x': 980, 'y': 700, 'roadNode': 'gw_ced_e', 'icon': '🌿', 'color': '#10b981'},
    {'id': 'gw_amphi', 'name': 'Amphitheater & Central Lawn', 'desc': 'Open-air cultural events lawn and weekend gatherings', 'x': 580, 'y': 560, 'roadNode': 'gw_lake_s', 'icon': '🎭', 'color': '#8b5cf6'},
    {'id': 'gw_ev', 'name': 'EV Fast-Charging Plaza', 'desc': '12 high-power DC charging stations for residents and visitors', 'x': 160, 'y': 440, 'roadNode': 'gw_junc_entry', 'icon': '⚡', 'color': '#0284c7'},
    {'id': 'gw_gate_east', 'name': 'East Forest Gate', 'desc': 'Automated RFID exit towards Carmelaram station road', 'x': 1100, 'y': 480, 'roadNode': 'gw_gate_east', 'icon': '🚪', 'color': '#059669'}
]

greenwood_layout = {
    'id': 'greenwood',
    'name': 'Greenwood Orchards',
    'location': 'Sarjapur Road / Carmelaram, Bangalore East',
    'type': 'Luxury Villa Layout',
    'unitType': 'Villa',
    'bounds': {'minX': 40, 'maxX': 1180, 'minY': 160, 'maxY': 840},
    'center': {'x': 600, 'y': 480},
    'groundPolygon': "60,480 120,220 300,160 880,160 1060,200 1140,480 1060,780 880,820 300,820 120,760 Z",
    'borderTreesPath': "M 60,480 Q 120,180 300,160 T 880,160 T 1140,480 T 880,820 T 300,820 Z",
    'gardenPark': {'x': 460, 'y': 455, 'w': 240, 'h': 50, 'rx': 8, 'label': "Orchard Central Park"},
    'roads': {
        'nodes': gw_nodes,
        'edges': gw_edges
    },
    'plots': gw_plots,
    'amenities': gw_amenities,
    'roadLabels': [
        { 'name': "ORCHARD BOULEVARD", 'x': 420, 'y': 480, 'vertical': False },
        { 'name': "MAGNOLIA AVENUE", 'x': 420, 'y': 260, 'vertical': False },
        { 'name': "CEDAR WAY", 'x': 420, 'y': 700, 'vertical': False },
        { 'name': "PINE COURT", 'x': 280, 'y': 370, 'vertical': True },
        { 'name': "PALM DRIVE", 'x': 880, 'y': 370, 'vertical': True }
    ],
    'defaultStartGate': 'gw_gate_main',
    'gates': [
        { 'id': 'gw_gate_main', 'label': 'Grand Arch Main Gate (West)', 'nodeId': 'gw_gate_main' },
        { 'id': 'gw_gate_east', 'label': 'East Forest Gate (East)', 'nodeId': 'gw_gate_east' }
    ],
    'sectors': ['Orchard Boulevard', 'Magnolia Avenue', 'Pine Court', 'Palm Drive', 'Cedar Way']
}

# 3. Build Tech Horizon Campus Layout
th_nodes = {
    'th_gate_main':     {'id': 'th_gate_main', 'x': 580, 'y': 820, 'label': 'Main Security Gate 1 (South)'},
    'th_gate_north':    {'id': 'th_gate_north', 'x': 580, 'y': 150, 'label': 'Express Cargo Gate 2 (North)'},

    # Central Innovation Corridor (Vertical at x=580)
    'th_south_round':   {'id': 'th_south_round', 'x': 580, 'y': 680, 'label': 'South Welcome Plaza'},
    'th_center_plaza':  {'id': 'th_center_plaza', 'x': 580, 'y': 480, 'label': 'Central Innovation Plaza'},
    'th_north_round':   {'id': 'th_north_round', 'x': 580, 'y': 280, 'label': 'North Gateway Roundabout'},

    # West Silicon Corridor (at x=260)
    'th_west_n':        {'id': 'th_west_n', 'x': 260, 'y': 280, 'label': 'Silicon North'},
    'th_west_m':        {'id': 'th_west_m', 'x': 260, 'y': 480, 'label': 'Silicon Central'},
    'th_west_s':        {'id': 'th_west_s', 'x': 260, 'y': 680, 'label': 'Silicon South'},

    # East Cyber Corridor (at x=900)
    'th_east_n':        {'id': 'th_east_n', 'x': 900, 'y': 280, 'label': 'Cyber North'},
    'th_east_m':        {'id': 'th_east_m', 'x': 900, 'y': 480, 'label': 'Cyber Central'},
    'th_east_s':        {'id': 'th_east_s', 'x': 900, 'y': 680, 'label': 'Cyber South'},

    # Mid Connectors
    'th_west_mid_link': {'id': 'th_west_mid_link', 'x': 420, 'y': 480, 'label': 'West Innovation Link'},
    'th_east_mid_link': {'id': 'th_east_mid_link', 'x': 740, 'y': 480, 'label': 'East Innovation Link'}
}

th_edges_raw = [
    # Main Central Spine (Innovation Boulevard at x=580)
    ('th_gate_main', 'th_south_round', 'Innovation Boulevard', 'primary'),
    ('th_south_round', 'th_center_plaza', 'Innovation Boulevard', 'primary'),
    ('th_center_plaza', 'th_north_round', 'Innovation Boulevard', 'primary'),
    ('th_north_round', 'th_gate_north', 'Innovation Boulevard', 'primary'),

    # Silicon Avenue (West Spine at x=260)
    ('th_west_n', 'th_west_m', 'Silicon Avenue', 'secondary'),
    ('th_west_m', 'th_west_s', 'Silicon Avenue', 'secondary'),

    # Cyber Boulevard (East Spine at x=900)
    ('th_east_n', 'th_east_m', 'Cyber Boulevard', 'secondary'),
    ('th_east_m', 'th_east_s', 'Cyber Boulevard', 'secondary'),

    # North Crossway (Quantum Way at y=280)
    ('th_west_n', 'th_north_round', 'Quantum Way', 'secondary'),
    ('th_north_round', 'th_east_n', 'Quantum Way', 'secondary'),

    # Central Crossway (Alpha Link at y=480)
    ('th_west_m', 'th_west_mid_link', 'Alpha Link', 'primary'),
    ('th_west_mid_link', 'th_center_plaza', 'Alpha Link', 'primary'),
    ('th_center_plaza', 'th_east_mid_link', 'Alpha Link', 'primary'),
    ('th_east_mid_link', 'th_east_m', 'Alpha Link', 'primary'),

    # South Crossway (Tech Avenue at y=680)
    ('th_west_s', 'th_south_round', 'Tech Avenue', 'secondary'),
    ('th_south_round', 'th_east_s', 'Tech Avenue', 'secondary'),
]

th_edges = []
for u, v, road, rtype in th_edges_raw:
    th_edges.append({'u': u, 'v': v, 'road': road, 'type': rtype})
    th_edges.append({'u': v, 'v': u, 'road': road, 'type': rtype})

# Generate 36 Corporate Office Towers & Tech Blocks
th_plots = {}

def add_block(bid, bnum, road, block, facing, x, y, w, h, node, color='yellow'):
    th_plots[str(bid)] = {
        'id': str(bid),
        'number': str(bnum),
        'road': road,
        'block': block,
        'facing': facing,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'roadNode': node,
        'color': color
    }

# West Sector - Towers A & B (Blocks 101 to 112)
for i in range(4):
    add_block(f"T-A{i+1}", f"Tower A{i+1}", "Silicon Avenue", "Alpha Tech Sector", "East", 185, 310 + i * 44, 60, 36, "th_west_m", "green")
    add_block(f"T-B{i+1}", f"Tower B{i+1}", "Silicon Avenue", "Beta Enterprise Sector", "West", 285, 310 + i * 44, 60, 36, "th_west_m", "yellow")

for i in range(4):
    add_block(f"10{i+1}", f"Block 10{i+1}", "Silicon Avenue", "Silicon West Labs", "East", 185, 510 + i * 40, 60, 32, "th_west_s", "yellow")

# Central Sector - Tech Blocks (Blocks 201 to 210)
for i in range(5):
    add_block(f"20{i+1}", f"Block 20{i+1}", "Innovation Boulevard", "Core Innovation Hub", "West", 495, 310 + i * 42, 68, 34, "th_center_plaza", "green")
    add_block(f"20{i+6}", f"Block 20{i+6}", "Innovation Boulevard", "Core Innovation Hub", "East", 595, 310 + i * 42, 68, 34, "th_center_plaza", "yellow")

# East Sector - Towers C & D (Blocks 301 to 310)
for i in range(4):
    add_block(f"T-C{i+1}", f"Tower C{i+1}", "Cyber Boulevard", "Cloud & AI Labs", "East", 825, 310 + i * 44, 60, 36, "th_east_m", "green")
    add_block(f"T-D{i+1}", f"Tower D{i+1}", "Cyber Boulevard", "Data Systems Hub", "West", 925, 310 + i * 44, 60, 36, "th_east_m", "yellow")

for i in range(6):
    add_block(f"30{i+1}", f"Block 30{i+1}", "Cyber Boulevard", "Cyber Enterprise Park", "East", 825, 510 + i * 36, 60, 30, "th_east_s", "yellow")

th_amenities = [
    {'id': 'th_gate_main', 'name': 'Main Security Gate 1 (South)', 'desc': 'Visitor badge pass counter & automated vehicle boom barrier', 'x': 580, 'y': 820, 'roadNode': 'th_gate_main', 'icon': '🚪', 'color': '#059669'},
    {'id': 'th_food_court', 'name': 'Central Cafeteria & Food Plaza', 'desc': '40,000 sq ft multi-cuisine food court, cafes & bakery', 'x': 580, 'y': 480, 'roadNode': 'th_center_plaza', 'icon': '🍽️', 'color': '#2563eb'},
    {'id': 'th_convention', 'name': 'Auditorium & Convention Hall', 'desc': '800-seat amphitheater & executive briefing center', 'x': 420, 'y': 480, 'roadNode': 'th_west_mid_link', 'icon': '🏛️', 'color': '#8b5cf6'},
    {'id': 'th_mlcp', 'name': 'Multi-Level Car Parking (MLCP)', 'desc': '6-level automated parking garage with 2,500 bays', 'x': 180, 'y': 680, 'roadNode': 'th_west_s', 'icon': '🅿️', 'color': '#0284c7'},
    {'id': 'th_ev_bay', 'name': 'Supercharger EV Charging Bay', 'desc': 'Fast-charging stations for 30 electric cars and two-wheelers', 'x': 980, 'y': 680, 'roadNode': 'th_east_s', 'icon': '⚡', 'color': '#f59e0b'},
    {'id': 'th_sports', 'name': 'Sports Arena & Gymnasium', 'desc': 'Indoor badminton, basketball court, and state-of-the-art gym', 'x': 180, 'y': 280, 'roadNode': 'th_west_n', 'icon': '🏀', 'color': '#16a34a'},
    {'id': 'th_clinic', 'name': 'Emergency Medical Clinic', 'desc': '24/7 on-campus first aid, ambulance bay, and pharmacy', 'x': 980, 'y': 280, 'roadNode': 'th_east_n', 'icon': '🏥', 'color': '#ef4444'},
    {'id': 'th_gate_north', 'name': 'Express Cargo Gate 2 (North)', 'desc': 'Delivery logistics & employee shuttle bus bay', 'x': 580, 'y': 150, 'roadNode': 'th_gate_north', 'icon': '🚪', 'color': '#059669'}
]

tech_horizon_layout = {
    'id': 'tech_horizon',
    'name': 'Tech Horizon Campus',
    'location': 'Electronic City Phase 1, Bangalore',
    'type': 'Enterprise Tech Park',
    'unitType': 'Tower/Block',
    'bounds': {'minX': 100, 'maxX': 1100, 'minY': 120, 'maxY': 860},
    'center': {'x': 580, 'y': 480},
    'groundPolygon': "580,120 980,180 1080,480 980,780 580,850 180,780 80,480 180,180 Z",
    'borderTreesPath': "M 580,120 L 980,180 L 1080,480 L 980,780 L 580,850 L 180,780 L 80,480 L 180,180 Z",
    'gardenPark': {'x': 420, 'y': 460, 'w': 320, 'h': 40, 'rx': 6, 'label': "Central Plaza Green"},
    'roads': {
        'nodes': th_nodes,
        'edges': th_edges
    },
    'plots': th_plots,
    'amenities': th_amenities,
    'roadLabels': [
        { 'name': "INNOVATION BOULEVARD", 'x': 580, 'y': 380, 'vertical': True },
        { 'name': "SILICON AVENUE", 'x': 260, 'y': 380, 'vertical': True },
        { 'name': "CYBER BOULEVARD", 'x': 900, 'y': 380, 'vertical': True },
        { 'name': "QUANTUM WAY", 'x': 420, 'y': 280, 'vertical': False },
        { 'name': "ALPHA LINK", 'x': 420, 'y': 480, 'vertical': False }
    ],
    'defaultStartGate': 'th_gate_main',
    'gates': [
        { 'id': 'th_gate_main', 'label': 'Main Security Gate 1 (South)', 'nodeId': 'th_gate_main' },
        { 'id': 'th_gate_north', 'label': 'Express Cargo Gate 2 (North)', 'nodeId': 'th_gate_north' }
    ],
    'sectors': ['Innovation Boulevard', 'Silicon Avenue', 'Cyber Boulevard', 'Quantum Way', 'Alpha Link']
}

all_layouts = {
    'himagiri': himagiri_layout,
    'greenwood': greenwood_layout,
    'tech_horizon': tech_horizon_layout
}

# Export to layouts_data.js
js_content = f"window.LAYOUTS = {json.dumps(all_layouts, indent=2)};\n"
with open('layouts_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"SUCCESS: layouts_data.js generated with {len(all_layouts)} layouts!")
print(f"  - Himagiri: {len(himagiri_layout['plots'])} plots, {len(himagiri_layout['amenities'])} amenities")
print(f"  - Greenwood: {len(greenwood_layout['plots'])} villas, {len(greenwood_layout['amenities'])} amenities")
print(f"  - Tech Horizon: {len(tech_horizon_layout['plots'])} blocks, {len(tech_horizon_layout['amenities'])} amenities")

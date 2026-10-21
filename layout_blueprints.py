# layout_blueprints.py
# Authentic architectural blueprints for Bangalore communities

BLUEPRINTS = {
    # 1. BRIGADE GATEWAY (Rajajinagar / Malleswaram)
    # 40-acre lifestyle enclave with 2-acre man-made lake, Orion Mall, WTC & curved towers
    'brigade_gateway': {
        'groundPolygon': "80,480 180,140 600,120 1080,140 1140,480 1080,820 600,840 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 600,120 L 1080,140 L 1140,480 L 1080,820 L 600,840 L 180,820 Z",
        'waterBody': {'x': 540, 'y': 380, 'w': 240, 'h': 160, 'rx': 30, 'label': 'Orion Gateway Lake & Promenade'},
        'landmarks': [
            {'x': 840, 'y': 440, 'w': 220, 'h': 230, 'rx': 8, 'label': '🛍️ Orion Mall & Waterfront Multiplex', 'fill': '#1e1b4b', 'stroke': '#818cf8'},
            {'x': 840, 'y': 170, 'w': 220, 'h': 190, 'rx': 8, 'label': '🏢 World Trade Center (32-Floor Tower)', 'fill': '#0f172a', 'stroke': '#38bdf8'}
        ],
        'gardenPark': {'x': 400, 'y': 240, 'w': 180, 'h': 60, 'rx': 8, 'label': 'Sheraton Grand Garden Lawn'},
        'defaultStartGate': 'bg_gate_main',
        'nodes': {
            'bg_gate_main':   {'id': 'bg_gate_main', 'x': 80, 'y': 480, 'label': 'Main Gate (Dr. Rajkumar Road)'},
            'bg_junc_w':      {'id': 'bg_junc_w', 'x': 240, 'y': 480, 'label': 'Gateway West Roundabout'},
            'bg_junc_nw':     {'id': 'bg_junc_nw', 'x': 240, 'y': 260, 'label': 'Aster & Banyan Crescent Cross'},
            'bg_junc_n':      {'id': 'bg_junc_n', 'x': 540, 'y': 220, 'label': 'North Lake Boulevard Cross'},
            'bg_junc_ne':     {'id': 'bg_junc_ne', 'x': 800, 'y': 220, 'label': 'WTC Malleswaram Plaza'},
            'bg_gate_wtc':    {'id': 'bg_gate_wtc', 'x': 1080, 'y': 170, 'label': 'Gate 2 (WTC Malleswaram Link)'},
            'bg_lake_n':      {'id': 'bg_lake_n', 'x': 540, 'y': 340, 'label': 'Lake Boardwalk North'},
            'bg_lake_s':      {'id': 'bg_lake_s', 'x': 540, 'y': 580, 'label': 'Lake Boardwalk South'},
            'bg_junc_sw':     {'id': 'bg_junc_sw', 'x': 240, 'y': 700, 'label': 'Ebony & Fern Crescent Cross'},
            'bg_junc_s':      {'id': 'bg_junc_s', 'x': 540, 'y': 740, 'label': 'South Gate Access Link'},
            'bg_junc_se':     {'id': 'bg_junc_se', 'x': 800, 'y': 720, 'label': 'Orion South Promenade Cross'},
            'bg_gate_orion':  {'id': 'bg_gate_orion', 'x': 1090, 'y': 560, 'label': 'Gate 3 (Orion Mall Lake Entry)'}
        },
        'edges': [
            ('bg_gate_main', 'bg_junc_w', 'Gateway Boulevard', 'primary'),
            ('bg_junc_w', 'bg_junc_nw', 'Gateway Boulevard', 'primary'),
            ('bg_junc_nw', 'bg_junc_n', 'Gateway Boulevard', 'primary'),
            ('bg_junc_n', 'bg_junc_ne', 'WTC Ring Link', 'primary'),
            ('bg_junc_ne', 'bg_gate_wtc', 'WTC Ring Link', 'secondary'),
            ('bg_junc_w', 'bg_junc_sw', 'Gateway Boulevard', 'primary'),
            ('bg_junc_sw', 'bg_junc_s', 'Gateway Boulevard', 'primary'),
            ('bg_junc_s', 'bg_junc_se', 'Orion Mall Parkway', 'primary'),
            ('bg_junc_se', 'bg_gate_orion', 'Orion Mall Parkway', 'primary'),
            ('bg_junc_n', 'bg_lake_n', 'Lake Promenade Way', 'secondary'),
            ('bg_lake_n', 'bg_lake_s', 'Lake Promenade Way', 'secondary'),
            ('bg_lake_s', 'bg_junc_s', 'Lake Promenade Way', 'secondary'),
            ('bg_junc_w', 'bg_lake_n', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Aster Tower', 240, 190, 'bg_junc_nw', 'Gateway Boulevard', 'South'),
            ('Banyan Tower', 460, 170, 'bg_junc_n', 'Gateway Boulevard', 'South'),
            ('Cedar Tower', 200, 370, 'bg_junc_w', 'Gateway Boulevard', 'East'),
            ('Deodar Tower', 200, 590, 'bg_junc_sw', 'Gateway Boulevard', 'East'),
            ('Ebony Tower', 320, 740, 'bg_junc_sw', 'Gateway Boulevard', 'North'),
            ('Fern Tower', 560, 780, 'bg_junc_s', 'Gateway Boulevard', 'North'),
            ('Gulmohar Tower', 760, 750, 'bg_junc_se', 'Orion Mall Parkway', 'North')
        ],
        'roadLabels': [
            {'name': 'GATEWAY BOULEVARD', 'x': 230, 'y': 480, 'vertical': True},
            {'name': 'ORION LAKE PROMENADE', 'x': 620, 'y': 360, 'vertical': False},
            {'name': 'WTC RING LINK', 'x': 780, 'y': 205, 'vertical': False},
            {'name': 'DR. RAJKUMAR CORRIDOR', 'x': 160, 'y': 490, 'vertical': False},
            {'name': 'ORION MALL PARKWAY', 'x': 800, 'y': 690, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Sheraton Grand Club & Spa', 'desc': 'Heated indoor pool, spa, fine dining, ballroom & helipad', 'x': 400, 'y': 240, 'node': 'bg_junc_nw', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'wtc', 'name': 'World Trade Center Bangalore', 'desc': '32 floors premier commercial tower and global trade hub', 'x': 840, 'y': 170, 'node': 'bg_junc_ne', 'type': 'civic', 'icon': '🏢'},
            {'id': 'mall', 'name': 'Orion Mall & PVR Cinemas', 'desc': 'Bangalore flagship waterfront mall with 150+ international stores', 'x': 840, 'y': 440, 'node': 'bg_gate_orion', 'type': 'mall', 'icon': '🛍️'}
        ]
    },

    # 2. SALARPURIA SATTVA GREENAGE (Hosur Road, Bommanahalli)
    # 21-acre oval superblock with 8 towers encircling 60,000 sq ft Clayey Park & 4 pools
    'sattva_greenage': {
        'groundPolygon': "100,480 200,160 500,120 740,120 1040,160 1140,480 1040,800 740,840 500,840 200,800 Z",
        'borderTreesPath': "M 100,480 Q 200,140 620,120 Q 1040,140 1140,480 Q 1040,820 620,840 Q 200,820 100,480 Z",
        'waterBody': {'x': 500, 'y': 430, 'w': 240, 'h': 100, 'rx': 20, 'label': 'Clayey Park 4-Tier Resort Pools & Lagoon'},
        'gardenPark': {'x': 440, 'y': 310, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Greenage Central Botanical Lawns'},
        'defaultStartGate': 'sg_gate_hosur',
        'nodes': {
            'sg_gate_hosur':  {'id': 'sg_gate_hosur', 'x': 620, 'y': 840, 'label': 'Gate 1 (Hosur Main Road)'},
            'sg_gate_north':  {'id': 'sg_gate_north', 'x': 620, 'y': 130, 'label': 'Gate 2 (Bommanahalli Service Road)'},
            'sg_ring_s':      {'id': 'sg_ring_s', 'x': 620, 'y': 740, 'label': 'South Ring Boulevard'},
            'sg_ring_sw':     {'id': 'sg_ring_sw', 'x': 360, 'y': 680, 'label': 'Elm & Oak Boulevard Curve'},
            'sg_ring_w':      {'id': 'sg_ring_w', 'x': 240, 'y': 480, 'label': 'Magnolia West Parkway'},
            'sg_ring_nw':     {'id': 'sg_ring_nw', 'x': 360, 'y': 280, 'label': 'Alpine & Aster Curve'},
            'sg_ring_n':      {'id': 'sg_ring_n', 'x': 620, 'y': 220, 'label': 'North Ring Boulevard'},
            'sg_ring_ne':     {'id': 'sg_ring_ne', 'x': 880, 'y': 280, 'label': 'Birch & Cedar Curve'},
            'sg_ring_e':      {'id': 'sg_ring_e', 'x': 1000, 'y': 480, 'label': 'Ebony East Promenade'},
            'sg_ring_se':     {'id': 'sg_ring_se', 'x': 880, 'y': 680, 'label': 'Cedar & Elm South Curve'},
            'sg_ctr_hub':     {'id': 'sg_ctr_hub', 'x': 620, 'y': 480, 'label': 'Clayey Park Central Plaza'}
        },
        'edges': [
            ('sg_gate_hosur', 'sg_ring_s', 'Hosur Access Way', 'primary'),
            ('sg_gate_north', 'sg_ring_n', 'North Service Link', 'primary'),
            ('sg_ring_s', 'sg_ring_sw', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_sw', 'sg_ring_w', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_w', 'sg_ring_nw', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_nw', 'sg_ring_n', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_n', 'sg_ring_ne', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_ne', 'sg_ring_e', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_e', 'sg_ring_se', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_se', 'sg_ring_s', 'Greenage Ring Boulevard', 'primary'),
            ('sg_ring_w', 'sg_ctr_hub', 'Clayey Park Drive', 'secondary'),
            ('sg_ring_e', 'sg_ctr_hub', 'Clayey Park Drive', 'secondary'),
            ('sg_ring_n', 'sg_ctr_hub', 'Central Link', 'secondary'),
            ('sg_ring_s', 'sg_ctr_hub', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Alpine Tower', 320, 200, 'sg_ring_nw', 'Greenage Ring Boulevard', 'South'),
            ('Aster Tower', 580, 160, 'sg_ring_n', 'Greenage Ring Boulevard', 'South'),
            ('Birch Tower', 840, 200, 'sg_ring_ne', 'Greenage Ring Boulevard', 'South'),
            ('Cedar Tower', 960, 360, 'sg_ring_e', 'Greenage Ring Boulevard', 'West'),
            ('Ebony Tower', 940, 600, 'sg_ring_se', 'Greenage Ring Boulevard', 'West'),
            ('Elm Tower', 740, 730, 'sg_ring_s', 'Greenage Ring Boulevard', 'North'),
            ('Oak Tower', 440, 730, 'sg_ring_sw', 'Greenage Ring Boulevard', 'North'),
            ('Magnolia Tower', 220, 410, 'sg_ring_w', 'Greenage Ring Boulevard', 'East')
        ],
        'roadLabels': [
            {'name': 'GREENAGE RING BOULEVARD', 'x': 620, 'y': 200, 'vertical': False},
            {'name': 'CLAYEY PARK DRIVE', 'x': 620, 'y': 550, 'vertical': False},
            {'name': 'HOSUR ROAD CORRIDOR', 'x': 620, 'y': 800, 'vertical': False},
            {'name': 'LAKESIDE LINK', 'x': 230, 'y': 480, 'vertical': True},
            {'name': 'EBONY PARKWAY', 'x': 990, 'y': 480, 'vertical': True}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Clayey Park Grand Clubhouse', 'desc': '60,000 sq ft clubhouse with 4 swimming pools, 2 squash courts & bowling alley', 'x': 620, 'y': 440, 'node': 'sg_ctr_hub', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'sports', 'name': 'Greenage Multi-Sport Arena', 'desc': 'Tennis courts, skating rink, football turf and athletic tracks', 'x': 880, 'y': 680, 'node': 'sg_ring_se', 'type': 'sports', 'icon': '🎾'}
        ]
    },

    # 3. SOBHA DREAM ACRES (Panathur / Balagere)
    # 81-acre precast township with 4 radial wings along dual-carriageway parkway
    'sobha_dream_acres': {
        'groundPolygon': "80,480 180,140 1060,140 1160,480 1060,820 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 1060,140 L 1160,480 L 1060,820 L 180,820 Z",
        'waterBody': {'x': 520, 'y': 440, 'w': 200, 'h': 80, 'rx': 16, 'label': 'Sobha Club Oasis 5-Lane Lap Pool'},
        'gardenPark': {'x': 440, 'y': 310, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Dream Acres Central Forest Park'},
        'landmarks': [
            {'x': 980, 'y': 410, 'w': 140, 'h': 140, 'rx': 8, 'label': 'Sobha Precast Engineering Hub', 'fill': '#0f172a', 'stroke': '#0ea5e9'}
        ],
        'defaultStartGate': 'sda_gate_west',
        'nodes': {
            'sda_gate_west':  {'id': 'sda_gate_west', 'x': 90, 'y': 480, 'label': 'Gate 1 (Balagere Main Road)'},
            'sda_junc_w':     {'id': 'sda_junc_w', 'x': 240, 'y': 480, 'label': 'West Radial Roundabout'},
            'sda_junc_ctr':   {'id': 'sda_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Oasis Plaza'},
            'sda_junc_e':     {'id': 'sda_junc_e', 'x': 960, 'y': 480, 'label': 'East Radial Roundabout'},
            'sda_gate_east':  {'id': 'sda_gate_east', 'x': 1140, 'y': 480, 'label': 'Gate 2 (Panathur Tech Link)'},
            'sda_wing_nw':    {'id': 'sda_wing_nw', 'x': 280, 'y': 260, 'label': 'Rainforest Radial Cross'},
            'sda_wing_n_ctr': {'id': 'sda_wing_n_ctr', 'x': 620, 'y': 240, 'label': 'Pine Radial Cross'},
            'sda_wing_ne':    {'id': 'sda_wing_ne', 'x': 940, 'y': 260, 'label': 'Coral Radial Cross'},
            'sda_wing_sw':    {'id': 'sda_wing_sw', 'x': 280, 'y': 700, 'label': 'Palm Radial Cross'},
            'sda_wing_s_ctr': {'id': 'sda_wing_s_ctr', 'x': 620, 'y': 720, 'label': 'Cedar Radial Cross'},
            'sda_wing_se':    {'id': 'sda_wing_se', 'x': 940, 'y': 700, 'label': 'Spring Radial Cross'}
        },
        'edges': [
            ('sda_gate_west', 'sda_junc_w', 'Dream Acres Parkway', 'primary'),
            ('sda_junc_w', 'sda_junc_ctr', 'Dream Acres Parkway', 'primary'),
            ('sda_junc_ctr', 'sda_junc_e', 'Dream Acres Parkway', 'primary'),
            ('sda_junc_e', 'sda_gate_east', 'Dream Acres Parkway', 'primary'),
            ('sda_junc_w', 'sda_wing_nw', 'Rainforest Boulevard', 'secondary'),
            ('sda_junc_w', 'sda_wing_sw', 'Palm Boulevard', 'secondary'),
            ('sda_junc_ctr', 'sda_wing_n_ctr', 'Oasis Central Drive', 'secondary'),
            ('sda_junc_ctr', 'sda_wing_s_ctr', 'Oasis Central Drive', 'secondary'),
            ('sda_junc_e', 'sda_wing_ne', 'Coral Boulevard', 'secondary'),
            ('sda_junc_e', 'sda_wing_se', 'Spring Avenue', 'secondary'),
            ('sda_wing_nw', 'sda_wing_n_ctr', 'North Perimeter Ring', 'secondary'),
            ('sda_wing_n_ctr', 'sda_wing_ne', 'North Perimeter Ring', 'secondary'),
            ('sda_wing_sw', 'sda_wing_s_ctr', 'South Perimeter Ring', 'secondary'),
            ('sda_wing_s_ctr', 'sda_wing_se', 'South Perimeter Ring', 'secondary')
        ],
        'blocks': [
            ('Rainforest Wing', 260, 190, 'sda_wing_nw', 'Rainforest Boulevard', 'South'),
            ('Pine Wing', 580, 170, 'sda_wing_n_ctr', 'Oasis Central Drive', 'South'),
            ('Coral Wing', 900, 190, 'sda_wing_ne', 'Coral Boulevard', 'South'),
            ('Palm Wing', 260, 720, 'sda_wing_sw', 'Palm Boulevard', 'North'),
            ('Cedar Wing', 580, 740, 'sda_wing_s_ctr', 'Oasis Central Drive', 'North'),
            ('Spring Wing', 900, 720, 'sda_wing_se', 'Spring Avenue', 'North')
        ],
        'roadLabels': [
            {'name': 'DREAM ACRES GRAND PARKWAY', 'x': 620, 'y': 460, 'vertical': False},
            {'name': 'RAINFOREST BOULEVARD', 'x': 270, 'y': 350, 'vertical': True},
            {'name': 'CORAL BOULEVARD', 'x': 950, 'y': 350, 'vertical': True},
            {'name': 'PALM BOULEVARD', 'x': 270, 'y': 610, 'vertical': True},
            {'name': 'SPRING AVENUE', 'x': 950, 'y': 610, 'vertical': True}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Clubhouse Oasis 1', 'desc': 'Grand 5-pool sports complex with squash, badminton and bowling', 'x': 620, 'y': 440, 'node': 'sda_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'sports', 'name': 'Sobha Athletic Stadium', 'desc': 'Full-size cricket ground, football pitch and synthetic running tracks', 'x': 960, 'y': 260, 'node': 'sda_wing_ne', 'type': 'sports', 'icon': '🏏'}
        ]
    },

    # 4. PRESTIGE SONG OF THE SOUTH (Begur-Koppa Road)
    # Musical themed community along Begur Lakefront
    'prestige_song_south': {
        'groundPolygon': "90,520 220,200 620,150 1020,160 1130,420 1040,780 620,820 200,780 Z",
        'borderTreesPath': "M 90,520 L 220,200 L 620,150 L 1020,160 L 1130,420 L 1040,780 L 620,820 L 200,780 Z",
        'waterBody': {'x': 780, 'y': 170, 'w': 280, 'h': 130, 'rx': 24, 'label': 'Begur Lakefront Nature Promenade'},
        'gardenPark': {'x': 400, 'y': 440, 'w': 240, 'h': 80, 'rx': 10, 'label': 'Musical Amphitheater & Gardens'},
        'defaultStartGate': 'pss_gate_main',
        'nodes': {
            'pss_gate_main':  {'id': 'pss_gate_main', 'x': 90, 'y': 520, 'label': 'Gate 1 (Begur-Koppa Road)'},
            'pss_entry':      {'id': 'pss_entry', 'x': 220, 'y': 520, 'label': 'Song Boulevard Entrance'},
            'pss_junc_w':     {'id': 'pss_junc_w', 'x': 340, 'y': 520, 'label': 'Symphony Way Junction'},
            'pss_junc_ctr':   {'id': 'pss_junc_ctr', 'x': 580, 'y': 520, 'label': 'Grand Symphony Plaza'},
            'pss_junc_lake':  {'id': 'pss_junc_lake', 'x': 840, 'y': 440, 'label': 'Lakeview Promenade Cross'},
            'pss_gate_lake':  {'id': 'pss_gate_lake', 'x': 1100, 'y': 420, 'label': 'Gate 2 (Lakeview Trail Access)'},
            'pss_melody_n':   {'id': 'pss_melody_n', 'x': 480, 'y': 300, 'label': 'Melody Parkway North'},
            'pss_rhythm_ne':  {'id': 'pss_rhythm_ne', 'x': 780, 'y': 320, 'label': 'Rhythm Avenue Promenade'},
            'pss_harmony_s':  {'id': 'pss_harmony_s', 'x': 580, 'y': 700, 'label': 'Harmony Avenue South'}
        },
        'edges': [
            ('pss_gate_main', 'pss_entry', 'Song of South Boulevard', 'primary'),
            ('pss_entry', 'pss_junc_w', 'Song of South Boulevard', 'primary'),
            ('pss_junc_w', 'pss_junc_ctr', 'Song of South Boulevard', 'primary'),
            ('pss_junc_ctr', 'pss_junc_lake', 'Lakeview Promenade', 'primary'),
            ('pss_junc_lake', 'pss_gate_lake', 'Lakeview Promenade', 'primary'),
            ('pss_junc_w', 'pss_melody_n', 'Melody Parkway', 'secondary'),
            ('pss_melody_n', 'pss_rhythm_ne', 'Lakeview Promenade', 'secondary'),
            ('pss_rhythm_ne', 'pss_junc_lake', 'Rhythm Avenue', 'secondary'),
            ('pss_junc_ctr', 'pss_harmony_s', 'Harmony Avenue', 'secondary'),
            ('pss_junc_w', 'pss_harmony_s', 'Symphony Way', 'secondary')
        ],
        'blocks': [
            ('Symphony Tower', 260, 360, 'pss_junc_w', 'Symphony Way', 'East'),
            ('Melody Tower', 480, 240, 'pss_melody_n', 'Melody Parkway', 'South'),
            ('Harmony Tower', 620, 660, 'pss_harmony_s', 'Harmony Avenue', 'North'),
            ('Rhythm Tower', 860, 420, 'pss_junc_lake', 'Lakeview Promenade', 'West')
        ],
        'roadLabels': [
            {'name': 'SONG OF SOUTH BOULEVARD', 'x': 440, 'y': 505, 'vertical': False},
            {'name': 'LAKEVIEW PROMENADE', 'x': 900, 'y': 390, 'vertical': False},
            {'name': 'MELODY PARKWAY', 'x': 430, 'y': 380, 'vertical': True},
            {'name': 'HARMONY AVENUE', 'x': 590, 'y': 620, 'vertical': True}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Grand Symphony Clubhouse', 'desc': 'Double-height clubhouse, gym, mini-theatre & banquet halls', 'x': 580, 'y': 440, 'node': 'pss_junc_ctr', 'type': 'clubhouse', 'icon': '🎭'},
            {'id': 'lake', 'name': 'Lake Promenade & Reflection Deck', 'desc': 'Serene natural lakefront jogging track', 'x': 840, 'y': 220, 'node': 'pss_junc_lake', 'type': 'nature', 'icon': '🌊'}
        ]
    },

    # 5. BRIGADE MILLENNIUM (JP Nagar 7th Phase)
    # Botanical blocks encircling the famous Woodrose Club & MLR Convention Centre
    'brigade_millennium': {
        'groundPolygon': "120,480 240,160 620,130 1000,160 1120,480 1000,800 620,830 240,800 Z",
        'borderTreesPath': "M 120,480 L 240,160 L 620,130 L 1000,160 L 1120,480 L 1000,800 L 620,830 L 240,800 Z",
        'waterBody': {'x': 540, 'y': 430, 'w': 160, 'h': 80, 'rx': 12, 'label': 'Woodrose Club Heated Pool'},
        'gardenPark': {'x': 440, 'y': 310, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Millennium Heritage Tree Park'},
        'landmarks': [
            {'x': 760, 'y': 430, 'w': 180, 'h': 110, 'rx': 8, 'label': '🏛️ MLR Convention Centre', 'fill': '#1e293b', 'stroke': '#a855f7'}
        ],
        'defaultStartGate': 'bm_gate_main',
        'nodes': {
            'bm_gate_main':   {'id': 'bm_gate_main', 'x': 120, 'y': 480, 'label': 'Main Gate (24th Main Road)'},
            'bm_junc_entry':  {'id': 'bm_junc_entry', 'x': 260, 'y': 480, 'label': 'Millennium Boulevard Entrance'},
            'bm_junc_ctr':    {'id': 'bm_junc_ctr', 'x': 620, 'y': 480, 'label': 'Woodrose Central Hub'},
            'bm_gate_east':   {'id': 'bm_gate_east', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Puttenahalli Lake Link)'},
            'bm_cassia_nw':   {'id': 'bm_cassia_nw', 'x': 320, 'y': 280, 'label': 'Cassia Link North'},
            'bm_jacaranda_ne':{'id': 'bm_jacaranda_ne', 'x': 800, 'y': 260, 'label': 'Jacaranda Way North'},
            'bm_laburnum_e':  {'id': 'bm_laburnum_e', 'x': 960, 'y': 480, 'label': 'Laburnum Court East'},
            'bm_magnolia_se': {'id': 'bm_magnolia_se', 'x': 800, 'y': 680, 'label': 'Magnolia Parkway South'},
            'bm_mayflower_sw':{'id': 'bm_mayflower_sw', 'x': 320, 'y': 680, 'label': 'Mayflower Way South'}
        },
        'edges': [
            ('bm_gate_main', 'bm_junc_entry', 'Millennium Boulevard', 'primary'),
            ('bm_junc_entry', 'bm_junc_ctr', 'Millennium Boulevard', 'primary'),
            ('bm_junc_ctr', 'bm_laburnum_e', 'MLR Parkway', 'primary'),
            ('bm_laburnum_e', 'bm_gate_east', 'MLR Parkway', 'primary'),
            ('bm_junc_entry', 'bm_cassia_nw', 'Cassia Link', 'secondary'),
            ('bm_cassia_nw', 'bm_jacaranda_ne', 'Woodrose Club Avenue', 'secondary'),
            ('bm_jacaranda_ne', 'bm_laburnum_e', 'Woodrose Club Avenue', 'secondary'),
            ('bm_junc_entry', 'bm_mayflower_sw', 'Mayflower Way', 'secondary'),
            ('bm_mayflower_sw', 'bm_magnolia_se', 'Woodrose Club Avenue', 'secondary'),
            ('bm_magnolia_se', 'bm_laburnum_e', 'Woodrose Club Avenue', 'secondary'),
            ('bm_junc_ctr', 'bm_cassia_nw', 'Central Link', 'secondary'),
            ('bm_junc_ctr', 'bm_jacaranda_ne', 'Central Link', 'secondary'),
            ('bm_junc_ctr', 'bm_magnolia_se', 'Central Link', 'secondary'),
            ('bm_junc_ctr', 'bm_mayflower_sw', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Cassia Block', 300, 240, 'bm_cassia_nw', 'Cassia Link', 'South'),
            ('Jacaranda Block', 800, 220, 'bm_jacaranda_ne', 'Woodrose Club Avenue', 'South'),
            ('Laburnum Block', 940, 480, 'bm_laburnum_e', 'MLR Parkway', 'West'),
            ('Magnolia Block', 780, 680, 'bm_magnolia_se', 'Woodrose Club Avenue', 'North'),
            ('Mayflower Block', 300, 660, 'bm_mayflower_sw', 'Mayflower Way', 'North')
        ],
        'roadLabels': [
            {'name': 'MILLENNIUM BOULEVARD', 'x': 440, 'y': 465, 'vertical': False},
            {'name': 'WOODROSE CLUB AVENUE', 'x': 620, 'y': 245, 'vertical': False},
            {'name': 'MLR PARKWAY', 'x': 860, 'y': 465, 'vertical': False},
            {'name': 'CASSIA LINK', 'x': 310, 'y': 380, 'vertical': True},
            {'name': 'MAYFLOWER WAY', 'x': 310, 'y': 580, 'vertical': True}
        ],
        'amenities': [
            {'id': 'club', 'name': 'The Woodrose Club', 'desc': 'Renowned country club with swimming pool, squash, tennis, restaurants', 'x': 540, 'y': 440, 'node': 'bm_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'hall', 'name': 'MLR Convention Centre', 'desc': 'Premier 500-seat cultural theatre and convention auditorium', 'x': 760, 'y': 440, 'node': 'bm_laburnum_e', 'type': 'auditorium', 'icon': '🏛️'}
        ]
    },

    # 6. PURVA WESTEND (Kudlu Gate / Hosur Road)
    # Cinema themed with Open Air Cinema & Fantasy Wave Pool
    'purva_westend': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,820 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,820 L 220,800 Z",
        'waterBody': {'x': 500, 'y': 420, 'w': 240, 'h': 90, 'rx': 18, 'label': 'Fantasy Beach Resort Wave Pool'},
        'landmarks': [
            {'x': 440, 'y': 280, 'w': 360, 'h': 70, 'rx': 8, 'label': '🎬 London West End Open Air Cinema', 'fill': '#1e1b4b', 'stroke': '#f43f5e'}
        ],
        'defaultStartGate': 'pw_gate_main',
        'nodes': {
            'pw_gate_main':   {'id': 'pw_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Kudlu Gate Main Entry)'},
            'pw_junc_entry':  {'id': 'pw_junc_entry', 'x': 240, 'y': 480, 'label': 'Westend Boulevard Entrance'},
            'pw_junc_ctr':    {'id': 'pw_junc_ctr', 'x': 620, 'y': 480, 'label': 'Broadway Cinema Plaza'},
            'pw_gate_east':   {'id': 'pw_gate_east', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Hosur Road Link)'},
            'pw_broadway_nw': {'id': 'pw_broadway_nw', 'x': 340, 'y': 270, 'label': 'Broadway Promenade North'},
            'pw_opera_ne':    {'id': 'pw_opera_ne', 'x': 860, 'y': 270, 'label': 'Opera Court North'},
            'pw_westend_sw':  {'id': 'pw_westend_sw', 'x': 340, 'y': 690, 'label': 'West End Drive South'},
            'pw_cinema_se':   {'id': 'pw_cinema_se', 'x': 860, 'y': 690, 'label': 'Cinema Walkway South'}
        },
        'edges': [
            ('pw_gate_main', 'pw_junc_entry', 'Westend Boulevard', 'primary'),
            ('pw_junc_entry', 'pw_junc_ctr', 'Westend Boulevard', 'primary'),
            ('pw_junc_ctr', 'pw_gate_east', 'Westend Boulevard', 'primary'),
            ('pw_junc_entry', 'pw_broadway_nw', 'Broadway Promenade', 'secondary'),
            ('pw_broadway_nw', 'pw_opera_ne', 'Cinema Walkway', 'secondary'),
            ('pw_opera_ne', 'pw_gate_east', 'Opera Court', 'secondary'),
            ('pw_junc_entry', 'pw_westend_sw', 'Kudlu Link', 'secondary'),
            ('pw_westend_sw', 'pw_cinema_se', 'Cinema Walkway', 'secondary'),
            ('pw_cinema_se', 'pw_gate_east', 'Kudlu Link', 'secondary'),
            ('pw_junc_ctr', 'pw_broadway_nw', 'Central Link', 'secondary'),
            ('pw_junc_ctr', 'pw_opera_ne', 'Central Link', 'secondary'),
            ('pw_junc_ctr', 'pw_westend_sw', 'Central Link', 'secondary'),
            ('pw_junc_ctr', 'pw_cinema_se', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Broadway Tower', 300, 220, 'pw_broadway_nw', 'Broadway Promenade', 'South'),
            ('Opera Tower', 860, 220, 'pw_opera_ne', 'Opera Court', 'South'),
            ('West End Tower A', 300, 670, 'pw_westend_sw', 'Westend Boulevard', 'North'),
            ('West End Tower B', 860, 670, 'pw_cinema_se', 'Cinema Walkway', 'North')
        ],
        'roadLabels': [
            {'name': 'WESTEND BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'CINEMA WALKWAY', 'x': 620, 'y': 255, 'vertical': False},
            {'name': 'BROADWAY PROMENADE', 'x': 330, 'y': 380, 'vertical': True},
            {'name': 'OPERA COURT', 'x': 870, 'y': 380, 'vertical': True}
        ],
        'amenities': [
            {'id': 'cinema', 'name': 'Open Air Amphitheatre Cinema', 'desc': 'Private outdoor amphitheatre cinema with acoustic surround sound', 'x': 620, 'y': 310, 'node': 'pw_junc_ctr', 'type': 'entertainment', 'icon': '🎬'},
            {'id': 'pool', 'name': 'Fantasy Wave Pool & Resort Deck', 'desc': 'Artificial beach wave pool, swimming pool and palm cabanas', 'x': 620, 'y': 440, 'node': 'pw_junc_ctr', 'type': 'recreation', 'icon': '🌊'}
        ]
    },

    # 7. PRESTIGE SHANTINIKETAN (ITPL Main Road, Whitefield)
    # 105-acre mega township with Forum Shantiniketan Mall, business campus & crescent towers
    'prestige_shantiniketan': {
        'groundPolygon': "90,480 200,140 620,120 1050,140 1140,480 1050,820 620,840 200,820 Z",
        'borderTreesPath': "M 90,480 L 200,140 L 620,120 L 1050,140 L 1140,480 L 1050,820 L 620,840 L 200,820 Z",
        'gardenPark': {'x': 440, 'y': 360, 'w': 360, 'h': 110, 'rx': 12, 'label': '8-Acre Central Shantiniketan Urban Park'},
        'landmarks': [
            {'x': 420, 'y': 690, 'w': 420, 'h': 90, 'rx': 8, 'label': '🛍️ Forum Shantiniketan Mall & Multiplex', 'fill': '#1e1b4b', 'stroke': '#ec4899'},
            {'x': 180, 'y': 650, 'w': 180, 'h': 120, 'rx': 8, 'label': '💼 Crescent Business Campus', 'fill': '#0f172a', 'stroke': '#38bdf8'}
        ],
        'defaultStartGate': 'psn_gate_main',
        'nodes': {
            'psn_gate_main':  {'id': 'psn_gate_main', 'x': 90, 'y': 480, 'label': 'Gate 1 (ITPL Main Road)'},
            'psn_junc_w':     {'id': 'psn_junc_w', 'x': 240, 'y': 480, 'label': 'Crescent Boulevard West'},
            'psn_junc_ctr':   {'id': 'psn_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Shantiniketan Plaza'},
            'psn_junc_e':     {'id': 'psn_junc_e', 'x': 960, 'y': 480, 'label': 'Manor Way East Junction'},
            'psn_gate_hoodi': {'id': 'psn_gate_hoodi', 'x': 1130, 'y': 480, 'label': 'Gate 2 (Hoodi Railway Station Link)'},
            'psn_crescent_nw':{'id': 'psn_crescent_nw', 'x': 340, 'y': 250, 'label': 'Crescent Towers Cross'},
            'psn_windsor_n':  {'id': 'psn_windsor_n', 'x': 620, 'y': 230, 'label': 'Windsor Park Boulevard'},
            'psn_manor_ne':   {'id': 'psn_manor_ne', 'x': 900, 'y': 260, 'label': 'Manor Crest Way'},
            'psn_forum_s':    {'id': 'psn_forum_s', 'x': 620, 'y': 670, 'label': 'Forum Mall Access Avenue'}
        },
        'edges': [
            ('psn_gate_main', 'psn_junc_w', 'Shantiniketan Boulevard', 'primary'),
            ('psn_junc_w', 'psn_junc_ctr', 'Shantiniketan Boulevard', 'primary'),
            ('psn_junc_ctr', 'psn_junc_e', 'Shantiniketan Boulevard', 'primary'),
            ('psn_junc_e', 'psn_gate_hoodi', 'Shantiniketan Boulevard', 'primary'),
            ('psn_junc_w', 'psn_crescent_nw', 'Crescent Way', 'secondary'),
            ('psn_crescent_nw', 'psn_windsor_n', 'Urban Park Drive', 'secondary'),
            ('psn_windsor_n', 'psn_manor_ne', 'Urban Park Drive', 'secondary'),
            ('psn_manor_ne', 'psn_junc_e', 'Manor Way', 'secondary'),
            ('psn_junc_ctr', 'psn_forum_s', 'Forum Mall Access Avenue', 'primary'),
            ('psn_junc_w', 'psn_forum_s', 'Mall Ring Link', 'secondary'),
            ('psn_junc_e', 'psn_forum_s', 'Mall Ring Link', 'secondary')
        ],
        'blocks': [
            ('Crescent North Tower', 340, 210, 'psn_crescent_nw', 'Crescent Way', 'South'),
            ('Windsor Park Tower', 620, 190, 'psn_windsor_n', 'Urban Park Drive', 'South'),
            ('Manor Crest Tower', 900, 230, 'psn_manor_ne', 'Manor Way', 'South'),
            ('Springs Residential Tower', 320, 440, 'psn_junc_w', 'Shantiniketan Boulevard', 'East')
        ],
        'roadLabels': [
            {'name': 'SHANTINIKETAN BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'URBAN PARK DRIVE', 'x': 620, 'y': 215, 'vertical': False},
            {'name': 'FORUM MALL ACCESS AVENUE', 'x': 620, 'y': 635, 'vertical': False},
            {'name': 'CRESCENT WAY', 'x': 250, 'y': 365, 'vertical': True}
        ],
        'amenities': [
            {'id': 'mall', 'name': 'Forum Shantiniketan Mall', 'desc': 'Flagship lifestyle destination with 200+ brands, IMAX cinema and open-air plaza', 'x': 620, 'y': 730, 'node': 'psn_forum_s', 'type': 'mall', 'icon': '🛍️'},
            {'id': 'club', 'name': 'Shantiniketan Club', 'desc': 'Expansive sports pavilion, squash courts, tennis, gym and swimming pool', 'x': 620, 'y': 410, 'node': 'psn_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # 8. BHARTIYA CITY NIKOO HOMES (Thanisandra Main Road)
    # 125-acre integrated smart city with High Street Rambler & Central Park
    'bhartiya_city': {
        'groundPolygon': "80,480 180,140 620,130 1060,140 1150,480 1060,820 620,830 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 620,130 L 1060,140 L 1150,480 L 1060,820 L 620,830 L 180,820 Z",
        'gardenPark': {'x': 500, 'y': 380, 'w': 260, 'h': 120, 'rx': 14, 'label': '7-Acre Smart Central Park & Lake'},
        'waterBody': {'x': 540, 'y': 440, 'w': 180, 'h': 50, 'rx': 10, 'label': 'Smart Lake & Swan Pond'},
        'landmarks': [
            {'x': 420, 'y': 260, 'w': 420, 'h': 55, 'rx': 6, 'label': '🛍️ Bhartiya Rambler High Street Retail', 'fill': '#1e1b4b', 'stroke': '#3b82f6'}
        ],
        'defaultStartGate': 'bc_gate_main',
        'nodes': {
            'bc_gate_main':   {'id': 'bc_gate_main', 'x': 80, 'y': 480, 'label': 'Gate 1 (Thanisandra Main Road)'},
            'bc_junc_w':      {'id': 'bc_junc_w', 'x': 240, 'y': 480, 'label': 'Nikoo Boulevard West'},
            'bc_junc_ctr':    {'id': 'bc_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Smart Park Plaza'},
            'bc_junc_e':      {'id': 'bc_junc_e', 'x': 920, 'y': 480, 'label': 'Bhartiya High Street Cross'},
            'bc_gate_east':   {'id': 'bc_gate_east', 'x': 1130, 'y': 480, 'label': 'Gate 2 (Chikkagubbi Link)'},
            'bc_nikoo_nw':    {'id': 'bc_nikoo_nw', 'x': 340, 'y': 280, 'label': 'Nikoo Homes A Parkway'},
            'bc_rambler_ne':  {'id': 'bc_rambler_ne', 'x': 860, 'y': 280, 'label': 'Rambler High Street North'},
            'bc_nikoo_sw':    {'id': 'bc_nikoo_sw', 'x': 340, 'y': 690, 'label': 'Nikoo Homes B Parkway'},
            'bc_park_se':     {'id': 'bc_park_se', 'x': 860, 'y': 690, 'label': 'Central Park South Drive'}
        },
        'edges': [
            ('bc_gate_main', 'bc_junc_w', 'Nikoo Boulevard', 'primary'),
            ('bc_junc_w', 'bc_junc_ctr', 'Nikoo Boulevard', 'primary'),
            ('bc_junc_ctr', 'bc_junc_e', 'Nikoo Boulevard', 'primary'),
            ('bc_junc_e', 'bc_gate_east', 'Bhartiya High Street', 'primary'),
            ('bc_junc_w', 'bc_nikoo_nw', 'Nikoo Boulevard', 'secondary'),
            ('bc_nikoo_nw', 'bc_rambler_ne', 'Rambler Way', 'secondary'),
            ('bc_rambler_ne', 'bc_junc_e', 'Bhartiya High Street', 'secondary'),
            ('bc_junc_w', 'bc_nikoo_sw', 'Central Park Parkway', 'secondary'),
            ('bc_nikoo_sw', 'bc_park_se', 'Central Park Parkway', 'secondary'),
            ('bc_park_se', 'bc_junc_e', 'Bhartiya High Street', 'secondary'),
            ('bc_junc_ctr', 'bc_nikoo_nw', 'Central Link', 'secondary'),
            ('bc_junc_ctr', 'bc_nikoo_sw', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Nikoo Homes A', 340, 240, 'bc_nikoo_nw', 'Nikoo Boulevard', 'South'),
            ('Nikoo Homes B', 340, 680, 'bc_nikoo_sw', 'Central Park Parkway', 'North'),
            ('Central Park Enclave', 860, 450, 'bc_junc_e', 'Bhartiya High Street', 'West'),
            ('Sky Villa Tower', 860, 220, 'bc_rambler_ne', 'Rambler Way', 'South')
        ],
        'roadLabels': [
            {'name': 'NIKOO BOULEVARD', 'x': 440, 'y': 495, 'vertical': False},
            {'name': 'BHARTIYA HIGH STREET', 'x': 920, 'y': 380, 'vertical': True},
            {'name': 'RAMBLER WAY', 'x': 620, 'y': 245, 'vertical': False},
            {'name': 'CENTRAL PARK PARKWAY', 'x': 620, 'y': 715, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'The Black Swan Clubhouse', 'desc': 'Smart city clubhouse, infinity rooftop pool, cycling track and theatre', 'x': 620, 'y': 380, 'node': 'bc_junc_ctr', 'type': 'clubhouse', 'icon': '🦢'},
            {'id': 'park', 'name': 'Central Park Smart Promenade', 'desc': '7-acre smart park with interactive water features and outdoor fitness', 'x': 620, 'y': 440, 'node': 'bc_junc_ctr', 'type': 'park', 'icon': '🌳'}
        ]
    },

    # 9. SOBHA CITY (Thanisandra Main Road)
    # Mediterranean-themed township with 4-acre lagoon & sandy beach
    'sobha_city': {
        'groundPolygon': "100,480 220,150 620,120 1020,150 1140,480 1020,810 620,840 220,810 Z",
        'borderTreesPath': "M 100,480 Q 220,130 620,120 Q 1020,130 1140,480 Q 1020,830 620,840 Q 220,830 100,480 Z",
        'waterBody': {'x': 460, 'y': 380, 'w': 320, 'h': 140, 'rx': 28, 'label': '4-Acre Mediterranean Sand Lagoon & Water Sports'},
        'gardenPark': {'x': 440, 'y': 250, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Mediterranean Pebble Promenade & Lawns'},
        'defaultStartGate': 'sc_gate_main',
        'nodes': {
            'sc_gate_main':   {'id': 'sc_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Thanisandra Main Road)'},
            'sc_junc_w':      {'id': 'sc_junc_w', 'x': 240, 'y': 480, 'label': 'Sobha City Boulevard West'},
            'sc_junc_ctr':    {'id': 'sc_junc_ctr', 'x': 620, 'y': 480, 'label': 'Grand Mediterranean Plaza'},
            'sc_junc_e':      {'id': 'sc_junc_e', 'x': 980, 'y': 480, 'label': 'Santorini Way East'},
            'sc_gate_east':   {'id': 'sc_gate_east', 'x': 1130, 'y': 480, 'label': 'Gate 2 (Service Exit)'},
            'sc_santorini_nw':{'id': 'sc_santorini_nw', 'x': 320, 'y': 280, 'label': 'Santorini Way North'},
            'sc_casaserena_ne':{'id': 'sc_casaserena_ne', 'x': 900, 'y': 280, 'label': 'Casa Serena Parkway'},
            'sc_amalfi_sw':   {'id': 'sc_amalfi_sw', 'x': 320, 'y': 680, 'label': 'Amalfi Way South'},
            'sc_mykonos_se':  {'id': 'sc_mykonos_se', 'x': 900, 'y': 680, 'label': 'Mykonos & Amphitheater Cross'}
        },
        'edges': [
            ('sc_gate_main', 'sc_junc_w', 'Sobha City Boulevard', 'primary'),
            ('sc_junc_w', 'sc_junc_ctr', 'Sobha City Boulevard', 'primary'),
            ('sc_junc_ctr', 'sc_junc_e', 'Sobha City Boulevard', 'primary'),
            ('sc_junc_e', 'sc_gate_east', 'Sobha City Boulevard', 'primary'),
            ('sc_junc_w', 'sc_santorini_nw', 'Santorini Way', 'secondary'),
            ('sc_santorini_nw', 'sc_casaserena_ne', 'Casa Serena Parkway', 'secondary'),
            ('sc_casaserena_ne', 'sc_junc_e', 'Casa Serena Parkway', 'secondary'),
            ('sc_junc_w', 'sc_amalfi_sw', 'Amalfi Way', 'secondary'),
            ('sc_amalfi_sw', 'sc_mykonos_se', 'Amphitheater Drive', 'secondary'),
            ('sc_mykonos_se', 'sc_junc_e', 'Amphitheater Drive', 'secondary'),
            ('sc_junc_ctr', 'sc_santorini_nw', 'Central Link', 'secondary'),
            ('sc_junc_ctr', 'sc_casaserena_ne', 'Central Link', 'secondary'),
            ('sc_junc_ctr', 'sc_amalfi_sw', 'Central Link', 'secondary'),
            ('sc_junc_ctr', 'sc_mykonos_se', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Santorini Tower', 280, 240, 'sc_santorini_nw', 'Santorini Way', 'South'),
            ('Casa Serena Tower', 860, 240, 'sc_casaserena_ne', 'Casa Serena Parkway', 'South'),
            ('Mykonos Block', 860, 660, 'sc_mykonos_se', 'Amphitheater Drive', 'North'),
            ('Amalfi Wing', 280, 660, 'sc_amalfi_sw', 'Amalfi Way', 'North')
        ],
        'roadLabels': [
            {'name': 'SOBHA CITY BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'CASA SERENA PARKWAY', 'x': 620, 'y': 265, 'vertical': False},
            {'name': 'AMPHITHEATER DRIVE', 'x': 620, 'y': 705, 'vertical': False},
            {'name': 'SANTORINI WAY', 'x': 310, 'y': 380, 'vertical': True}
        ],
        'amenities': [
            {'id': 'lagoon', 'name': 'Mediterranean Beach Lagoon', 'desc': '4-acre sand beach lagoon with canoeing, beach volleyball and boardwalk', 'x': 620, 'y': 440, 'node': 'sc_junc_ctr', 'type': 'water', 'icon': '🏖️'},
            {'id': 'club', 'name': 'Club Santorini', 'desc': 'Grand Mediterranean clubhouse, Olympic pool and amphitheater', 'x': 620, 'y': 250, 'node': 'sc_junc_ctr', 'type': 'clubhouse', 'icon': '🏛️'}
        ]
    },

    # 10. RMZ GALLERIA (Yelahanka)
    # Mixed-use development with RMZ Galleria Mall at base and twin residential towers on podium
    'rmz_galleria': {
        'groundPolygon': "110,480 220,180 620,160 1020,180 1110,480 1020,780 620,800 220,780 Z",
        'borderTreesPath': "M 110,480 L 220,180 L 620,160 L 1020,180 L 1110,480 L 1020,780 L 620,800 L 220,780 Z",
        'waterBody': {'x': 520, 'y': 420, 'w': 200, 'h': 70, 'rx': 14, 'label': 'Podium Sky Infinity Pool & Sun Deck'},
        'landmarks': [
            {'x': 360, 'y': 640, 'w': 520, 'h': 110, 'rx': 8, 'label': '🛍️ RMZ Galleria Mall & INOX Multiplex', 'fill': '#1e1b4b', 'stroke': '#6366f1'}
        ],
        'defaultStartGate': 'rmz_gate_main',
        'nodes': {
            'rmz_gate_main':  {'id': 'rmz_gate_main', 'x': 110, 'y': 480, 'label': 'Gate 1 (Yelahanka Main Road)'},
            'rmz_junc_w':     {'id': 'rmz_junc_w', 'x': 260, 'y': 480, 'label': 'Galleria Boulevard West'},
            'rmz_junc_ctr':   {'id': 'rmz_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Galleria Plaza'},
            'rmz_junc_e':     {'id': 'rmz_junc_e', 'x': 960, 'y': 480, 'label': 'Mall Ring Link East'},
            'rmz_gate_east':  {'id': 'rmz_gate_east', 'x': 1100, 'y': 480, 'label': 'Gate 2 (BBMP Office Link)'},
            'rmz_tower_a':    {'id': 'rmz_tower_a', 'x': 360, 'y': 310, 'label': 'Tower A Podium Access'},
            'rmz_tower_b':    {'id': 'rmz_tower_b', 'x': 860, 'y': 310, 'label': 'Tower B Podium Access'},
            'rmz_mall_s':     {'id': 'rmz_mall_s', 'x': 620, 'y': 620, 'label': 'Galleria Mall Entrance Court'}
        },
        'edges': [
            ('rmz_gate_main', 'rmz_junc_w', 'Galleria Boulevard', 'primary'),
            ('rmz_junc_w', 'rmz_junc_ctr', 'Galleria Boulevard', 'primary'),
            ('rmz_junc_ctr', 'rmz_junc_e', 'Galleria Boulevard', 'primary'),
            ('rmz_junc_e', 'rmz_gate_east', 'Galleria Boulevard', 'primary'),
            ('rmz_junc_w', 'rmz_tower_a', 'Yelahanka Main Parkway', 'secondary'),
            ('rmz_tower_a', 'rmz_tower_b', 'Sky Deck Promenade', 'secondary'),
            ('rmz_tower_b', 'rmz_junc_e', 'Mall Ring Link', 'secondary'),
            ('rmz_junc_w', 'rmz_mall_s', 'Mall Ring Link', 'primary'),
            ('rmz_mall_s', 'rmz_junc_e', 'Mall Ring Link', 'primary'),
            ('rmz_junc_ctr', 'rmz_mall_s', 'Central Link', 'primary')
        ],
        'blocks': [
            ('Tower A', 360, 270, 'rmz_tower_a', 'Galleria Boulevard', 'South'),
            ('Tower B', 780, 270, 'rmz_tower_b', 'Mall Ring Link', 'South')
        ],
        'roadLabels': [
            {'name': 'GALLERIA BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'SKY DECK PROMENADE', 'x': 620, 'y': 295, 'vertical': False},
            {'name': 'MALL RING LINK', 'x': 620, 'y': 605, 'vertical': False}
        ],
        'amenities': [
            {'id': 'mall', 'name': 'RMZ Galleria Mall', 'desc': 'Iconic Yelahanka lifestyle destination with 100+ stores & food court', 'x': 620, 'y': 680, 'node': 'rmz_mall_s', 'type': 'mall', 'icon': '🛍️'},
            {'id': 'deck', 'name': 'Podium Sky Club', 'desc': 'Rooftop infinity swimming pool, sky lounge and gym', 'x': 620, 'y': 420, 'node': 'rmz_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # 11. WHITEFIELD INNER CIRCLE (Whitefield Heritage)
    # Historic concentric circle layout with colonial circular park and radial links
    'whitefield_inner_circle': {
        'groundPolygon': "620,120 900,180 1080,360 1140,480 1080,600 900,780 620,840 340,780 160,600 100,480 160,360 340,180 Z",
        'borderTreesPath': "M 620,120 L 900,180 L 1080,360 L 1140,480 L 1080,600 L 900,780 L 620,840 L 340,780 L 160,600 L 100,480 L 160,360 L 340,180 Z",
        'gardenPark': {'x': 480, 'y': 380, 'w': 280, 'h': 200, 'rx': 100, 'label': 'Historic Whitefield Inner Circle Heritage Park'},
        'defaultStartGate': 'wic_gate_west',
        'nodes': {
            'wic_gate_west':  {'id': 'wic_gate_west', 'x': 100, 'y': 480, 'label': 'Gate 1 (Whitefield Main Road)'},
            'wic_out_w':      {'id': 'wic_out_w', 'x': 220, 'y': 480, 'label': 'Outer Circle West Cross'},
            'wic_in_w':       {'id': 'wic_in_w', 'x': 380, 'y': 480, 'label': 'Inner Circle West'},
            'wic_park_ctr':   {'id': 'wic_park_ctr', 'x': 620, 'y': 480, 'label': 'Historic Gazebo Hub'},
            'wic_in_e':       {'id': 'wic_in_e', 'x': 860, 'y': 480, 'label': 'Inner Circle East'},
            'wic_out_e':      {'id': 'wic_out_e', 'x': 1020, 'y': 480, 'label': 'Outer Circle East Cross'},
            'wic_gate_east':  {'id': 'wic_gate_east', 'x': 1130, 'y': 480, 'label': 'Gate 2 (Post Office Road Link)'},
            'wic_in_n':       {'id': 'wic_in_n', 'x': 620, 'y': 280, 'label': 'Inner Circle North'},
            'wic_out_n':      {'id': 'wic_out_n', 'x': 620, 'y': 160, 'label': 'Outer Circle North (Waverly Way)'},
            'wic_in_s':       {'id': 'wic_in_s', 'x': 620, 'y': 680, 'label': 'Inner Circle South'},
            'wic_out_s':      {'id': 'wic_out_s', 'x': 620, 'y': 800, 'label': 'Outer Circle South'}
        },
        'edges': [
            ('wic_gate_west', 'wic_out_w', 'Church Street Link', 'primary'),
            ('wic_out_w', 'wic_in_w', 'Church Street Link', 'primary'),
            ('wic_in_w', 'wic_park_ctr', 'Inner Circle Boulevard', 'primary'),
            ('wic_park_ctr', 'wic_in_e', 'Inner Circle Boulevard', 'primary'),
            ('wic_in_e', 'wic_out_e', 'Post Office Road', 'primary'),
            ('wic_out_e', 'wic_gate_east', 'Post Office Road', 'primary'),
            ('wic_in_w', 'wic_in_n', 'Inner Circle Boulevard', 'secondary'),
            ('wic_in_n', 'wic_in_e', 'Inner Circle Boulevard', 'secondary'),
            ('wic_in_e', 'wic_in_s', 'Inner Circle Boulevard', 'secondary'),
            ('wic_in_s', 'wic_in_w', 'Inner Circle Boulevard', 'secondary'),
            ('wic_out_w', 'wic_out_n', 'Outer Circle Way', 'secondary'),
            ('wic_out_n', 'wic_out_e', 'Outer Circle Way', 'secondary'),
            ('wic_out_e', 'wic_out_s', 'Outer Circle Way', 'secondary'),
            ('wic_out_s', 'wic_out_w', 'Outer Circle Way', 'secondary'),
            ('wic_in_n', 'wic_out_n', 'Waverly Road Parkway', 'secondary'),
            ('wic_in_s', 'wic_out_s', 'Waverly Road Parkway', 'secondary')
        ],
        'roadLabels': [
            {'name': 'INNER CIRCLE BOULEVARD', 'x': 620, 'y': 265, 'vertical': False},
            {'name': 'OUTER CIRCLE WAY', 'x': 620, 'y': 145, 'vertical': False},
            {'name': 'CHURCH STREET LINK', 'x': 250, 'y': 495, 'vertical': False},
            {'name': 'WAVERLY ROAD PARKWAY', 'x': 630, 'y': 740, 'vertical': True}
        ],
        'amenities': [
            {'id': 'park', 'name': 'Whitefield Inner Circle Heritage Park', 'desc': 'Colonial circular park with giant rain trees and heritage gazebo', 'x': 620, 'y': 480, 'node': 'wic_park_ctr', 'type': 'park', 'icon': '🌳'}
        ]
    },

    # 12. SOUTH CITY LAYOUT (Arekere / Bannerghatta Road)
    # 34-acre high-rise enclave overlooking Arekere Lake
    'south_city_layout': {
        'groundPolygon': "90,480 200,160 620,140 1040,160 1120,480 1040,820 620,850 200,820 Z",
        'borderTreesPath': "M 90,480 L 200,160 L 620,140 L 1040,160 L 1120,480 L 1040,820 L 620,850 L 200,820 Z",
        'waterBody': {'x': 360, 'y': 730, 'w': 520, 'h': 80, 'rx': 16, 'label': 'Arekere Lakefront Boardwalk & Wetland Bird Zone'},
        'gardenPark': {'x': 440, 'y': 440, 'w': 360, 'h': 70, 'rx': 10, 'label': 'South City Central Woodlands Park'},
        'defaultStartGate': 'scl_gate_main',
        'nodes': {
            'scl_gate_main':  {'id': 'scl_gate_main', 'x': 90, 'y': 480, 'label': 'Gate 1 (Bannerghatta Main Road)'},
            'scl_junc_w':     {'id': 'scl_junc_w', 'x': 240, 'y': 480, 'label': 'South City West Boulevard Cross'},
            'scl_junc_ctr':   {'id': 'scl_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Woodlands Plaza'},
            'scl_junc_e':     {'id': 'scl_junc_e', 'x': 960, 'y': 480, 'label': 'Parkside East Junction'},
            'scl_gate_lake':  {'id': 'scl_gate_lake', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Arekere Lake Trail Link)'},
            'scl_north_quad': {'id': 'scl_north_quad', 'x': 360, 'y': 260, 'label': 'North Quad Drive'},
            'scl_park_ne':    {'id': 'scl_park_ne', 'x': 780, 'y': 260, 'label': 'Central Parkside Way'},
            'scl_south_lake': {'id': 'scl_south_lake', 'x': 520, 'y': 680, 'label': 'South Lake Promenade'}
        },
        'edges': [
            ('scl_gate_main', 'scl_junc_w', 'South City Boulevard', 'primary'),
            ('scl_junc_w', 'scl_junc_ctr', 'South City Boulevard', 'primary'),
            ('scl_junc_ctr', 'scl_junc_e', 'South City Boulevard', 'primary'),
            ('scl_junc_e', 'scl_gate_lake', 'South City Boulevard', 'primary'),
            ('scl_junc_w', 'scl_north_quad', 'North Quad Drive', 'secondary'),
            ('scl_north_quad', 'scl_park_ne', 'Woodlands Parkway', 'secondary'),
            ('scl_park_ne', 'scl_junc_e', 'Central Parkside Way', 'secondary'),
            ('scl_junc_w', 'scl_south_lake', 'South Lake Promenade', 'secondary'),
            ('scl_south_lake', 'scl_junc_e', 'South Lake Promenade', 'secondary'),
            ('scl_junc_ctr', 'scl_south_lake', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('North Quad Tower', 360, 210, 'scl_north_quad', 'North Quad Drive', 'South'),
            ('Central Parkside Tower', 740, 210, 'scl_park_ne', 'Central Parkside Way', 'South'),
            ('South Lakeview Tower', 520, 630, 'scl_south_lake', 'South Lake Promenade', 'North')
        ],
        'roadLabels': [
            {'name': 'SOUTH CITY BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'WOODLANDS PARKWAY', 'x': 620, 'y': 245, 'vertical': False},
            {'name': 'SOUTH LAKE PROMENADE', 'x': 620, 'y': 665, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'South City Clubhouse & Sports Deck', 'desc': 'Tennis courts, squash, swimming pool and fitness center', 'x': 620, 'y': 440, 'node': 'scl_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'lake', 'name': 'Arekere Lake Boardwalk', 'desc': 'Restored lakefront jogging tracks and wetland bird watching zone', 'x': 620, 'y': 730, 'node': 'scl_south_lake', 'type': 'nature', 'icon': '🦆'}
        ]
    },

    # 13. PRESTIGE LAKESIDE HABITAT (Varthur)
    # 102-acre Disney themed community on the shores of Varthur Lake
    'prestige_lakeside': {
        'groundPolygon': "90,480 200,160 620,130 1040,160 1120,480 1040,820 620,840 200,820 Z",
        'borderTreesPath': "M 90,480 L 200,160 L 620,130 L 1040,160 L 1120,480 L 1040,820 L 620,840 L 200,820 Z",
        'waterBody': {'x': 200, 'y': 140, 'w': 820, 'h': 80, 'rx': 18, 'label': 'Varthur Lakefront Promenade & Water Sports'},
        'gardenPark': {'x': 440, 'y': 440, 'w': 360, 'h': 70, 'rx': 10, 'label': 'Disney Fantasy Fairway Gardens'},
        'defaultStartGate': 'plh_gate_main',
        'nodes': {
            'plh_gate_main':  {'id': 'plh_gate_main', 'x': 90, 'y': 480, 'label': 'Gate 1 (Varthur Main Road)'},
            'plh_junc_w':     {'id': 'plh_junc_w', 'x': 240, 'y': 480, 'label': 'Lakeside Boulevard West'},
            'plh_junc_ctr':   {'id': 'plh_junc_ctr', 'x': 620, 'y': 480, 'label': 'Disney Fantasy Plaza'},
            'plh_junc_e':     {'id': 'plh_junc_e', 'x': 960, 'y': 480, 'label': 'Lakeside Boulevard East'},
            'plh_gate_lake':  {'id': 'plh_gate_lake', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Lake Promenade Link)'},
            'plh_lake_a':     {'id': 'plh_lake_a', 'x': 300, 'y': 280, 'label': 'Lakeview Tower A Parkway'},
            'plh_lake_b':     {'id': 'plh_lake_b', 'x': 600, 'y': 260, 'label': 'Lakeview Tower B Parkway'},
            'plh_lake_c':     {'id': 'plh_lake_c', 'x': 900, 'y': 280, 'label': 'Lakeview Tower C Parkway'},
            'plh_villa_s':    {'id': 'plh_villa_s', 'x': 600, 'y': 690, 'label': 'Disney Villa Fairway Cross'}
        },
        'edges': [
            ('plh_gate_main', 'plh_junc_w', 'Lakeside Boulevard', 'primary'),
            ('plh_junc_w', 'plh_junc_ctr', 'Lakeside Boulevard', 'primary'),
            ('plh_junc_ctr', 'plh_junc_e', 'Lakeside Boulevard', 'primary'),
            ('plh_junc_e', 'plh_gate_lake', 'Lakeside Boulevard', 'primary'),
            ('plh_junc_w', 'plh_lake_a', 'Lakeview Drive', 'secondary'),
            ('plh_lake_a', 'plh_lake_b', 'Lakeview Drive', 'secondary'),
            ('plh_lake_b', 'plh_lake_c', 'Lakeview Drive', 'secondary'),
            ('plh_lake_c', 'plh_junc_e', 'Lakeview Drive', 'secondary'),
            ('plh_junc_w', 'plh_villa_s', 'Disney Fairway', 'secondary'),
            ('plh_villa_s', 'plh_junc_e', 'Disney Fairway', 'secondary'),
            ('plh_junc_ctr', 'plh_villa_s', 'Central Link', 'secondary'),
            ('plh_junc_ctr', 'plh_lake_b', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Lakeview Tower A', 300, 240, 'plh_lake_a', 'Lakeside Boulevard', 'South'),
            ('Lakeview Tower B', 600, 220, 'plh_lake_b', 'Lakeside Boulevard', 'South'),
            ('Lakeview Tower C', 900, 240, 'plh_lake_c', 'Lakeside Boulevard', 'South'),
            ('Disney Villa Enclave', 600, 660, 'plh_villa_s', 'Disney Fairway', 'North')
        ],
        'roadLabels': [
            {'name': 'LAKESIDE BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'LAKEVIEW DRIVE', 'x': 600, 'y': 245, 'vertical': False},
            {'name': 'DISNEY FAIRWAY', 'x': 600, 'y': 675, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Disney Grand Fantasy Clubhouse', 'desc': 'Double-deck Olympic pool, bowling alley, cricket pitch & cafe', 'x': 620, 'y': 440, 'node': 'plh_junc_ctr', 'type': 'clubhouse', 'icon': '🏰'},
            {'id': 'lake', 'name': 'Varthur Lake Viewing Promenade', 'desc': 'Scenic pedestrian boardwalk and sunset pavilion on Varthur waters', 'x': 600, 'y': 150, 'node': 'plh_lake_b', 'type': 'nature', 'icon': '🌊'}
        ]
    },

    # 14. MANTRI TRANQUIL (Kanakapura Road / Gubbalala)
    # Hillside stepped terraced towers adjacent to Turahalli Forest
    'mantri_tranquil': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,830 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,830 L 220,800 Z",
        'gardenPark': {'x': 440, 'y': 380, 'w': 360, 'h': 80, 'rx': 10, 'label': 'Turahalli Forest View Terraced Gardens'},
        'waterBody': {'x': 540, 'y': 480, 'w': 160, 'h': 70, 'rx': 12, 'label': 'Club Tranquil Heated Indoor Pool'},
        'defaultStartGate': 'mt_gate_main',
        'nodes': {
            'mt_gate_main':   {'id': 'mt_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Kanakapura Main Road)'},
            'mt_junc_w':      {'id': 'mt_junc_w', 'x': 240, 'y': 480, 'label': 'West Ridge Roundabout'},
            'mt_junc_ctr':    {'id': 'mt_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Valley Plaza'},
            'mt_junc_e':      {'id': 'mt_junc_e', 'x': 960, 'y': 480, 'label': 'East Forest Junction'},
            'mt_gate_forest': {'id': 'mt_gate_forest', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Turahalli Forest Link)'},
            'mt_ridge_w':     {'id': 'mt_ridge_w', 'x': 300, 'y': 280, 'label': 'Tower A-C Ridge Drive'},
            'mt_ridge_n':     {'id': 'mt_ridge_n', 'x': 620, 'y': 240, 'label': 'Tower D-F North Cross'},
            'mt_valley_e':    {'id': 'mt_valley_e', 'x': 900, 'y': 340, 'label': 'Tower G-H Valley Way'},
            'mt_ridge_s':     {'id': 'mt_ridge_s', 'x': 620, 'y': 690, 'label': 'Tower J South Ridge Drive'}
        },
        'edges': [
            ('mt_gate_main', 'mt_junc_w', 'Tranquil Boulevard', 'primary'),
            ('mt_junc_w', 'mt_junc_ctr', 'Tranquil Boulevard', 'primary'),
            ('mt_junc_ctr', 'mt_junc_e', 'Tranquil Boulevard', 'primary'),
            ('mt_junc_e', 'mt_gate_forest', 'Tranquil Boulevard', 'primary'),
            ('mt_junc_w', 'mt_ridge_w', 'Forest View Link', 'secondary'),
            ('mt_ridge_w', 'mt_ridge_n', 'Forest View Link', 'secondary'),
            ('mt_ridge_n', 'mt_valley_e', 'Forest View Link', 'secondary'),
            ('mt_valley_e', 'mt_junc_e', 'Forest View Link', 'secondary'),
            ('mt_junc_w', 'mt_ridge_s', 'Gubbalala Parkway', 'secondary'),
            ('mt_ridge_s', 'mt_junc_e', 'Gubbalala Parkway', 'secondary'),
            ('mt_junc_ctr', 'mt_ridge_n', 'Central Promenade', 'primary'),
            ('mt_junc_ctr', 'mt_ridge_s', 'Central Promenade', 'primary')
        ],
        'blocks': [
            ('Tower A-C', 300, 260, 'mt_ridge_w', 'Tranquil Boulevard', 'South'),
            ('Tower D-F', 620, 220, 'mt_ridge_n', 'Forest View Link', 'South'),
            ('Tower G-H', 880, 320, 'mt_valley_e', 'Central Promenade', 'West'),
            ('Tower J', 620, 670, 'mt_ridge_s', 'Gubbalala Parkway', 'North')
        ],
        'roadLabels': [
            {'name': 'TRANQUIL BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'FOREST VIEW LINK', 'x': 620, 'y': 225, 'vertical': False},
            {'name': 'GUBBALALA PARKWAY', 'x': 620, 'y': 675, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Club Tranquil', 'desc': 'Indoor badminton, squash, heated pool, sauna & health spa', 'x': 620, 'y': 440, 'node': 'mt_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'nature', 'name': 'Turahalli Forest Trail Access', 'desc': 'Direct private gateway to Turahalli rock hillocks & nature preserve', 'x': 960, 'y': 480, 'node': 'mt_gate_forest', 'type': 'nature', 'icon': '🌲'}
        ]
    },

    # 15. BRIGADE MEADOWS (Kanakapura Road / Saaket)
    # 60-acre self-contained satellite township
    'brigade_meadows': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,830 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,830 L 220,800 Z",
        'waterBody': {'x': 520, 'y': 440, 'w': 200, 'h': 75, 'rx': 14, 'label': 'Meadows Sports Complex & Swimming Pool'},
        'landmarks': [
            {'x': 740, 'y': 440, 'w': 180, 'h': 90, 'rx': 8, 'label': '🏪 Meadows Commercial Arcade & Clinic', 'fill': '#1e1b4b', 'stroke': '#38bdf8'}
        ],
        'defaultStartGate': 'bme_gate_main',
        'nodes': {
            'bme_gate_main':  {'id': 'bme_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Kanakapura Expressway)'},
            'bme_junc_w':     {'id': 'bme_junc_w', 'x': 240, 'y': 480, 'label': 'Meadows West Junction'},
            'bme_junc_ctr':   {'id': 'bme_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Arcade Plaza'},
            'bme_junc_e':     {'id': 'bme_junc_e', 'x': 960, 'y': 480, 'label': 'Wisteria East Cross'},
            'bme_gate_east':  {'id': 'bme_gate_east', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Koppa Link)'},
            'bme_plumeria':   {'id': 'bme_plumeria', 'x': 320, 'y': 280, 'label': 'Plumeria Drive'},
            'bme_wisteria':   {'id': 'bme_wisteria', 'x': 840, 'y': 280, 'label': 'Wisteria Way'},
            'bme_saaket':     {'id': 'bme_saaket', 'x': 580, 'y': 690, 'label': 'Saaket Link South'}
        },
        'edges': [
            ('bme_gate_main', 'bme_junc_w', 'Meadows Boulevard', 'primary'),
            ('bme_junc_w', 'bme_junc_ctr', 'Meadows Boulevard', 'primary'),
            ('bme_junc_ctr', 'bme_junc_e', 'Meadows Boulevard', 'primary'),
            ('bme_junc_e', 'bme_gate_east', 'Meadows Boulevard', 'primary'),
            ('bme_junc_w', 'bme_plumeria', 'Plumeria Drive', 'secondary'),
            ('bme_plumeria', 'bme_wisteria', 'Kanakapura Corridor', 'secondary'),
            ('bme_wisteria', 'bme_junc_e', 'Wisteria Way', 'secondary'),
            ('bme_junc_w', 'bme_saaket', 'Saaket Link', 'secondary'),
            ('bme_saaket', 'bme_junc_e', 'Saaket Link', 'secondary'),
            ('bme_junc_ctr', 'bme_saaket', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Plumeria Tower', 300, 240, 'bme_plumeria', 'Plumeria Drive', 'South'),
            ('Wisteria Tower', 840, 240, 'bme_wisteria', 'Wisteria Way', 'South'),
            ('Saaket Block', 580, 670, 'bme_saaket', 'Saaket Link', 'North')
        ],
        'roadLabels': [
            {'name': 'MEADOWS BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'KANAKAPURA CORRIDOR', 'x': 620, 'y': 265, 'vertical': False},
            {'name': 'SAAKET LINK', 'x': 620, 'y': 675, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Club Meadows', 'desc': 'Clubhouse, lap pool, badminton court, gym & banquet', 'x': 620, 'y': 440, 'node': 'bme_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'},
            {'id': 'arcade', 'name': 'Signature Commercial Arcade', 'desc': 'Supermarket, clinic, pharmacy and coffee shop', 'x': 740, 'y': 440, 'node': 'bme_junc_ctr', 'type': 'civic', 'icon': '🏪'}
        ]
    },

    # 16. PURVA PANORAMA (Bannerghatta Road / Kalena Agrahara)
    # High-rise society on elevated ground with panoramic vistas
    'purva_panorama': {
        'groundPolygon': "110,480 220,180 620,160 1020,180 1110,480 1020,780 620,800 220,780 Z",
        'borderTreesPath': "M 110,480 L 220,180 L 620,160 L 1020,180 L 1110,480 L 1020,780 L 620,800 L 220,780 Z",
        'waterBody': {'x': 520, 'y': 430, 'w': 200, 'h': 75, 'rx': 14, 'label': 'Panorama Infinity Edge Pool & Spa'},
        'defaultStartGate': 'pp_gate_main',
        'nodes': {
            'pp_gate_main':   {'id': 'pp_gate_main', 'x': 110, 'y': 480, 'label': 'Gate 1 (Bannerghatta Main Road)'},
            'pp_junc_w':      {'id': 'pp_junc_w', 'x': 260, 'y': 480, 'label': 'Panorama Boulevard West'},
            'pp_junc_ctr':    {'id': 'pp_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Infinity Pool Plaza'},
            'pp_junc_e':      {'id': 'pp_junc_e', 'x': 960, 'y': 480, 'label': 'Kalena Agrahara East Cross'},
            'pp_gate_east':   {'id': 'pp_gate_east', 'x': 1100, 'y': 480, 'label': 'Gate 2 (Noble Residency Link)'},
            'pp_tower_a':     {'id': 'pp_tower_a', 'x': 360, 'y': 310, 'label': 'Tower A Parkway'},
            'pp_tower_b':     {'id': 'pp_tower_b', 'x': 860, 'y': 510, 'label': 'Tower B Promenade'}
        },
        'edges': [
            ('pp_gate_main', 'pp_junc_w', 'Panorama Boulevard', 'primary'),
            ('pp_junc_w', 'pp_junc_ctr', 'Panorama Boulevard', 'primary'),
            ('pp_junc_ctr', 'pp_junc_e', 'Panorama Boulevard', 'primary'),
            ('pp_junc_e', 'pp_gate_east', 'Panorama Boulevard', 'primary'),
            ('pp_junc_w', 'pp_tower_a', 'Kalena Agrahara Link', 'secondary'),
            ('pp_tower_a', 'pp_junc_ctr', 'Kalena Agrahara Link', 'secondary'),
            ('pp_junc_ctr', 'pp_tower_b', 'Valley View Way', 'secondary'),
            ('pp_tower_b', 'pp_junc_e', 'Valley View Way', 'secondary')
        ],
        'blocks': [
            ('Tower A', 360, 270, 'pp_tower_a', 'Panorama Boulevard', 'South'),
            ('Tower B', 820, 500, 'pp_tower_b', 'Kalena Agrahara Link', 'West')
        ],
        'roadLabels': [
            {'name': 'PANORAMA BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'KALENA AGRAHARA LINK', 'x': 360, 'y': 290, 'vertical': False},
            {'name': 'VALLEY VIEW WAY', 'x': 860, 'y': 490, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Panorama Vista Club', 'desc': 'Infinity pool, gymnasium, multi-purpose hall & squash', 'x': 620, 'y': 430, 'node': 'pp_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # 17. DIVYASREE REPUBLIC OF WHITEFIELD (EPIP)
    # 14-acre contemporary urban campus
    'divyasree_republic': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,820 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,820 L 220,800 Z",
        'waterBody': {'x': 520, 'y': 440, 'w': 200, 'h': 80, 'rx': 14, 'label': 'Republic Olympic Swimming Facility'},
        'gardenPark': {'x': 440, 'y': 310, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Contemporary Sculpture & Sunken Plaza'},
        'defaultStartGate': 'dr_gate_main',
        'nodes': {
            'dr_gate_main':   {'id': 'dr_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (EPIP Main Road)'},
            'dr_junc_w':      {'id': 'dr_junc_w', 'x': 240, 'y': 480, 'label': 'Republic West Cross'},
            'dr_junc_ctr':    {'id': 'dr_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Sunken Plaza'},
            'dr_junc_e':      {'id': 'dr_junc_e', 'x': 960, 'y': 480, 'label': 'Republic East Cross'},
            'dr_gate_east':   {'id': 'dr_gate_east', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Kundalahalli Link)'},
            'dr_alpha':       {'id': 'dr_alpha', 'x': 340, 'y': 270, 'label': 'Tower Alpha Parkway'},
            'dr_beta':        {'id': 'dr_beta', 'x': 860, 'y': 270, 'label': 'Tower Beta Parkway'},
            'dr_gamma':       {'id': 'dr_gamma', 'x': 340, 'y': 690, 'label': 'Tower Gamma Drive'},
            'dr_delta':       {'id': 'dr_delta', 'x': 860, 'y': 690, 'label': 'Tower Delta Drive'}
        },
        'edges': [
            ('dr_gate_main', 'dr_junc_w', 'Republic Boulevard', 'primary'),
            ('dr_junc_w', 'dr_junc_ctr', 'Republic Boulevard', 'primary'),
            ('dr_junc_ctr', 'dr_junc_e', 'Republic Boulevard', 'primary'),
            ('dr_junc_e', 'dr_gate_east', 'Republic Boulevard', 'primary'),
            ('dr_junc_w', 'dr_alpha', 'Alpha Parkway', 'secondary'),
            ('dr_alpha', 'dr_beta', 'Alpha Parkway', 'secondary'),
            ('dr_beta', 'dr_junc_e', 'Beta Promenade', 'secondary'),
            ('dr_junc_w', 'dr_gamma', 'EPIP Access Way', 'secondary'),
            ('dr_gamma', 'dr_delta', 'EPIP Access Way', 'secondary'),
            ('dr_delta', 'dr_junc_e', 'Beta Promenade', 'secondary'),
            ('dr_junc_ctr', 'dr_alpha', 'Central Link', 'secondary'),
            ('dr_junc_ctr', 'dr_beta', 'Central Link', 'secondary'),
            ('dr_junc_ctr', 'dr_gamma', 'Central Link', 'secondary'),
            ('dr_junc_ctr', 'dr_delta', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Tower Alpha', 300, 240, 'dr_alpha', 'Republic Boulevard', 'South'),
            ('Tower Beta', 860, 240, 'dr_beta', 'Alpha Parkway', 'South'),
            ('Tower Gamma', 300, 670, 'dr_gamma', 'EPIP Access Way', 'North'),
            ('Tower Delta', 860, 670, 'dr_delta', 'Beta Promenade', 'North')
        ],
        'roadLabels': [
            {'name': 'REPUBLIC BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'ALPHA PARKWAY', 'x': 620, 'y': 255, 'vertical': False},
            {'name': 'EPIP ACCESS WAY', 'x': 620, 'y': 705, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Republic Central Club', 'desc': 'Olympic pool, squash, badminton, co-working hub and cafe', 'x': 620, 'y': 440, 'node': 'dr_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # 18. SOWPARNIKA THE COLUMNS (Whitefield)
    # Roman architecture inspired quad-tower layout
    'sowparnika_columns': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,820 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,820 L 220,800 Z",
        'gardenPark': {'x': 460, 'y': 430, 'w': 280, 'h': 80, 'rx': 12, 'label': 'Roman Column Piazza & Classical Fountain'},
        'defaultStartGate': 'scol_gate_main',
        'nodes': {
            'scol_gate_main': {'id': 'scol_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Whitefield Main Entry)'},
            'scol_junc_w':    {'id': 'scol_junc_w', 'x': 240, 'y': 480, 'label': 'West Colonnade Cross'},
            'scol_junc_ctr':  {'id': 'scol_junc_ctr', 'x': 620, 'y': 480, 'label': 'Roman Fountain Forum'},
            'scol_junc_e':    {'id': 'scol_junc_e', 'x': 960, 'y': 480, 'label': 'East Colonnade Cross'},
            'scol_gate_east': {'id': 'scol_gate_east', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Hope Farm Link)'},
            'scol_corinth':   {'id': 'scol_corinth', 'x': 340, 'y': 280, 'label': 'Corinthian Way'},
            'scol_doric':     {'id': 'scol_doric', 'x': 860, 'y': 280, 'label': 'Doric Avenue'},
            'scol_ionic':     {'id': 'scol_ionic', 'x': 340, 'y': 680, 'label': 'Ionic Parkway'},
            'scol_tuscan':    {'id': 'scol_tuscan', 'x': 860, 'y': 680, 'label': 'Tuscan Walkway'}
        },
        'edges': [
            ('scol_gate_main', 'scol_junc_w', 'Columns Boulevard', 'primary'),
            ('scol_junc_w', 'scol_junc_ctr', 'Columns Boulevard', 'primary'),
            ('scol_junc_ctr', 'scol_junc_e', 'Columns Boulevard', 'primary'),
            ('scol_junc_e', 'scol_gate_east', 'Columns Boulevard', 'primary'),
            ('scol_junc_w', 'scol_corinth', 'Corinthian Way', 'secondary'),
            ('scol_corinth', 'scol_doric', 'Classical Promenade', 'secondary'),
            ('scol_doric', 'scol_junc_e', 'Doric Avenue', 'secondary'),
            ('scol_junc_w', 'scol_ionic', 'Ionic Parkway', 'secondary'),
            ('scol_ionic', 'scol_tuscan', 'Classical Promenade', 'secondary'),
            ('scol_tuscan', 'scol_junc_e', 'Tuscan Walkway', 'secondary'),
            ('scol_junc_ctr', 'scol_corinth', 'Central Link', 'secondary'),
            ('scol_junc_ctr', 'scol_doric', 'Central Link', 'secondary'),
            ('scol_junc_ctr', 'scol_ionic', 'Central Link', 'secondary'),
            ('scol_junc_ctr', 'scol_tuscan', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Corinthian Tower', 320, 260, 'scol_corinth', 'Corinthian Way', 'South'),
            ('Doric Tower', 840, 260, 'scol_doric', 'Doric Avenue', 'South'),
            ('Ionic Tower', 320, 660, 'scol_ionic', 'Ionic Parkway', 'North'),
            ('Tuscan Tower', 840, 660, 'scol_tuscan', 'Tuscan Walkway', 'North')
        ],
        'roadLabels': [
            {'name': 'COLUMNS BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'CLASSICAL PROMENADE', 'x': 620, 'y': 265, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'The Colosseum Clubhouse', 'desc': 'Roman amphitheater, heated pool, gym, banquet & squash', 'x': 620, 'y': 430, 'node': 'scol_junc_ctr', 'type': 'clubhouse', 'icon': '🏛️'}
        ]
    },

    # 19. GREEN GLEN LAYOUT (Bellandur)
    # Tech hub residential community along Bellandur Lake promenade
    'green_glen': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,820 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,820 L 220,800 Z",
        'waterBody': {'x': 260, 'y': 150, 'w': 700, 'h': 70, 'rx': 16, 'label': 'Bellandur Lake Waterfront Trail'},
        'defaultStartGate': 'gg_gate_main',
        'nodes': {
            'gg_gate_main':   {'id': 'gg_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Outer Ring Road Access)'},
            'gg_junc_w':      {'id': 'gg_junc_w', 'x': 260, 'y': 480, 'label': 'Green Glen Boulevard West'},
            'gg_junc_ctr':    {'id': 'gg_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Glen Roundabout'},
            'gg_junc_e':      {'id': 'gg_junc_e', 'x': 960, 'y': 480, 'label': 'Lakeview Way East'},
            'gg_gate_east':   {'id': 'gg_gate_east', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Sobha Dahlia Link)'},
            'gg_north':       {'id': 'gg_north', 'x': 360, 'y': 290, 'label': 'Glen North Promenade'},
            'gg_east':        {'id': 'gg_east', 'x': 860, 'y': 290, 'label': 'Lakeview Way North'},
            'gg_south':       {'id': 'gg_south', 'x': 620, 'y': 680, 'label': 'Bellandur Ring Link South'}
        },
        'edges': [
            ('gg_gate_main', 'gg_junc_w', 'Green Glen Boulevard', 'primary'),
            ('gg_junc_w', 'gg_junc_ctr', 'Green Glen Boulevard', 'primary'),
            ('gg_junc_ctr', 'gg_junc_e', 'Green Glen Boulevard', 'primary'),
            ('gg_junc_e', 'gg_gate_east', 'Green Glen Boulevard', 'primary'),
            ('gg_junc_w', 'gg_north', 'Glen North Way', 'secondary'),
            ('gg_north', 'gg_east', 'Lakeview Way', 'secondary'),
            ('gg_east', 'gg_junc_e', 'Lakeview Way', 'secondary'),
            ('gg_junc_w', 'gg_south', 'Bellandur Ring Link', 'secondary'),
            ('gg_south', 'gg_junc_e', 'Bellandur Ring Link', 'secondary'),
            ('gg_junc_ctr', 'gg_south', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Glen North Block', 350, 270, 'gg_north', 'Green Glen Boulevard', 'South'),
            ('Glen South Block', 780, 270, 'gg_east', 'Lakeview Way', 'South'),
            ('Lakeview Residency', 560, 660, 'gg_south', 'Bellandur Ring Link', 'North')
        ],
        'roadLabels': [
            {'name': 'GREEN GLEN BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'LAKEVIEW WAY', 'x': 620, 'y': 275, 'vertical': False},
            {'name': 'BELLANDUR RING LINK', 'x': 620, 'y': 665, 'vertical': False}
        ],
        'amenities': [
            {'id': 'park', 'name': 'Green Glen Recreation Park', 'desc': 'Children park, jogging path and basketball court', 'x': 620, 'y': 440, 'node': 'gg_junc_ctr', 'type': 'park', 'icon': '🌳'}
        ]
    },

    # 20. NEOTOWN ELECTRONIC CITY (Electronic City Phase 1)
    # 120-acre smart integrated township
    'neo_town': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,820 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,820 L 220,800 Z",
        'gardenPark': {'x': 440, 'y': 430, 'w': 360, 'h': 70, 'rx': 10, 'label': 'Neotown Central Smart Solar Plaza'},
        'defaultStartGate': 'nt_gate_main',
        'nodes': {
            'nt_gate_main':   {'id': 'nt_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Electronic City Elevated Flyover)'},
            'nt_junc_w':      {'id': 'nt_junc_w', 'x': 240, 'y': 480, 'label': 'Smondo Boulevard West'},
            'nt_junc_ctr':    {'id': 'nt_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Neotown Plaza'},
            'nt_junc_e':      {'id': 'nt_junc_e', 'x': 960, 'y': 480, 'label': 'Silicon Way East'},
            'nt_gate_east':   {'id': 'nt_gate_east', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Wipro Campus Link)'},
            'nt_smondo':      {'id': 'nt_smondo', 'x': 340, 'y': 280, 'label': 'Smondoville Parkway'},
            'nt_silicon':     {'id': 'nt_silicon', 'x': 860, 'y': 380, 'label': 'Neo Silicon Court'},
            'nt_infy':        {'id': 'nt_infy', 'x': 440, 'y': 690, 'label': 'Infy View Drive'}
        },
        'edges': [
            ('nt_gate_main', 'nt_junc_w', 'Neotown Boulevard', 'primary'),
            ('nt_junc_w', 'nt_junc_ctr', 'Neotown Boulevard', 'primary'),
            ('nt_junc_ctr', 'nt_junc_e', 'Neotown Boulevard', 'primary'),
            ('nt_junc_e', 'nt_gate_east', 'Neotown Boulevard', 'primary'),
            ('nt_junc_w', 'nt_smondo', 'Smondoville Parkway', 'secondary'),
            ('nt_smondo', 'nt_silicon', 'Tech City Link', 'secondary'),
            ('nt_silicon', 'nt_junc_e', 'Silicon Way', 'secondary'),
            ('nt_junc_w', 'nt_infy', 'Infy View Drive', 'secondary'),
            ('nt_infy', 'nt_junc_e', 'Tech City Link', 'secondary'),
            ('nt_junc_ctr', 'nt_infy', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Smondoville Tower', 320, 260, 'nt_smondo', 'Smondo Boulevard', 'South'),
            ('Neo Silicon Block', 860, 380, 'nt_silicon', 'Silicon Way', 'West'),
            ('Infy View Tower', 440, 680, 'nt_infy', 'Tech City Link', 'North')
        ],
        'roadLabels': [
            {'name': 'NEOTOWN BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'SMONDOVILLE PARKWAY', 'x': 340, 'y': 380, 'vertical': True},
            {'name': 'SILICON WAY', 'x': 860, 'y': 440, 'vertical': True}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Neotown Grand Clubhouse', 'desc': 'Infinity pool, gym, bowling alley and co-working lounge', 'x': 620, 'y': 440, 'node': 'nt_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # 21. MANYATA TECH PARK RESIDENCY (Nagavara / Outer Ring Road)
    # High-rise executive enclave adjacent to Manyata Tech Park
    'manyata_residency': {
        'groundPolygon': "100,480 220,160 620,140 1020,160 1120,480 1020,800 620,820 220,800 Z",
        'borderTreesPath': "M 100,480 L 220,160 L 620,140 L 1020,160 L 1120,480 L 1020,800 L 620,820 L 220,800 Z",
        'landmarks': [
            {'x': 760, 'y': 420, 'w': 220, 'h': 180, 'rx': 8, 'label': '💼 Embassy Manyata Tech Park', 'fill': '#0f172a', 'stroke': '#38bdf8'}
        ],
        'defaultStartGate': 'mr_gate_main',
        'nodes': {
            'mr_gate_main':   {'id': 'mr_gate_main', 'x': 100, 'y': 480, 'label': 'Gate 1 (Outer Ring Road Flyover)'},
            'mr_junc_w':      {'id': 'mr_junc_w', 'x': 260, 'y': 480, 'label': 'Manyata Boulevard West'},
            'mr_junc_ctr':    {'id': 'mr_junc_ctr', 'x': 620, 'y': 480, 'label': 'Executive Plaza Cross'},
            'mr_junc_e':      {'id': 'mr_junc_e', 'x': 960, 'y': 480, 'label': 'Tech Park Skywalk Access'},
            'mr_gate_tech':   {'id': 'mr_gate_tech', 'x': 1110, 'y': 480, 'label': 'Gate 2 (Nagavara Lake & Metro Link)'},
            'mr_north':       {'id': 'mr_north', 'x': 360, 'y': 280, 'label': 'Residency North Drive'},
            'mr_ne':          {'id': 'mr_ne', 'x': 780, 'y': 260, 'label': 'Nagavara Ring Parkway'},
            'mr_south':       {'id': 'mr_south', 'x': 460, 'y': 680, 'label': 'Tech Park Link South'}
        },
        'edges': [
            ('mr_gate_main', 'mr_junc_w', 'Manyata Boulevard', 'primary'),
            ('mr_junc_w', 'mr_junc_ctr', 'Manyata Boulevard', 'primary'),
            ('mr_junc_ctr', 'mr_junc_e', 'Manyata Boulevard', 'primary'),
            ('mr_junc_e', 'mr_gate_tech', 'Manyata Boulevard', 'primary'),
            ('mr_junc_w', 'mr_north', 'Residency Way', 'secondary'),
            ('mr_north', 'mr_ne', 'Nagavara Ring Parkway', 'secondary'),
            ('mr_ne', 'mr_junc_e', 'Nagavara Ring Parkway', 'secondary'),
            ('mr_junc_w', 'mr_south', 'Tech Park Link', 'secondary'),
            ('mr_south', 'mr_junc_e', 'Tech Park Link', 'secondary'),
            ('mr_junc_ctr', 'mr_south', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Residency North', 360, 260, 'mr_north', 'Manyata Boulevard', 'South'),
            ('Residency South', 780, 240, 'mr_ne', 'Nagavara Ring Parkway', 'South'),
            ('Tech Enclave Block', 460, 670, 'mr_south', 'Tech Park Link', 'North')
        ],
        'roadLabels': [
            {'name': 'MANYATA BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'NAGAVARA RING PARKWAY', 'x': 620, 'y': 245, 'vertical': False},
            {'name': 'TECH PARK LINK', 'x': 620, 'y': 665, 'vertical': False}
        ],
        'amenities': [
            {'id': 'tech', 'name': 'Manyata Executive Club & Spa', 'desc': 'Rooftop pool, executive conference center, squash and dining', 'x': 620, 'y': 440, 'node': 'mr_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # 22. OZONE URBANA (NH-44, Devanahalli)
    # 185-acre mega-township near Airport
    'ozone_urbana': {
        'groundPolygon': "80,480 180,140 1060,140 1160,480 1060,820 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 1060,140 L 1160,480 L 1060,820 L 180,820 Z",
        'gardenPark': {'x': 440, 'y': 380, 'w': 360, 'h': 80, 'rx': 10, 'label': 'Urbana Central 7-Acre Sports Ground & Park'},
        'waterBody': {'x': 520, 'y': 480, 'w': 200, 'h': 70, 'rx': 12, 'label': 'Olympic Swimming Complex'},
        'defaultStartGate': 'ou_gate_main',
        'nodes': {
            'ou_gate_main':   {'id': 'ou_gate_main', 'x': 80, 'y': 480, 'label': 'Gate 1 (NH-44 Airport Highway)'},
            'ou_junc_w':      {'id': 'ou_junc_w', 'x': 240, 'y': 480, 'label': 'Urbana Boulevard West'},
            'ou_junc_ctr':    {'id': 'ou_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Urbana Roundabout'},
            'ou_junc_e':      {'id': 'ou_junc_e', 'x': 960, 'y': 480, 'label': 'Sports Arena Junction'},
            'ou_gate_east':   {'id': 'ou_gate_east', 'x': 1140, 'y': 480, 'label': 'Gate 2 (Devanahalli Airport Road)'},
            'ou_prime':       {'id': 'ou_prime', 'x': 320, 'y': 280, 'label': 'Urbana Prime Drive'},
            'ou_aqua':        {'id': 'ou_aqua', 'x': 840, 'y': 260, 'label': 'Urbana Aqua Parkway'},
            'ou_meadows':     {'id': 'ou_meadows', 'x': 620, 'y': 690, 'label': 'Urbana Meadows Avenue'}
        },
        'edges': [
            ('ou_gate_main', 'ou_junc_w', 'Urbana Boulevard', 'primary'),
            ('ou_junc_w', 'ou_junc_ctr', 'Urbana Boulevard', 'primary'),
            ('ou_junc_ctr', 'ou_junc_e', 'Urbana Boulevard', 'primary'),
            ('ou_junc_e', 'ou_gate_east', 'Urbana Boulevard', 'primary'),
            ('ou_junc_w', 'ou_prime', 'Airport Parkway', 'secondary'),
            ('ou_prime', 'ou_aqua', 'Sports Arena Way', 'secondary'),
            ('ou_aqua', 'ou_junc_e', 'Sports Arena Way', 'secondary'),
            ('ou_junc_w', 'ou_meadows', 'Central Promenade', 'secondary'),
            ('ou_meadows', 'ou_junc_e', 'Central Promenade', 'secondary'),
            ('ou_junc_ctr', 'ou_meadows', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Urbana Prime', 300, 260, 'ou_prime', 'Urbana Boulevard', 'South'),
            ('Urbana Aqua', 840, 240, 'ou_aqua', 'Sports Arena Way', 'South'),
            ('Urbana Meadows', 620, 670, 'ou_meadows', 'Airport Parkway', 'North')
        ],
        'roadLabels': [
            {'name': 'URBANA BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'SPORTS ARENA WAY', 'x': 620, 'y': 245, 'vertical': False},
            {'name': 'AIRPORT PARKWAY', 'x': 620, 'y': 675, 'vertical': False}
        ],
        'amenities': [
            {'id': 'sports', 'name': 'National Cricket Academy & Sports Arena', 'desc': 'Floodlit cricket stadium, athletic track, tennis courts and Olympic pool', 'x': 620, 'y': 440, 'node': 'ou_junc_ctr', 'type': 'sports', 'icon': '🏏'}
        ]
    },

    # 23. PRESTIGE MISTY WATERS (Hebbal / Outer Ring Road)
    # Waterfront high-rise overlooking Hebbal Lake
    'prestige_misty_waters': {
        'groundPolygon': "110,480 220,180 620,160 1020,180 1110,480 1020,780 620,800 220,780 Z",
        'borderTreesPath': "M 110,480 L 220,180 L 620,160 L 1020,180 L 1110,480 L 1020,780 L 620,800 L 220,780 Z",
        'waterBody': {'x': 260, 'y': 150, 'w': 700, 'h': 70, 'rx': 16, 'label': 'Hebbal Lake Observation Waterfront'},
        'defaultStartGate': 'pmw_gate_main',
        'nodes': {
            'pmw_gate_main':  {'id': 'pmw_gate_main', 'x': 110, 'y': 480, 'label': 'Gate 1 (Hebbal Outer Ring Road)'},
            'pmw_junc_w':     {'id': 'pmw_junc_w', 'x': 260, 'y': 480, 'label': 'Misty Waters Boulevard West'},
            'pmw_junc_ctr':   {'id': 'pmw_junc_ctr', 'x': 620, 'y': 480, 'label': 'Central Cascade Plaza'},
            'pmw_junc_e':     {'id': 'pmw_junc_e', 'x': 960, 'y': 480, 'label': 'Lakeview Promenade East'},
            'pmw_gate_east':  {'id': 'pmw_gate_east', 'x': 1100, 'y': 480, 'label': 'Gate 2 (Nagavara Approach Link)'},
            'pmw_a':          {'id': 'pmw_a', 'x': 360, 'y': 310, 'label': 'Tower A Parkway'},
            'pmw_b':          {'id': 'pmw_b', 'x': 800, 'y': 490, 'label': 'Tower B Parkway'}
        },
        'edges': [
            ('pmw_gate_main', 'pmw_junc_w', 'Misty Waters Boulevard', 'primary'),
            ('pmw_junc_w', 'pmw_junc_ctr', 'Misty Waters Boulevard', 'primary'),
            ('pmw_junc_ctr', 'pmw_junc_e', 'Misty Waters Boulevard', 'primary'),
            ('pmw_junc_e', 'pmw_gate_east', 'Misty Waters Boulevard', 'primary'),
            ('pmw_junc_w', 'pmw_a', 'Lakeview Parkway', 'secondary'),
            ('pmw_a', 'pmw_junc_ctr', 'Central Pool Way', 'secondary'),
            ('pmw_junc_ctr', 'pmw_b', 'Hebbal Ring Link', 'secondary'),
            ('pmw_b', 'pmw_junc_e', 'Hebbal Ring Link', 'secondary')
        ],
        'blocks': [
            ('Tower A', 360, 270, 'pmw_a', 'Misty Waters Boulevard', 'South'),
            ('Tower B', 800, 470, 'pmw_b', 'Lakeview Parkway', 'West')
        ],
        'roadLabels': [
            {'name': 'MISTY WATERS BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'LAKEVIEW PARKWAY', 'x': 360, 'y': 290, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Cascade Lakefront Clubhouse', 'desc': 'Heated pool, waterfall lounge, squash and sky deck', 'x': 620, 'y': 440, 'node': 'pmw_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },

    # 24. GODREJ WOODSMAN ESTATE (Bellary Road, Hebbal)
    # Heritage rain tree residential society on Airport Highway
    'godrej_woodsman': {
        'groundPolygon': "110,480 220,180 620,160 1020,180 1110,480 1020,780 620,800 220,780 Z",
        'borderTreesPath': "M 110,480 L 220,180 L 620,160 L 1020,180 L 1110,480 L 1020,780 L 620,800 L 220,780 Z",
        'gardenPark': {'x': 440, 'y': 380, 'w': 360, 'h': 80, 'rx': 10, 'label': '70-Year-Old Preserved Rain Tree Park'},
        'defaultStartGate': 'gw_gate_main',
        'nodes': {
            'gw_gate_main':   {'id': 'gw_gate_main', 'x': 110, 'y': 480, 'label': 'Gate 1 (Bellary Airport Highway)'},
            'gw_junc_w':      {'id': 'gw_junc_w', 'x': 260, 'y': 480, 'label': 'Woodsman Boulevard West'},
            'gw_junc_ctr':    {'id': 'gw_junc_ctr', 'x': 620, 'y': 480, 'label': 'Rain Tree Central Hub'},
            'gw_junc_e':      {'id': 'gw_junc_e', 'x': 960, 'y': 480, 'label': 'Airport Highway Link East'},
            'gw_gate_east':   {'id': 'gw_gate_east', 'x': 1100, 'y': 480, 'label': 'Gate 2 (Hebbal Flyover Link)'},
            'gw_a':           {'id': 'gw_a', 'x': 360, 'y': 310, 'label': 'Woodsman Tower A Parkway'},
            'gw_b':           {'id': 'gw_b', 'x': 800, 'y': 490, 'label': 'Woodsman Tower B Parkway'}
        },
        'edges': [
            ('gw_gate_main', 'gw_junc_w', 'Woodsman Boulevard', 'primary'),
            ('gw_junc_w', 'gw_junc_ctr', 'Woodsman Boulevard', 'primary'),
            ('gw_junc_ctr', 'gw_junc_e', 'Woodsman Boulevard', 'primary'),
            ('gw_junc_e', 'gw_gate_east', 'Woodsman Boulevard', 'primary'),
            ('gw_junc_w', 'gw_a', 'Bellary Road Parkway', 'secondary'),
            ('gw_a', 'gw_junc_ctr', 'Bellary Road Parkway', 'secondary'),
            ('gw_junc_ctr', 'gw_b', 'Airport Highway Link', 'secondary'),
            ('gw_b', 'gw_junc_e', 'Airport Highway Link', 'secondary')
        ],
        'blocks': [
            ('Woodsman Tower A', 360, 270, 'gw_a', 'Woodsman Boulevard', 'South'),
            ('Woodsman Tower B', 800, 470, 'gw_b', 'Airport Highway Link', 'West')
        ],
        'roadLabels': [
            {'name': 'WOODSMAN BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'BELLARY ROAD PARKWAY', 'x': 360, 'y': 290, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Woodsman Rain Tree Clubhouse', 'desc': 'Half-acre infinity pool, gym, squash and golf putting green', 'x': 620, 'y': 440, 'node': 'gw_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    },


    # 25. CONCORDE NAPA VALLEY (Kanakapura Road)
    # California-themed luxury villa township with Napa Boulevard, Sonoma Drive & vineyard promenade
    'concorde_napa_valley': {
        'groundPolygon': "80,480 180,140 1060,140 1160,480 1060,820 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 1060,140 L 1160,480 L 1060,820 L 180,820 Z",
        'waterBody': {'x': 520, 'y': 440, 'w': 200, 'h': 75, 'rx': 14, 'label': 'Napa Valley Lakeside Heated Pool & Spa'},
        'gardenPark': {'x': 440, 'y': 310, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Sonoma Vineyard Lawns & Olive Groves'},
        'defaultStartGate': 'cnv_gate_main',
        'nodes': {
            'cnv_gate_main':  {'id': 'cnv_gate_main', 'x': 80, 'y': 480, 'label': 'Gate 1 (Kanakapura Main Road)'},
            'cnv_junc_w':     {'id': 'cnv_junc_w', 'x': 240, 'y': 480, 'label': 'Napa Court West Roundabout'},
            'cnv_junc_ctr':   {'id': 'cnv_junc_ctr', 'x': 620, 'y': 480, 'label': 'Grand Napa Plaza'},
            'cnv_junc_e':     {'id': 'cnv_junc_e', 'x': 960, 'y': 480, 'label': 'Sonoma Way East Roundabout'},
            'cnv_gate_east':  {'id': 'cnv_gate_east', 'x': 1140, 'y': 480, 'label': 'Gate 2 (Valley Link Access)'},
            'cnv_napa_nw':    {'id': 'cnv_napa_nw', 'x': 320, 'y': 270, 'label': 'Napa Court North Drive'},
            'cnv_vine_ne':    {'id': 'cnv_vine_ne', 'x': 860, 'y': 270, 'label': 'Vineyard Parkway North'},
            'cnv_sonoma_sw':  {'id': 'cnv_sonoma_sw', 'x': 320, 'y': 690, 'label': 'Sonoma Drive South'},
            'cnv_valley_se':  {'id': 'cnv_valley_se', 'x': 860, 'y': 690, 'label': 'Valley Link South'}
        },
        'edges': [
            ('cnv_gate_main', 'cnv_junc_w', 'Napa Boulevard', 'primary'),
            ('cnv_junc_w', 'cnv_junc_ctr', 'Napa Boulevard', 'primary'),
            ('cnv_junc_ctr', 'cnv_junc_e', 'Napa Boulevard', 'primary'),
            ('cnv_junc_e', 'cnv_gate_east', 'Napa Boulevard', 'primary'),
            ('cnv_junc_w', 'cnv_napa_nw', 'Napa Court Drive', 'secondary'),
            ('cnv_napa_nw', 'cnv_vine_ne', 'Vineyard Parkway', 'secondary'),
            ('cnv_vine_ne', 'cnv_junc_e', 'Vineyard Parkway', 'secondary'),
            ('cnv_junc_w', 'cnv_sonoma_sw', 'Sonoma Drive', 'secondary'),
            ('cnv_sonoma_sw', 'cnv_valley_se', 'Valley Link', 'secondary'),
            ('cnv_valley_se', 'cnv_junc_e', 'Valley Link', 'secondary'),
            ('cnv_junc_ctr', 'cnv_napa_nw', 'Central Link', 'secondary'),
            ('cnv_junc_ctr', 'cnv_sonoma_sw', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Napa Court Villas', 300, 240, 'cnv_napa_nw', 'Napa Boulevard', 'South'),
            ('Vineyard Villas', 860, 240, 'cnv_vine_ne', 'Vineyard Parkway', 'South'),
            ('Sonoma Way Villas', 300, 670, 'cnv_sonoma_sw', 'Sonoma Drive', 'North'),
            ('Valley View Villas', 860, 670, 'cnv_valley_se', 'Valley Link', 'North')
        ],
        'roadLabels': [
            {'name': 'NAPA BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'VINEYARD PARKWAY', 'x': 620, 'y': 255, 'vertical': False},
            {'name': 'SONOMA DRIVE', 'x': 620, 'y': 705, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Club Napa Grande', 'desc': 'Lakeside clubhouse, tennis courts, infinity pool and bowling alley', 'x': 620, 'y': 440, 'node': 'cnv_junc_ctr', 'type': 'clubhouse', 'icon': '🍷'}
        ]
    },

    # 26. PALM MEADOWS (Whitefield)
    # Iconic sprawling luxury villa township
    'palm_meadows': {
        'groundPolygon': "80,480 180,140 1060,140 1160,480 1060,820 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 1060,140 L 1160,480 L 1060,820 L 180,820 Z",
        'waterBody': {'x': 520, 'y': 440, 'w': 200, 'h': 75, 'rx': 14, 'label': 'Club Palm Meadows Lagoon Pool'},
        'gardenPark': {'x': 440, 'y': 310, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Royal Palm Tree Avenues & Central Park'},
        'defaultStartGate': 'pm_gate_main',
        'nodes': {
            'pm_gate_main':   {'id': 'pm_gate_main', 'x': 80, 'y': 480, 'label': 'Gate 1 (Varthur Main Road)'},
            'pm_junc_w':      {'id': 'pm_junc_w', 'x': 240, 'y': 480, 'label': 'Royal Palm West Cross'},
            'pm_junc_ctr':    {'id': 'pm_junc_ctr', 'x': 620, 'y': 480, 'label': 'Palm Meadows Club Plaza'},
            'pm_junc_e':      {'id': 'pm_junc_e', 'x': 960, 'y': 480, 'label': 'Orchid Way East Cross'},
            'pm_gate_east':   {'id': 'pm_gate_east', 'x': 1140, 'y': 480, 'label': 'Gate 2 (Airport Link)'},
            'pm_royal_nw':    {'id': 'pm_royal_nw', 'x': 320, 'y': 270, 'label': 'Royal Palm Drive'},
            'pm_meadow_ne':   {'id': 'pm_meadow_ne', 'x': 860, 'y': 270, 'label': 'Meadows Boulevard North'},
            'pm_orchid_sw':   {'id': 'pm_orchid_sw', 'x': 320, 'y': 690, 'label': 'Orchid Way South'},
            'pm_hibiscus_se': {'id': 'pm_hibiscus_se', 'x': 860, 'y': 690, 'label': 'Hibiscus Court South'}
        },
        'edges': [
            ('pm_gate_main', 'pm_junc_w', 'Palm Meadows Boulevard', 'primary'),
            ('pm_junc_w', 'pm_junc_ctr', 'Palm Meadows Boulevard', 'primary'),
            ('pm_junc_ctr', 'pm_junc_e', 'Palm Meadows Boulevard', 'primary'),
            ('pm_junc_e', 'pm_gate_east', 'Palm Meadows Boulevard', 'primary'),
            ('pm_junc_w', 'pm_royal_nw', 'Royal Palm Drive', 'secondary'),
            ('pm_royal_nw', 'pm_meadow_ne', 'Meadows Boulevard', 'secondary'),
            ('pm_meadow_ne', 'pm_junc_e', 'Meadows Boulevard', 'secondary'),
            ('pm_junc_w', 'pm_orchid_sw', 'Orchid Way', 'secondary'),
            ('pm_orchid_sw', 'pm_hibiscus_se', 'Hibiscus Court', 'secondary'),
            ('pm_hibiscus_se', 'pm_junc_e', 'Hibiscus Court', 'secondary'),
            ('pm_junc_ctr', 'pm_royal_nw', 'Central Link', 'secondary'),
            ('pm_junc_ctr', 'pm_orchid_sw', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Royal Palm Villas', 300, 240, 'pm_royal_nw', 'Palm Meadows Boulevard', 'South'),
            ('Meadows Court Villas', 860, 240, 'pm_meadow_ne', 'Meadows Boulevard', 'South'),
            ('Orchid Enclave Villas', 300, 670, 'pm_orchid_sw', 'Orchid Way', 'North'),
            ('Hibiscus View Villas', 860, 670, 'pm_hibiscus_se', 'Hibiscus Court', 'North')
        ],
        'roadLabels': [
            {'name': 'PALM MEADOWS BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'MEADOWS BOULEVARD', 'x': 620, 'y': 255, 'vertical': False},
            {'name': 'ORCHID WAY', 'x': 620, 'y': 705, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Club Palm Meadows & Spa', 'desc': 'World-class country resort with 3 pools, squash, tennis, gym & dining', 'x': 620, 'y': 440, 'node': 'pm_junc_ctr', 'type': 'clubhouse', 'icon': '🌴'}
        ]
    },

    # 27. PRESTIGE GOLFSHIRE (Nandi Hills Road, Devanahalli)
    # Signature 275-acre golf villa resort at the foot of Nandi Hills
    'prestige_golfshire': {
        'groundPolygon': "80,480 180,140 1060,140 1160,480 1060,820 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 1060,140 L 1160,480 L 1060,820 L 180,820 Z",
        'waterBody': {'x': 480, 'y': 430, 'w': 280, 'h': 90, 'rx': 20, 'label': 'Nandi Foothills Golf Lake & Water Hazard'},
        'gardenPark': {'x': 440, 'y': 280, 'w': 360, 'h': 70, 'rx': 10, 'label': '18-Hole Championship Golf Course & Greens'},
        'landmarks': [
            {'x': 760, 'y': 430, 'w': 200, 'h': 100, 'rx': 8, 'label': '🏨 JW Marriott Golf Resort & Spa', 'fill': '#1e1b4b', 'stroke': '#f59e0b'}
        ],
        'defaultStartGate': 'pg_gate_main',
        'nodes': {
            'pg_gate_main':   {'id': 'pg_gate_main', 'x': 80, 'y': 480, 'label': 'Gate 1 (Nandi Hills Highway)'},
            'pg_junc_w':      {'id': 'pg_junc_w', 'x': 240, 'y': 480, 'label': 'Fairway Green West Cross'},
            'pg_junc_ctr':    {'id': 'pg_junc_ctr', 'x': 620, 'y': 480, 'label': 'Golfshire Clubhouse Hub'},
            'pg_junc_e':      {'id': 'pg_junc_e', 'x': 960, 'y': 480, 'label': 'Nandi Foothill East Cross'},
            'pg_gate_resort': {'id': 'pg_gate_resort', 'x': 1140, 'y': 480, 'label': 'Gate 2 (JW Marriott Resort Link)'},
            'pg_fairway_nw':  {'id': 'pg_fairway_nw', 'x': 320, 'y': 270, 'label': 'Fairway Green Parkway'},
            'pg_nandi_ne':    {'id': 'pg_nandi_ne', 'x': 860, 'y': 270, 'label': 'Nandi Foothill Drive'},
            'pg_lake_sw':     {'id': 'pg_lake_sw', 'x': 320, 'y': 690, 'label': 'Golf Lake Promenade South'},
            'pg_greens_se':   {'id': 'pg_greens_se', 'x': 860, 'y': 690, 'label': 'Clubhouse Link South'}
        },
        'edges': [
            ('pg_gate_main', 'pg_junc_w', 'Golfshire Boulevard', 'primary'),
            ('pg_junc_w', 'pg_junc_ctr', 'Golfshire Boulevard', 'primary'),
            ('pg_junc_ctr', 'pg_junc_e', 'Golfshire Boulevard', 'primary'),
            ('pg_junc_e', 'pg_gate_resort', 'Golfshire Boulevard', 'primary'),
            ('pg_junc_w', 'pg_fairway_nw', 'Fairway Green Parkway', 'secondary'),
            ('pg_fairway_nw', 'pg_nandi_ne', 'Fairway Green Parkway', 'secondary'),
            ('pg_nandi_ne', 'pg_junc_e', 'Nandi Foothill Drive', 'secondary'),
            ('pg_junc_w', 'pg_lake_sw', 'Golf Lake Promenade', 'secondary'),
            ('pg_lake_sw', 'pg_greens_se', 'Golf Lake Promenade', 'secondary'),
            ('pg_greens_se', 'pg_junc_e', 'Clubhouse Link', 'secondary'),
            ('pg_junc_ctr', 'pg_fairway_nw', 'Central Link', 'secondary'),
            ('pg_junc_ctr', 'pg_lake_sw', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Fairway Enclave Villas', 300, 240, 'pg_fairway_nw', 'Golfshire Boulevard', 'South'),
            ('Nandi View Mansions', 860, 240, 'pg_nandi_ne', 'Nandi Foothill Drive', 'South'),
            ('Lakeview Golf Villas', 300, 670, 'pg_lake_sw', 'Golf Lake Promenade', 'North'),
            ('Putting Green Villas', 860, 670, 'pg_greens_se', 'Clubhouse Link', 'North')
        ],
        'roadLabels': [
            {'name': 'GOLFSHIRE BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'FAIRWAY GREEN PARKWAY', 'x': 620, 'y': 255, 'vertical': False},
            {'name': 'GOLF LAKE PROMENADE', 'x': 620, 'y': 705, 'vertical': False}
        ],
        'amenities': [
            {'id': 'golf', 'name': 'Falcon Greens Golf Clubhouse', 'desc': 'Bob Hunt designed 18-hole championship golf course & pro shop', 'x': 620, 'y': 440, 'node': 'pg_junc_ctr', 'type': 'sports', 'icon': '⛳'},
            {'id': 'hotel', 'name': 'JW Marriott Bengaluru Prestige Golfshire Resort', 'desc': '5-star luxury resort, convention center & helipad', 'x': 760, 'y': 430, 'node': 'pg_junc_e', 'type': 'hotel', 'icon': '🏨'}
        ]
    },

    # 28. ADARSH PALM RETREAT (Bellandur / Outer Ring Road)
    # Premier luxury red-roof villa & tower community
    'adarsh_palm_retreat': {
        'groundPolygon': "80,480 180,140 1060,140 1160,480 1060,820 180,820 Z",
        'borderTreesPath': "M 80,480 L 180,140 L 1060,140 L 1160,480 L 1060,820 L 180,820 Z",
        'waterBody': {'x': 520, 'y': 440, 'w': 200, 'h': 75, 'rx': 14, 'label': 'Club Retreat Heated Pool & Lagoon'},
        'gardenPark': {'x': 440, 'y': 310, 'w': 360, 'h': 60, 'rx': 8, 'label': 'Palm Tree Avenues & Botanical Lawns'},
        'defaultStartGate': 'apr_gate_main',
        'nodes': {
            'apr_gate_main':  {'id': 'apr_gate_main', 'x': 80, 'y': 480, 'label': 'Gate 1 (Outer Ring Road Bellandur)'},
            'apr_junc_w':     {'id': 'apr_junc_w', 'x': 240, 'y': 480, 'label': 'Palm Retreat Boulevard West'},
            'apr_junc_ctr':   {'id': 'apr_junc_ctr', 'x': 620, 'y': 480, 'label': 'Club Retreat Central Plaza'},
            'apr_junc_e':     {'id': 'apr_junc_e', 'x': 960, 'y': 480, 'label': 'Villa Enclave East Roundabout'},
            'apr_gate_east':  {'id': 'apr_gate_east', 'x': 1140, 'y': 480, 'label': 'Gate 2 (Devarabisanahalli Link)'},
            'apr_redroof_nw': {'id': 'apr_redroof_nw', 'x': 320, 'y': 270, 'label': 'Red Roof Villa Parkway'},
            'apr_tower_ne':   {'id': 'apr_tower_ne', 'x': 860, 'y': 270, 'label': 'Retreat Towers Drive'},
            'apr_villa_sw':   {'id': 'apr_villa_sw', 'x': 320, 'y': 690, 'label': 'Palm Way South'},
            'apr_lake_se':    {'id': 'apr_lake_se', 'x': 860, 'y': 690, 'label': 'Lakeside Link South'}
        },
        'edges': [
            ('apr_gate_main', 'apr_junc_w', 'Palm Retreat Boulevard', 'primary'),
            ('apr_junc_w', 'apr_junc_ctr', 'Palm Retreat Boulevard', 'primary'),
            ('apr_junc_ctr', 'apr_junc_e', 'Palm Retreat Boulevard', 'primary'),
            ('apr_junc_e', 'apr_gate_east', 'Palm Retreat Boulevard', 'primary'),
            ('apr_junc_w', 'apr_redroof_nw', 'Red Roof Villa Parkway', 'secondary'),
            ('apr_redroof_nw', 'apr_tower_ne', 'Retreat Towers Drive', 'secondary'),
            ('apr_tower_ne', 'apr_junc_e', 'Retreat Towers Drive', 'secondary'),
            ('apr_junc_w', 'apr_villa_sw', 'Palm Way', 'secondary'),
            ('apr_villa_sw', 'apr_lake_se', 'Lakeside Link', 'secondary'),
            ('apr_lake_se', 'apr_junc_e', 'Lakeside Link', 'secondary'),
            ('apr_junc_ctr', 'apr_redroof_nw', 'Central Link', 'secondary'),
            ('apr_junc_ctr', 'apr_villa_sw', 'Central Link', 'secondary')
        ],
        'blocks': [
            ('Red Roof Villas', 300, 240, 'apr_redroof_nw', 'Palm Retreat Boulevard', 'South'),
            ('Retreat Towers', 860, 240, 'apr_tower_ne', 'Retreat Towers Drive', 'South'),
            ('Palm Grove Villas', 300, 670, 'apr_villa_sw', 'Palm Way', 'North'),
            ('Lakeside Enclave', 860, 670, 'apr_lake_se', 'Lakeside Link', 'North')
        ],
        'roadLabels': [
            {'name': 'PALM RETREAT BOULEVARD', 'x': 620, 'y': 495, 'vertical': False},
            {'name': 'RETREAT TOWERS DRIVE', 'x': 620, 'y': 255, 'vertical': False},
            {'name': 'PALM WAY', 'x': 620, 'y': 705, 'vertical': False}
        ],
        'amenities': [
            {'id': 'club', 'name': 'Adarsh Palm Retreat Club', 'desc': 'Double-deck heated pool, squash courts, gymnasium & dining', 'x': 620, 'y': 440, 'node': 'apr_junc_ctr', 'type': 'clubhouse', 'icon': '🏊'}
        ]
    }

}

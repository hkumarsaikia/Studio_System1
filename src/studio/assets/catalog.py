from __future__ import annotations

from dataclasses import dataclass
from typing import Any

STYLE_VARIANT = 'flat_infographic'


@dataclass(frozen=True)
class AssetFamily:
    id: str
    label: str
    assets: tuple[str, ...]
    tags: tuple[str, ...]
    allowed_scene_roles: tuple[str, ...]
    catalog_kind: str = 'master'


def _parse_assets(multiline: str) -> tuple[str, ...]:
    return tuple(line.strip() for line in multiline.splitlines() if line.strip())


MASTER_ASSET_FAMILIES: tuple[AssetFamily, ...] = (
    AssetFamily(
        id='people_society',
        label='People & Society',
        assets=_parse_assets('''
person
person_group
crowd
worker
office_worker
manager
business_person
consumer
customer
citizen
voter
student
teacher
doctor
family
child
elderly_person
entrepreneur
influencer
politician
protester
'''),
        tags=('people', 'society', 'human'),
        allowed_scene_roles=('hook', 'tension', 'conclusion', 'real_world_example'),
    ),
    AssetFamily(
        id='buildings_infrastructure',
        label='Buildings & Infrastructure',
        assets=_parse_assets('''
house
apartment_building
city_skyline
skyscraper
suburban_house
luxury_house
empty_house
office_building
corporate_headquarters
factory
warehouse
bank_building
hospital
school
university
government_building
court_building
data_center
power_plant
airport
shopping_mall
small_business_store
restaurant
'''),
        tags=('building', 'infrastructure', 'city'),
        allowed_scene_roles=('real_world_example', 'macro_context', 'system_boundary'),
    ),
    AssetFamily(
        id='money_economy',
        label='Money & Economy',
        assets=_parse_assets('''
money_coins
money_stack
money_bag
banknote
credit_card
debit_card
digital_payment
interest_symbol
loan_document
debt_chain
tax_symbol
cash_register
price_tag
shopping_cart
wallet
investment_chart
wealth_pyramid
income_arrow
salary_icon
stock_market
stock_chart
gold_bar
crypto_coin
blockchain_symbol
'''),
        tags=('economy', 'money', 'finance'),
        allowed_scene_roles=('root_cause', 'mechanism', 'data_lens', 'takeaway'),
    ),
    AssetFamily(
        id='charts_data_visualization',
        label='Charts & Data Visualization',
        assets=_parse_assets('''
line_chart_up
line_chart_down
bar_chart
pie_chart
inflation_chart
price_curve
demand_supply_graph
economic_cycle_graph
bubble_chart
network_chart
growth_arrow
decline_arrow
trend_line
'''),
        tags=('chart', 'data', 'visualization'),
        allowed_scene_roles=('data_lens', 'feedback_loop', 'mechanism'),
    ),
    AssetFamily(
        id='systems_network_diagrams',
        label='Systems & Network Diagrams',
        assets=_parse_assets('''
node
network_nodes
network_connections
flow_diagram
system_loop
feedback_loop
circular_flow
supply_chain
hierarchy_pyramid
decision_tree
domino_chain
'''),
        tags=('system', 'network', 'diagram'),
        allowed_scene_roles=('system_boundary', 'mechanism', 'feedback_loop'),
    ),
    AssetFamily(
        id='arrows_flow_indicators',
        label='Arrows & Flow Indicators',
        assets=_parse_assets('''
arrow_up
arrow_down
arrow_left
arrow_right
curved_arrow
loop_arrow
cycle_arrow
double_arrow
flow_arrow
timeline_arrow
process_arrow
cause_effect_arrow
'''),
        tags=('arrow', 'flow', 'direction'),
        allowed_scene_roles=('mechanism', 'feedback_loop', 'takeaway'),
    ),
    AssetFamily(
        id='work_productivity',
        label='Work & Productivity',
        assets=_parse_assets('''
briefcase
office_desk
laptop
email
meeting_table
task_list
calendar
clock
overtime_clock
career_ladder
promotion_arrow
burnout_icon
'''),
        tags=('work', 'productivity', 'office'),
        allowed_scene_roles=('real_world_example', 'root_cause', 'takeaway'),
    ),
    AssetFamily(
        id='technology_internet',
        label='Technology & Internet',
        assets=_parse_assets('''
smartphone
app_grid
notification_bell
algorithm_symbol
ai_brain
robot
data_cloud
server
database
internet_globe
wifi_signal
cybersecurity_lock
code_symbol
'''),
        tags=('technology', 'internet', 'digital'),
        allowed_scene_roles=('mechanism', 'system_boundary', 'real_world_example'),
    ),
    AssetFamily(
        id='social_media_system',
        label='Social Media System',
        assets=_parse_assets('''
like_icon
comment_icon
share_icon
follower_counter
social_network_graph
hashtag_symbol
viral_arrow
content_feed
notification_pop
creator_icon
camera_icon
video_icon
live_stream_icon
trend_arrow
'''),
        tags=('social', 'media', 'platform'),
        allowed_scene_roles=('hook', 'mechanism', 'feedback_loop', 'real_world_example'),
    ),
    AssetFamily(
        id='governance_power',
        label='Governance & Power',
        assets=_parse_assets('''
parliament
court_hammer
law_document
constitution_scroll
election_ballot
voting_box
flag
police_badge
surveillance_camera
spy_satellite
military_tank
diplomacy_handshake
border_gate
'''),
        tags=('governance', 'power', 'institution'),
        allowed_scene_roles=('system_boundary', 'root_cause', 'macro_context'),
    ),
    AssetFamily(
        id='global_systems',
        label='Global Systems',
        assets=_parse_assets('''
earth_globe
world_map
trade_routes
shipping_container
cargo_ship
airplane
pipeline
energy_grid
satellite
communication_network
migration_arrow
'''),
        tags=('global', 'geopolitics', 'trade'),
        allowed_scene_roles=('macro_context', 'system_boundary', 'mechanism'),
    ),
    AssetFamily(
        id='crisis_risk',
        label='Crisis & Risk',
        assets=_parse_assets('''
warning_triangle
system_crack
collapse_domino
falling_graph
bank_run
financial_crash
market_panic
cracked_building
power_grid_failure
supply_chain_break
water_shortage
climate_heat
storm_icon
wildfire
flood
pandemic_virus
'''),
        tags=('risk', 'crisis', 'failure'),
        allowed_scene_roles=('tension', 'feedback_loop', 'externality', 'macro_context'),
    ),
    AssetFamily(
        id='environment_resources',
        label='Environment & Resources',
        assets=_parse_assets('''
tree
forest
water_drop
river
mountain
sun
wind_turbine
solar_panel
oil_barrel
gas_pipeline
farmland
food_supply
'''),
        tags=('environment', 'resource', 'ecology'),
        allowed_scene_roles=('externality', 'macro_context', 'real_world_example'),
    ),
    AssetFamily(
        id='future_technology',
        label='Future & Technology',
        assets=_parse_assets('''
ai_network
robot_worker
autonomous_car
smart_city
digital_currency
quantum_chip
automation_factory
future_city
space_satellite
drone
'''),
        tags=('future', 'technology', 'systems'),
        allowed_scene_roles=('macro_context', 'mechanism', 'takeaway'),
    ),
    AssetFamily(
        id='abstract_system_symbols',
        label='Abstract System Symbols',
        assets=_parse_assets('''
gear
lightbulb
puzzle_piece
magnet
chain
broken_chain
key
lock
search_icon
question_mark
exclamation_mark
target
signal_wave
balance_scale
'''),
        tags=('abstract', 'symbol', 'system'),
        allowed_scene_roles=('hook', 'mechanism', 'takeaway', 'conclusion'),
    ),
)

COMPATIBILITY_ASSET_FAMILIES: tuple[AssetFamily, ...] = (
    AssetFamily(
        id='legacy_compatibility',
        label='Legacy Compatibility',
        assets=('bird', 'fish', 'bee', 'deer', 'turtle', 'shield', 'lightning'),
        tags=('legacy', 'compatibility'),
        allowed_scene_roles=('hook', 'real_world_example', 'externality', 'takeaway'),
        catalog_kind='compatibility',
    ),
)

MASTER_ASSET_IDS = tuple(asset for family in MASTER_ASSET_FAMILIES for asset in family.assets)
MASTER_ASSET_ID_SET = set(MASTER_ASSET_IDS)
if len(MASTER_ASSET_IDS) != 219 or len(MASTER_ASSET_ID_SET) != 219:
    raise RuntimeError(f'Master asset catalog must contain exactly 219 unique ids, found {len(MASTER_ASSET_ID_SET)}')

COMPATIBILITY_ASSET_IDS = tuple(asset for family in COMPATIBILITY_ASSET_FAMILIES for asset in family.assets)
CATALOG_ASSET_IDS = MASTER_ASSET_IDS + COMPATIBILITY_ASSET_IDS
CATALOG_ASSET_ID_SET = set(CATALOG_ASSET_IDS)

EXPLICIT_ALIASES: dict[str, tuple[str, ...]] = {
    'person': ('CharacterHappy', 'CharacterSad', 'CharacterGeek', 'person_adult_female', 'person_adult_male', 'person_youth', 'person_senior'),
    'robot': ('PropDeclarativeRobot',),
    'server': ('PropServer',),
    'satellite': ('PropDeclarativeSaturn',),
    'house': ('home',),
    'shopping_cart': ('cart',),
    'data_cloud': ('cloud',),
    'ai_brain': ('ai',),
    'algorithm_symbol': ('algorithm',),
    'network_nodes': ('network',),
    'flow_arrow': ('arrow',),
    'loop_arrow': ('loop',),
    'bank_building': ('bank',),
    'money_coins': ('coin',),
    'bar_chart': ('chart',),
    'earth_globe': ('earth', 'globe'),
    'video_icon': ('media', 'video', 'play'),
    'law_document': ('law',),
    'balance_scale': ('scale',),
    'signal_wave': ('wave',),
    'police_badge': ('people_shield',),
    'energy_grid': ('power',),
    'airplane': ('transport',),
    'shield': ('security_shield',),
}

LEGACY_ALIAS_MAP: dict[str, str] = {
    'shield': 'shield',
    'lightning': 'lightning',
    'home': 'house',
    'cart': 'shopping_cart',
    'cloud': 'data_cloud',
    'ai': 'ai_brain',
    'algorithm': 'algorithm_symbol',
    'network': 'network_nodes',
    'arrow': 'flow_arrow',
    'loop': 'loop_arrow',
    'bank': 'bank_building',
    'coin': 'money_coins',
    'chart': 'bar_chart',
    'growth': 'line_chart_up',
    'earth': 'earth_globe',
    'globe': 'earth_globe',
    'media': 'video_icon',
    'video': 'video_icon',
    'play': 'video_icon',
    'law': 'law_document',
    'scale': 'balance_scale',
    'wave': 'signal_wave',
    'transport': 'airplane',
    'people': 'person_group',
    'book': 'constitution_scroll',
    'security_shield': 'shield',
    'people_shield': 'police_badge',
    'CharacterHappy': 'person',
    'CharacterSad': 'person',
    'CharacterGeek': 'person',
    'PropDeclarativeRobot': 'robot',
    'PropServer': 'server',
    'PropDeclarativeSaturn': 'satellite',
}

ALIAS_INDEX: dict[str, str] = dict(LEGACY_ALIAS_MAP)
for canonical_id, aliases in EXPLICIT_ALIASES.items():
    for alias in aliases:
        ALIAS_INDEX.setdefault(alias, canonical_id)


FAMILY_BY_ASSET_ID = {
    asset_id: family.id
    for family in MASTER_ASSET_FAMILIES + COMPATIBILITY_ASSET_FAMILIES
    for asset_id in family.assets
}


def asset_id_to_component_name(asset_id: str) -> str:
    parts = [part for part in asset_id.split('_') if part]
    return ''.join(part[:1].upper() + part[1:] for part in parts)


def family_for_asset(asset_id: str) -> str:
    canonical = canonical_asset_id(asset_id)
    return FAMILY_BY_ASSET_ID[canonical]


def family_definition(family_id: str) -> AssetFamily:
    for family in MASTER_ASSET_FAMILIES + COMPATIBILITY_ASSET_FAMILIES:
        if family.id == family_id:
            return family
    raise KeyError(f'Unknown asset family: {family_id}')


def list_master_asset_ids() -> tuple[str, ...]:
    return MASTER_ASSET_IDS


def list_catalog_asset_ids(include_compatibility: bool = True) -> tuple[str, ...]:
    return CATALOG_ASSET_IDS if include_compatibility else MASTER_ASSET_IDS


def list_family_ids(include_compatibility: bool = True) -> tuple[str, ...]:
    families = MASTER_ASSET_FAMILIES + (COMPATIBILITY_ASSET_FAMILIES if include_compatibility else ())
    return tuple(family.id for family in families)


def canonical_asset_id(asset_id: str) -> str:
    return ALIAS_INDEX.get(asset_id, asset_id)


def build_alias_index() -> dict[str, str]:
    return dict(ALIAS_INDEX)


def asset_tags(asset_id: str) -> list[str]:
    canonical = canonical_asset_id(asset_id)
    family_id = FAMILY_BY_ASSET_ID[canonical]
    family = family_definition(family_id)
    token_tags = [token for token in canonical.split('_') if token]
    return sorted(set(token_tags + list(family.tags) + [family.id, STYLE_VARIANT]))


def asset_allowed_scene_roles(asset_id: str) -> list[str]:
    canonical = canonical_asset_id(asset_id)
    family = family_definition(FAMILY_BY_ASSET_ID[canonical])
    return list(family.allowed_scene_roles)


def asset_aliases(asset_id: str) -> list[str]:
    canonical = canonical_asset_id(asset_id)
    aliases = list(EXPLICIT_ALIASES.get(canonical, ()))
    aliases.extend(alias for alias, target in LEGACY_ALIAS_MAP.items() if target == canonical and alias not in aliases)
    return sorted(set(aliases))


def asset_catalog_entry(asset_id: str) -> dict[str, Any]:
    canonical = canonical_asset_id(asset_id)
    family = family_definition(FAMILY_BY_ASSET_ID[canonical])
    return {
        'id': canonical,
        'family': family.id,
        'familyLabel': family.label,
        'tags': asset_tags(canonical),
        'aliases': asset_aliases(canonical),
        'allowedSceneRoles': list(family.allowed_scene_roles),
        'styleVariant': STYLE_VARIANT,
        'catalogKind': family.catalog_kind,
        'componentName': asset_id_to_component_name(canonical),
    }


def all_catalog_entries(include_compatibility: bool = True) -> list[dict[str, Any]]:
    asset_ids = list_catalog_asset_ids(include_compatibility=include_compatibility)
    return [asset_catalog_entry(asset_id) for asset_id in asset_ids]

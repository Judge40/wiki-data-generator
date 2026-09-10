from pathlib import Path

import jinja2
import pytest

import parser

TEMPLATES_DIR = Path(__file__).parent / "templates"
_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR))


def _render_monster(overrides: dict | None = None) -> str:
    """Render monster.html.jinja with default stats, overridden as needed per-test."""
    data = {
        "name": "Test Monster",
        "hp": 10,
        "mp": 20,
        "str": 30,
        "offensive_str": 31,
        "defensive_str": 32,
        "intel": 40,
        "offensive_intel": 41,
        "defensive_intel": 42,
        "wisdom": 50,
        "dex": 60,
        "offensive_dex": 61,
        "defensive_dex": 62,
        "moral": "Moral Value",
        "locations": ["Map 70", "Map 71"],
        "drops": [
            {
                "name": "Map 70",
                "items": [
                    {
                        "id": 80,
                        "name": "Item 80",
                        "rates": [{"value": "80%", "label": None}],
                    }
                ],
            }
        ],
    } | (overrides or {})
    return _env.get_template("monster.html.jinja").render(**data)


def test_parse_stats_raises_when_unknown_type():
    with pytest.raises(RuntimeError):
        parser.parse_stats(1, "unknown", "<html></html>")


def test_parse_item_stats_raises_when_page_is_empty():
    item_html = _env.get_template("empty_page.html.jinja").render()

    with pytest.raises(RuntimeError):
        parser.parse_stats(1, "item", item_html)


def test_parse_item_stats_raises_when_unknown_race():
    item_html = _env.get_template("item.html.jinja").render(
        name="Test Item",
        type="Not A Recognised Race Label",
        stats={"Weight": 5},
    )

    with pytest.raises(RuntimeError):
        parser.parse_stats(1, "item", item_html)


@pytest.mark.parametrize(
    "race_label, expected_race",
    [
        ("Human", "Human"),
        ("Devil", "Devil"),
        ("Human & Devil", "Neutral"),
    ],
)
def test_parse_item_stats_returns_expected_race(race_label, expected_race):
    item_html = _env.get_template("item.html.jinja").render(
        name="Test Item",
        type=f"{race_label} Item",
        stats={
            "Weight": 0,
        },
    )

    result = parser.parse_stats(1, "item", item_html)

    assert result["race"] == expected_race


def test_parse_item_stats_raises_when_weight_is_missing():
    item_html = _env.get_template("item.html.jinja").render(
        name="Test Item",
        type="Human Armour",
        stats={"Defense": "10~20"},
    )

    with pytest.raises(RuntimeError):
        parser.parse_stats(1, "item", item_html)


def test_parse_item_stats_returns_expected_dict_when_type_is_armour():
    item_html = _env.get_template("item.html.jinja").render(
        name="Test Armour",
        type="Human Armour",
        stats={
            "Defense": "10~20",
            "Weight": 30,
            "Durability": 40,
        },
    )

    result = parser.parse_stats(1, "item", item_html)

    assert len(result) == 8
    assert result["id"] == 1
    assert result["name"] == "Test Armour"
    assert result["race"] == "Human"
    assert result["type"] == "Armour"
    assert result["defense_min"] == 10
    assert result["defense_max"] == 20
    assert result["weight"] == 30
    assert result["durability"] == 40


def test_parse_item_stats_returns_expected_dict_when_type_is_weapon():
    item_html = _env.get_template("item.html.jinja").render(
        name="Test Weapon",
        type="Human Sword",
        stats={
            "Attack": "10~20",
            "Weight": 30,
            "Durability": 40,
            "Speed": "A(500)",
        },
    )

    result = parser.parse_stats(1, "item", item_html)

    assert len(result) == 9
    assert result["id"] == 1
    assert result["name"] == "Test Weapon"
    assert result["race"] == "Human"
    assert result["type"] == "Sword"
    assert result["attack_min"] == 10
    assert result["attack_max"] == 20
    assert result["weight"] == 30
    assert result["durability"] == 40
    assert result["speed"] == "A(500)"


def test_parse_item_stats_returns_expected_dict_when_type_is_misc():
    item_html = _env.get_template("item.html.jinja").render(
        name="Test Misc Item",
        type="Human Sundry",
        stats={"Weight": 5},
    )

    result = parser.parse_stats(1, "item", item_html)

    assert len(result) == 5
    assert result["id"] == 1
    assert result["name"] == "Test Misc Item"
    assert result["race"] == "Human"
    assert result["type"] == "Sundry"
    assert result["weight"] == 5


def test_parse_item_stats_includes_requirements():
    item_html = _env.get_template("item.html.jinja").render(
        name="Test Armour",
        type="Human Armour",
        stats={
            "Weight": 10,
        },
        reqs={
            "Str": 20,
            "Dex": 30,
            "Skill": 40,
        },
    )

    result = parser.parse_stats(1, "item", item_html)

    assert result["req_str"] == 20
    assert result["req_dex"] == 30
    assert result["req_skill"] == 40


def test_parse_monster_stats_raises_when_page_is_empty():
    monster_html = _env.get_template("empty_page.html.jinja").render()

    with pytest.raises(RuntimeError):
        parser.parse_stats(1, "monster", monster_html)


def test_parse_monster_stats_returns_expected_dict():
    monster_html = _render_monster()

    result = parser.parse_stats(1, "monster", monster_html)

    assert len(result) == 17
    assert result["id"] == 1
    assert result["name"] == "Test Monster"
    assert result["hp"] == 10
    assert result["mp"] == 20
    assert result["strength"] == 30
    assert result["offensive_strength"] == 31
    assert result["defensive_strength"] == 32
    assert result["intelligence"] == 40
    assert result["offensive_intelligence"] == 41
    assert result["defensive_intelligence"] == 42
    assert result["wisdom"] == 50
    assert result["dexterity"] == 60
    assert result["offensive_dexterity"] == 61
    assert result["defensive_dexterity"] == 62
    assert result["moral"] == "Moral Value"
    assert result["maps"][0] == "Map 70"
    assert result["maps"][1] == "Map 71"
    assert result["drops"] == [
        {"monster_id": 1, "item_id": 80, "map": "Map 70", "drop_rate": 80.0}
    ]


def test_parse_monster_stats_keeps_moral_as_the_literal_string_none():
    monster_html = _render_monster({"moral": "None"})

    result = parser.parse_stats(1, "monster", monster_html)

    assert result["moral"] == "None"


def test_parse_monster_stats_handles_empty_locations():
    monster_html = _render_monster({"locations": []})

    result = parser.parse_stats(1, "monster", monster_html)

    assert result["maps"] == []


def test_parse_monster_stats_handles_empty_drops():
    monster_html = _render_monster({"drops": []})

    result = parser.parse_stats(1, "monster", monster_html)

    assert result["drops"] == []


def test_parse_monster_stats_parses_multiple_drops_across_multiple_maps():
    monster_html = _render_monster(
        {
            "drops": [
                {
                    "name": "Map 1",
                    "items": [
                        {
                            "id": 10,
                            "name": "Item 10",
                            "rates": [
                                {"value": "90.00%", "label": "Bonus 1"},
                                {"value": "95.00%", "label": "Bonus 2"},
                                {"value": "100%", "label": "Bonus 3"},
                            ],
                        },
                        {
                            "id": 11,
                            "name": "Item 11",
                            "rates": [
                                {"value": "0.01%", "label": None},
                                {"value": "0.50%", "label": "Bonus"},
                            ],
                        },
                    ],
                },
                {
                    "name": "Map 2",
                    "items": [
                        {
                            "id": 20,
                            "name": "Item 20",
                            "rates": [{"value": "0.20%", "label": None}],
                        }
                    ],
                },
            ]
        }
    )

    result = parser.parse_stats(1, "monster", monster_html)

    assert result["drops"] == [
        {"monster_id": 1, "item_id": 10, "map": "Map 1", "drop_rate": 90.0},
        {"monster_id": 1, "item_id": 11, "map": "Map 1", "drop_rate": 0.01},
        {"monster_id": 1, "item_id": 20, "map": "Map 2", "drop_rate": 0.2},
    ]

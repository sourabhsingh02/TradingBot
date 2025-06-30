import json
from pathlib import Path
from typing import List, Dict

STRATEGY_FILE = Path("saved_strategies.json")


def _read_file() -> List[Dict]:
    if STRATEGY_FILE.exists():
        with open(STRATEGY_FILE, "r") as f:
            return json.load(f)
    return []


def _write_file(data: List[Dict]) -> None:
    with open(STRATEGY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_saved_strategies() -> List[Dict]:
    return _read_file()


def save_strategy(strategy: Dict) -> None:
    """
    Save a new strategy.
    Raises Error if a strategy with the same *name* already exists.
    """
    strategies = _read_file()

    if any(s["name"] == strategy["name"] for s in strategies):
        raise ValueError(f"A strategy named '{strategy['name']}' already exists")

    strategies.append(strategy)
    _write_file(strategies)


def search_saved_strategies(query: str) -> List[Dict]:
    strategies = _read_file()
    return [s for s in strategies if query.lower() in s["name"].lower()]



def delete_strategy(name: str) -> None:
    strategies = _read_file()
    updated = [s for s in strategies if s["name"] != name]

    if len(strategies) == len(updated):
        raise ValueError(f"No strategy named '{name}' found")

    _write_file(updated)

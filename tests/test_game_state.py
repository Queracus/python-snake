import pytest
from game import GameState


def test_game_state_transitions():
    assert GameState.MENU.value == 1
    assert GameState.PLAYING.value == 2
    assert GameState.PAUSED.value == 3
    assert GameState.GAME_OVER.value == 5
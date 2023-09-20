import os
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from databallpy.errors import DataBallPyError
from databallpy.get_match import get_match
from databallpy.match import Match
from databallpy.utils.utils import MISSING_INT
from databallpy.warnings import DataBallPyWarning
from expected_outcomes import (
    DRIBBLE_EVENTS_OPTA_TRACAB,
    PASS_EVENTS_OPTA_TRACAB,
    SHOT_EVENTS_OPTA_TRACAB,
)


class TestMatch(unittest.TestCase):
    def setUp(self):
        td_tracab_loc = "tests/test_data/tracab_td_test.dat"
        md_tracab_loc = "tests/test_data/tracab_metadata_test.xml"
        ed_opta_loc = "tests/test_data/f24_test.xml"
        md_opta_loc = "tests/test_data/f7_test.xml"
        self.td_provider = "tracab"
        self.ed_provider = "opta"

        self.expected_match_tracab_opta = get_match(
            tracking_data_loc=td_tracab_loc,
            tracking_metadata_loc=md_tracab_loc,
            tracking_data_provider="tracab",
            event_data_loc=ed_opta_loc,
            event_metadata_loc=md_opta_loc,
            event_data_provider="opta",
            check_quality=False,
        )

        self.expected_match_tracab = get_match(
            tracking_data_loc=td_tracab_loc,
            tracking_metadata_loc=md_tracab_loc,
            tracking_data_provider="tracab",
            check_quality=False,
        )

        td_metrica_loc = "tests/test_data/metrica_tracking_data_test.txt"
        md_metrica_loc = "tests/test_data/metrica_metadata_test.xml"
        ed_metrica_loc = "tests/test_data/metrica_event_data_test.json"

        self.expected_match_metrica = get_match(
            tracking_data_loc=td_metrica_loc,
            tracking_metadata_loc=md_metrica_loc,
            tracking_data_provider="metrica",
            event_data_loc=ed_metrica_loc,
            event_metadata_loc=md_metrica_loc,
            event_data_provider="metrica",
            check_quality=False,
        )

        self.match_to_sync = get_match(
            tracking_data_loc="tests/test_data/sync/tracab_td_sync_test.dat",
            tracking_metadata_loc="tests/test_data/sync/tracab_metadata_sync_test.xml",
            tracking_data_provider="tracab",
            event_data_loc="tests/test_data/sync/opta_events_sync_test.xml",
            event_metadata_loc="tests/test_data/sync/opta_metadata_sync_test.xml",
            event_data_provider="opta",
            check_quality=False,
        )

        self.expected_match_opta = get_match(
            event_data_loc=ed_opta_loc,
            event_metadata_loc=md_opta_loc,
            event_data_provider="opta",
        )

    def test_match_eq(self):
        assert self.expected_match_metrica == self.expected_match_metrica
        assert self.expected_match_metrica != self.expected_match_tracab_opta

    def test_match_copy(self):
        copied = self.expected_match_tracab_opta.copy()
        assert self.expected_match_tracab_opta == copied

        copied.pitch_dimensions[0] = 22.0
        assert self.expected_match_tracab_opta != copied

        copied.pitch_dimensions[0] = self.expected_match_tracab_opta.pitch_dimensions[0]
        assert self.expected_match_tracab_opta == copied

        copied.tracking_data.iloc[0, 0] = -100000.0
        assert self.expected_match_tracab_opta != copied

    def test_match_post_init(self):
        # tracking data
        with self.assertRaises(TypeError):
            Match(
                tracking_data="tracking_data",
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=pd.DataFrame(
                    {"frame": [1], "home_1_x": [12], "ball_z": [13]}
                ),
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # tracking data provider
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=14.3,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # event data
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data="event_data",
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=pd.DataFrame(
                    {
                        "event_id": [1],
                        "player": ["player_1"],
                        "databallpy_event": ["pass"],
                    }
                ),
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=pd.DataFrame(
                    {
                        "event_id": [1],
                        "databallpy_event": ["pass"],
                        "period_id": [1],
                        "team_id": [1],
                        "player_id": [1],
                        "start_x": [1],
                        "start_y": [1],
                        "player": ["player_1"],
                        "datetime": ["2020-01-01 00:00:00"],  # not datetime object
                    }
                ),
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=pd.DataFrame(
                    {
                        "event_id": [1],
                        "databallpy_event": ["pass"],
                        "period_id": [1],
                        "team_id": [1],
                        "player_id": [1],
                        "start_x": [1],
                        "start_y": [1],
                        "player": ["player_1"],
                        "datetime": pd.to_datetime(
                            ["2020-01-01 00:00:00"]
                        ),  # no timezone assigned
                    }
                ),
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # event data provider
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=["opta"],
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # pitch dimensions
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions={1: 22, 2: 11},
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=[10.0, 11.0, 12.0],
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=[10, 11.0],
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # periods
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=[1, 2, 3, 4, 5],
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=pd.DataFrame({"times": [1, 2, 3, 4, 5]}),
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=pd.DataFrame({"period": [0, 1, 2, 3, 4]}),
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=pd.DataFrame({"period": [1, 1, 2, 3, 4, 5]}),
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            periods = self.expected_match_tracab_opta.periods.copy()
            periods["start_datetime_ed"] = periods["start_datetime_ed"].dt.tz_localize(
                None
            )
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # frame rate
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=25.0,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=-25,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # team id
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=123.0,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # team name
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=["teamone"],
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # team score
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=11.5,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=-3,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # team formation
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=[1, 4, 2, 2],
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation="one-four-three-three",
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # team players
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players="one-four-three-three",
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(ValueError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players.drop(
                    "shirt_num", axis=1
                ),
                country=self.expected_match_tracab_opta.country,
            )

        # pitch axis
        with self.assertWarns(DataBallPyWarning):
            td_changed = self.expected_match_tracab_opta.tracking_data.copy()
            td_changed["ball_x"] += 10.0
            Match(
                tracking_data=td_changed,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertWarns(DataBallPyWarning):
            td_changed = self.expected_match_tracab_opta.tracking_data.copy()
            td_changed["ball_y"] += 10.0

            Match(
                tracking_data=td_changed,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # playing direction
        with self.assertRaises(DataBallPyError):
            td_changed = self.expected_match_tracab_opta.tracking_data.copy()
            td_changed.loc[0, "home_34_x"] = 3.0

            Match(
                tracking_data=td_changed,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        with self.assertRaises(DataBallPyError):
            td_changed = self.expected_match_tracab_opta.tracking_data.copy()
            td_changed.loc[0, "away_17_x"] = -3.0
            Match(
                tracking_data=td_changed,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
            )

        # country
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=["Netherlands", "Germany"],
            )
        # shot_events
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
                shot_events=["shot", "goal"],
            )
        # shot_events
        with self.assertRaises(TypeError):
            Match(
                tracking_data=self.expected_match_tracab_opta.tracking_data,
                tracking_data_provider=self.td_provider,
                event_data=self.expected_match_tracab_opta.event_data,
                event_data_provider=self.ed_provider,
                pitch_dimensions=self.expected_match_tracab_opta.pitch_dimensions,
                periods=self.expected_match_tracab_opta.periods,
                frame_rate=self.expected_match_tracab_opta.frame_rate,
                home_team_id=self.expected_match_tracab_opta.home_team_id,
                home_formation=self.expected_match_tracab_opta.home_formation,
                home_score=self.expected_match_tracab_opta.home_score,
                home_team_name=self.expected_match_tracab_opta.home_team_name,
                home_players=self.expected_match_tracab_opta.home_players,
                away_team_id=self.expected_match_tracab_opta.away_team_id,
                away_formation=self.expected_match_tracab_opta.away_formation,
                away_score=self.expected_match_tracab_opta.away_score,
                away_team_name=self.expected_match_tracab_opta.away_team_name,
                away_players=self.expected_match_tracab_opta.away_players,
                country=self.expected_match_tracab_opta.country,
                shot_events={"shot": "goal"},
            )

    def test_preprosessing_status(self):
        match = self.match_to_sync.copy()
        match.allow_synchronise_tracking_and_event_data = True
        assert match.is_synchronised is False
        assert (
            match.preprocessing_status
            == "Preprocessing status:\n\tis_synchronised = False"
        )
        match.synchronise_tracking_and_event_data(n_batches_per_half=1)
        assert match.is_synchronised is True
        assert (
            match.preprocessing_status
            == "Preprocessing status:\n\tis_synchronised = True"
        )

    def test_synchronise_tracking_and_event_data_not_allowed(self):
        match = self.match_to_sync.copy()
        match.allow_synchronise_tracking_and_event_data = False
        with self.assertRaises(DataBallPyError):
            match.synchronise_tracking_and_event_data(n_batches_per_half=1)

    def test__repr__(self):
        assert (
            self.expected_match_metrica.__repr__()
            == "databallpy.match.Match object: Team A 0 - 2 Team B 2019-02-21 03:30:07"
        )
        assert (
            self.expected_match_metrica.name
            == "Team A 0 - 2 Team B 2019-02-21 03:30:07"
        )

    def test_match__eq__(self):
        assert not self.expected_match_tracab_opta == pd.DataFrame()

    def test_match_name(self):
        assert (
            self.expected_match_tracab_opta.name
            == "TeamOne 3 - 1 TeamTwo 2023-01-14 16:46:39"
        )
        assert (
            self.expected_match_opta.name == "TeamOne 3 - 1 TeamTwo 2023-01-22 12:18:32"
        )

    def test_match_home_players_column_ids(self):
        assert self.expected_match_tracab_opta.home_players_column_ids() == [
            "home_34_x",
            "home_34_y",
        ]

    def test_match_away_players_column_ids(self):
        assert self.expected_match_tracab_opta.away_players_column_ids() == [
            "away_17_x",
            "away_17_y",
        ]

    def test_match_player_column_id_to_full_name(self):
        res_name_home = self.expected_match_tracab_opta.player_column_id_to_full_name(
            "home_1"
        )
        assert res_name_home == "Piet Schrijvers"

        res_name_away = self.expected_match_tracab_opta.player_column_id_to_full_name(
            "away_2"
        )
        assert res_name_away == "TestSpeler"

    def test_match_player_id_to_column_id(self):
        res_column_id_home = self.expected_match_tracab_opta.player_id_to_column_id(
            19367
        )
        assert res_column_id_home == "home_1"

        res_column_id_away = self.expected_match_tracab_opta.player_id_to_column_id(
            450445
        )
        assert res_column_id_away == "away_2"

        with self.assertRaises(ValueError):
            self.expected_match_tracab_opta.player_id_to_column_id(4)

    def test_match_shots_df_without_td_features(self):
        expected_df = pd.DataFrame(
            {
                "event_id": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].event_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].event_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].event_id,
                ],
                "player_id": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].player_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].player_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].player_id,
                ],
                "period_id": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].period_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].period_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].period_id,
                ],
                "minutes": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].minutes,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].minutes,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].minutes,
                ],
                "seconds": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].seconds,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].seconds,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].seconds,
                ],
                "datetime": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].datetime,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].datetime,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].datetime,
                ],
                "start_x": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].start_x,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].start_x,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].start_x,
                ],
                "start_y": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].start_y,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].start_y,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].start_y,
                ],
                "team_id": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].team_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].team_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].team_id,
                ],
                "shot_outcome": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].shot_outcome,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].shot_outcome,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].shot_outcome,
                ],
                "y_target": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].y_target,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].y_target,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].y_target,
                ],
                "z_target": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].z_target,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].z_target,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].z_target,
                ],
                "body_part": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].body_part,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].body_part,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].body_part,
                ],
                "type_of_play": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].type_of_play,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].type_of_play,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].type_of_play,
                ],
                "first_touch": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].first_touch,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].first_touch,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].first_touch,
                ],
                "created_oppertunity": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].created_oppertunity,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].created_oppertunity,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].created_oppertunity,
                ],
                "related_event_id": [
                    SHOT_EVENTS_OPTA_TRACAB[2512690515].related_event_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690516].related_event_id,
                    SHOT_EVENTS_OPTA_TRACAB[2512690517].related_event_id,
                ],
                "ball_goal_distance": [np.nan, np.nan, np.nan],
                "ball_gk_distance": [np.nan, np.nan, np.nan],
                "shot_angle": [np.nan, np.nan, np.nan],
                "gk_angle": [np.nan, np.nan, np.nan],
                "pressure_on_ball": [np.nan, np.nan, np.nan],
                "n_obstructive_players": [MISSING_INT, MISSING_INT, MISSING_INT],
            }
        )
        match = self.expected_match_tracab_opta.copy()
        # make sure it will not try to add tracking data features
        match.allow_synchronise_tracking_and_event_data = False
        shots_df = self.expected_match_tracab_opta.shots_df
        pd.testing.assert_frame_equal(shots_df, expected_df)

    @patch(
        "databallpy.load_data.event_data.shot_event."
        "ShotEvent.add_tracking_data_features"
    )
    def test_match_shots_df_tracking_data_features(
        self, mock_add_tracking_data_features
    ):
        mock_add_tracking_data_features.return_value = "Return value"

        # for away team shot
        match = self.expected_match_tracab_opta.copy()
        match.tracking_data["event_id"] = [np.nan, np.nan, np.nan, np.nan, 2512690516]
        match.tracking_data["databallpy_event"] = [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            "shot",
        ]
        match._is_synchronised = True
        match.shot_events = {2512690516: match.shot_events[2512690516]}
        match.add_tracking_data_features_to_shots()

        expected_team_side = "away"
        expected_td_frame = match.tracking_data.iloc[-1]
        pitch_dimension = match.pitch_dimensions
        expected_column_id = "away_1"
        expected_gk_column_id = "home_1"

        called_args, _ = mock_add_tracking_data_features.call_args_list[-1]
        called_td_frame = called_args[0]
        called_team_side = called_args[1]
        called_pitch_dimension = called_args[2]
        called_column_id = called_args[3]
        called_gk_column_id = called_args[4]

        pd.testing.assert_series_equal(called_td_frame, expected_td_frame)
        assert called_team_side == expected_team_side
        assert called_pitch_dimension == pitch_dimension
        assert called_column_id == expected_column_id
        assert called_gk_column_id == expected_gk_column_id

        # for home team shot
        match = self.expected_match_tracab_opta.copy()
        match.tracking_data["event_id"] = [np.nan, np.nan, 2512690515, np.nan, np.nan]
        match.tracking_data["databallpy_event"] = [
            np.nan,
            np.nan,
            "own_goal",
            np.nan,
            np.nan,
        ]
        match._is_synchronised = True
        match.shot_events = {2512690515: match.shot_events[2512690515]}
        match.add_tracking_data_features_to_shots()

        expected_team_side = "home"
        expected_td_frame = match.tracking_data.iloc[-3]
        pitch_dimension = match.pitch_dimensions
        expected_column_id = "home_2"
        expected_gk_column_id = "away_2"

        called_args, _ = mock_add_tracking_data_features.call_args_list[-1]
        called_td_frame = called_args[0]
        called_team_side = called_args[1]
        called_pitch_dimension = called_args[2]
        called_column_id = called_args[3]
        called_gk_column_id = called_args[4]

        pd.testing.assert_series_equal(called_td_frame, expected_td_frame)
        assert called_team_side == expected_team_side
        assert called_pitch_dimension == pitch_dimension
        assert called_column_id == expected_column_id
        assert called_gk_column_id == expected_gk_column_id

        with self.assertRaises(DataBallPyError):
            match._is_synchronised = False
            match.add_tracking_data_features_to_shots()

    def test_match_dribbles_df_without_td_features(self):
        expected_df = pd.DataFrame(
            {
                "event_id": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].event_id],
                "player_id": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].player_id],
                "period_id": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].period_id],
                "minutes": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].minutes],
                "seconds": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].seconds],
                "datetime": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].datetime],
                "start_x": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].start_x],
                "start_y": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].start_y],
                "team_id": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].team_id],
                "related_event_id": [
                    DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].related_event_id
                ],
                "duel_type": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].duel_type],
                "outcome": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].outcome],
                "has_opponent": [DRIBBLE_EVENTS_OPTA_TRACAB[2499594285].has_opponent],
            }
        )
        dribbles_df = self.expected_match_tracab_opta.dribbles_df
        pd.testing.assert_frame_equal(dribbles_df, expected_df)

    def test_match_passes_df_without_td_features(self):
        expected_df = pd.DataFrame(
            {
                "event_id": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].event_id,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].event_id,
                ],
                "player_id": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].player_id,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].player_id,
                ],
                "period_id": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].period_id,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].period_id,
                ],
                "minutes": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].minutes,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].minutes,
                ],
                "seconds": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].seconds,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].seconds,
                ],
                "datetime": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].datetime,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].datetime,
                ],
                "start_x": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].start_x,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].start_x,
                ],
                "start_y": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].start_y,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].start_y,
                ],
                "team_id": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].team_id,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].team_id,
                ],
                "outcome": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].outcome,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].outcome,
                ],
                "end_x": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].end_x,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].end_x,
                ],
                "end_y": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].end_y,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].end_y,
                ],
                "length": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].length,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].length,
                ],
                "angle": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].angle,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].angle,
                ],
                "pass_type": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].pass_type,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].pass_type,
                ],
                "set_piece": [
                    PASS_EVENTS_OPTA_TRACAB[2499594225].set_piece,
                    PASS_EVENTS_OPTA_TRACAB[2499594243].set_piece,
                ],
            }
        )
        passes_df = self.expected_match_tracab_opta.passes_df
        pd.testing.assert_frame_equal(passes_df, expected_df)

    def test_match_requires_event_data_wrapper(self):
        match = self.expected_match_opta.copy()
        with self.assertRaises(DataBallPyError):
            match.synchronise_tracking_and_event_data()

    def test_match_requires_tracking_data_wrapper(self):
        match = self.expected_match_tracab.copy()
        with self.assertRaises(DataBallPyError):
            match.synchronise_tracking_and_event_data()

    def test_save_match(self):
        assert not os.path.exists(
            "tests/test_data/TeamOne 3 - 1 TeamTwo 2023-01-22 16:46:39.pickle"
        )
        match = self.match_to_sync.copy()
        match.allow_synchronise_tracking_and_event_data = True
        match.save_match(path="tests/test_data")
        assert os.path.exists(
            "tests/test_data/TeamOne 3 - 1 TeamTwo 2023-01-22 16:46:39.pickle"
        )
        os.remove("tests/test_data/TeamOne 3 - 1 TeamTwo 2023-01-22 16:46:39.pickle")

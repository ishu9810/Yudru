import unittest

from src.communication.message_parser import parse_message


class FakeMsg:
    def __init__(self, msg_type, **kwargs):
        self._msg_type = msg_type
        for key, val in kwargs.items():
            setattr(self, key, val)

    def get_type(self):
        return self._msg_type


class TestMavlinkParser(unittest.TestCase):
    def test_parse_position(self):
        msg = FakeMsg("GLOBAL_POSITION_INT", lat=370000000, lon=-1220000000, relative_alt=10000, hdg=9000)
        parsed = parse_message(msg)
        self.assertAlmostEqual(37.0, parsed["lat"])
        self.assertAlmostEqual(-122.0, parsed["lon"])
        self.assertAlmostEqual(10.0, parsed["alt_m"])
        self.assertEqual(90.0, parsed["heading_deg"])

    def test_parse_sys_status(self):
        msg = FakeMsg("SYS_STATUS", voltage_battery=15000, battery_remaining=66)
        parsed = parse_message(msg)
        self.assertEqual(15.0, parsed["battery_v"])
        self.assertEqual(66, parsed["battery_pct"])


if __name__ == "__main__":
    unittest.main()

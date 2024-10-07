from src.interfaces.common.enums import Granularity


def test_enum_granularity():
    assert Granularity.DAILY.value == "daily"
    assert Granularity.WEEKLY.value == "weekly"
    assert len(Granularity.list()) > 0

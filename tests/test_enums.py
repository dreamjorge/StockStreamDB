import pytest
from src.interfaces.common.enums import Granularity  # Adjust the import path as necessary
from enum import Enum  # Ensure this is imported

def test_granularity_list():
    # Ensure the list method returns the expected values
    expected = ['hourly', 'daily', 'weekly', 'monthly']
    assert Granularity.list() == expected

@pytest.mark.parametrize("granularity, expected_rule", [
    (Granularity.HOURLY, 'H'),
    (Granularity.DAILY, 'D'),
    (Granularity.WEEKLY, 'W'),
    (Granularity.MONTHLY, 'M'),
])
def test_resample_rule(granularity, expected_rule):
    # Ensure the correct resample rule is returned for each granularity
    assert granularity.resample_rule() == expected_rule


def test_resample_rule_invalid_granularity():
    # Test invalid granularity by passing a value that doesn't exist in the Granularity enum
    invalid_granularity = "invalid"
    
    # Simulate passing the invalid granularity and ensure a ValueError is raised
    with pytest.raises(ValueError, match=f"'{invalid_granularity}' is not a valid Granularity"):
        Granularity(invalid_granularity).resample_rule()
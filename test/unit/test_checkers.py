"""These tests confirm that the checkers can handle various exceptions"""
from pathlib import Path

import pytest
import python_ags4

from app.checkers import check_bgs, check_ags
from app.bgs_rules import bgs_rules_version

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'

AGS_FILE_DATA = {
    'example_ags.ags': ('2 error(s) found in file!', False),
    'empty.ags': ('6 error(s) found in file!', False),
    'real/43370.ags': ('139 error(s) found in file!', False),
    'extension_is.bad': ('ERROR: extension_is.bad is not .ags format', False),
}


@pytest.mark.parametrize('filename, expected_rules', [
    ('example_ags.ags', []),
    ('random_binary.ags', ['UnicodeDecodeError']),
    ('nonsense.ags', ['Rule 2a', 'Rule 3', 'Rule 5', 'Rule 13', 'Rule 14', 'Rule 15', 'Rule 17']),
    ('empty.ags', ['Rule 13', 'Rule 14', 'Rule 15', 'Rule 17']),
    ('real/A3040_03.ags', ['Rule 2a', 'Rule 3', 'Rule 2c', 'Rule 19a', 'Rule 19b', 'Rule 4a', 'Rule 5']),
    ('real/43370.ags', ['Rule 2a', 'Rule 1']),
    ('real/JohnStPrimarySchool.ags', ['Rule 2a', 'Rule 4b', 'Rule 5', 'Rule 3']),
    ('real/19684.ags', ['Rule 2a', 'Rule 3', 'Rule 5', 'Rule 13', 'Rule 14', 'Rule 15', 'Rule 17', 'General']),
    # This file crashes because it asks for user input
    # ('real/E52A4379 (2).ags', {}),
])
def test_check_ags(filename, expected_rules):
    """Check that broken rules are returned and exceptions handled correctly."""
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = check_ags(filename)

    # Assert
    # Check that metadata fields are correct
    assert result['checker'] == f'python_ags4 v{python_ags4.__version__}'
    assert list(result['errors'].keys()) == expected_rules


@pytest.mark.parametrize('filename, expected_rules, file_read_message', [
    ('example_ags.ags',
     [], None),
    ('random_binary.ags',
     [], None),
    ('nonsense.ags',
     ['Rule 2a', 'Rule 3', 'Rule 5', 'Rule 13', 'Rule 14', 'Rule 15', 'Rule 17'],
     None),
    ('empty.ags',
     ['Rule 13', 'Rule 14', 'Rule 15', 'Rule 17'],
     None),
    ('real/A3040_03.ags',
     ['Rule 2a', 'Rule 3', 'Rule 2c', 'Rule 19a', 'Rule 19b', 'Rule 4a', 'Rule 5'],
     None),
    ('real/43370.ags',
     ['Rule 2a', 'Rule 1'],
     None),
    ('real/JohnStPrimarySchool.ags',
     ['Rule 2a', 'Rule 4b', 'Rule 5', 'Rule 3'],
     None),
    ('real/19684.ags',
     ['Rule 2a', 'Rule 3', 'Rule 5', 'Rule 13', 'Rule 14', 'Rule 15', 'Rule 17', 'General'],
     None),
    # This file crashes because it asks for user input
    # ('real/E52A4379 (2).ags', {}),
])
def test_check_bgs(filename, expected_rules, file_read_message):
    """Check different rules and file_read_messages are reported correctly."""
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = check_bgs(filename)

    # Assert
    # Check that metadata fields are correct
    assert result['checker'] == f'bgs_rules v{bgs_rules_version}'
    assert list(result['errors'].keys()) == expected_rules
    file_read_errors = result['errors'].get('File read error')
    if file_read_errors:
        assert len(file_read_errors) == 1
        assert file_read_errors[0]['desc'] == file_read_message

import pytest
from score_processor import ScoreProcessor

@pytest.fixture
def processor():
    """Provides a fresh ScoreProcessor instance before each test."""
    return ScoreProcessor()

def test_successful_calculation(processor, tmp_path):
    # 1. Create a temporary text file and write a valid number inside it
    test_file = tmp_path / "valid_score.txt"
    test_file.write_text("85")
    
    # 2. Run the processor on the temporary file
    result = processor.process_score_file(str(test_file))
    
    # 3. Verify 85 * 10 = 850
    assert result == 850

def test_missing_file_raises_error(processor):
    # Verify that a non-existent file triggers the FileNotFoundError
    with pytest.raises(FileNotFoundError):
        processor.process_score_file("this_file_does_not_exist.txt")

def test_invalid_data_raises_error(processor, tmp_path):
    # 1. Create a temporary text file with letters instead of numbers
    test_file = tmp_path / "bad_score.txt"
    test_file.write_text("eighty-five")
    
    # 2. Verify that it triggers a ValueError
    with pytest.raises(ValueError):
        processor.process_score_file(str(test_file))
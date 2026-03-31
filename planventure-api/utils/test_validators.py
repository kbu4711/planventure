import pytest
from .validators import validate_email, validate_username

def test_valid_emails():
    """Test validation of properly formatted email addresses"""
    valid_emails = [
        "test@example.com",
        "user.name@domain.com",
        "user+tag@example.co.uk",
        "123@domain.com",
        "user@sub.domain.com"
    ]
    for email in valid_emails:
        assert validate_email(email) is True

def test_invalid_emails():
    """Test validation of improperly formatted email addresses"""
    invalid_emails = [
        "test@.com",
        "@domain.com",
        "test@domain",
        "test@domain.",
        "test.domain.com",
        "test@domain@.com",
        "test space@domain.com"
    ]
    for email in invalid_emails:
        assert validate_email(email) is False

def test_edge_cases():
    """Test validation with edge cases"""
    assert validate_email("") is False
    with pytest.raises(TypeError):
        validate_email(None)

def test_valid_usernames():
    """Test validation of properly formatted usernames"""
    valid_usernames = [
        "user123",
        "_user",
        "john_doe",
        "a123",
        "Developer42",
        "code_master",
        "Alice_Bob_123"
    ]
    for username in valid_usernames:
        assert validate_username(username) is True

def test_invalid_usernames():
    """Test validation of improperly formatted usernames"""
    invalid_usernames = [
        "ab",  # too short
        "a" * 17,  # too long
        "123user",  # starts with number
        "__user",  # multiple underscores at start
        "user name",  # contains space
        "user@name",  # special character
        "-user",  # starts with hyphen
        "user-",  # ends with hyphen
    ]
    for username in invalid_usernames:
        assert validate_username(username) is False

def test_username_edge_cases():
    """Test username validation with edge cases"""
    assert validate_username("") is False
    with pytest.raises(TypeError):
        validate_username(None)


# New Username Validator Tests

def test_new_username_valid_starts_with_letter():
    """Test usernames starting with letters"""
    valid_usernames = [
        "abc",  # minimum length (3)
        "user",
        "Admin123",
        "john_doe",
        "alice_bob_1",
        "TestUser99",
        "a_b_c_d_e_f_g_h"  # 16 chars (maximum length)
    ]
    for username in valid_usernames:
        assert validate_username(username) is True, f"Expected {username} to be valid"


def test_new_username_valid_starts_with_single_underscore():
    """Test usernames starting with single underscore"""
    valid_usernames = [
        "_ab",  # minimum length after underscore
        "_user",
        "_test123",
        "_john_doe",
        "_a_b_c_d_e_f_g"  # 16 chars starting with underscore
    ]
    for username in valid_usernames:
        assert validate_username(username) is True, f"Expected {username} to be valid"


def test_new_username_valid_with_numbers_and_underscores():
    """Test usernames containing numbers and underscores after first character"""
    valid_usernames = [
        "a1b",
        "user_123",
        "test_user_99",
        "a_1_2_3_test_4"
    ]
    for username in valid_usernames:
        assert validate_username(username) is True, f"Expected {username} to be valid"


def test_new_username_invalid_too_short():
    """Test usernames under 3 characters"""
    invalid_usernames = [
        "a",
        "ab",
        "_a",
        "_",
        ""
    ]
    for username in invalid_usernames:
        assert validate_username(username) is False, f"Expected {username} to be invalid"


def test_new_username_invalid_too_long():
    """Test usernames over 16 characters"""
    invalid_usernames = [
        "a" * 17,
        "user_name_is_long_17",
        "_this_is_over_16_chars"
    ]
    for username in invalid_usernames:
        assert validate_username(username) is False, f"Expected {username} to be invalid"


def test_new_username_invalid_starts_with_number():
    """Test usernames starting with numbers"""
    invalid_usernames = [
        "1user",
        "123abc",
        "9_test"
    ]
    for username in invalid_usernames:
        assert validate_username(username) is False, f"Expected {username} to be invalid"


def test_new_username_invalid_multiple_underscores_at_start():
    """Test usernames starting with multiple underscores"""
    invalid_usernames = [
        "__user",
        "___test",
        "__a",
        "____"
    ]
    for username in invalid_usernames:
        assert validate_username(username) is False, f"Expected {username} to be invalid"


def test_new_username_invalid_special_characters():
    """Test usernames with invalid special characters"""
    invalid_usernames = [
        "user@name",
        "user-name",
        "user.name",
        "user name",
        "user!",
        "test#user",
        "user$",
        "user%",
        "user&name",
        "user(test)",
        "user+test"
    ]
    for username in invalid_usernames:
        assert validate_username(username) is False, f"Expected {username} to be invalid"


def test_new_username_invalid_lowercase_special_chars():
    """Test usernames with lowercase or symbols that aren't allowed"""
    invalid_usernames = [
        "user\nname",  # newline
        "user\tname",  # tab
        "user\rname",  # carriage return
    ]
    for username in invalid_usernames:
        assert validate_username(username) is False, f"Expected {username} to be invalid"


def test_new_username_edge_cases_min_max():
    """Test edge cases at minimum and maximum lengths"""
    # Minimum valid (3 chars)
    assert validate_username("abc") is True
    assert validate_username("_ab") is True
    assert validate_username("ab") is False  # Just under minimum
    
    # Maximum valid (16 chars)
    assert validate_username("a" * 16) is True
    assert validate_username("_" + "a" * 15) is True
    assert validate_username("a" * 17) is False  # Just over maximum


def test_new_username_case_sensitivity():
    """Test that usernames accept both upper and lowercase letters"""
    valid_usernames = [
        "User",
        "USER",
        "user",
        "uSeR_teSt",
        "ABC123",
        "_AaBbCc"
    ]
    for username in valid_usernames:
        assert validate_username(username) is True, f"Expected {username} to be valid"


def test_new_username_type_errors():
    """Test username validation with non-string types"""
    with pytest.raises(TypeError):
        validate_username(None)
    with pytest.raises(AttributeError):
        validate_username(123)
    with pytest.raises(AttributeError):
        validate_username([])
    with pytest.raises(AttributeError):
        validate_username({})
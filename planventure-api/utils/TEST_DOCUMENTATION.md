# Test Documentation: test_validators.py

This document provides comprehensive documentation of all unit tests in `test_validators.py`. These tests validate two main validator functions: `validate_email()` and `validate_username()`.

---

## Overview

**Total Tests:** 18  
**Test File:** `utils/test_validators.py`  
**Modules Tested:** `validators.validate_email()`, `validators.validate_username()`  
**Test Framework:** pytest

---

## Email Validator Tests

### 1. test_valid_emails

**Purpose:** Validate that properly formatted email addresses are accepted

**Requirements Tested:**
- Email addresses with standard format (user@domain.com)
- Email addresses with dots in local part (user.name@domain.com)
- Email addresses with plus signs for filtering (user+tag@example.co.uk)
- Email addresses starting with numbers (123@domain.com)
- Email addresses with subdomain levels (user@sub.domain.com)

**Test Cases:**
```
✓ test@example.com
✓ user.name@domain.com
✓ user+tag@example.co.uk
✓ 123@domain.com
✓ user@sub.domain.com
```

**Expected Result:** All test cases should return `True`

---

### 2. test_invalid_emails

**Purpose:** Validate that improperly formatted email addresses are rejected

**Requirements Tested:**
- Emails with missing domain name (test@.com)
- Emails with missing local part (@domain.com)
- Emails without top-level domain (test@domain)
- Emails with trailing dot on domain (test@domain.)
- Emails without @ symbol (test.domain.com)
- Emails with multiple @ symbols (test@domain@.com)
- Emails with spaces (test space@domain.com)

**Test Cases:**
```
✗ test@.com
✗ @domain.com
✗ test@domain
✗ test@domain.
✗ test.domain.com
✗ test@domain@.com
✗ test space@domain.com
```

**Expected Result:** All test cases should return `False`

---

### 3. test_edge_cases (Email)

**Purpose:** Test edge cases for email validation

**Requirements Tested:**
- Empty string handling
- None/null value handling

**Test Cases:**
```
✗ "" (empty string)
✗ None (raises TypeError)
```

**Expected Result:** 
- Empty string returns `False`
- `None` raises `TypeError`

---

## Legacy Username Validator Tests

These tests verify the original username validator behavior before the new requirements were implemented.

### 4. test_valid_usernames

**Purpose:** Validate that properly formatted usernames are accepted

**Test Cases:**
```
✓ user123
✓ _user
✓ john_doe
✓ a123
✓ Developer42
✓ code_master
✓ Alice_Bob_123
```

**Expected Result:** All test cases should return `True`

---

### 5. test_invalid_usernames

**Purpose:** Validate that improperly formatted usernames are rejected

**Test Cases:**
```
✗ ab (too short - less than 3 chars)
✗ aaaaaaaaaaaaaaaaaa (too long - more than 16 chars)
✗ 123user (starts with number)
✗ __user (multiple underscores at start)
✗ user name (contains space)
✗ user@name (special character)
✗ -user (starts with hyphen)
✗ user- (ends with hyphen)
```

**Expected Result:** All test cases should return `False`

---

### 6. test_username_edge_cases (Legacy)

**Purpose:** Test edge cases for username validation

**Test Cases:**
```
✗ "" (empty string)
✗ None (raises TypeError)
```

**Expected Result:**
- Empty string returns `False`
- `None` raises `TypeError`

---

## New Username Validator Tests

These tests comprehensively validate the new username requirements:
- **Length:** 3-16 characters
- **First character:** Letter or single underscore
- **Subsequent characters:** Letters, numbers, underscores
- **Prohibited:** No double underscores at start, no special characters

### 7. test_new_username_valid_starts_with_letter

**Purpose:** Validate usernames that start with a letter

**Requirements:**
- Minimum length of 3 characters
- First character is a letter (A-Z, a-z)
- Can contain letters, numbers, underscores after first character

**Test Cases:**
```
✓ abc (minimum length)
✓ user
✓ Admin123
✓ john_doe
✓ alice_bob_1
✓ TestUser99
✓ a_b_c_d_e_f_g_h (16 chars - maximum length)
```

**Expected Result:** All test cases should return `True`

---

### 8. test_new_username_valid_starts_with_single_underscore

**Purpose:** Validate usernames that start with a single underscore

**Requirements:**
- First character is underscore (_)
- Second character must be letter or number (prevents double underscores)
- Remaining characters can be letters, numbers, underscores

**Test Cases:**
```
✓ _ab (minimum length after underscore)
✓ _user
✓ _test123
✓ _john_doe
✓ _a_b_c_d_e_f_g (16 chars - maximum length)
```

**Expected Result:** All test cases should return `True`

---

### 9. test_new_username_valid_with_numbers_and_underscores

**Purpose:** Validate usernames with mixed numbers and underscores

**Requirements:**
- After first character, can contain any combination of letters, numbers, underscores

**Test Cases:**
```
✓ a1b
✓ user_123
✓ test_user_99
✓ a_1_2_3_test_4
```

**Expected Result:** All test cases should return `True`

---

### 10. test_new_username_invalid_too_short

**Purpose:** Reject usernames with fewer than 3 characters

**Requirements:**
- Minimum length validation: < 3 chars should fail

**Test Cases:**
```
✗ a (1 character)
✗ ab (2 characters)
✗ _a (2 characters total)
✗ _ (1 character)
✗ "" (0 characters - empty)
```

**Expected Result:** All test cases should return `False`

---

### 11. test_new_username_invalid_too_long

**Purpose:** Reject usernames with more than 16 characters

**Requirements:**
- Maximum length validation: > 16 chars should fail

**Test Cases:**
```
✗ aaaaaaaaaaaaaaaaaaa (17 characters)
✗ user_name_is_long_17 (21 characters)
✗ _this_is_over_16_chars (22 characters)
```

**Expected Result:** All test cases should return `False`

---

### 12. test_new_username_invalid_starts_with_number

**Purpose:** Reject usernames starting with numeric digits

**Requirements:**
- First character must be letter or underscore, NOT a number

**Test Cases:**
```
✗ 1user
✗ 123abc
✗ 9_test
```

**Expected Result:** All test cases should return `False`

---

### 13. test_new_username_invalid_multiple_underscores_at_start

**Purpose:** Reject usernames starting with multiple underscores

**Requirements:**
- Only single underscore allowed at start
- Double or triple underscores should fail

**Test Cases:**
```
✗ __user (double underscore)
✗ ___test (triple underscore)
✗ __a (double underscore, short)
✗ ____ (only underscores)
```

**Expected Result:** All test cases should return `False`

---

### 14. test_new_username_invalid_special_characters

**Purpose:** Reject usernames containing special characters

**Requirements:**
- Only letters (A-Z, a-z), numbers (0-9), and underscores (_) allowed
- No punctuation, spaces, or symbols

**Test Cases:**
```
✗ user@name (@ symbol)
✗ user-name (- hyphen)
✗ user.name (. dot)
✗ user name (space)
✗ user! (exclamation)
✗ test#user (# hash)
✗ user$ ($ dollar)
✗ user% (% percent)
✗ user&name (& ampersand)
✗ user(test) (parentheses)
✗ user+test (+ plus)
```

**Expected Result:** All test cases should return `False`

---

### 15. test_new_username_invalid_lowercase_special_chars

**Purpose:** Reject usernames with control characters

**Requirements:**
- No whitespace or control characters allowed

**Test Cases:**
```
✗ user\nname (newline character)
✗ user\tname (tab character)
✗ user\rname (carriage return character)
```

**Expected Result:** All test cases should return `False`

---

### 16. test_new_username_edge_cases_min_max

**Purpose:** Test boundary conditions at minimum and maximum lengths

**Requirements Tested:**
- Minimum valid length (3 chars)
- Maximum valid length (16 chars)
- Just below minimum (2 chars) - should fail
- Just above maximum (17 chars) - should fail

**Test Cases:**
```
✓ abc (minimum valid)
✓ _ab (minimum valid with underscore)
✗ ab (below minimum)
✓ aaaaaaaaaaaaaaaa (maximum valid, 16 'a's)
✓ _aaaaaaaaaaaaaaa (maximum valid starting with underscore, 16 chars total)
✗ aaaaaaaaaaaaaaaaa (above maximum, 17 'a's)
```

**Expected Result:**
- 3-char usernames return `True`
- 2-char usernames return `False`
- 16-char usernames return `True`
- 17-char usernames return `False`

---

### 17. test_new_username_case_sensitivity

**Purpose:** Validate that both uppercase and lowercase letters are accepted

**Requirements:**
- Usernames can contain mixed case letters
- Case sensitivity should not prevent validation

**Test Cases:**
```
✓ User (mixed case)
✓ USER (all uppercase)
✓ user (all lowercase)
✓ uSeR_teSt (mixed case with underscore)
✓ ABC123 (uppercase with numbers)
✓ _AaBbCc (underscore start with mixed case)
```

**Expected Result:** All test cases should return `True`

---

### 18. test_new_username_type_errors

**Purpose:** Validate proper error handling for non-string types

**Requirements:**
- `None` should raise `TypeError`
- Non-string types (int, list, dict) should raise `AttributeError`

**Test Cases:**
```
✗ None (raises TypeError)
✗ 123 (raises AttributeError - integer)
✗ [] (raises AttributeError - list)
✗ {} (raises AttributeError - dict)
```

**Expected Result:**
- `validate_username(None)` raises `TypeError`
- `validate_username(123)` raises `AttributeError`
- `validate_username([])` raises `AttributeError`
- `validate_username({})` raises `AttributeError`

---

## Test Execution Summary

**Command:** `pytest utils/test_validators.py -v`

**Expected Output:**
```
===================== 18 passed in 0.25s =====================
```

### Test Statistics
- **Total Tests:** 18
- **Email Tests:** 3
- **Legacy Username Tests:** 3
- **New Username Tests:** 12
- **Success Rate:** 100%

---

## Regex Pattern Reference

### Email Validator Pattern
```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

**Components:**
- `^` - Start of string
- `[a-zA-Z0-9._%+-]+` - Local part: letters, numbers, dot, underscore, percent, plus, hyphen
- `@` - Required separator
- `[a-zA-Z0-9.-]+` - Domain name: letters, numbers, dot, hyphen
- `\.` - Required dot in domain
- `[a-zA-Z]{2,}` - TLD: 2+ letters
- `$` - End of string

### Username Validator Pattern
```regex
^([a-zA-Z][a-zA-Z0-9_]{2,15}|_[a-zA-Z0-9][a-zA-Z0-9_]{1,14})$
```

**Components:**
- `^` - Start of string
- First alternative: `[a-zA-Z][a-zA-Z0-9_]{2,15}`
  - Starts with letter
  - Followed by 2-15 chars (letters, numbers, underscores)
  - Total: 3-16 chars
- `|` - OR
- Second alternative: `_[a-zA-Z0-9][a-zA-Z0-9_]{1,14}`
  - Starts with single underscore
  - Followed by letter or number (prevents __)
  - Followed by 1-14 chars (letters, numbers, underscores)
  - Total: 3-16 chars
- `$` - End of string

---

## Validator Requirements Matrix

| Requirement | Email | Username |
|-------------|-------|----------|
| Min Length | 2 chars (local@domain.ext) | 3 chars |
| Max Length | No limit | 16 chars |
| Start Char | Letter/number | Letter or single `_` |
| Allowed Chars | a-z, 0-9, `._%+-` | a-z, 0-9, `_` |
| Must Have | `@` and `.` | None |
| No Spaces | ✓ | ✓ |
| No Special Chars | Limited | ✓ Underscores only |
| Case Sensitive | No (based on RFC) | No (accepted both) |

---

## Notes

- All tests use pytest framework with verbose output (`-v` flag)
- Tests use `assert` statements for comparisons
- Type error tests use `pytest.raises()` context manager
- Each test is independent and can be run individually
- Tests are organized logically: legacy first, then new comprehensive tests

---

## Running Tests

**Run all tests:**
```bash
pytest utils/test_validators.py -v
```

**Run specific test:**
```bash
pytest utils/test_validators.py::test_new_username_valid_starts_with_letter -v
```

**Run tests matching pattern:**
```bash
pytest utils/test_validators.py -k "new_username" -v
```

**Run with coverage:**
```bash
pytest utils/test_validators.py --cov=utils.validators --cov-report=html
```

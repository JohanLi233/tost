import pytest

# Skip all tests here if the native extension is not present
pytest.importorskip("tost._tost")

from tost import encode, decode


def test_encode_empty_array():
    obj = {"empty": []}
    result = encode(obj)
    assert result == "empty[0]:"


def test_encode_array_of_arrays():
    obj = {"matrix": [[1, 2], [3, 4]]}
    result = encode(obj)
    assert "matrix[2]:" in result
    assert "- [2]:" in result
    assert "1,2" in result and "3,4" in result


def test_encode_list_array_non_tabular():
    obj = {"items": [{"a": 1}, {"a": 1, "b": 2}]}
    result = encode(obj)
    assert "items[2]:" in result
    assert "- a: 1" in result
    assert "b: 2" in result


@pytest.mark.parametrize(
    "value, expected_sub",
    [
        ("", 's: ""'),
        ("  leading", 's: "  leading"'),
        ("1.0", 's: "1.0"'),
        ("true", 's: "true"'),
        ("A:B", 's: "A:B"'),
    ],
)
def test_string_quoting(value, expected_sub):
    obj = {"s": value}
    result = encode(obj)
    assert expected_sub in result


def test_decode_invalid_tabular_row_len():
    s = "items[2]{a,b}:\n  1,2\n  3"
    with pytest.raises(ValueError):
        decode(s)


def test_decode_array_of_arrays():
    s = "matrix[2]:\n  - [2]: 1,2\n  - [2]: 3,4"
    out = decode(s)
    assert isinstance(out, dict)
    assert out["matrix"] == [[1, 2], [3, 4]]


def test_decode_empty_array():
    s = "items[0]:"
    out = decode(s)
    assert out == {"items": []}


def test_decode_root_inline_array():
    s = "[#3|]: a|b|c"
    out = decode(s)
    assert out == ["a", "b", "c"]


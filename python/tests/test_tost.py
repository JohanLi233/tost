"""
Tests for TOON Python API
"""

import pytest

# Skip all tests in this module if the Rust extension isn't available
pytest.importorskip("tost._tost")

from tost import encode, decode


def test_encode_simple_object():
    """Test encoding a simple object"""
    obj = {"id": 123, "name": "Ada", "active": True}
    result = encode(obj)
    assert "id: 123" in result
    assert "name: Ada" in result
    assert "active: true" in result


def test_encode_tabular_array():
    """Test encoding a tabular array"""
    obj = {
        "items": [
            {"sku": "A1", "qty": 2, "price": 9.99},
            {"sku": "B2", "qty": 1, "price": 14.5}
        ]
    }
    result = encode(obj)
    assert "items[2]{sku,qty,price}:" in result
    assert "A1,2,9.99" in result or "A1,2,9.99" in result


def test_encode_inline_array():
    """Test encoding an inline array"""
    obj = {"tags": ["javascript", "typescript", "nodejs"]}
    result = encode(obj)
    assert "tags[3]:" in result
    assert "javascript" in result


def test_encode_nested_object():
    """Test encoding nested objects"""
    obj = {
        "user": {
            "id": 123,
            "name": "Ada"
        }
    }
    result = encode(obj)
    assert "user:" in result
    assert "id: 123" in result
    assert "name: Ada" in result


def test_decode_simple_object():
    """Test decoding a simple object"""
    toon_str = "id: 123\nname: Ada\nactive: true"
    result = decode(toon_str)
    assert result["id"] == 123
    assert result["name"] == "Ada"
    assert result["active"] is True


def test_decode_tabular_array():
    """Test decoding a tabular array"""
    toon_str = "items[2]{sku,qty,price}:\n  A1,2,9.99\n  B2,1,14.5"
    result = decode(toon_str)
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["sku"] == "A1"
    assert result["items"][0]["qty"] == 2


def test_roundtrip():
    """Test encoding and decoding back"""
    original = {
        "id": 123,
        "name": "Ada",
        "tags": ["python", "rust"],
        "items": [
            {"sku": "A1", "qty": 2},
            {"sku": "B2", "qty": 1}
        ]
    }
    encoded = encode(original)
    decoded = decode(encoded)
    
    assert decoded["id"] == original["id"]
    assert decoded["name"] == original["name"]
    assert decoded["tags"] == original["tags"]
    assert len(decoded["items"]) == len(original["items"])
    assert decoded["items"][0]["sku"] == original["items"][0]["sku"]


def test_encode_with_options():
    """Test encoding with custom options"""
    obj = {"items": [{"sku": "A1", "qty": 2}]}
    result = encode(obj, indent=4, delimiter="|", length_marker="#")
    assert "items[#1|]{sku|qty}:" in result
    assert "A1|2" in result


def test_quote_hyphen_behavior():
    """Strings with internal hyphen are not quoted; leading hyphen are quoted"""
    obj = {"a": "MOUSE-BT", "b": "-item"}
    result = encode(obj)
    assert "a: MOUSE-BT" in result
    assert 'b: "-item"' in result


if __name__ == "__main__":
    pytest.main([__file__])

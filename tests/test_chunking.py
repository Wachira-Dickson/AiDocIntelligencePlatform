from app.services.chunking_service import chunk_text

def test_empty_text():
    assert chunk_text("") == []
    assert chunk_text(" ") == []
    print("Empty text: PASSED")

def test_short_text():
    text = "This is a short document."
    chunks = chunk_text(text)

    assert chunks == [text]
    print("Short text: PASSED")

def test_long_text():
    text = "word " * 600

    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=50,
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 500 for chunk in chunks)
    print("Long text splitting: PASSED")

def test_overlap():
    text = "abcdefghij klmnopqrst uvwxyz"

    chunks = chunk_text(
        text,
        chunk_size=15,
        overlap=5,
    )

    assert len(chunks) > 1
    assert chunks[0][-5:] in chunks[1]
    print("Chunk overlap: PASSED")

def test_invalid_parameters():
    try:
        chunk_text("Some text", chunk_size=0)
        raise AssertionError("Expected ValueError for chunk_size=0")
    except ValueError:
        pass


    try:
        chunk_text("Some text", chunk_size=10, overlap=10)
        raise AssertionError("Expected ValueError for overlap >= chunk_size")
    except ValueError:
        pass

    print("Invalid parameters: PASSED")

if __name__ == "__main__":
    test_empty_text()
    test_short_text()
    test_long_text()
    test_overlap()
    test_invalid_parameters()

    print("\nAll chunking test passed!")
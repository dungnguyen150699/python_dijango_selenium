import pytest
from spacy.tokens import Doc
from spacy.symbols import SPACE
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,accuracy_threshold", [("es_ancora-ud-dev001_10.json", 0.97)],
)
def test_es_morphologizer_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(
        NLP, data_path, {"pos_acc": accuracy_threshold, "morph_acc": accuracy_threshold}
    )


def test_es_morphologizer_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("Some\nspaces are\tnecessary.")
    assert doc[0].pos != SPACE
    assert doc[0].pos_ != "SPACE"
    assert doc[1].pos == SPACE
    assert doc[1].pos_ == "SPACE"
    assert doc[1].tag_ == "SPACE"
    assert doc[2].pos != SPACE
    assert doc[3].pos != SPACE
    assert doc[4].pos == SPACE


def test_es_morphologizer_return_char(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    text = (
        "hi Aaron,\r\n\r\nHow is your schedule today, I was wondering if "
        "you had time for a phone\r\ncall this afternoon?\r\n\r\n\r\n"
    )
    doc = NLP(text)
    for token in doc:
        if token.is_space:
            assert token.pos == SPACE
    assert doc[3].text == "\r\n\r\n"
    assert doc[3].is_space
    assert doc[3].pos == SPACE

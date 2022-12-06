from datetime import datetime
from unittest import mock

import pytest

from src.model.annotation import Annotation, AnnotationType


@mock.patch('src.model.actor.Actor', autospec=True)
def test_correct_initialization(actor):
    annotation = Annotation("id", AnnotationType.OTHER, actor, datetime(2022, 1, 1), "comment")
    assert annotation.spdx_id == "id"
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.annotator == actor
    assert annotation.annotation_date == datetime(2022, 1, 1)
    assert annotation.annotation_comment == "comment"


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_spdx_id(actor):
    with pytest.raises(TypeError):
        Annotation(42, AnnotationType.OTHER, actor, datetime(2022, 1, 1), "comment")


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_annotation_type(actor):
    with pytest.raises(TypeError):
        Annotation("id", 42, actor, datetime(2022, 1, 1), "comment")


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_annotator(actor):
    with pytest.raises(TypeError):
        Annotation("id", AnnotationType.OTHER, 42, datetime(2022, 1, 1), "comment")


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_annotation_date(actor):
    with pytest.raises(TypeError):
        Annotation("id", AnnotationType.OTHER, actor, 42, "comment")


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_annotation_comment(actor):
    with pytest.raises(TypeError):
        Annotation("id", AnnotationType.OTHER, actor, datetime(2022, 1, 1), 42)

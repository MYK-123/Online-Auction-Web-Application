
import pytest

from src.app import return_app
from src.constants import UPLOAD_FOLDER


def test_conf():
	assert return_app().config['UPLOAD_FOLDER'] == UPLOAD_FOLDER


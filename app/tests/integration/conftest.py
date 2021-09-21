import pytest
from typing import Generator
from learning_loop_node.tests import test_helper
import shutil
from learning_loop_node import conftest


@pytest.fixture()
def web() -> Generator:
    with test_helper.LiveServerSession() as c:
        yield c


@pytest.fixture(autouse=True, scope='function')
def cleanup():
    shutil.rmtree(conftest.data_folder_for_tests, ignore_errors=True)


@pytest.fixture(autouse=True, scope='module')
def create_project():
    test_helper.LiveServerSession().delete(f"/api/zauberzeug/projects/pytest?keep_images=true")
    project_configuration = {'project_name': 'pytest', 'inbox': 0, 'annotate': 0, 'review': 0, 'complete': 3, 'image_style': 'beautiful',
                             'categories': 2, 'thumbs': False, 'tags': 0, 'trainings': 1, 'detections': 3, 'annotations': 0, 'skeleton': False}
    assert test_helper.LiveServerSession().post(f"/api/zauberzeug/projects/generator",
                                                json=project_configuration).status_code == 200
    yield
    test_helper.LiveServerSession().delete(f"/api/zauberzeug/projects/pytest?keep_images=true")

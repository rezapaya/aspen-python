import sys

import pytest
from aspen.testing.filesystem_fixture import FilesystemFixture
from aspen.testing.harness import Harness
from aspen.website import Website


@pytest.yield_fixture
def fs():
    fs = FilesystemFixture()
    yield fs
    fs.remove()


@pytest.yield_fixture
def module_scrubber():
    before = set(sys.modules.keys())
    yield
    after = set(sys.modules.keys())
    for name in after - before:
        del sys.modules[name]


@pytest.yield_fixture
def sys_path(fs, module_scrubber):
    sys.path.insert(0, fs.root)
    yield fs
    sys.path.remove(fs.root)


@pytest.yield_fixture
def harness():
    www = FilesystemFixture()
    project = FilesystemFixture()
    yield Harness(www, project)
    www.remove()
    project.remove()


@pytest.yield_fixture
def handle(harness):
    def handle(url_path):
        return harness.get(url_path)
    yield handle
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function

from astropy.tests.helper import pytest

from .. import main


def test_help():
    # Just a smoke test, really
    main.main_from_args(['help'])


def test_invalid_command():
    with pytest.raises(SystemExit) as e:
        main.main_from_args([])
    assert e.value.code == 2

    with pytest.raises(SystemExit) as e:
        main.main_from_args(['foo'])
    assert e.value.code == 2

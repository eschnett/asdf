import pytest

import asdf
from asdf.exceptions import AsdfConversionWarning

from . import _helpers as helpers


def test_undefined_tag():
    # This tests makes sure that ASDF still returns meaningful structured data
    # even when it encounters a schema tag that it does not specifically
    # implement as an extension
    from numpy import array

    yaml = """
undefined_data:
  !<tag:nowhere.org:custom/undefined_tag-1.0.0>
    - 5
    - {'message': 'there is no tag'}
    - !core/ndarray-1.0.0
      [[1, 2, 3], [4, 5, 6]]
    - !<tag:nowhere.org:custom/also_undefined-1.3.0>
        - !core/ndarray-1.0.0 [[7],[8],[9],[10]]
        - !core/complex-1.0.0 3.14j
"""
    buff = helpers.yaml_to_asdf(yaml)
    with pytest.warns(Warning) as warning:
        afile = asdf.open(buff)
        missing = afile.tree["undefined_data"]

    assert missing[0] == 5
    assert missing[1] == {"message": "there is no tag"}
    assert (missing[2] == array([[1, 2, 3], [4, 5, 6]])).all()
    assert (missing[3][0] == array([[7], [8], [9], [10]])).all()
    assert missing[3][1] == 3.14j

    # There are two undefined tags, so we expect two warnings
    # filter out only AsdfConversionWarning
    warning = [w for w in warning if w.category == AsdfConversionWarning]
    assert len(warning) == 2
    for i, tag in enumerate(["also_undefined-1.3.0", "undefined_tag-1.0.0"]):
        assert (
            str(warning[i].message)
            == f"tag:nowhere.org:custom/{tag} is not recognized, converting to raw Python data structure"
        )

    # Make sure no warning occurs if explicitly ignored
    buff.seek(0)
    with helpers.assert_no_warnings():
        afile = asdf.open(buff, ignore_unrecognized_tag=True)

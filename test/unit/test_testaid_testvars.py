import pytest
from testaid.exceptions import TemplatesResolveFailed


def test_testaid_testvars_is_not_none(testvars):
    assert testvars is not None


def test_testaid_testvars_exception_testvarsresolvefailed():
    msg = 'my_msg'
    with pytest.raises(
            TemplatesResolveFailed,
            match=r'^my_msg$'):
        raise TemplatesResolveFailed(msg)

# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.


import pytest

from helpers import utils  # pylint: disable=import-error


@pytest.mark.parametrize('val1, val2', [
    ({'a': 1}, {'a': 1}),
    ({'a': 1, 'b': 2}, {'a': 1}),
    ({'a': [1, 2, 3]}, {'a': [1]}),
    ({'a': [1, 2, 3]}, {'a': [..., 2]}),
    (1.0, 1.00000001),
    ("foobarbaz", "foo*baz"),
])
def test_partial_compare_equal(val1, val2):
    assert utils.partial_compare(val1, val2)


@pytest.mark.parametrize('val1, val2', [
    ({'a': 1}, {'a': 2}),
    ({'a': 1}, {'b': 1}),
    ({'a': 1, 'b': 2}, {'a': 2}),
    ({'a': [1]}, {'a': [1, 2, 3]}),
    ({'a': [1]}, {'a': [2, 3, 4]}),
    ([1], {1: 2}),
    ({1: 1}, {1: [1]}),
    ({'a': [1, 2, 3]}, {'a': [..., 3]}),
    ("foo*baz", "foobarbaz"),
])
def test_partial_compare_not_equal(val1, val2):
    assert not utils.partial_compare(val1, val2)


@pytest.mark.parametrize('pattern, value, expected', [
    ('foo', 'foo', True),
    ('foo', 'bar', False),
    ('foo', 'Foo', False),
    ('foo', 'foobar', False),
    ('foo', 'barfoo', False),

    ('foo*', 'foobarbaz', True),
    ('*bar', 'foobar', True),
    ('foo*baz', 'foobarbaz', True),

    ('foo[b]ar', 'foobar', False),
    ('foo[b]ar', 'foo[b]ar', True),

    ('foo?ar', 'foobar', False),
    ('foo?ar', 'foo?ar', True),
])
def test_pattern_match(pattern, value, expected):
    assert utils.pattern_match(pattern=pattern, value=value) == expected

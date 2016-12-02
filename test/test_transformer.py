#!/usr/bin/env python3
#
# Copyright (C) 2016 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from repology.transformer import PackageTransformer
from repology.package import Package

class TestPackageTransformer(unittest.TestCase):
    def test_ignore(self):
        p = Package(name="foo", version="1.0")
        self.assertEqual(p.ignore, False)
        PackageTransformer(rulestext='[ { ignore: true } ]').Process(p)
        self.assertEqual(p.ignore, True)

    def test_unignore(self):
        p = Package(name="foo", version="1.0")
        self.assertEqual(p.ignore, False)
        PackageTransformer(rulestext='[ { ignore: true }, { unignore: true } ]').Process(p)
        self.assertEqual(p.ignore, False)

    def test_ignorever(self):
        p = Package(name="foo", version="1.0")
        self.assertEqual(p.ignoreversion, False)
        PackageTransformer(rulestext='[ { ignorever: true } ]').Process(p)
        self.assertEqual(p.ignoreversion, True)

    def test_unignorever(self):
        p = Package(name="foo", version="1.0")
        self.assertEqual(p.ignoreversion, False)
        PackageTransformer(rulestext='[ { ignorever: true }, { unignorever: true } ]').Process(p)
        self.assertEqual(p.ignoreversion, False)

    def test_setname(self):
        p = Package(name="foo", version="1.0")
        PackageTransformer(rulestext='[ { setname: "bar" } ]').Process(p)
        self.assertEqual(p.name, "foo")
        self.assertEqual(p.effname, "bar")

    def test_setname_subst(self):
        p = Package(name="foo", version="1.0")
        PackageTransformer(rulestext='[ { setname: "bar_$0" } ]').Process(p)
        self.assertEqual(p.name, "foo")
        self.assertEqual(p.effname, "bar_foo")

    def test_match_name(self):
        p1 = Package(name="p1", version="1.0", family="foo")
        p2 = Package(name="p2", version="2.0", family="bar")
        t = PackageTransformer(rulestext='[ { name: p1, setname: bar } ]')
        t.Process(p1)
        t.Process(p2)
        self.assertEqual(p1.effname, "bar")
        self.assertEqual(p2.effname, "p2")

    def test_match_namepat(self):
        p1 = Package(name="p1", version="1.0", family="foo")
        p2 = Package(name="p2", version="2.0", family="bar")
        t = PackageTransformer(rulestext='[ { namepat: ".*1", setname: bar } ]')
        t.Process(p1)
        t.Process(p2)
        self.assertEqual(p1.effname, "bar")
        self.assertEqual(p2.effname, "p2")

    def test_match_ver(self):
        p1 = Package(name="p1", version="1.0", family="foo")
        p2 = Package(name="p2", version="2.0", family="bar")
        t = PackageTransformer(rulestext='[ { ver: "1.0", setname: bar } ]')
        t.Process(p1)
        t.Process(p2)
        self.assertEqual(p1.effname, "bar")
        self.assertEqual(p2.effname, "p2")

    def test_match_verpat(self):
        p1 = Package(name="p1", version="1.0", family="foo")
        p2 = Package(name="p2", version="2.0", family="bar")
        t = PackageTransformer(rulestext='[ { verpat: "1.*", setname: bar } ]')
        t.Process(p1)
        t.Process(p2)
        self.assertEqual(p1.effname, "bar")
        self.assertEqual(p2.effname, "p2")

    def test_match_verlonger(self):
        p1 = Package(name="p1", version="1.0.0", family="foo")
        p2 = Package(name="p2", version="1.0", family="bar")
        t = PackageTransformer(rulestext='[ { verlonger: 2, setname: bar } ]')
        t.Process(p1)
        t.Process(p2)
        self.assertEqual(p1.effname, "bar")
        self.assertEqual(p2.effname, "p2")

    def test_match_family(self):
        p1 = Package(name="p1", version="1.0", family="foo")
        p2 = Package(name="p2", version="2.0", family="bar")
        t = PackageTransformer(rulestext='[ { families: [ foo ], setname: bar } ]')
        t.Process(p1)
        t.Process(p2)
        self.assertEqual(p1.effname, "bar")
        self.assertEqual(p2.effname, "p2")

if __name__ == '__main__':
    unittest.main()

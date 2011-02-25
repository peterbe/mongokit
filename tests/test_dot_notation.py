#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010, Nicolas Clairon
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest

from mongokit import *

class AlwaysDotNotationTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = Connection()
        self.db = self.connection['test']
        self.col = self.db['mongokit']

    def tearDown(self):
        self.connection['test'].drop_collection('mongokit')

    def test_simple_structure(self):
        class MyDoc(Document):
            __collection__ = 'mongokit'
            structure = {
                "foo":unicode,
                "bar":{"name":unicode,
                       "age":int},
            }
        self.connection.register([MyDoc])
        mydoc = self.col.MyDoc()
        mydoc["foo"] = u"bar"
        mydoc["bar"]["name"] = u"Bill"
        mydoc["bar"]["age"] = 42
        mydoc.save()
        assert isinstance(mydoc['_id'], ObjectId)
        mydoc, = self.db.MyDoc.collection.find()
        assert isinstance(mydoc, dict)
        assert mydoc['foo'] == u"bar"
        assert mydoc['bar']['name'] == u"Bill"
        try:
            mydoc['not']
            raise AssertionError
        except KeyError:
            pass
        self.col.always_dot_notation = True
        mydoc, = self.db.MyDoc.collection.find()
        assert mydoc.foo == u"bar"
        assert mydoc.bar.name == u"Bill"
        assert mydoc.bar.age == 42
        try:
            mydoc['not']
            raise AssertionError
        except KeyError:
            pass

    def xtest_collection_directly_no_wrap(self):
        class MyDoc(Document):
            __collection__ = 'mongokit'
            use_dot_notation = False
            structure = {
                "foo":unicode,
                "bar":{"name":unicode,
                       "age":int},
            }
        self.connection.register([MyDoc])
        mydoc = self.col.MyDoc()
        mydoc["foo"] = u"bar"
        mydoc["bar"]["name"] = u"Bill"
        mydoc["bar"]["age"] = 42
        mydoc.save()
        assert isinstance(mydoc['_id'], ObjectId)
        assert self.db.MyDoc.find().count() == 1
        mydoc, = self.db.MyDoc.collection.find()
        assert isinstance(mydoc, dict)
        try:
            mydoc.foo
        except AttributeError:
            pass
        assert mydoc['foo'] == u"bar"
        assert mydoc['bar']['name'] == u"Bill"
        assert mydoc['bar']['age'] == 42

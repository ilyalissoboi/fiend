# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import factories


# Create your tests here.
class OpeningTestCase(TestCase):
    def setUp(self):
        pass

    def test_basic_fit(self):
        opening = factories.OpeningFactory()
        seeker = factories.SeekerFactory()
        fit_result = opening.calculate_fit(seeker)

        self.assertEqual(fit_result > 0, True)

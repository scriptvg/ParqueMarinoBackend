#!/usr/bin/env python
"""
Test runner for messaging app tests
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'
    django.setup()
    
    # Import and run tests
    from django.test.runner import DiscoverRunner
    
    # Run tests for messaging app
    test_runner = DiscoverRunner(verbosity=2, interactive=False)
    failures = test_runner.run_tests(['apps.support.messaging'])
    
    sys.exit(bool(failures))
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    logger.info("Starting Django management utility...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LandParcel.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Ensure Django is installed, "
            "the virtual environment is activated, and the PYTHONPATH is set correctly."
        ) from exc
        
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
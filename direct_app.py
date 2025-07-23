#!/usr/bin/env python
"""
Direct Flask application for deployment on Render with Python 3.13
This file contains all necessary patches and workarounds for Python 3.13 compatibility
"""
import sys
import os
import warnings

# Apply patches for Python 3.13 compatibility
if sys.version_info >= (3, 13):
    print(f"Running on Python {sys.version}")
    
    # Suppress warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=UserWarning)
    os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'
    
    # Patch typing.Generic to handle TypingOnly issues
    import typing
    
    # Store original method
    original_init_subclass = typing.Generic.__init_subclass__
    
    @classmethod
    def patched_init_subclass(cls, *args, **kwargs):
        try:
            return original_init_subclass(*args, **kwargs)
        except AssertionError as e:
            error_msg = str(e)
            if ("directly inherits from TypingOnly" in error_msg or 
                "напрямую наследует TypingOnly" in error_msg):
                print(f"Warning: Ignoring TypingOnly assertion for {cls.__name__}")
                return None
            raise
    
    # Apply the patch
    typing.Generic.__init_subclass__ = patched_init_subclass
    print("Python 3.13 compatibility patches applied successfully")

# Now import Flask and create the application
from app import create_app

# Create the Flask application
app = create_app()

# This allows the app to be imported by gunicorn
if __name__ == '__main__':
    app.run(debug=True)
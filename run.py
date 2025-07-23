#!/usr/bin/env python
"""
Flask Shop Application
"""
import sys

# Apply compatibility patches for Python 3.13 if needed
if sys.version_info >= (3, 13):
    try:
        from compat_py313 import apply_patches
        apply_patches()
        print("Applied compatibility patches for Python 3.13")
    except ImportError:
        print("Warning: compat_py313 module not found, compatibility issues may occur with Python 3.13")

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
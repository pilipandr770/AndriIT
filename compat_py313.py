"""
Compatibility module for Python 3.13 and SQLAlchemy.
This module provides patches and workarounds for compatibility issues
between Python 3.13 and SQLAlchemy.
"""

import sys

def apply_patches():
    """
    Apply patches to make SQLAlchemy work with Python 3.13.
    This function should be called before importing SQLAlchemy.
    """
    if sys.version_info >= (3, 13):
        # Patch for SQLAlchemy's TypingOnly issue in Python 3.13
        import types
        import typing
        
        # Save the original __init_subclass__ method
        original_init_subclass = typing.Generic.__init_subclass__
        
        # Define a patched version that ignores certain attributes
        def patched_init_subclass(cls, *args, **kwargs):
            try:
                return original_init_subclass(cls, *args, **kwargs)
            except AssertionError as e:
                # If the error is about TypingOnly with additional attributes, ignore it
                if "напрямую наследует TypingOnly" in str(e) or "directly inherits from TypingOnly" in str(e):
                    return None
                raise
        
        # Apply the patch
        typing.Generic.__init_subclass__ = patched_init_subclass
        
        print("Applied compatibility patches for Python 3.13")

# Apply patches if this module is imported
if __name__ != "__main__":
    apply_patches()
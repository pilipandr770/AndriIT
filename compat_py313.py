"""
Compatibility module for Python 3.13 and SQLAlchemy.
This module provides patches and workarounds for compatibility issues
between Python 3.13 and SQLAlchemy.
"""

import sys
import os

def apply_patches():
    """
    Apply patches to make SQLAlchemy work with Python 3.13.
    This function should be called before importing SQLAlchemy.
    """
    if sys.version_info >= (3, 13):
        try:
            # Patch for SQLAlchemy's TypingOnly issue in Python 3.13
            import typing
            from sqlalchemy.util import langhelpers
            
            # Save the original __init_subclass__ method
            original_init_subclass = langhelpers.TypingOnly.__init_subclass__
            
            # Define a patched version that ignores certain attributes
            @classmethod
            def patched_init_subclass(cls, **kwargs):
                # Remove problematic attributes that cause issues in Python 3.13
                for attr in ['__firstlineno__', '__static_attributes__']:
                    if hasattr(cls, attr):
                        delattr(cls, attr)
                
                try:
                    return original_init_subclass(**kwargs)
                except AssertionError as e:
                    # If the error is about TypingOnly with additional attributes, ignore it
                    if "directly inherits from TypingOnly" in str(e) or "напрямую наследует TypingOnly" in str(e):
                        print(f"Warning: Ignoring TypingOnly assertion error for {cls}: {e}")
                        return None
                    raise
            
            # Apply the patch
            langhelpers.TypingOnly.__init_subclass__ = patched_init_subclass
            
            print("Applied compatibility patches for Python 3.13")
            
        except ImportError as e:
            print(f"Warning: Could not apply Python 3.13 compatibility patches: {e}")
        except Exception as e:
            print(f"Warning: Error applying Python 3.13 compatibility patches: {e}")

# Set environment variable to force Python 3.11 if possible
if 'PYTHON_VERSION' not in os.environ:
    os.environ['PYTHON_VERSION'] = '3.11.0'

# Apply patches if this module is imported
if __name__ != "__main__":
    apply_patches()
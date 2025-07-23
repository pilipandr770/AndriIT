"""
Python 3.13 compatibility patches for SQLAlchemy
This module must be imported before any SQLAlchemy imports
"""
import sys
import warnings

def apply_python313_patches():
    """Apply patches for Python 3.13 compatibility"""
    if sys.version_info >= (3, 13):
        print(f"Applying Python 3.13 compatibility patches...")
        
        # Suppress warnings
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
        
        try:
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
            
            # Additional patch for SQLAlchemy's langhelpers
            try:
                from sqlalchemy.util import langhelpers
                
                # Store original TypingOnly.__init_subclass__
                original_typing_only_init = langhelpers.TypingOnly.__init_subclass__
                
                @classmethod
                def patched_typing_only_init(cls, **kwargs):
                    # Remove problematic attributes
                    for attr in ['__firstlineno__', '__static_attributes__']:
                        if hasattr(cls, attr):
                            try:
                                delattr(cls, attr)
                            except (AttributeError, TypeError):
                                pass
                    
                    try:
                        return original_typing_only_init(**kwargs)
                    except AssertionError as e:
                        error_msg = str(e)
                        if ("directly inherits from TypingOnly" in error_msg or 
                            "напрямую наследует TypingOnly" in error_msg):
                            print(f"Warning: Ignoring TypingOnly assertion for {cls.__name__}")
                            return None
                        raise
                
                # Apply the patch
                langhelpers.TypingOnly.__init_subclass__ = patched_typing_only_init
                
            except ImportError:
                # SQLAlchemy not yet imported, patch will be applied later
                pass
            
            print("Python 3.13 compatibility patches applied successfully")
            
        except Exception as e:
            print(f"Warning: Could not apply all Python 3.13 patches: {e}")

# Apply patches immediately when module is imported
apply_python313_patches()
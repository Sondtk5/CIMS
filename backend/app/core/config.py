# Global config for app mode (DEMO or PRODUCTION)
_current_mode = "PRODUCTION"  # Default to production

def set_mode(mode: str):
    """Set application mode: DEMO or PRODUCTION"""
    global _current_mode
    if mode not in ["DEMO", "PRODUCTION"]:
        raise ValueError("Mode must be DEMO or PRODUCTION")
    _current_mode = mode

def get_mode() -> str:
    """Get current application mode"""
    return _current_mode

def is_demo_mode() -> bool:
    """Check if currently in demo mode"""
    return _current_mode == "DEMO"

def is_production_mode() -> bool:
    """Check if currently in production mode"""
    return _current_mode == "PRODUCTION"

# Global config for app mode (DEMO or PRODUCTION)
# Use dict to ensure state persists across imports
_config = {
    "mode": "PRODUCTION"  # Default to production
}

def set_mode(mode: str):
    """Set application mode: DEMO or PRODUCTION - Updates runtime config"""
    if mode not in ["DEMO", "PRODUCTION"]:
        raise ValueError("Mode must be DEMO or PRODUCTION")
    _config["mode"] = mode
    print(f"✅ Mode switched to: {mode}")

def get_mode() -> str:
    """Get current application mode"""
    return _config.get("mode", "PRODUCTION")

def is_demo_mode() -> bool:
    """Check if currently in demo mode"""
    return get_mode() == "DEMO"

def is_production_mode() -> bool:
    """Check if currently in production mode"""
    return get_mode() == "PRODUCTION"

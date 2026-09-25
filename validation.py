""" Input error checking & search filter logic """

def validate_app_input(app_name, category, owner, url):
    """Validates that all form fields are filled and not showing placeholder text."""
    if (not app_name or app_name.startswith("Enter") or 
        not category or category.startswith("Select") or 
        not owner or owner.startswith("Enter") or 
        not url or url == "https://"):
        return False, "All fields are required!"
    
    return True, ""

def format_url(url):
    """Ensures the URL string includes a proper web protocol prefix."""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url

""" Input error checking & search filter logic """

def validate_app_input(app_name, category, owner, url):
    """Validates that all form fields are filled, not placeholders, and contain valid text."""
    if (not app_name or app_name.startswith("Enter") or 
        not category or category.startswith("Select") or 
        not owner or owner.startswith("Enter") or 
        not url or url == "https://" or url.startswith("https://...") or url == "https://..."):
        return False, "All fields are required!"
    
    #--------- Check for letters in the form field -----------------
    fields_to_check = [
        (app_name, "App Name must contain at least one letter."),
        (category, "Category must contain at least one letter."),
        (owner, "Business Owner name must contain at least one letter.")
    ]
    
    # Loop through each field to ensure it has at least one alphabetical letter
    for text_value, error_message in fields_to_check:
        has_letter = False
        for char in text_value:
            if char.isalpha():
                has_letter = True
                break
                
        if not has_letter:
            return False, error_message

    return True, ""

def format_url(url):
    """Ensures the URL string includes a proper web protocol prefix."""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url

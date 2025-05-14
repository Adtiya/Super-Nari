
def get_focus_from_feature(feature_desc):
    keywords = ["login", "dashboard", "profile", "chat", "persona"]
    for word in keywords:
        if word in feature_desc.lower():
            return f"Focus: {word} module"
    return "Focus: general UI"

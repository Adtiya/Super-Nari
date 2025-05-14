
def log_pattern(project, feature):
    with open("pattern_log.txt", "a") as f:
        f.write(f"User built feature: {feature} in project: {project}\n")

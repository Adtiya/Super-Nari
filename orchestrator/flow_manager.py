
def sequence_agents(methodology):
    if methodology == "agile":
        return ["planner", "dev", "test"]
    elif methodology == "waterfall":
        return ["planner", "dev", "test", "review"]
    else:
        return ["planner", "dev"]

def min_path_length(model):
    return min([min(ant.path_lengths) for ant in model.schedule.agents])

def colorize(value, good_threshold, bad_threshold):
    if value >= good_threshold:
        return "🟢 " + str(round(value, 3))
    elif value <= bad_threshold:
        return "🔴 " + str(round(value, 3))
    else:
        return "🟡 " + str(round(value, 3))


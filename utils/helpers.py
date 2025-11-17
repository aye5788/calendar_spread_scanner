def fmt(x, digits=4):
    try:
        return round(x, digits)
    except:
        return x

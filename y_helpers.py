def find_by_id(givenId, idList):
    return next((item for item in idList if item['id'] == givenId), None)


def find_index_by_id(givenId, idList):
    return next((idList.index(item) for item in idList if item['id'] == givenId), -1)


def find_by_name(array, name):
    try:
        return next((item for item in array if item.name == name), None)
    except:
        return next((item for item in array if item['name'] == name), None)


def stringify_time_units(value):
    return str(value).zfill(2)


def pretty_print_time(seconds):
    secondsBase = int(seconds)
    hourFromSeconds = 60 * 60
    minuteFromSeconds = 60
    hours = secondsBase // hourFromSeconds
    minutes = (secondsBase % hourFromSeconds) // minuteFromSeconds
    seconds = secondsBase % minuteFromSeconds

    return "{} h {} m {}s".format(stringify_time_units(hours),
                                  stringify_time_units(minutes),
                                  stringify_time_units(seconds))


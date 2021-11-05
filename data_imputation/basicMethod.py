def simpleMethod(data, method, max):
    """
    data = data.fillna(data.mean(), limit = max)
    data = data.fillna(data.median(), limit = max

    """
    return data
    
def fillNAMethod(data, method, max):
    result = data.fillna(method=method, limit=max, limit_direction='both')
    return result

def simpleIntMethod(data, method, max):
    result = data.interpolate(method=method, limit = max, limit_direction='both')
    return result

def orderIntMethod(data, method, max):
    result = data.fillna(method=method, limit=max, limit_direction='both')
    return result
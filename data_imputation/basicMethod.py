def simpleMethod(data, method, max):
    """
    data = data.fillna(data.mean(), limit = max)
    data = data.fillna(data.median(), limit = max

    """
    return data
# fillNAMethods = ['bfill','ffill']
# simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
# orderIntMethods = [  'polynomial', 'spline']

def fillNAMethod(data, method, max):
    result = data.fillna(method=method, limit=max)
    return result

def simpleIntMethod(data, method, max):
    result = data.interpolate(method=method, limit = max, limit_direction='both')
    return result

def orderIntMethod(data, method, max):
    result = data.interpolate(method=method, limit = max, order = 2, limit_direction='both')
    return result
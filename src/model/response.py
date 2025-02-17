def result(code: int, message: str, data: any = None):
    return {
        "code": code,
        "message": message,
        "data": data
    }
    
    
def success_result(message: str = "success", data: any = None):
    return result(0, message, data)
    
    
def failed_result(message: str = "failed", data: any = None):
    return result(1, message, data)

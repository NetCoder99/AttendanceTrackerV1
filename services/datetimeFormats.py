from models.data_models import Classes


def GetDayName(day_of_week: int) -> str:
    match day_of_week:
        case 1: return 'Monday'
        case 2: return 'Tuesday'
        case 3: return 'Wednesday'
        case 4: return 'Thursday'
        case 5: return 'Friday'
        case 6: return 'Saturday'
        case 7: return 'Sunday'
        case _: return 'Unknown'

def GetPrintStartAndStop(class_record: Classes) -> str:
    return f'{class_record.classStartTime:>8} TO {class_record.classFinisTime:>8}'
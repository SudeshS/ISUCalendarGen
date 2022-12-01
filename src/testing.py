from CalendarModel import parse_cal, generateICSFile, checkCalendarFormat


def test_no_events():   # test with no events
    f_path = 'data/input_isu_cal_i.ics'
    test_cal = parse_cal(f_path)
    if checkCalendarFormat(test_cal):
        generateICSFile(test_cal)
    else:
        print("Format Error")


def test_with_events():  # test with four events
    f_path = 'data/input_isu_cal_i.ics'
    test_cal = parse_cal(f_path)
    if checkCalendarFormat(test_cal):
        generateICSFile(test_cal)
    else:
        print("Format Error")


if __name__ == "__main__":
    test_no_events()
    test_with_events()

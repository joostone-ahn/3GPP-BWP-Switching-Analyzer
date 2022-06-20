def time_abs(n):
    hour = int(n.split(':')[0])
    min = int(n.split(':')[1])
    sec = int(n.split(':')[2].split('.')[0])
    mils = n.split(':')[2].split('.')[1]
    if len(mils) == 6:
        mils = int(round(int(mils),-3)*0.001)
    elif len(mils) == 3:
        mils = int(mils)
    elif len(mils) == 1:
        mils = int(mils)*100
    total = hour * 60 * 60 + min * 60 + sec + mils * 0.001
    return total

def time_ext(n):
    time_ext_hour = round(n // 3600)
    time_ext_str = str(time_ext_hour).zfill(2) + ':'

    time_ext_min = round(n % 3600 // 60)
    time_ext_str += str(time_ext_min).zfill(2) + ':'

    time_ext_etc = round(n % 3600 % 60, 3)

    time_ext_sec = int(time_ext_etc)
    time_ext_str += str(time_ext_sec).zfill(2) + '.'

    time_ext_mils = time_ext_etc-time_ext_sec
    time_ext_mils = round(time_ext_mils,3) *1000
    if time_ext_mils == 0:
        time_ext_str += '000'
    else:
        time_ext_str += str(int(time_ext_mils)).zfill(3)


    return time_ext_str

def time_diff(a, b):
    time_diff = round(b-a, 3)

    time_diff_hour = round(time_diff // 3600)
    time_diff_str = str(time_diff_hour).zfill(2) + ':'

    time_diff_min = round(time_diff % 3600 // 60)
    time_diff_str += str(time_diff_min).zfill(2) + ':'

    time_diff_etc = round(time_diff % 3600 % 60, 3)

    time_diff_sec = int(time_diff_etc)
    time_diff_str += str(time_diff_sec).zfill(2) + '.'

    time_diff_mils = time_diff_etc - time_diff_sec
    time_diff_mils = round(time_diff_mils, 3) * 1000
    if time_diff_mils == 0:
        time_diff_str += '000'
    else:
        time_diff_str += str(int(time_diff_mils)).zfill(3)

    return time_diff_str


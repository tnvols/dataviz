import datetime
start_time = "2014-07-01"
end_time = "2014-08-20"
start_dt = datetime.datetime.strptime(start_time, '%Y-%m-%d')
start_dlist = list(start_dt.timetuple())
end_dt = datetime.datetime.strptime(end_time, '%Y-%m-%d')
end_dlist = list(end_dt.timetuple())
date_list = [(end_dlist[0] - start_dlist[0]), (end_dlist[1] - start_dlist[1]), (end_dlist[2] - start_dlist[2])]
print date_list

print int((end_time[0:4] + end_time[5:7] + end_time[8:]))-int((start_time[0:4] + start_time[5:7] + start_time[8:]))

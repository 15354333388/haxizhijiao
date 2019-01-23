# -*- coding: utf-8 -*-
import time


class ChangeTime(object):

    @staticmethod
    def change_time_to_date(timeType, timeStamp=None):  # 将时间戳转换成任意形式的日期
        if not timeStamp:
            timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime(timeType, timeArray)
        return otherStyleTime

    @staticmethod
    def change_date_to_time(date):  # 将日期转化为时间戳
        return time.mktime(date.timetuple())
    #
    # time.mktime(query['u_createtime'].timetuple())
    # if ("OPTIONS".equals(httpRequest.getMethod())){
    # filterChain.doFilter(httpRequest, httpResponse);
    # return;
    # }
from icalendar import Calendar, Event
import uuid
import json

with open('overall.json', 'r') as zongbiao:
    KeBiao = json.load(zongbiao)
    allkb = KeBiao['data']

cal = Calendar()
cal.add('VERSION','2.0')
cal.add('X-WR-CALNAME','生成ics文件测试')
cal.add('X-APPLE-CALENDAR-COLOR','#540EB9')
cal.add('X-WR-TIMEZONE','Asia/Shanghai')

bgtime = ['0','080000','085000','095000','104000','113000','140500','145500','154500','164000','173000','183000','192000','201000']
edtime = ['0','084500','093500','103500','112500','121500','145000','154000','163000','172500','181500','191500','200500','205500']
days = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
year = KeBiao['year']
month = KeBiao['month']
wkday = KeBiao['day']

for week in allkb:
    wkday = wkday + 7
    if (wkday > days[month]):
        wkday = wkday - days[month]
        month = month + 1 
        if (month > 12):
            month = 1
    strday = "%02d" % wkday
    strmonth = "%02d" % month
    basedate = int(str(year) + strmonth + strday)
    for day in week['data'][0]['data']:
        if (day['day']==8):
            continue
        date = basedate + day['day']
        courses = day['curriculumList']
        for course in courses:
            if (course['hasClass']==False):
                continue
            event = Event()
            bg = bgtime[course['fromClass']]
            ed = edtime[course['endClass']]
            classname = course['name']
            if (classname == None):
                classname = '没有上课地点'
            classroom = course['classroom']
            teacher = course['teacher']
            event.add('UID',str.upper(str(uuid.uuid4())))
            event.add('DTSTART;TZID=Asia/Shanghai', str(date) + 'T' + bg)
            event.add('DTEND;TZID=Asia/Shanghai', str(date) + 'T' + ed)
            event.add('SUMMARY', classname)
            event.add('SEQUENCE','0')
            event.add('DESCRIPTION','Teacher: ' + teacher)
            event.add('LOCATION', classroom)
            cal.add_component(event)

f = open('all.ics', 'wb')
f.write(cal.to_ical())
f.close()


        
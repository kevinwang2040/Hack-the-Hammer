import sys
import twitter
import time
import mraa

buzz = mraa.Gpio(29)
buzz.dir(mraa.DIR_OUT)

print("What time would you like your alarm? (24 hour format)")
hour = int(input("Enter the hour: "))
minute = int(input("Enter the minute: "))
second = int(input("Enter the second: "))

hour = hour - 19
if hour < 0:
    hour = 24 + hour

bus = input("Are you a bus student? (Y/N) ")

api = twitter.Api(consumer_key="EywEWq2n20NwBgGTyzIEeB0U8",
                      consumer_secret="nHVSWuGpBCeQ4d33UHiRevjEqy5lgN8BeNFVNpZbaXF2TqrWGC",
                      access_token_key="838169904499015681-9OQ5Xl6yVQK6IBhJKT62AYpYluxtUGd",
                      access_token_secret="J5hiTjjKRZ4ATU3tF4r1LhO86Az8NZbgtcKtQGbd6QQJe")

kevin = 838169904499015681
aaron = 959804517494771712
peel = 23796987

statuses = api.GetUserTimeline(kevin)

#non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#print("Hi".translate(non_bmp_map))

old = statuses[0].text

alarm = True

#main running loop
while True:
    buzz.write(0)
    #print(alarm)
    statuses = api.GetUserTimeline(kevin)
    new = statuses[0].text
    if new != old:
        #print(old)
        #print(new)
        #print("check")
        old = new
        if bus == "Y":
            if ("school" in new and ("close" in new or "cancel" in new)) or ("bus" in new and "cancel" in new):
                alarm = False
            else:
                alarm = True
        else:        
            if "school" in new and ("close" in new or "cancel" in new):
                alarm = False
            else:
                alarm = True

    #print(time.localtime().tm_hour)

    #alarm goes off at set time if alarm is on
    #print(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
    if time.localtime().tm_hour == hour  and time.localtime().tm_min == minute and time.localtime().tm_sec >= second:
        #print("time reached")
        if alarm:
            #print("alarm goes off")
            buzz.write(1)
            time.sleep(3)
            alarm = False
        else:
            #print("no alarm")

    if time.localtime().tm_hour == 0  and time.localtime().tm_min == 0 and time.localtime().tm_sec == 0:
        alarm = True


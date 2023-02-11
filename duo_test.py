#!/usr/bin/python3
'''Testing Duolingo from Python
'''

#Create a file named config.py to import with the username/password
import smtplib
import config
from Duolingo import duolingo


NAME = config.username
PASSWORD = config.password
FROM = config.From
TO = config.To
MAILSERVER = config.Mailserver
DEBUG = config.Debug


LINGO = duolingo.Duolingo(NAME, PASSWORD)
#print("USER_DATA.tracking_properties =-----------------")
#print(LINGO.__dict__['user_data'].__dict__['tracking_properties'])

#print("USER=-----------------")
#print(LINGO.get_user_info())

#print("Streak=-----------------")
STREAK = LINGO.get_streak_info()
if not STREAK['streak_extended_today']:
    print("No streak")

#print("TODAY=-----------------")
DAILYXP = LINGO.get_daily_xp_progress()

HAS_FREEZE = LINGO.__dict__['user_data'].__dict__['tracking_properties']['has_item_streak_freeze']
RUPEE_WAGER = LINGO.__dict__['user_data'].__dict__['tracking_properties']['has_item_rupee_wager']
STREAK_WAGER = LINGO.__dict__['user_data'].__dict__['tracking_properties']['has_item_streak_wager']
NUM_FREEZE = LINGO.__dict__['user_data'].__dict__['tracking_properties']['num_item_streak_freeze']

MAILOBJ = smtplib.SMTP(MAILSERVER, 25)
if not HAS_FREEZE or NUM_FREEZE < 2:
    #buy freeze
    print("Num freezes less than 2. About to buy one")
    LINGO.buy_item('streak_freeze', 'en')
    MSG = ("From: %s\r\nTo: %s\r\nSubject: DuoLingo Script on m59ss02\r\n\r\n\
            Bought a Streak Freeze" %(FROM, TO))
    try:
        MAILOBJ.sendmail(FROM, TO, MSG)
    except NameError:
        print("Unable to connect to mail server")
        #raise ValueError("Unable to send email")
    except ValueError:
        #raise ValueError("Unable to send email")
        print("Unable to send mail")
        #pass
else:
    print("Does have streak freeze")
    MSG = ("From: %s\r\nTo: %s\r\nSubject: DuoLingo Script on m59ss02\r\n\r\n\
            Streak Freeze Ok for the day" %(FROM, TO))
    try:
        MAILOBJ.sendmail(FROM, TO, MSG)
    except NameError:
        print("Unable to connect to mail server")
        #raise ValueError("Unable to send email")
    except ValueError:
        #raise ValueError("Unable to send email")
        print("Unable to send mail")
        #pass

if not RUPEE_WAGER:
    print("Does not have rupee wager")
    try:
        LINGO.buy_item('rupee_wager', 'en')
        print("Bought a Rupee Wager")
    except Exception:
        raise ValueError("Unable to buy Rupee Wager")
else:
    print("Does have rupee wager")

#if not STREAK_WAGER:
#    print("Does not have streak wager")
#    try:
#        LINGO.buy_item('streak_wager', 'en')
#        print("Bought a Streak Wager")
#        #print("DEBUG: Should have, but did not buy a Streak Wager")
#    except Exception:
#        raise ValueError("Unable to buy Streak Wager")
#else:
#    print("Does have streak wager")

if DAILYXP['xp_today'] == 0 or (not STREAK['streak_extended_today']):
    print("XP = 0")

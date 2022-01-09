# Script coded to read new announcements from eclass and send them via a telegram bot.

It is designed to run on a Raspberry Pi Zero 2 W

Scheduled to run every 6 minutes (through crontab)

Added cronitor.io job so it can be monitored more easily

Connects to eclass (University of Thessaly), gets new announcements and sends them via a telegram bot to you.

May work on other eclass platforms of Greek Unis but will probably need some editing in the links and html tags to read the announncements correctly.



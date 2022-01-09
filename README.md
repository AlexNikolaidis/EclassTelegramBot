# Get new announcements from eclass as a message via a telegram bot.

Designed to run on a Raspberry Pi Zero 2 W

Scheduled to run every 6 minutes (through crontab)

Cronitor.io integration so it can be monitored more easily

Connects to eclass (University of Thessaly), gets new announcements and sends them via a telegram bot to you.

May work on other eclass platforms of Greek Unis but will probably need some editing in the links and html tags to read the announncements correctly.

You need a telegram bot token id (from BotFather), chat id (where to send the messages) and a cronitor API Key to send the updates

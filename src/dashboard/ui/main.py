from os import system
from util.general import colorize
from step.select import stepSelect
from step.transcode import stepTranscode
from step.torrent import stepTorrent
from step.extra import stepExtra
from step.upload import stepUpload

def printJobsUISelector(dashboard):
    dashboard.jobsUIEnabled = True
    selection = input("")
    selection = "1" if selection == "" else selection
    if selection == "1":
        dashboard.jobsUIShowCompleted = not dashboard.jobsUIShowCompleted
    elif selection == "2":
        dashboard.jobsUIEnabled = False
        return
    
    printJobsUISelector(dashboard)

def printMainUI(dashboard):
    system("clear")
    print(f'{colorize("gray", f"Nyan Anime Toolkit - Menu")}')
    print("1) List jobs")
    print("2) Add a job")
    print("3) Other")
    print("4) Quit")
    selection = input("> Selection? [2]: ")
    selection = "2" if selection == "" else selection

    if selection == "1":
        printJobsUISelector(dashboard)
    elif selection == "2":
        system("clear")
        print(f'{colorize("gray", f"Nyan Anime Toolkit - Add a job")}')
        print("1) Transcode (used to transcode anime)")
        print("2) Create torrent (used to create a torrent for an anime)")
        print("3) Upload (used to upload anime)")
        print("4) Back")
        selection = input("> Selection? [1]: ")
        selection = "1" if selection == "" else selection

        if selection == "1":
            stepSelect()
            stepTranscode(dashboard)
        elif selection == "2":
            stepTorrent(dashboard)
        elif selection == "3":
            stepUpload(dashboard)
    elif selection == "3":
        system("clear")
        print(f'{colorize("gray", f"Nyan Anime Toolkit - Other")}')
        print("1) Extra (used for extra post-processing)")
        print("2) Back")
        selection = input("> Selection? [1]: ")
        selection = "1" if selection == "" else selection

        if selection == "1":
            stepExtra()
    elif selection == "4":
        exit(0)
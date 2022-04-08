import subprocess
from os import system, path
from util.general import colorize
from step.select import stepSelect
from step.transcode import stepTranscode
from step.extra import stepExtra, downloadPoster
from job.download import DownloadJob
from job.torrent import TorrentJob
from job.upload import UploadJob
from job.collection import JobCollection
from util.api import fetchAnilist, fetchMAL

def printJobsUISelector(dashboard):
    dashboard.jobsUIEnabled = True
    selection = input("")
    selection = "1" if selection == "" else selection
    if selection == "1":
        dashboard.jobsUIShowCompleted = not dashboard.jobsUIShowCompleted
    elif selection == "2":
        dashboard.jobsUICollapse = not dashboard.jobsUICollapse
    elif selection == "3":
        dashboard.jobsUIEnabled = False
        return
    
    printJobsUISelector(dashboard)

def printMainUI(dashboard):
    system("clear")
    print(f'{colorize("gray", f"Nyan Anime Toolkit - Menu")}')
    print("1) List jobs")
    print("2) Add a job")
    print("3) Other")
    print("4) RSS")
    print("5) Quit")
    selection = input("> Selection? [2]: ")
    selection = "2" if selection == "" else selection

    if selection == "1":
        printJobsUISelector(dashboard)
    elif selection == "2":
        system("clear")
        print(f'{colorize("gray", f"Nyan Anime Toolkit - Add a job")}')
        print("1) Complete series (transcodes, creates a torrent and uploads an entire series)")
        print("2) New episodes (trancodes and uploads new episodes)")
        print("3) Only download")
        print("4) Only transcode (entire series)")
        print("5) Only transcode (new episodes)")
        print("6) Only create torrent (entire series)")
        print("7) Only upload")
        print("8) Back")
        selection = input("> Selection? [8]: ")
        selection = "8" if selection == "" else selection

        if selection == "1":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Complete series")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            jobs = []

            selection = input("> Download torrent? [n]: ")
            selection = "n" if selection == "" else selection
            if selection == "y":
                opt_magnet = ""
                if not path.exists(f"/usr/src/nyananime/torrents/{opt_id}/link.conf"):
                    opt_magnet = input("> Magnet link?: ")
                else:
                    opt_magnet = subprocess.getoutput(f'cat "/usr/src/nyananime/torrents/{opt_id}/link.conf"')
                jobs.append(DownloadJob(opt_id, None, opt_magnet))
            else:
                stepSelect(dashboard, opt_id)

            # Poster is needed for the torrent
            if not path.exists(f"/usr/src/nyananime/dest-episodes/{opt_id}/poster.webp"):
                media = fetchAnilist(opt_id)
                downloadPoster(opt_id, media["coverImage"]["extraLarge"])

            selection = input("> Process extra data now? [n]: ")
            selection = "n" if selection == "" else selection
            if selection == "y":
                opt_mal_id = input("> Anime ID? (ID from myanimelist.net): ")
                stepExtra(opt_id, opt_mal_id)
            
            jobs.extend(stepTranscode(dashboard, opt_id))
            jobs.append(TorrentJob(opt_id))
            jobs.append(UploadJob(opt_id, None))
            dashboard.addJobCollection(JobCollection(f"Complete series job for '{opt_id}'", jobs))
        elif selection == "2":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - New episodes")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            opt_i = input("> First episode index?: ")
            jobs = []

            selection = input("> Download torrent? [n]: ")
            selection = "n" if selection == "" else selection
            if selection == "y":
                opt_magnet = ""
                if not path.exists(f"/usr/src/nyananime/torrents/{opt_id}/link.conf"):
                    opt_magnet = input("> Magnet link?: ")
                else:
                    opt_magnet = subprocess.getoutput(f'cat "/usr/src/nyananime/torrents/{opt_id}/link.conf"')
                jobs.append(DownloadJob(opt_id, opt_i, opt_magnet))
            else:
                stepSelect(dashboard, opt_id)

            selection = input("> Process extra data now? [n]: ")
            selection = "n" if selection == "" else selection
            if selection == "y":
                opt_mal_id = input("> Anime ID? (ID from myanimelist.net): ")
                stepExtra(opt_id, opt_mal_id, True)
            
            jobs.extend(stepTranscode(dashboard, opt_id, opt_i))
            jobs.append(UploadJob(opt_id, opt_i))
            dashboard.addJobCollection(JobCollection(f"New episodes job for '{opt_id}'", jobs))
        elif selection == "3":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Only download")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            opt_magnet = ""
            if not path.exists(f"/usr/src/nyananime/torrents/{opt_id}/link.conf"):
                opt_magnet = input("> Magnet link?: ")
            else:
                opt_magnet = subprocess.getoutput(f'cat "/usr/src/nyananime/torrents/{opt_id}/link.conf"')
                
            dashboard.addJobCollection(JobCollection(f"Only download job for '{opt_id}'", [DownloadJob(opt_id, None, opt_magnet)]))
        elif selection == "4":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Only transcode")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            stepSelect(dashboard, opt_id)
            dashboard.addJobCollection(JobCollection(f"Only transcode job for '{opt_id}'", stepTranscode(dashboard, opt_id)))
        elif selection == "5":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Only transcode")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            opt_i = input("> First episode index?: ")
            stepSelect(dashboard, opt_id)
            dashboard.addJobCollection(JobCollection(f"Only transcode job for '{opt_id}'", stepTranscode(dashboard, opt_id, opt_i)))
        elif selection == "6":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Only torrent")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            dashboard.addJobCollection(JobCollection(f"Only torrent job for '{opt_id}'", [TorrentJob(opt_id)]))
        elif selection == "7":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Only upload")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            dashboard.addJobCollection(JobCollection(f"Only upload job for '{opt_id}'", [UploadJob(opt_id, None)]))
    elif selection == "3":
        system("clear")
        print(f'{colorize("gray", f"Nyan Anime Toolkit - Other")}')
        print("1) Add complete series data")
        print("2) Add new episodes data")
        print("3) Get series timestamp")
        print("4) Load previous jobs")
        print("5) Back")
        selection = input("> Selection? [4]: ")
        selection = "4" if selection == "" else selection

        if selection == "1":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Add complete series data")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            opt_mal_id = input("> Anime ID? (ID from myanimelist.net): ")
            stepExtra(opt_id, opt_mal_id)
        elif selection == "2":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Add new episodes data")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            opt_mal_id = input("> Anime ID? (ID from myanimelist.net): ")
            stepExtra(opt_id, opt_mal_id, True)
        elif selection == "3":
            system("clear")
            print(f'{colorize("gray", f"Nyan Anime Toolkit - Get series timestamp")}')
            opt_id = input("> Anime ID? (ID from anilist.co): ")
            opt_mal_id = input("> Anime ID? (ID from myanimelist.net): ")
            media = fetchAnilist(opt_id)
            mediaMAL = fetchMAL(opt_mal_id, media["episodes"])
            print(f"UPDATE animes SET timestamp = {mediaMAL['timestamp']} WHERE id = '{opt_id}';")
            input("Press enter...")
        elif selection == "4":
            dashboard.loadJobs()
    elif selection == "4":
        system("clear")
        print(f'{colorize("gray", f"Nyan Anime Toolkit - RSS")}')
        print("1) Reload RSS config")
        print("2) List pending jobs")
        print("3) Create pending jobs")
        print("4) Back")
        selection = input("> Selection? [4]: ")
        selection = "4" if selection == "" else selection

        if selection == "1":
            system("clear")
            print("Reloading RSS...")
            dashboard.loadRSS()
        elif selection == "2":
            system("clear")
            jobs = dashboard.createRSSJobs(True)
            print(f"Pending jobs ({len(jobs)}):")
            for job in jobs:
                print(job)
            input("Press enter...")
        elif selection == "3":
            dashboard.createRSSJobs()
    elif selection == "5":
        exit(0)
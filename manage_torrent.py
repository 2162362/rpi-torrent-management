import sys
import os
import datetime
import re
import json

def copy_file(file_type, file_source, file_name):
    date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    script_dir = "./custom_scripts"
    with open(os.path.join("/home", "pi","config.json")) as f:
        config = json.load(f)
    log_file = open(config["file_log_path"], "a+")
    log_file.seek(0)
    logs = log_file.read().splitlines()
    if file_source in logs:
        print(f"{date_string}: {file_source} was already logged previously")
        log_file.close()
        return

    if file_type == "Movies":
        destination = "/mnt/seagate/jellyfin_media/movies/"
        os.system(f"cp -r {file_source} {destination}")
        log_file.write(f"{date_string}: {file_source} was copied to {destination}\n")
    elif file_type == "Series":
        destination = "/mnt/seagate/jellyfin_media/series/"
        os.system(f"cp -r {file_source} {destination}")
        log_file.write(f"{date_string}: {file_source} was copied to {destination}\n")

        #construct custom script path
        regex_pattern = r".+?(?=S\d)"
        modified_file_name = re.findall(regex_pattern, file_name)[0]
        script_path = os.path.join("home", "pi", "custom_scripts", modified_file_name + "py")

        # execute custom script if it exists
        if os.path.isfile(script_path):
            os.system(f"python {script_path} {destination} {file_name}")
            log_file.write(f"{date_string}: Executed custom script {script_path}\n")
    elif file_type == "Games":
        destination = "/mnt/mitsai/torrents/games/" + file_name
        log_file.write(f"{date_string}: {file_source} was stored in {destination}\n")
    elif file_type == "Other":
        destination = "/mnt/mitsai/torrents/other/" + file_name
        log_file.write(f"{date_string}: {file_source} was stored in {destination}\n")
    else:
        log_file.write(f"{date_string}: {file_source} was not processed, because {file_type} is not a valid file type\n")
    log_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python manage_torrent.py <file_type> <file_source> <file_name>")
        sys.exit(1)
    try:
        copy_file(sys.argv[1], sys.argv[2], sys.argv[3])
    except Exception as e:
        log_file = open("/mnt/mitsai/torrents/logs.txt", "a+")
        log_file.write(str(e))

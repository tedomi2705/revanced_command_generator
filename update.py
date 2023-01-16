import requests
import json
import os
import wget

revanced_cli_download_link = requests.get(
    "https://api.github.com/repos/revanced/revanced-cli/releases/latest"
).json()["assets"][0]["browser_download_url"]
revanced_cli_file_name = revanced_cli_download_link.split("/")[-1]

revanced_patches_download_link = requests.get(
    "https://api.github.com/repos/revanced/revanced-patches/releases/latest"
).json()["assets"][1]["browser_download_url"]
revanced_patches_file_name = revanced_patches_download_link.split("/")[-1]

revanced_integrations_download_link = requests.get(
    "https://api.github.com/repos/revanced/revanced-integrations/releases/latest"
).json()["assets"][0]["browser_download_url"]
revanced_integrations_file_name = revanced_integrations_download_link.split("/")[-1]

revanced_list = [k for k in os.listdir() if "revanced" in k]

if revanced_cli_file_name not in revanced_list:
    for k in revanced_list:
        if "revanced-cli" in k:
            os.remove(k)
    wget.download(revanced_cli_download_link)
    print("\nrevanced-cli updated")

if revanced_patches_file_name not in revanced_list:
    for k in revanced_list:
        if "revanced-patches" in k:
            os.remove(k)
    wget.download(revanced_patches_download_link)
    print("\nrevanced-patches updated")

if revanced_integrations_file_name not in revanced_list:
    for k in revanced_list:
        if "revanced-patches" in k:
            os.remove(k)
    wget.download(revanced_integrations_download_link)
    print("\nrevanced-integrations updated")

# get youtube version

youtube_version = requests.get(
    "https://raw.githubusercontent.com/revanced/revanced-patches/main/patches.json"
).json()[0]["compatiblePackages"][0]["versions"][0]

print("Youtube version: " + youtube_version)

youtube_apk = ""
for k in os.listdir():
    if youtube_version in k:
        youtube_apk = k
if youtube_apk == "":
    print("Youtube apk not found")
    exit()

print("Generating revanced script...")
command = (
    f"adb install {youtube_apk} \njava -jar {revanced_cli_file_name} "
    f"-a {youtube_apk} "
    f"-d 3d43ac27 "
    f"-o revanced_{youtube_apk} "
    f"-b {revanced_patches_file_name} "
    f"-i {revanced_integrations_file_name} "
    f"-e microg-support "
    f"-m {revanced_integrations_file_name} "
    f"--mount "
)
excluded_patches = [
    "custom-branding",
    "disable-fullscreen-panels",
    "disable-startup-shorts-player",
    "disable-zoom-haptics",
    "enable-wide-searchbar",
    "hdr-auto-brightness",
    "hide-album-cards",
    "hide-artist-card",
    "hide-autoplay-button",
    "hide-breaking-news-shelf",
    "hide-captions-button",
    "hide-cast-button",
    "hide-create-button",
    "hide-crowdfunding-box",
    "hide-email-address",
    "hide-endscreen-cards",
    "hide-info-cards",
    "hide-my-mix",
    "hide-shorts-button",
    "hide-time-and-seekbar",
    "spoof-app-version",
]
for k in excluded_patches:
    command += f"-e {k} "
with open("revanced.bat", "w") as f:
    f.write(command)

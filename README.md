# Drift
An open source browser based on the PyQtWebEngine and PyQt5 framework 

> [!NOTE]
> (Sorry for overhyping Beta 4 and V1.0 in the [Release](https://github.com/DriftBR/Drift/releases/tag/v1.0_beta4)

## New features
This is a visual refresh of [NuggyNet](https://www.github.com/DriftBR/NuggyNet3). Here are some awesome new features:
* Tabs (v3 didn't have them)
* "French" menu (Removed but came back in this version)
* "Education" mode (Removes IceSocial sidebar)
* [IceSocial](https://www.icesocial.net) sidebar

## Planned features
Here are future ideas for Drift:
* Smooth scrolling
* YT videos higher than 360p
* Not give up after V3

## The team:
People who are on the Drift team so far:
* [@i486nugget](https://www.github.com/i486nugget) - Lead developer and designer
* [@Folder_svg](https://bsky.app/profile/foldersvg.bsky.social) - UI concept designer
* [@timi2506](https://bsky.app/profile/tim.glos-omu.uk) - Dude compiling macOS versions

### ***FEEL FREE TO CONTRIBUTE IF YOU KNOW PYTHON AND PYQT***

> [!IMPORTANT]  
> This app might soon become Mac-only (Apple Silicon) due to the fact that the owner is getting a Mac soon and will make it natively on Xcode without the hell that Python is. 

> [!NOTE]
> Mac and Linux users, you do your bit by contributing and adding build instructions

# Building
1) Make sure you have Python 3.12.4 installed with "pip"
2) Download code as zip and extract
3) Open CMD/Terminal and navigate to extracted zip directory and run command `pip install -r requirements.txt`
4) Run the script to make sure everything works. Once it does, here's the building bit:
5) Run `pip install pyinstaller`
6) In the same directory, run ```pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --name "drift" --add-data "Assets;Assets/"  ""```
7) Navigate to the brand new "dist" folder
8) All done

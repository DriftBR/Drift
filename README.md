# Drift
An open source browser based on the PyQtWebEngine and PyQt5 framework 

## New features
This is a visual refresh of [NuggyNet](https://www.github.com/DriftBR/NuggyNet3). Here are some awesome new features:
* Tabs (v3 didn't have them)
* "French" menu (Removed but came back in this version)
* "School" mode (Removes IceSocial sidebar)
* [IceSocial](https://www.icesocial.net) sidebar

## Planned features
Here are future ideas for Drift:
* <It's a little empty here, come back when I have ideas.>

***FEEL FREE TO CONTRIBUTE IF YOU KNOW PYTHON AND PYQT***

> [!IMPORTANT]  
> This app might soon become Mac-only (Apple Silicon) due to the fact that the owner is getting a Mac soon and will make it natively on Xcode without the hell that Python is. 

> [!NOTE]
> Mac and Linux users, you do your bit by contributing and adding build instructions

# Building
1) Make sure you have Python 3.12.4 installed with "pip"
2) Download code as zip and extract
3) Open CMD window and navigate to extracted zip directory and run command `pip install -r requirements.txt`
4) Run the script to make sure everything works. Once it does, here's the building bit:
5) Run `pip install pyinstaller`
6) In the same directory, run `pyinstaller --onefile --noconsole --icon=icon.ico --add-data="nwin.html:." --add-data="about.png:." app.py`
7) Navigate to the brand new "dist" folder
8) All done

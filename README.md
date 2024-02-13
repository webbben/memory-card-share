# Memory card share

This repo was made to facilitate sharing virtual gamecube memory cards between friends. It's assumed you're using this with Dolphin emulator on gamecube games.

# Setup Instructions

Go to the [/install](https://github.com/webbben/memory-card-share/tree/master/install) folder and follow the instructions for your operating system. If you use windows, then you should be able to simply run the windows setup wizard and it will take care of pretty much everything for you.

# User Guide

At this point, it's assumed you've completed the installation and setup completely. The rest of this file will provide guidelines for how this program is intended to be used.

## Running this program!

To start this program, run the "run" file for your OS. This will be `run-windows.bat` or `run-unix.sh`.

This starts up the menu so you can get started!

<img width="292" alt="image" src="https://github.com/webbben/memory-card-share/assets/38891424/fc737b91-3476-4a5f-8cc5-42fb3d61eb48">

## General flow of use
This application is meant to make sure more than one person isn't playing on a memory card at the same time. This is because that will likely cause data corruption or data loss (one person overwrites the other's data).

So, here's a quick overview of the flow:
* Open this application when you want to play a gamecube game
* Checkout an available memory card to play with.
* Leave this application running, and go play your game in Dolphin.
* When you're done playing, you can close Dolphin. Return to this application.
* Save your changes, and exit. This will release your lock and upload the memory card data to github so other users can play now.

### Checking out a memory card
This is the first step to playing - if you haven't checked a memory card out, you should not play using that memory card! Otherwise you will probably lose your changes.

When you look at the memory cards to choose from, available ones will be green. Locked memory cards will show as red, and will tell you which user has it locked and for how long.
If someone has held the lock on a memory card for really long time, you might wanna contact them to make sure they didn't forget.

Once you checkout a memory card (aka "lock" it), it's yours to use and others will be prevented from checking it out.

Currently, you can in theory check out as many cards as you like, but you should really only check out one or two at a time. the only reason you'd check out two is if you want to visit someone else's town in animal crossing, probably.

### Using the memory card in Dolphin
Once you've checked out a memory card, the first thing you should do is make sure Dolphin has the correct path set to this memory card file. You can change the memory card file path in Dolphin's Config:

![image](https://github.com/webbben/memory-card-share/assets/38891424/5d178e5c-345c-4f54-bebc-1cb2efd00280)

You should point to the **region** folder inside the memory card folder that you want to use.  Otherwise Dolphin will complain.  So, if you're using "Card A" and you're playing a Japanese game, you should use `/memory-cards/Card A/JPN`:

![image](https://github.com/webbben/memory-card-share/assets/38891424/30fdf4cc-7fcf-48aa-a8f0-ba4470afea31)

Notes:
* Make sure you are set to use a "GCI folder". If you don't have that option, you might need to download a more recent version of Dolphin.
* Once you set the path to a memory card, you won't need to change it or re-set it again unless you decide to checkout a different memory card in the future.

### Saving your data
After playing with a memory card in Dolphin, Dolphin will save your changes to the memory card files inside the memory card folder.
Return to this application (it should still be open from when you checked out a memory card) and go to the "Save your changes" menu option.

The changes to the memory card files should be found, and you should see the name of your memory card in the file path(s). Sometimes more than one file is created or changed, so no worries if more than one file is found.
If everything looks correct to you, go ahead and save your changes. Upon saving, you will be prompted to unlock your memory cards. You should probably do this unless you plan to immediately resume playing.

### Discarding your changes ("Hard Reset")
If you decide for some reason that you don't want to keep the changes you've made to your memory card data, you can opt to `hard reset`. Hard reseting will completely replace your local files with the version currently stored in github. If you do this, it goes without saying that this action is **irreversible**.

Also note that this "hard reset" option can be used for ensuring the integrity of your local files and scripts. If your local files have been unexpectedly changed, or if there is an update to the source code, it's recommended you do a hard reset to make sure everything is up to date and functioning correctly. I'll probably be adding some code that checks for source code updates and forcibly hard resets to install them in the near future.

### Releasing your locked memory cards
There are two ways locked memory cards can be released:
* having them unlocked when you save your changes
* closing the application using the 'Quit' option on the main menu
  * this will only release your locks if you've saved your changes already

It's crucial for you to make sure you unlock your memory cards before leaving, because if you forget to then other users won't be able to play on them!
So, please don't forget. If you do end up forgetting for a long period of time, and you also haven't saved your changes yet, then you risk losing your progress in the locked memory card.

### Exiting
Once you're done playing, you can go ahead and close this application.  It's recommended you use the 'Quit' option from the menu though, since it does some checks to make sure you've saved your data and unlocked your memory cards.

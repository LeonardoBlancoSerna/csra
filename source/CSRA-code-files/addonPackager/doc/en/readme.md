# Utility manual for NVDA add-ons

This add-on tries to be a utility package for our installed and uninstalled add-ons.

In the different areas we try to be as fast as possible giving the possibility of doing actions to our complements in a massive way and not having to go one by one as in the add-on manager.

The areas already added as new features will be improved in the different versions.

This add-on can be launched from the Tools / Utility menu for NVDA add-ons.

The add-on does not have a assigned key shortcut for quick use.

You can add a gesture in the menu Preferences / Input Gestos... and look for Utility for NVDA add-ons.

## Disclaimer

The end user is the last responsible for the use of the add-on.

Everything is intended to be as reliable as possible but problems can always arise so the complement author will not be responsible for any problems arising from the use of this supplement.

# General description

The application is covered in 3 sections.

* 1st section: List where we can choose the category we want to use. It's where the focus remains every time we call the plugin.

We'll move up and down on that list.

* 2nd section: The area that includes the content of the category we have chosen.

This area is changing depending on the category. Description of categories later.

We can access from the categories with key shortcuts or tabulating.

* 3rd section: This section contains an editing box that will be activated when any action is executed giving information to the user of what is happening. The user will also be informed with a progress bar in all actions.

It also includes the buttons that will allow us to interact depending on what happened when doing the action as a Close button which will close the plugin.

As long as there is no current action the plugin can be closed with Escape, Alt+F4 or tabulated to the Close button.

## Plug-in packer

If we choose this category when we tabulate we will fall into a list with all the add-ons we have installed, regardless of whether they are enabled, disabled or not supported.

We can also go quickly with Alt+L, on this list we can select with space all those add-ons we want to choose to make a backup in a directory we choose.

Each add-on will be generated with its name and version and the identifier “_gen”, these generated add-ons can be installed with NVDA without any problems.

If we tab a button called Selection or we can quickly access Alt+S, that button if we press it will display a menu to select or disselect all add-ons quickly.

If we return to tabular we will fall on the Generate button or fast access Alt+G, if we press that button and have at least one marked add-on will open a window to choose the directory where we want to save the selected add-ons.

Once the directory has been chosen and the generation of the add-ons will begin. The focus will remain in a single reading box in which information will appear next to a progress bar that will tell us about the percentage it carries. The closing button, as well as the rest of the interface will be disabled until the action of generating the add-ons ends.

Once the action is over, we will be informed if everything was successful or there was a problem and if we now tabulate we can choose OK (Alt+A), Cancel (Alt+C) or close the interface if we wish.

The buttons accept and cancel will come out as the action is over.

In order to generate the add-ons it is essential to have at least one of the opposite marked we will be informed with an explanatory message.

## Multiple installer

This category will allow us to choose a Directory where we have accessories and we will be able to install them all at once.

When we enter that category we will fall into a button called Select a directory with add-ons to install... or shortcut (Alt+S), if we press it, give us a window to choose the directory containing add-ons.

The rest of the interface in this category is disabled until we choose a directory.

When we choose a directory the focus will leave us in the only reading box where we will be informed of what is going on while scanning for add-ons we will also receive information from the progress bar.

We will be informed once the scan is finished if there was any problem and how to act. To say that you only accept plugins that comply with the NVDA API that we have installed by discarding any incompatible or damaged plugins.

Once the scan is finished and if you found add-ons and we accept the list will be activated with the names of the add-ons you have found in that directory.

We can quickly go to that list with (Alt+L), on that list we will be able to choose as many accessories as we want to dial them with space.

If we tabulate we will have the same button select that there are on the screen Plug-in packers and that I will not explain why it is their same use.

If we tab again we will fall on the Install or Quick Access button (Alt+I).

If we have at least one selected add-on and press that button the installation of the add-on will be done either from one or more without displaying the classic installation NVDA window, with this we streamline the installation of add-ons.

Saying that this step also has protections as an API check, that the plugin is not damaged and other internal things of NVDA. Everything to always try the best functioning of our reader.

When we give the button to install the focus it will remain in the single reading box where it will be reported what the plugin is doing.

Also, when it's over, we were informed whether everything was a success or whether there was any plugin that could not be installed or whether there were errors.

Depending on what happened, the button will either accept or cancel next to the close button.

If you activate the accept button it is because NVDA to install some add-on and to apply the changes you need to restart, if you press it NVDA restart and we will already have the plugins or plugin installed.

If we do not accept and close we will not be able to use the add-on again until we reboot NVDA this is a protection to avoid duplicating actions.

If otherwise there were bugs and only the cancel button is presented, we can press it and return to the interface to do other things.

### WARNING

This category is implemented to streamline the installation of add-ons, but misused by installing add-ons can result in a poor performance of the reader. It is the responsibility of the user to use it properly.

## Uninstall Add-ons

This category will allow us to uninstall add-ons in a quick and single stroke.

We can choose from the list any of the accessories we have installed. We can select with space. To go quickly to the list (Alt+L).

We also have the selection button (Alt+S) that performs the function exactly as in the previous categories and will not explain again.

If we tabulate we will find the Uninstall button or quick access (Alt+D) if we press it and we have one or more selected plugins will leave the focus on the reading field and inform us of what it is doing.

We will also be informed through the progress bar.

Once finished we will be informed of the result and as in the Multiple Installer category we will be given the button to accept that you need to restart NVDA or cancel that something went wrong and the button close.

Remember that if we close in this category and have not responded to the need to restart the add-on it will not be used again until NVDA does not restart.

##

The uninstallation of add-ons once we have given the Uninstall button has no turning back so it is convenient to make sure that we know where to get the add-ons that we delete in case we want to reinstall them as if that add-on contains information in the add-on directory itself, that information will be deleted.

It is not usually of good praxis and NVDA does not recommend that the plugins keep information in the same directory of the add-on, but this is already a decision of the plugin programmer.

Therefore, I repeat myself to use this category under your responsibility.

## Enable/disable add-ons

This category will allow us to enable or mass disable our accessories.

If we enter the category we will fall into the list of the plugins that are enabled we can quickly access with (Alt+L), we can mark those plugins that we want to disable with the space bar.

If we have disabled add-ons then we will have a second list with such add-ons, we can quickly move between listings with (Alt+L) in that disabling list we can also mark those that we want to enable with the space bar.

We can mark add-ons in the two lists taking into account that the action will be done inverse by disabling those plugins marked in the list of enabled as enabling those add-ons that are marked in the list of disabled.

This category also has a select button but with a small difference, when we press it it will contain a submenu for each listing by selecting or disselecting everything for the list we choose.

If we tabulate we will find the Proceeding or Quick Access button (Alt+P), if we press it, leave the focus on the reading only box and inform us of what it is doing.

Once the action is finished it will happen just as in the previous categories informing and activating the corresponding buttons.

I recall again that if the action is satisfactory and we do not restart the add-on will not be used until NVDA restarts.

## Modifier of manifests

In this category we can change the manifest and thus be able to reconcile the plugins with the API required by NVDA. We can change the manifest to installed add-ons or add-ons that we have in a NVDA add-on file.

Now according to the latest NVDA policy and even new changes, each year in the first version of NVDA programmers will have to change the version to match their manifest with the NVDA version.

There will be programmers who will do so immediately, others who will be late and others who will simply not do so for abandoning supplements or for any reason.

In this last case we have to make the change of the property lastTestedNVDAVersion by hand and if we have many plugins we will have to waste time, also it is not a task for all users as there are many levels of users.

Also if we want to test the betas and the RCs we will have to change this parameter in the manifests otherwise we will not be able to have the complement installed.

Well NVDA is a constantly evolving reader so many times there are accessories that stay on the road due to lack of development and lack of adapting them to the changes that NVDA brings in its evolution.

This means that changing the date in the manifests solves a momentary problem in order to continue using those supplements that are not updated or that the developer delays updating them. But there will be supplements that will not only serve to change the manifest and need internal changes to adapt to the new versions, in that case the complement will be broken and only contact the author of the add-on.

It is well advised to update the supplements that come out with the changes in the manifests, although we have changed with this utility the date since it is possible that those supplements bring apart from the adaptation of the manifest other modifications that the developer has made.

Once we access this category we will fall into the list that will contain all the add-ons that we have installed together with its API version. We can quickly access with (Alt+L), we can select those add-ons that we want to change your manifest by clicking on them and as many as we want.

If we tabulate we will fall into three combined frames:

* Select larger version: This combined box has to match the date of the version that will have NVDA.

* Select version Less: Here with leaving in 1 is enough however and put the four versions that come out year in case there are changes. ( Anything can happen)

♪ Select a review: In this box combined with leaving 0 is enough, however I have placed up to 9 also in case.

If we tab, we have again the select button that will allow us to select or disselect all the add-ons in the list.

If we return to tabular we will fall on the Process button or quickly access (Alt+P).

If we press this button, a menu with the following options will be displayed:

♪ Processing installed, if we choose this option, the process of changing the manifest to the add-ons we have installed and have selected. It will be changed by what we have chosen in the larger, smaller and revised combined tables.

♪ Processing a plugin file, if we choose this option we will open a file window where we will have to choose the add-on file that we want to change the manifest. To say that before we have to choose the larger, smaller and revised version to apply.

If we choose to change the manifest to a file and the process was satisfactory, in the source directory of the plugin will generate another add-on with the same name but with the "_gen_modify_manifest" collet this will be the one containing the modified manifest to be used.

With either of the options we will be left the focus on the single reading box and informed of what happens.

Behavior will be the same as in previous categories with the buttons to accept and cancel.

I remember that if we choose a plugin file before we need to change the combined frames of larger version, smaller and revision to apply to the file we choose that configuration to the manifest.

##

The use of this utility and its results is exclusively under the responsibility of the end user.

## Complementary documentation

In this category and seeing that there are people who find it hard to read the documentation of the add-ons we can just that, consult the documentation that the authors have written to know how to handle the add-ons.

In this category we will find a list with quick access (Alt+L) in which all the add-ons that have documentation will be displayed, excluding those that for any reason have no documentation.

If we tabulate we will find a button called Open Add-on Documentation or Quick Access (Alt+A), if we press or call that button from the list will open in our default browser the add-on documentation we have chosen on the list.

# Translators and collaborators:

If someone wants to collaborate with translations, they can do so by the Github add-on repository or by sending an email to xebolax@gmail.com

♪ English: Automatic translation

# Change log.
## Update Information:
This add-on will follow the following upgrade path:

Only versions of larger size (e.g. v3.1) are listed in this record.

Versions of larger type.menor.x (e.g. v3.1.2) are translation updates.

The changes in the add-on will be reflected in this section explaining the latest developments.

The main document will not be modified as an orientation for the user.

The user is responsible for reviewing this section to be informed of the changes.

## Version 1.0.

♪ Initial version.

It will be rewritten from scratch what was the former Plug-in Packer together with the incorporation of new functions.

The add-on switches from name to Utility for NVDA add-ons but still maintains the internal name that NVDA handles in (addonPackager).

By launching this version, the crycric add-on will be left unmaintained as this add-on already includes the change of manifests.

Translated by ArgosTranslate


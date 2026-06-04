# this will be used to import and export data from the settings
# so easily settings export will print all the current data for visualization in a nice readable format maybe tables or smt
# settings import will let the user replace all existing data so we need to read thorug all teh data and let the user replace it with new data or keep the old data if they want to
# to make all easier we read all txt in settings allowet the user to select which they wanna edit so
# settings export -> prints all current settings in a nice format
# settings import -> prompts the user to select which setting they wanna edit then prompts them to enter new data for that setting then saves the new data to the appropriate txt file
import os

from registry import register
from prompt_toolkit.shortcuts import radiolist_dialog


@register('settings')
def settings(args):
    if not args:
        print("Usage: settings <export|import>")
        return
    
    action = args[0].lower()

    if action == 'export':
        export_settings()
    elif action == 'import':
        import_settings()
    else:
        print(f"Unknown action: {action}")

def export_settings():
    print("Exporting settings...")
    for file in os.listdir('settings'):
        if file.endswith('.txt'):
            print(f"\n{file}:")
            with open(f'settings/{file}') as f:
                print(f.read())

def import_settings():
    print("Importing settings...")
    txt_files = [file for file in os.listdir('settings') if file.endswith('.txt')]
    if not txt_files:
        print("No settings files found.")
        return
    
    print("Available settings files:")

    selection = radiolist_dialog(
        title="Select Settings File",
        text="Choose a settings file to edit:",
        values=[(str(i), file) for i, file in enumerate(txt_files, start=1)]
    ).run()

    #for some reason it returns the int rather than the file name so we need to convert it back to the file name
    if selection is None:
        print("No file selected.")
        return
    print(f"Selected file: {txt_files[int(selection)-1]}")

    # let the user decide which value to change also using radiolist_dialog
    # we can read the file and split it by lines then split each line by = to get the key and value then we can use the keys as options for the radiolist_dialog
    options = []
    with open(f'settings/{txt_files[int(selection)-1]}') as f:
        options = f.read().splitlines()

    print(f"Current settings in {txt_files[int(selection)-1]}:")

    setting_selection = radiolist_dialog(
        title="Select Setting to Edit",
        text="Choose a setting to edit:",
        values=[(str(i), option) for i, option in enumerate(options, start=1)]
    ).run()

    print(f"Selected setting: {options[int(setting_selection)-1]}")
    new_data = input(f"Enter new data for {txt_files[int(selection)-1]} (leave blank to keep current data): ")
    
    if new_data:
        # we need to just replace the new data the selecteed one not the entire file so we can read the file and split it by lines then replace the selected line with the new data then write the file back
        # but we need to keep the format so 
        # settingName=settingValue
        with open(f'settings/{txt_files[int(selection)-1]}') as f:
            lines = f.read().splitlines()

        idx = int(setting_selection) - 1
        key = lines[idx].split("=", 1)[0]
        lines[idx] = f"{key}={new_data}"

        with open(f'settings/{txt_files[int(selection)-1]}', 'w') as f:
            f.write('\n'.join(lines))

        print(f"{txt_files[int(selection)-1]} has been updated, new data: {new_data}")
    else:
        print(f"{txt_files[int(selection)-1]} remains unchanged.")
# this will be used to import and export data from the settings
# so easily settings export will print all the current data for visualization in a nice readable format maybe tables or smt
# settings import will let the user replace all existing data so we need to read thorug all teh data and let the user replace it with new data or keep the old data if they want to
# to make all easier we read all txt in settings allowet the user to select which they wanna edit so
# settings export -> prints all current settings in a nice format
# settings import -> prompts the user to select which setting they wanna edit then prompts them to enter new data for that setting then saves the new data to the appropriate txt file
import os

from registry import register
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit import prompt

# Resolve settings directory relative to this file (cli/commands/settings.py -> cli/settings)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SETTINGS_DIR = os.path.join(BASE_DIR, 'settings')


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
    if not os.path.isdir(SETTINGS_DIR):
        print("Settings directory not found.")
        return

    for file in os.listdir(SETTINGS_DIR):
        if file.endswith('.txt'):
            path = os.path.join(SETTINGS_DIR, file)
            print(f"\n{file}:")
            try:
                with open(path, encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"Failed to read {file}: {e}")

def import_settings():
    print("Importing settings...")
    if not os.path.isdir(SETTINGS_DIR):
        print("Settings directory not found.")
        return

    txt_files = [file for file in os.listdir(SETTINGS_DIR) if file.endswith('.txt')]
    if not txt_files:
        print("No settings files found.")
        return
    
    print("Available settings files:")

    # Use filename as the dialog value so the return is the filename directly
    selection = radiolist_dialog(
        title="Select Settings File",
        text="Choose a settings file to edit:",
        values=[(file, file) for file in txt_files]
    ).run()

    if selection is None:
        print("No file selected.")
        return
    selected_file = selection
    print(f"Selected file: {selected_file}")

    # let the user decide which value to change also using radiolist_dialog
    # we can read the file and split it by lines then split each line by = to get the key and value then we can use the keys as options for the radiolist_dialog
    path = os.path.join(SETTINGS_DIR, selected_file)
    try:
        with open(path, encoding='utf-8') as f:
            lines = f.read().splitlines()
    except Exception as e:
        print(f"Failed to read {selected_file}: {e}")
        return

    # parse lines into key/value where possible and present user-friendly options
    kv = []
    for line in lines:
        if '=' in line:
            k, v = line.split('=', 1)
            kv.append((k.strip(), v.strip()))
        else:
            kv.append((line.strip(), ''))

    if not kv:
        print(f"No settings in {selected_file}.")
        return

    setting_selection = radiolist_dialog(
        title="Select Setting to Edit",
        text="Choose a setting to edit:",
        values=[(key, f"{key} = {value}") for key, value in kv]
    ).run()

    if setting_selection is None:
        print("No setting selected.")
        return

    selected_key = setting_selection
    # prompt for new value using prompt_toolkit to avoid mixing input() with radiolist_dialog
    new_data = prompt(f"Enter new value for '{selected_key}' (leave blank to keep current value): ")
    
    if new_data:
        # replace the corresponding key in the original lines preserving order
        updated = False
        for i, line in enumerate(lines):
            if line.split('=', 1)[0].strip() == selected_key:
                lines[i] = f"{selected_key}={new_data}"
                updated = True
                break

        if not updated:
            # append as new line
            lines.append(f"{selected_key}={new_data}")

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            print(f"{selected_file} has been updated, new value for {selected_key}: {new_data}")
        except Exception as e:
            print(f"Failed to write {selected_file}: {e}")
    else:
        print(f"{selected_file} remains unchanged.")
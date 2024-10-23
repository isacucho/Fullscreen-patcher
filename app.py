import os
import zipfile
import shutil
import plistlib
import platform
def clear():
    os_type = platform.system()
    if os_type == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    
clear()
# Prompt the user to drag and drop the IPA file
ipa_path = input("Please drag and drop your IPA file here and press Enter: ").strip()

# Check if the IPA file exists and is valid
if not os.path.isfile(ipa_path) or not ipa_path.endswith(".ipa"):
    print("The file you provided is either not an IPA file or doesn't exist.")
    exit()

# Ask if the user wants to keep the original IPA file
while True:
    keep_original = input("Do you want to keep the original IPA file? (y/n): ").strip().lower()
    if keep_original == 'y':
        keep_original = True
        break
    elif keep_original == 'n':
        keep_original = False
        break
    else:
        print("Invalid input, please enter 'y' for yes or 'n' for no.")

# Extract the file name and directory
ipa_name = os.path.basename(ipa_path).replace('.ipa', '')
extract_path = os.path.join(os.getcwd(), ipa_name)

# Step 1: Unzip the IPA file
with zipfile.ZipFile(ipa_path, 'r') as ipa_zip:
    ipa_zip.extractall(extract_path)

# Step 2: Locate the Info.plist file (inside Payload/APP_NAME.app/)
app_path = os.path.join(extract_path, 'Payload')
app_folder = [f for f in os.listdir(app_path) if f.endswith('.app')][0]  # Find the .app folder
plist_path = os.path.join(app_path, app_folder, 'Info.plist')

# Step 3: Modify the Info.plist
with open(plist_path, 'rb') as plist_file:
    plist_data = plistlib.load(plist_file)

# Add the key if it doesn't exist
if 'UISupportsTrueScreenSizeOnMac' not in plist_data:
    plist_data['UISupportsTrueScreenSizeOnMac'] = True

# Write back the modified Info.plist
with open(plist_path, 'wb') as plist_file:
    plistlib.dump(plist_data, plist_file)

# Step 4: Recompress the IPA
ipa_dir = os.path.dirname(ipa_path)
if keep_original:
    modified_ipa_path = os.path.join(ipa_dir, f"{ipa_name}_modified.ipa")
else:
    modified_ipa_path = ipa_path  # Overwrite the original IPA

shutil.make_archive(ipa_name, 'zip', extract_path)
os.rename(f"{ipa_name}.zip", modified_ipa_path)

# Clean up extracted files
shutil.rmtree(extract_path)

print(f"Modified IPA saved as {modified_ipa_path}")
print("The IPA has been successfully modified.")

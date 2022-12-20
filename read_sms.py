import configparser
import binascii

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Read the INI file
config.read('/var/spool/gammu/inbox/IN20221220_141717_00_Beeline^M_00.txt')

# Create an empty dictionary to store the data
data = {}

# Iterate over the sections in the INI file
for section in config.sections():
  # Create a dictionary to store the keys and values in the section
  section_data = {}
  
  # Iterate over the keys and values in the section
  for key, value in config[section].items():
    # Add the key and value to the section data
    section_data[key] = value
    
  # Add the section data to the main dictionary
  data[section] = section_data

# The data dictionary now contains the contents of the INI file
print(data)

sms = ''

for i in data.keys():
    for k in data[i].keys():
        if 'text' in k:
            print(data[i][k])
            # smsb = bytes.fromhex(data[i][k])
            sms =  bytes.fromhex(data[i][k]).decode('utf-32-le')


print(sms)
# msg = ''
# with open('/var/spool/gammu/inbox/IN20221220_141717_00_Beeline^M_00.txt', 'r') as f:
#     # Initialize a list to store the comments
#     comments = []
#     # Read the file line by line
#     for line in f:
#         # Check if the line starts with a semicolon
#         if line.startswith(';'):
#             # The line is a comment, so remove the leading semicolon and store it
#             comments.append(line[1:])
#     msg = ''.join(comments[3:])

# print(''.join(comments[3:]))
# Google Sheets Setup Instructions

## Step 1: Create Google Cloud Project & Enable API
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing one
3. Enable Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

## Step 2: Create Service Account
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in service account details
4. Skip optional steps (roles/users)
5. Click "Done"

## Step 3: Generate Key File
1. Click on your new service account email
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Choose "JSON" format
5. Download the file
6. Rename it to 'service_account.json' and place it in this directory

## Step 4: Create Google Sheet
1. Create a new Google Sheet named 'Dataintab'
2. Share it with the service account email (found in service_account.json)
3. Give "Editor" permissions

## Step 5: Ready to Run
The system will automatically connect to the 'Dataintab' sheet using service_account.json credentials.

## Security Note
The service_account.json file contains sensitive information. 
Never commit it to version control!

## Quick Test
Once you have your service_account.json file and 'Dataintab' sheet created and shared, 
run the program and it will automatically:
- Connect to the Massive.io WebSocket
- Stream live options data
- Write data to your 'Dataintab' Google Sheet
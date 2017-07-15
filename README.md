# General

Script dumps all your VK messages. It is so dummy, that's why you have to perform some preparations to use it.

1. Install python3 with 'requests' module. Or run `pip install -r requirements.txt`
2. Install mongo and provide connection settings to the line: client = MongoClient('localhost', 27017)
You can also run it with docker by : `docker run --name vk-dumper-mongo -d -p 27017:27017 -v /path/to/empty/directory/for/mongo:/tmp/mongo -e DATA_DIR=/tmp/mongo mongo`
3. Create Standalone application in VK and copy App-id from settings.
4. Obtain token manually via : `https://oauth.vk.com/authorize?client_id=<APP_ID>&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=messages&response_type=token&v=5.67&state=1`
You can see access token in your browser's address field after #.
5. Copy access token to the beginning of the script.
6. Run `python main.py`
7. Don't forget to export results with : 
- `mongoexport --db vk --collection messages  --out messages.json`
- `mongoexport --db vk --collection users  --out users.json`
- `mongoexport --db vk --collection docs  --out docs.json`
- `mongoexport --db vk --collection photos  --out photos.json`
- `mongoexport --db vk --collection links  --out links.json`

Enjoy.

# Setup

Change hardcoded parameter out=1 to out=0 if you wanna get incoming messages.

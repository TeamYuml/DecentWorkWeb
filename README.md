# DecentWorkWeb
Project for creating profiles, register work, get job.

## Prerequisites

```
python 3.6
node v8.10.0
npm v6.5.0
```

## Installation

### VirtualEnv
```
source env/bin/activate
pip install -r requirements/local.txt
```

### Install JavaScript packages:
```
npm install
```

### Build JavaScript
```
npm run build
```

### Watch
```
npm run watch
```

### Database
Copy `decentwork/settings/db.py.base` to `decentwork/settings/db.py` and
```
./manage.py migrate
```

### Google Sign In Web
To install Google sign in you have to find google_credentials.json in decentwork/fixtures and
enter your client id and secret key from Google OAuth client API and then do:
```
./manage.py loaddata decentwork/fixtures/google_credentials.json
```

### Google Sign In mobile token
To install google authentication from mobile with oauth2 token u have to copy google_token.base file,
rename it to google_token.py and then fill CLIENT_ID setting with your client id from google android application.

### Other fixtures
Installing other fixtures needed for application to work
```
./manage.py loaddata cities professions users notices uprofiles
```

## Translations
To compile translations write
```
./manage.py compilemessages
```
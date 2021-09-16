# Nebula-Control

## Installation
```console
cd flask
python3.9 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Init testing database
```python
from app import db
db.create_all()
from app.models import User
admin = User(username='aatalay', password='1234')
db.session.add(admin)
db.session.commit()
```

### Init share folder
```console
mkdir share
```

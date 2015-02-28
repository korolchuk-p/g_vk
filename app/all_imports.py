from datetime import timedelta, datetime
from app import app
from flask import Flask, Request

app.secret_key = 'e5d3-bc79-56f6-9f66-913c-c76b-2abb-8f19-46cd-1b35-d15c-be39-384c-bab4-5769-50d3-e170-ac7f-60db-64f5-22dd-fcb9-c80f-866f-8c92-7b32-6ab8-383c-3bea-633d-8662-c2b8'

app.permanent_session_lifetime = timedelta(days=2000)

app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 *1024

import app.views
import app.forms


#!/usr/bin/env python3.14
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, port=5556, host='0.0.0.0')
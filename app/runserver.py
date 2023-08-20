from webapp.app import app

if __name__ == "__main__":
    app.run_server("127.0.0.1", port=80, debug=False, threaded=True, processes=1)

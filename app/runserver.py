from webapp.app import server

if __name__ == "__main__":
    server.run("127.0.0.1", port=80, debug=False, threaded=True, processes=1)

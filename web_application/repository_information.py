#!/usr/bin/python

from flask import Flask

app = Flask(__name__)

app.run()


# def run_server():
#     app.run()
#
# server = Process(target=app.run)
# server.start()
# # ...
# server.terminate()
# server.join()


@app.route("/Reposiory-information")
def Repository_information():
    return "Hello World"
    # return render_template('note.html', note=Repository.retrieve_info_of_repository())


if __name__ == '__main__':
    app.run()

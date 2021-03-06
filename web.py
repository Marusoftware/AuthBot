from flask import Flask

app=Flask(__name__)

def recaptcha(key,token):
    import json
    import urllib.request
    import urllib.parse
    url = "https://www.google.com/recaptcha/api/siteverify"
    post_data = {
        "secret":key,
        "response" : str(token)
    }
    post_data = urllib.parse.urlencode(post_data).encode("utf-8")
    with urllib.request.urlopen(url, data=post_data) as res:
        ans = res.read().decode("utf-8")
        ans = json.loads(ans)
    return ans["success"]

@app.route("/")
def index():
    return "test"

if __name__ == "__main__":
    app.run()
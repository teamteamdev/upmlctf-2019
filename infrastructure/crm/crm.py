from flask import Flask, render_template, session, redirect, request, render_template_string
from flask_session import Session
from generate import generate


app = Flask(__name__)
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)


@app.route("/logout/")
def logout():
    session.pop("login", None)
    session.pop("logged_in", None)
    session.pop("2fa", None)
    session.pop("token_id", None)
    session.pop("token_value", None)
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def main():
    if "logged_in" in session:
        redirect("/crm/")
    
    if "2fa" in session:
        redirect("/2fa/")
    
    error = ""
    
    if request.method == "POST":
        login = request.form.get("login", "").lower().strip()
        password = request.form.get("password", "").strip()
        if login == "" or password == "" or (login == "andreev" and password != "Andreev992019"):
            error = "Enter login or password"
        else:
            generate(session, login)
            
            return redirect("/2fa/")
            
    return render_template("login.html", error=error)


@app.route("/2fa/", methods=["GET", "POST"])
def twofa():
    if "2fa" not in session:
        return redirect("/")
    
    error = ""
    if request.method == "POST":
        token = request.form.get("token", "")
        if token == str(session["token_value"]):
            session["logged_in"] = True
            return redirect("/crm/")
        error = "Incorrect code"
        generate(session)
    
    return render_template("2fa.html", num=session["token_id"], error=error)

    
@app.route("/crm/")
def crm():
    if "logged_in" not in session:
        return redirect("/")
    
    f = open("templates/crm.html", "r", encoding="utf8").read().replace(">>>FDATA<<<", request.args.get("fdata", ""))
        
    return render_template_string(f)


app.secret_key = "23674453268746527063863163296326327620952526326267538642737252"
    
if __name__ == "__main__":
    app.run()

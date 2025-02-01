# python imports
import traceback

# installed imports
from flask_login import login_user, current_user, logout_user, login_required
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)

# local imports
from app import db, csrf, logger
from app.modules.verification import confirm_token
from app.models import User
from app.modules.email_utility import (
    send_registration_email,
    send_forgot_password_email,
)

auth = Blueprint("auth", __name__)


# Login --------------------------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        return render_template(
            "signup.html",
            next=request.args.get("next") or None,
        )
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.email == email).first()
        if not user or not user.check_password(password):
            logger.info(f"USER NOT FOUND WITH EMAIL: {email}")
            flash("Invalid username or password.", "danger")
            return render_template(
                "signup.html",
                next=request.args.get("next") or None,
            )
        login_user(user)
        logger.info(f"LOGGED IN USER: #{user.id} ({user.display_name()})")
        next_page = request.args.get("next")
        text = "You are now signed in!"
        if next_page:
            flash(text, "success")
            return redirect(next_page)
        else:
            flash(text, "success")
            return redirect(url_for("main.index"))


# Sign up ------------------------------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        return render_template("signup.html", title="Register")
    else:
        firstname = request.form.get("firstname").strip()
        lastname = request.form.get("lastname").strip()
        email = request.form.get("email").strip()
        phone_no = request.form.get("phoneNumber").strip()
        dob = request.form.get("dob").strip()
        password = request.form.get("password").strip()

        check = User.query.filter(User.email == email).first()
        if check:
            logger.error(
                f"An account already exists with this email: {email}. Please use a different email to sign up"
            )
            flash(
                "An account already exists with this email. Please use a different email to sign up",
                "danger",
            )
            return render_template("signup.html", title="Register")

        # create user class instance / database record
        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone_no=phone_no,
            dob=dob,
            password=password,
        )
        new_user.insert()
        # send_registration_email(new_user)
        login_user(new_user)
        logger.info(f"User created successfully! - {new_user.display_name()}")
        flash(
            "Your account has been created successfully! Follow the link in your inbox to verify your email.",
            "success",
        )
        return redirect(url_for("auth.login"))


# Edit Profile -----------------------------------------------
@auth.post("/edit-profile")
@login_required
def edit_profile():
    firstname = request.form.get("firstname").strip()
    lastname = request.form.get("lastname").strip()
    email = request.form.get("email").strip()
    organization = request.form.get("organization").strip()

    try:
        current_user.email_verified = email == current_user.email
        current_user.firstname = firstname
        current_user.lastname = lastname
        current_user.email = email
        current_user.organization = organization
        current_user.update()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("main.index"))
    except:
        logger.error(traceback.format_exc())
        db.session.rollback()

        flash("Failed to update profile. Please try again later.", "danger")
        return redirect(url_for("main.index"))


# Confirm email -----------------------------------
@auth.route("/confirm/<token>")
def confirm_email(token):
    logout_user()
    try:
        email = confirm_token(token)
        if email:
            user = User.query.filter(User.email == email).one()
            if user:
                user.email_verified = True
                user.update()
                return render_template("verify-email.html", success=True)
        else:
            return render_template("verify-email.html", success=False)
    except:
        logger.error(traceback.format_exc())
        return render_template("verify-email.html", success=False)


# Send verification email --------------------------------
@auth.get("/send-verification-email")
@login_required
def verification_email():
    try:
        if send_registration_email(current_user):
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 500
    except:
        logger.error(traceback.format_exc())
        return jsonify({"success": False}), 500


# Change password -------------------------------------
@auth.route("/change-password/<token>")
def change_password(token):
    email = confirm_token(token)
    logout_user()
    if email:
        return render_template(
            "update_password.html", email=email, title="Change password"
        )
    else:
        return render_template(
            "password-change.html", success=False, title="Change password"
        )


# Forgot password -----------------------------------------
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        return render_template("recover.html", title="Account Recovery")
    email = request.form.get("email")
    user = User.query.filter(User.email == email).one_or_none()
    if user:
        try:
            send = send_forgot_password_email(user)
            if send:
                flash("Follow the link we sent to reset your password.", "success")
                return render_template("login.html")
            flash(
                "There was an error sending the email please try again later.", "danger"
            )
            return render_template("login.html")
        except:
            flash(
                "There was an error sending the email, please try again later.",
                "danger",
            )
            return render_template("auth.html")
    flash("Your account was not found. Please proceed to create an account.", "danger")
    return render_template("login.html")


# Confirm new password ------------------------------------
@auth.post("/confirm-new-password")
@csrf.exempt
def confirm_new_password():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.email == email).one_or_none()
        if user:
            user.password_hash = user.get_password_hash(password)
            user.update()

            return render_template("password-change.html", success=True)
        else:
            return render_template("password-change.html", success=False)
    except:
        logger.error(traceback.format_exc())
        return render_template("password-change.html", success=False)


# Logout ----------------------------------
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app import db
from app.models import URL
from app.services import create_short_url, register_click

main = Blueprint("main", __name__)



@main.route("/", methods=["GET", "POST"])
def index():
    short_url = None

    original_url_value = ""
    custom_code_value = ""

    if request.method == "POST":
        original_url_value = request.form.get(
            "original_url", ""
        )

        custom_code_value = request.form.get(
            "custom_code", ""
        )

        try:
            url = create_short_url(
                original_url_value,
                custom_code_value
            )

            short_url = request.host_url.rstrip("/") + "/" + url.short_code

            flash(
                "Link został pomyślnie skrócony!",
                "success"
            )

            original_url_value = ""
            custom_code_value = ""

        except ValueError as error:
            flash(str(error), "danger")

    return render_template(
        "index.html",
        short_url=short_url,
        original_url_value=original_url_value,
        custom_code_value=custom_code_value,
    )



@main.route("/dashboard")
def dashboard():
    urls = URL.query.order_by(URL.created_at.desc()).all()

    total_links = len(urls)
    total_clicks = sum(url.clicks for url in urls)

    average_clicks = (
        round(total_clicks / total_links, 1)
        if total_links > 0
        else 0
    )

    return render_template(
        "dashboard.html",
        urls=urls,
        total_links=total_links,
        total_clicks=total_clicks,
        average_clicks=average_clicks,
    )


@main.route("/details/<int:url_id>")
def url_details(url_id):
    url = db.session.get(URL, url_id)

    if url is None:
        abort(404)

    short_url = url_for(
        "main.redirect_to_url",
        short_code=url.short_code,
        _external=True,
    )

    return render_template(
        "url_details.html",
        url=url,
        short_url=short_url,
    )


@main.route("/<short_code>")
def redirect_to_url(short_code):
    url = register_click(short_code)

    if url is None:
        abort(404)

    return redirect(url.original_url)


@main.route("/delete/<int:url_id>", methods=["POST"])
def delete_url(url_id):
    url = db.session.get(URL, url_id)

    if url is None:
        abort(404)

    db.session.delete(url)
    db.session.commit()

    flash("Link został usunięty.", "success")

    return redirect(url_for("main.dashboard"))


@main.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

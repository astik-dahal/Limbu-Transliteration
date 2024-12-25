#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for
from transliteration import (
    transliterate_limbu_to_roman,
    transliterate_limbu_to_devanagari,
    transliterate_devanagari_to_limbu,
    transliterate_roman_to_limbu,
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    We handle a single page that can do multiple transliteration modes.
    The user picks "limbu_to_roman", "limbu_to_devanagari", etc.,
    we call the appropriate function, and pass output to the template.
    """
    user_input = ""
    translit_mode = "limbu_to_roman"  # default
    output_text = ""
    debug_logs = []

    if request.method == "POST":
        # Which transliteration mode?
        translit_mode = request.form.get("translit_mode", "limbu_to_roman")
        user_input = request.form.get("user_input", "")

        if translit_mode == "limbu_to_roman":
            output_text = transliterate_limbu_to_roman(user_input, debug_log=debug_logs)
        elif translit_mode == "limbu_to_devanagari":
            output_text = transliterate_limbu_to_devanagari(user_input)
        elif translit_mode == "devanagari_to_limbu":
            output_text = transliterate_devanagari_to_limbu(user_input)
        elif translit_mode == "roman_to_limbu":
            output_text = transliterate_roman_to_limbu(user_input)
        else:
            debug_logs.append("Unknown transliteration mode.")

    return render_template(
        "index.html",
        translit_mode=translit_mode,
        user_input=user_input,
        output_text=output_text,
        debug_logs="\n".join(debug_logs),
    )

if __name__ == "__main__":
    app.run(debug=True)

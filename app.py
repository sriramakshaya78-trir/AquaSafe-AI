from flask import Flask, render_template, request, jsonify

import math
import os
import sys
import json
import sqlite3
import traceback
import threading
import webbrowser
from datetime import datetime, timezone

from aquasafe_logic import (
    check_parameters,
    determine_risk,
    calculate_safety_score,
    generate_treatment_recommendations,
    compare_water,
    compare_risk_levels
)


# ============================================================
# PATH SETUP
# ============================================================

if getattr(sys, "frozen", False):
    # When running as the packaged EXE
    PROJECT_ROOT = os.path.dirname(sys.executable)
    BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
else:
    # When running app.py directly
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BACKEND_DIR)


FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)


# ============================================================
# ERROR LOGGING
# ============================================================

LOG_PATH = os.path.join(PROJECT_ROOT, "AquaSafe_error.log")


def log_error():
    """
    Save the complete error traceback beside the EXE.
    This is useful if another Windows PC has a problem.
    """
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write("\n")
            log_file.write("=" * 80 + "\n")
            log_file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            log_file.write("\n")
            log_file.write(traceback.format_exc())
            log_file.write("\n")
            log_file.write("=" * 80 + "\n")
    except Exception:
        pass


# ============================================================
# SQLITE DATABASE
# ============================================================

PRIMARY_DATABASE_DIR = os.path.join(
    BACKEND_DIR,
    "database"
)

PRIMARY_DATABASE_PATH = os.path.join(
    PRIMARY_DATABASE_DIR,
    "aquasafe.db"
)


# Backup location for Windows PCs where the project folder
# cannot safely write to its own database folder.
LOCAL_APP_DATA = os.getenv(
    "LOCALAPPDATA",
    os.path.expanduser("~")
)

FALLBACK_DATABASE_DIR = os.path.join(
    LOCAL_APP_DATA,
    "AquaSafe AI"
)

FALLBACK_DATABASE_PATH = os.path.join(
    FALLBACK_DATABASE_DIR,
    "aquasafe.db"
)


DATABASE_DIR = PRIMARY_DATABASE_DIR
DATABASE_PATH = PRIMARY_DATABASE_PATH


def test_database_write(path):
    """
    Check whether SQLite can safely create/write in this location.
    The temporary table is rolled back, so it does not remain.
    """
    connection = None

    try:
        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        connection = sqlite3.connect(
            path,
            timeout=10
        )

        connection.execute("BEGIN")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS __aquasafe_write_test (
                id INTEGER
            )
        """)

        connection.execute(
            "DROP TABLE IF EXISTS __aquasafe_write_test"
        )

        connection.rollback()

        return True

    except Exception:
        if connection:
            try:
                connection.rollback()
            except Exception:
                pass

        return False

    finally:
        if connection:
            try:
                connection.close()
            except Exception:
                pass


def select_database_location():
    """
    Prefer the database inside the project folder.

    If Windows does not allow writing there, automatically
    use the user's LocalAppData folder.
    """
    global DATABASE_DIR
    global DATABASE_PATH

    try:
        os.makedirs(
            PRIMARY_DATABASE_DIR,
            exist_ok=True
        )
    except Exception:
        pass

    if test_database_write(PRIMARY_DATABASE_PATH):
        DATABASE_DIR = PRIMARY_DATABASE_DIR
        DATABASE_PATH = PRIMARY_DATABASE_PATH
        return

    # Fallback to a guaranteed user-writable location
    os.makedirs(
        FALLBACK_DATABASE_DIR,
        exist_ok=True
    )

    DATABASE_DIR = FALLBACK_DATABASE_DIR
    DATABASE_PATH = FALLBACK_DATABASE_PATH


select_database_location()


def get_db_connection():
    """
    Open SQLite database safely.
    """
    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the database table if it does not already exist.
    """
    connection = None

    try:
        connection = get_db_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS water_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                water TEXT NOT NULL,
                risk TEXT NOT NULL,
                safety_score INTEGER NOT NULL,
                problem_count INTEGER NOT NULL,
                problems TEXT NOT NULL,
                recommendations TEXT NOT NULL
            )
        """)

        connection.commit()

    except Exception:
        log_error()
        raise

    finally:
        if connection:
            try:
                connection.close()
            except Exception:
                pass


try:
    initialize_database()
except Exception:
    log_error()

    # Final emergency fallback
    try:
        DATABASE_DIR = FALLBACK_DATABASE_DIR
        DATABASE_PATH = FALLBACK_DATABASE_PATH

        os.makedirs(
            DATABASE_DIR,
            exist_ok=True
        )

        initialize_database()

    except Exception:
        log_error()


# ============================================================
# WATER PARAMETERS
# ============================================================

PARAMETERS = [
    "pH",
    "Hardness",
    "Solids",
    "Chloramines",
    "Sulfate",
    "Conductivity",
    "Organic Carbon",
    "Trihalomethanes",
    "Turbidity"
]


# ============================================================
# PAGE ROUTES
# ============================================================

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        log_error()
        raise


@app.route("/analyze")
def analyze_page():
    try:
        return render_template("analysis.html")
    except Exception:
        log_error()
        raise


@app.route("/result")
def result_page():
    try:
        return render_template("result.html")
    except Exception:
        log_error()
        raise


@app.route("/about")
def about_page():
    try:
        return render_template("about.html")
    except Exception:
        log_error()
        raise


@app.route("/history")
def history_page():
    try:
        return render_template("history.html")
    except Exception:
        log_error()
        raise


# ============================================================
# VALIDATION
# ============================================================

def validate_water_data(data):
    """
    Validate and convert the 9 water parameters into numbers.
    """

    if not data:
        return None, "No water data was received."

    water = {}

    for parameter in PARAMETERS:

        if parameter not in data:
            return None, f"Missing parameter: {parameter}"

        value = data[parameter]

        if value is None or str(value).strip() == "":
            return None, f"{parameter} cannot be empty."

        try:
            number = float(value)

        except (ValueError, TypeError):
            return None, f"{parameter} must be a number."

        if not math.isfinite(number):
            return None, f"{parameter} must be a valid number."

        if number < 0:
            return None, f"{parameter} cannot be negative."

        water[parameter] = number

    return water, None


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health", methods=["GET"])
def health_check():

    connection = None

    try:

        connection = get_db_connection()

        connection.execute(
            "SELECT 1"
        ).fetchone()

        return jsonify({
            "status": "online",
            "app": "AquaSafe AI",
            "database": "connected"
        }), 200

    except Exception as e:

        log_error()

        return jsonify({
            "status": "online",
            "app": "AquaSafe AI",
            "database": "disconnected",
            "error": str(e)
        }), 500

    finally:

        if connection:
            try:
                connection.close()
            except Exception:
                pass


# ============================================================
# ANALYZE WATER
# ============================================================

@app.route("/api/analyze", methods=["POST"])
def analyze_water():

    connection = None

    try:

        data = request.get_json(
            silent=True
        )

        water, validation_error = validate_water_data(
            data
        )

        if validation_error:

            return jsonify({
                "success": False,
                "error": validation_error
            }), 400


        # ----------------------------------------------------
        # ORIGINAL AQUASAFE PYTHON LOGIC
        # ----------------------------------------------------

        problems = check_parameters(
            water
        )

        risk = determine_risk(
            problems
        )

        safety_score = calculate_safety_score(
            problems
        )

        recommendations = generate_treatment_recommendations(
            problems
        )


        # ----------------------------------------------------
        # SAVE RESULT TO SQLITE
        # ----------------------------------------------------

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        risk_data = {
            "level": risk["level"],
            "symbol": risk["symbol"],
            "title": risk["title"]
        }


        connection = get_db_connection()

        cursor = connection.execute(
            """
            INSERT INTO water_tests (
                created_at,
                water,
                risk,
                safety_score,
                problem_count,
                problems,
                recommendations
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                json.dumps(water),
                json.dumps(risk_data),
                safety_score,
                len(problems),
                json.dumps(problems),
                json.dumps(recommendations)
            )
        )


        connection.commit()

        test_id = cursor.lastrowid


        # ----------------------------------------------------
        # RESPONSE TO FRONTEND
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "test_id": str(test_id),

            "water": water,

            "risk": risk,

            "safety_score": safety_score,

            "problems": problems,

            "recommendations": recommendations

        }), 200


    except sqlite3.Error as e:

        log_error()

        return jsonify({
            "success": False,
            "error": "Water analysis completed, but the result could not be saved."
        }), 500


    except Exception as e:

        log_error()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


    finally:

        if connection:

            try:
                connection.close()

            except Exception:
                pass


# ============================================================
# GET WATER TEST HISTORY
# ============================================================

@app.route("/api/history", methods=["GET"])
def get_history():

    connection = None

    try:

        connection = get_db_connection()

        records = connection.execute(
            """
            SELECT
                id,
                created_at,
                water,
                risk,
                safety_score,
                problem_count
            FROM water_tests
            ORDER BY id DESC
            """
        ).fetchall()


        history = []

        for record in records:

            history.append({

                "test_id": str(
                    record["id"]
                ),

                "created_at":
                    record["created_at"],

                "water":
                    json.loads(
                        record["water"]
                    ),

                "risk":
                    json.loads(
                        record["risk"]
                    ),

                "safety_score":
                    record["safety_score"],

                "problem_count":
                    record["problem_count"]

            })


        return jsonify({

            "success": True,

            "count":
                len(history),

            "history":
                history

        }), 200


    except sqlite3.Error:

        log_error()

        return jsonify({

            "success": False,

            "error":
                "Could not load water test history."

        }), 500


    except Exception as e:

        log_error()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


    finally:

        if connection:

            try:
                connection.close()

            except Exception:
                pass


# ============================================================
# GET ONE WATER TEST
# ============================================================

@app.route(
    "/api/history/<test_id>",
    methods=["GET"]
)
def get_single_test(test_id):

    connection = None

    try:

        try:

            numeric_id = int(
                test_id
            )

        except (ValueError, TypeError):

            return jsonify({

                "success": False,

                "error":
                    "Invalid test ID."

            }), 400


        connection = get_db_connection()

        record = connection.execute(
            """
            SELECT *
            FROM water_tests
            WHERE id = ?
            """,
            (numeric_id,)
        ).fetchone()


        if record is None:

            return jsonify({

                "success": False,

                "error":
                    "Water test not found."

            }), 404


        result = {

            "test_id":
                str(record["id"]),

            "created_at":
                record["created_at"],

            "water":
                json.loads(
                    record["water"]
                ),

            "risk":
                json.loads(
                    record["risk"]
                ),

            "safety_score":
                record["safety_score"],

            "problem_count":
                record["problem_count"],

            "problems":
                json.loads(
                    record["problems"]
                ),

            "recommendations":
                json.loads(
                    record["recommendations"]
                )

        }


        return jsonify({

            "success": True,

            "result":
                result

        }), 200


    except sqlite3.Error:

        log_error()

        return jsonify({

            "success": False,

            "error":
                "Could not retrieve the water test."

        }), 500


    except Exception as e:

        log_error()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


    finally:

        if connection:

            try:
                connection.close()

            except Exception:
                pass


# ============================================================
# DELETE ONE WATER TEST
# ============================================================

@app.route(
    "/api/history/<test_id>",
    methods=["DELETE"]
)
def delete_test(test_id):

    connection = None

    try:

        try:

            numeric_id = int(
                test_id
            )

        except (ValueError, TypeError):

            return jsonify({

                "success": False,

                "error":
                    "Invalid test ID."

            }), 400


        connection = get_db_connection()

        cursor = connection.execute(
            """
            DELETE FROM water_tests
            WHERE id = ?
            """,
            (numeric_id,)
        )


        connection.commit()

        deleted_count = cursor.rowcount


        if deleted_count == 0:

            return jsonify({

                "success": False,

                "error":
                    "Water test not found."

            }), 404


        return jsonify({

            "success": True,

            "message":
                "Water test deleted successfully.",

            "test_id":
                test_id

        }), 200


    except sqlite3.Error:

        log_error()

        return jsonify({

            "success": False,

            "error":
                "Could not delete the water test."

        }), 500


    except Exception as e:

        log_error()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


    finally:

        if connection:

            try:
                connection.close()

            except Exception:
                pass


# ============================================================
# COMPARE WATER
# ============================================================

@app.route(
    "/api/compare",
    methods=["POST"]
)
def compare_water_api():

    try:

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No comparison data was received."

            }), 400


        before_data = data.get(
            "before"
        )

        after_data = data.get(
            "after"
        )


        # ----------------------------------------------------
        # VALIDATE BEFORE WATER
        # ----------------------------------------------------

        before_water, before_error = validate_water_data(
            before_data
        )


        if before_error:

            return jsonify({

                "success": False,

                "error":
                    f"Before water: {before_error}"

            }), 400


        # ----------------------------------------------------
        # VALIDATE AFTER WATER
        # ----------------------------------------------------

        after_water, after_error = validate_water_data(
            after_data
        )


        if after_error:

            return jsonify({

                "success": False,

                "error":
                    f"After water: {after_error}"

            }), 400


        # ----------------------------------------------------
        # ANALYZE BEFORE
        # ----------------------------------------------------

        before_problems = check_parameters(
            before_water
        )

        before_risk = determine_risk(
            before_problems
        )

        before_score = calculate_safety_score(
            before_problems
        )


        # ----------------------------------------------------
        # ANALYZE AFTER
        # ----------------------------------------------------

        after_problems = check_parameters(
            after_water
        )

        after_risk = determine_risk(
            after_problems
        )

        after_score = calculate_safety_score(
            after_problems
        )


        # ----------------------------------------------------
        # PARAMETER COMPARISON
        # ----------------------------------------------------

        parameter_comparison = compare_water(
            before_water,
            after_water
        )


        # ----------------------------------------------------
        # RISK COMPARISON
        # ----------------------------------------------------

        try:

            risk_comparison = compare_risk_levels(
                before_risk,
                after_risk,
                before_score,
                after_score
            )

        except TypeError:

            risk_comparison = compare_risk_levels(
                before_water,
                after_water
            )


        # ----------------------------------------------------
        # RETURN COMPARISON
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "before": {

                "water":
                    before_water,

                "risk":
                    before_risk,

                "safety_score":
                    before_score

            },

            "after": {

                "water":
                    after_water,

                "risk":
                    after_risk,

                "safety_score":
                    after_score

            },

            "parameter_comparison":
                parameter_comparison,

            "risk_comparison":
                risk_comparison

        }), 200


    except Exception as e:

        log_error()

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# GLOBAL ERROR HANDLER
# ============================================================

@app.errorhandler(Exception)
def handle_global_error(error):

    log_error()

    return jsonify({

        "success": False,

        "error":
            str(error)

    }), 500


# ============================================================
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    def open_browser():

        try:

            webbrowser.open(
                "http://127.0.0.1:5000"
            )

        except Exception:

            log_error()


    # Give Flask a moment to start
    threading.Timer(
        1.5,
        open_browser
    ).start()


    try:

        app.run(

            host="127.0.0.1",

            port=5000,

            debug=False,

            use_reloader=False

        )

    except Exception:

        log_error()

        raise
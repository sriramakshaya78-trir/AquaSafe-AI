# ==========================================================
#                    AQUASAFE AI
#        Smart Water Safety & Treatment Advisor
# ==========================================================
#
# Features:
# 1. Check water-quality parameters
# 2. Identify problematic parameters
# 3. Determine risk level
# 4. Traffic-light system
# 5. Treatment recommendations
# 6. Safety score
# 7. Re-test feature
# 8. Before and After comparison
#
# ==========================================================


# ----------------------------------------------------------
# 1. REFERENCE LIMITS
# ----------------------------------------------------------

LIMITS = {

    "pH": {
        "min": 6.5,
        "max": 8.5
    },

    "Hardness": {
        "max": 300
    },

    "Solids": {
        "max": 1000
    },

    "Chloramines": {
        "max": 4
    },

    "Sulfate": {
        "max": 250
    },

    "Conductivity": {
        "max": 1000
    },

    "Organic Carbon": {
        "max": 5
    },

    "Trihalomethanes": {
        "max": 100
    },

    "Turbidity": {
        "max": 5
    }
}


# ==========================================================
# 2. CHECK INDIVIDUAL PARAMETERS
# ==========================================================

def check_parameters(water):

    problems = []

    # ------------------------------------------------------
    # pH
    # ------------------------------------------------------

    if water["pH"] < LIMITS["pH"]["min"]:

        problems.append({

            "parameter": "pH",
            "severity": "High",
            "issue": "pH is too low",

            "treatment":
            "Appropriate pH adjustment and water treatment"

        })

    elif water["pH"] > LIMITS["pH"]["max"]:

        problems.append({

            "parameter": "pH",
            "severity": "High",
            "issue": "pH is too high",

            "treatment":
            "Appropriate pH adjustment and water treatment"

        })

    # ------------------------------------------------------
    # Hardness
    # ------------------------------------------------------

    if water["Hardness"] > LIMITS["Hardness"]["max"]:

        problems.append({

            "parameter": "Hardness",
            "severity": "Moderate",
            "issue": "Hardness is high",

            "treatment":
            "Water softening treatment may be required"

        })

    # ------------------------------------------------------
    # Solids
    # ------------------------------------------------------

    if water["Solids"] > LIMITS["Solids"]["max"]:

        problems.append({

            "parameter": "Solids",
            "severity": "High",
            "issue": "Total dissolved solids are high",

            "treatment":
            "Identify dissolved constituents and use appropriate treatment"

        })

    # ------------------------------------------------------
    # Chloramines
    # ------------------------------------------------------

    if water["Chloramines"] > LIMITS["Chloramines"]["max"]:

        problems.append({

            "parameter": "Chloramines",
            "severity": "Moderate",
            "issue": "Chloramine level is elevated",

            "treatment":
            "Review and adjust the water treatment or disinfection process"

        })

    # ------------------------------------------------------
    # Sulfate
    # ------------------------------------------------------

    if water["Sulfate"] > LIMITS["Sulfate"]["max"]:

        problems.append({

            "parameter": "Sulfate",
            "severity": "High",
            "issue": "Sulfate level is high",

            "treatment":
            "Use appropriate sulfate-specific treatment"

        })

    # ------------------------------------------------------
    # Conductivity
    # ------------------------------------------------------

    if water["Conductivity"] > LIMITS["Conductivity"]["max"]:

        problems.append({

            "parameter": "Conductivity",
            "severity": "Moderate",
            "issue": "Conductivity is high",

            "treatment":
            "Investigate dissolved ions and select appropriate treatment"

        })

    # ------------------------------------------------------
    # Organic Carbon
    # ------------------------------------------------------

    if water["Organic Carbon"] > LIMITS["Organic Carbon"]["max"]:

        problems.append({

            "parameter": "Organic Carbon",
            "severity": "Moderate",
            "issue": "Organic carbon level is elevated",

            "treatment":
            "Investigate the contamination source and use appropriate treatment"

        })

    # ------------------------------------------------------
    # Trihalomethanes
    # ------------------------------------------------------

    if water["Trihalomethanes"] > LIMITS["Trihalomethanes"]["max"]:

        problems.append({

            "parameter": "Trihalomethanes",
            "severity": "High",
            "issue": "Trihalomethane level is elevated",

            "treatment":
            "Investigate and control disinfection by-product formation"

        })

    # ------------------------------------------------------
    # Turbidity
    # ------------------------------------------------------

    if water["Turbidity"] > LIMITS["Turbidity"]["max"]:

        problems.append({

            "parameter": "Turbidity",
            "severity": "High",
            "issue": "Turbidity is high",

            "treatment":
            "Use filtration or clarification"

        })

    return problems


# ==========================================================
# 3. DETERMINE OVERALL RISK
# ==========================================================

def determine_risk(problems):

    # No problems

    if len(problems) == 0:

        return {

            "level": "GREEN",
            "symbol": "🟢",
            "title": "LOW RISK"

        }

    high_risk_count = 0
    moderate_count = 0

    # Count problem severity

    for problem in problems:

        if problem["severity"] == "High":

            high_risk_count += 1

        elif problem["severity"] == "Moderate":

            moderate_count += 1


    # ------------------------------------------------------
    # RED - HIGH RISK
    # ------------------------------------------------------

    if high_risk_count >= 1:

        return {

            "level": "RED",
            "symbol": "🔴",
            "title": "HIGH RISK"

        }


    # ------------------------------------------------------
    # YELLOW - CAUTION
    # ------------------------------------------------------

    elif moderate_count >= 1:

        return {

            "level": "YELLOW",
            "symbol": "🟡",
            "title": "CAUTION"

        }


    # ------------------------------------------------------
    # GREEN - LOW RISK
    # ------------------------------------------------------

    else:

        return {

            "level": "GREEN",
            "symbol": "🟢",
            "title": "LOW RISK"

        }


# ==========================================================
# 4. CALCULATE SAFETY SCORE
# ==========================================================

def calculate_safety_score(problems):

    score = 100

    for problem in problems:

        if problem["severity"] == "High":

            score -= 20

        elif problem["severity"] == "Moderate":

            score -= 10


    # Prevent negative score

    if score < 0:

        score = 0


    return score


# ==========================================================
# 5. DISPLAY RESULT
# ==========================================================

def display_result(water):

    problems = check_parameters(water)

    risk = determine_risk(problems)

    safety_score = calculate_safety_score(problems)


    print("\n")
    print("=" * 60)

    print("                    AQUASAFE AI")

    print("             WATER SAFETY ASSESSMENT")

    print("=" * 60)


    # ------------------------------------------------------
    # GREEN
    # ------------------------------------------------------

    if risk["level"] == "GREEN":

        print("\n🟢 GREEN - LOW RISK")

        print("\nNo major parameter concerns were detected.")

        print(
            "The sample appears acceptable based on the"
        )

        print(
            "available measurements and configured rules."
        )


    # ------------------------------------------------------
    # YELLOW
    # ------------------------------------------------------

    elif risk["level"] == "YELLOW":

        print("\n🟡 YELLOW - CAUTION")

        print("\nSome water-quality parameters require attention.")

        print(
            "Appropriate corrective treatment and re-testing"
        )

        print(
            "may be needed before regular consumption."
        )


    # ------------------------------------------------------
    # RED
    # ------------------------------------------------------

    else:

        print("\n🔴 RED - HIGH RISK")

        print("\nSignificant water-quality concerns were detected.")

        print(
            "Do not consume the water directly until the"
        )

        print(
            "identified issues are addressed and the water"
        )

        print(
            "is re-tested."
        )


    # ------------------------------------------------------
    # SAFETY SCORE
    # ------------------------------------------------------

    print("\n" + "-" * 60)

    print("SAFETY SCORE")

    print("-" * 60)

    print("\nScore:", safety_score, "/ 100")


    # ------------------------------------------------------
    # SHOW PROBLEMS
    # ------------------------------------------------------

    if problems:

        print("\n" + "=" * 60)

        print("DETECTED PROBLEMS")

        print("=" * 60)


        for number, problem in enumerate(problems, start=1):

            print("\nProblem", number)

            print("Parameter :", problem["parameter"])

            print("Issue     :", problem["issue"])

            print("Severity  :", problem["severity"])

            print("Treatment :", problem["treatment"])


        # --------------------------------------------------
        # NEXT STEP
        # --------------------------------------------------

        print("\n" + "=" * 60)

        print("NEXT STEP")

        print("=" * 60)

        print("\n1. Address the identified water-quality problems.")

        print("2. Apply appropriate treatment.")

        print("3. Re-test the water after treatment.")

        print(
            "4. Do not assume that improvement in these"
        )

        print(
            "parameters guarantees complete drinking-water safety."
        )


    else:

        print("\nNo treatment recommendation is required")

        print(
            "based on the configured parameter rules."
        )


    print("\n" + "=" * 60)

    # Return results for re-test comparison

    return problems, risk, safety_score


# ==========================================================
# 6. GET PARAMETER STATUS
# ==========================================================

def get_parameter_status(parameter, value):

    # pH has minimum and maximum range

    if parameter == "pH":

        if (
            LIMITS["pH"]["min"]
            <= value
            <= LIMITS["pH"]["max"]
        ):

            return "NORMAL"

        else:

            return "ABNORMAL"


    # Other parameters only have maximum limits

    else:

        if value <= LIMITS[parameter]["max"]:

            return "NORMAL"

        else:

            return "ABNORMAL"


# ==========================================================
# 7. COMPARE BEFORE AND AFTER WATER
# ==========================================================

def compare_water(before_water, after_water):

    parameters = [

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


    print("\n")

    print("=" * 75)

    print("          BEFORE AND AFTER WATER COMPARISON")

    print("=" * 75)


    print(

        f"\n{'Parameter':<20}"

        f"{'Before':<15}"

        f"{'After':<15}"

        f"{'Result'}"

    )


    print("-" * 75)


    improved_count = 0

    worsened_count = 0

    unchanged_count = 0


    # ------------------------------------------------------
    # CHECK EACH PARAMETER
    # ------------------------------------------------------

    for parameter in parameters:


        before_value = before_water[parameter]

        after_value = after_water[parameter]


        before_status = get_parameter_status(

            parameter,

            before_value

        )


        after_status = get_parameter_status(

            parameter,

            after_value

        )


        # --------------------------------------------------
        # ABNORMAL -> NORMAL
        # --------------------------------------------------

        if (

            before_status == "ABNORMAL"

            and

            after_status == "NORMAL"

        ):

            result = "IMPROVED"

            improved_count += 1


        # --------------------------------------------------
        # NORMAL -> ABNORMAL
        # --------------------------------------------------

        elif (

            before_status == "NORMAL"

            and

            after_status == "ABNORMAL"

        ):

            result = "WORSENED"

            worsened_count += 1


        # --------------------------------------------------
        # BOTH ABNORMAL
        # --------------------------------------------------

        elif (

            before_status == "ABNORMAL"

            and

            after_status == "ABNORMAL"

        ):


            # pH comparison

            if parameter == "pH":


                safe_min = LIMITS["pH"]["min"]

                safe_max = LIMITS["pH"]["max"]


                # Distance from safe range

                if before_value < safe_min:

                    before_distance = safe_min - before_value

                else:

                    before_distance = before_value - safe_max


                if after_value < safe_min:

                    after_distance = safe_min - after_value

                else:

                    after_distance = after_value - safe_max


                if after_distance < before_distance:

                    result = "PARTIALLY IMPROVED"

                    improved_count += 1


                elif after_distance > before_distance:

                    result = "WORSENED"

                    worsened_count += 1


                else:

                    result = "NO CHANGE"

                    unchanged_count += 1


            # Other parameters

            else:


                if after_value < before_value:

                    result = "PARTIALLY IMPROVED"

                    improved_count += 1


                elif after_value > before_value:

                    result = "WORSENED"

                    worsened_count += 1


                else:

                    result = "NO CHANGE"

                    unchanged_count += 1


        # --------------------------------------------------
        # BOTH NORMAL
        # --------------------------------------------------

        else:

            result = "NORMAL"

            unchanged_count += 1


        print(

            f"{parameter:<20}"

            f"{before_value:<15.2f}"

            f"{after_value:<15.2f}"

            f"{result}"

        )


    print("-" * 75)


    return (

        improved_count,

        worsened_count,

        unchanged_count

    )


# ==========================================================
# 8. COMPARE RISK LEVELS
# ==========================================================

def compare_risk_levels(before_water, after_water):


    # ------------------------------------------------------
    # BEFORE ANALYSIS
    # ------------------------------------------------------

    before_problems = check_parameters(before_water)

    before_risk = determine_risk(before_problems)

    before_score = calculate_safety_score(before_problems)


    # ------------------------------------------------------
    # AFTER ANALYSIS
    # ------------------------------------------------------

    after_problems = check_parameters(after_water)

    after_risk = determine_risk(after_problems)

    after_score = calculate_safety_score(after_problems)


    # ------------------------------------------------------
    # DISPLAY COMPARISON
    # ------------------------------------------------------

    print("\n")

    print("=" * 60)

    print("             OVERALL RISK COMPARISON")

    print("=" * 60)


    # BEFORE

    print("\nBEFORE TREATMENT")

    print(

        before_risk["symbol"],

        before_risk["level"],

        "-",

        before_risk["title"]

    )

    print("Safety Score:", before_score, "/ 100")


    # AFTER

    print("\nAFTER TREATMENT")

    print(

        after_risk["symbol"],

        after_risk["level"],

        "-",

        after_risk["title"]

    )

    print("Safety Score:", after_score, "/ 100")


    print("\n" + "-" * 60)


    # ------------------------------------------------------
    # CHECK IMPROVEMENT
    # ------------------------------------------------------

    score_difference = after_score - before_score


    if score_difference > 0:


        print("\nOVERALL RESULT: WATER QUALITY IMPROVED")

        print(

            "Safety score improved by:",

            score_difference,

            "points."

        )


    elif score_difference < 0:


        print("\nOVERALL RESULT: WATER QUALITY WORSENED")

        print(

            "Safety score decreased by:",

            abs(score_difference),

            "points."

        )


    else:


        print("\nOVERALL RESULT: NO MAJOR CHANGE")

        print(

            "The safety score remains the same."

        )


    # ------------------------------------------------------
    # FINAL MESSAGE
    # ------------------------------------------------------

    print("\n" + "=" * 60)

    print("IMPORTANT NOTE")

    print("=" * 60)


    print(

        "\nImprovement in the configured parameters does not"

    )

    print(

        "guarantee complete drinking-water safety."

    )

    print(

        "Appropriate testing may still be required before"

    )

    print(

        "confirming that the water is safe for drinking."

    )


# ==========================================================
# 9. RE-TEST WATER
# ==========================================================

def retest_water(before_water):


    print("\n")

    print("=" * 60)

    print("                   RE-TEST WATER")

    print("=" * 60)


    print(

        "\nEnter the new water-quality values after treatment."

    )


    after_water = {}


    try:


        # --------------------------------------------------
        # INPUT AFTER-TREATMENT VALUES
        # --------------------------------------------------

        after_water["pH"] = float(

            input("\nEnter new pH: ")

        )


        after_water["Hardness"] = float(

            input("Enter new Hardness: ")

        )


        after_water["Solids"] = float(

            input("Enter new Total Solids/TDS: ")

        )


        after_water["Chloramines"] = float(

            input("Enter new Chloramines: ")

        )


        after_water["Sulfate"] = float(

            input("Enter new Sulfate: ")

        )


        after_water["Conductivity"] = float(

            input("Enter new Conductivity: ")

        )


        after_water["Organic Carbon"] = float(

            input("Enter new Organic Carbon: ")

        )


        after_water["Trihalomethanes"] = float(

            input("Enter new Trihalomethanes: ")

        )


        after_water["Turbidity"] = float(

            input("Enter new Turbidity: ")

        )


        # --------------------------------------------------
        # ANALYZE AFTER-TREATMENT WATER
        # --------------------------------------------------

        print("\n")

        print("=" * 60)

        print("          AFTER-TREATMENT ASSESSMENT")

        print("=" * 60)


        display_result(after_water)


        # --------------------------------------------------
        # BEFORE AND AFTER COMPARISON
        # --------------------------------------------------

        compare_water(

            before_water,

            after_water

        )


        # --------------------------------------------------
        # OVERALL RISK COMPARISON
        # --------------------------------------------------

        compare_risk_levels(

            before_water,

            after_water

        )


    except ValueError:


        print("\nINVALID INPUT")

        print(

            "Please enter numerical values only."

        )


# ==========================================================
# 10. MAIN PROGRAM
# ==========================================================

def main():


    print("\n")

    print("=" * 60)

    print("                  AQUASAFE AI")

    print("          WATER QUALITY RISK CHECKER")

    print("=" * 60)


    print(

        "\nEnter the available water-quality measurements."

    )


    water = {}


    try:


        # --------------------------------------------------
        # GET WATER VALUES
        # --------------------------------------------------

        water["pH"] = float(

            input("\nEnter pH: ")

        )


        water["Hardness"] = float(

            input("Enter Hardness: ")

        )


        water["Solids"] = float(

            input("Enter Total Solids/TDS: ")

        )


        water["Chloramines"] = float(

            input("Enter Chloramines: ")

        )


        water["Sulfate"] = float(

            input("Enter Sulfate: ")

        )


        water["Conductivity"] = float(

            input("Enter Conductivity: ")

        )


        water["Organic Carbon"] = float(

            input("Enter Organic Carbon: ")

        )


        water["Trihalomethanes"] = float(

            input("Enter Trihalomethanes: ")

        )


        water["Turbidity"] = float(

            input("Enter Turbidity: ")

        )


        # --------------------------------------------------
        # ANALYZE WATER
        # --------------------------------------------------

        display_result(water)


        # --------------------------------------------------
        # ASK USER FOR RE-TEST
        # --------------------------------------------------

        retest_choice = input(

            "\nDo you want to re-test the water after "
            "treatment? (yes/no): "

        ).lower()


        # --------------------------------------------------
        # RE-TEST
        # --------------------------------------------------

        if retest_choice == "yes":

            retest_water(water)


        else:


            print("\nRe-test skipped.")

            print(

                "You can test the water again after applying"

            )

            print(

                "the recommended treatment."

            )


    except ValueError:


        print("\nINVALID INPUT")

        print(

            "Please enter numerical values only."

        )

def generate_treatment_recommendations(problems):
    """
    Generate structured treatment recommendations based on
    the problems detected by AquaSafe AI.
    """

    recommendations = []

    treatment_map = {
        "pH": {
            "title": "pH Balancing",
            "methods": [
                "Check the water source and surrounding conditions.",
                "Use suitable pH correction treatment based on whether the water is too acidic or alkaline.",
                "Re-test the pH after treatment."
            ],
            "priority": "HIGH"
        },

        "Hardness": {
            "title": "Hardness Reduction",
            "methods": [
                "Consider a water softener for hardness reduction.",
                "Ion-exchange treatment can help reduce hardness.",
                "Re-test hardness after treatment."
            ],
            "priority": "MODERATE"
        },

        "Solids": {
            "title": "Dissolved Solids Reduction",
            "methods": [
                "Use suitable filtration to remove suspended material.",
                "Reverse osmosis can reduce many dissolved solids.",
                "Check the source of excessive dissolved solids.",
                "Re-test total dissolved solids after treatment."
            ],
            "priority": "HIGH"
        },

        "Chloramines": {
            "title": "Chloramine Reduction",
            "methods": [
                "Activated carbon filtration may help reduce chloramine levels.",
                "Review the disinfection process if the water is treated.",
                "Re-test chloramine concentration after treatment."
            ],
            "priority": "MODERATE"
        },

        "Sulfate": {
            "title": "Sulfate Reduction",
            "methods": [
                "Identify the source of elevated sulfate.",
                "Suitable membrane filtration can help reduce sulfate.",
                "Reverse osmosis may be considered for significant sulfate levels.",
                "Re-test sulfate after treatment."
            ],
            "priority": "HIGH"
        },

        "Conductivity": {
            "title": "Conductivity Reduction",
            "methods": [
                "Check for excessive dissolved ions or salts.",
                "Review the water source for possible mineral contamination.",
                "Membrane-based treatment may reduce conductivity.",
                "Re-test conductivity after treatment."
            ],
            "priority": "MODERATE"
        },

        "Organic Carbon": {
            "title": "Organic Carbon Reduction",
            "methods": [
                "Activated carbon filtration may help reduce organic compounds.",
                "Check the water source for organic contamination.",
                "Additional treatment may be required for persistent levels.",
                "Re-test organic carbon after treatment."
            ],
            "priority": "MODERATE"
        },

        "Trihalomethanes": {
            "title": "Trihalomethane Control",
            "methods": [
                "Review the disinfection process.",
                "Activated carbon treatment may help reduce certain organic contaminants.",
                "Investigate possible sources of organic matter.",
                "Re-test after treatment."
            ],
            "priority": "HIGH"
        },

        "Turbidity": {
            "title": "Turbidity Reduction",
            "methods": [
                "Use sediment filtration to remove suspended particles.",
                "Consider appropriate clarification or filtration.",
                "Check the water source for suspended contamination.",
                "Re-test turbidity after treatment."
            ],
            "priority": "HIGH"
        }
    }

    for problem in problems:

        parameter = problem.get("parameter")

        if parameter in treatment_map:

            treatment = treatment_map[parameter]

            recommendations.append({
                "parameter": parameter,
                "title": treatment["title"],
                "severity": problem.get("severity", "Unknown"),
                "priority": treatment["priority"],
                "issue": problem.get("issue", ""),
                "methods": treatment["methods"]
            })

    return recommendations




if __name__ == "__main__":

    main()
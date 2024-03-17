import streamlit as st
import numpy as np

def test_hypothesis(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
    """
    Tests the hypothesis that the treatment group has a higher conversion rate than the control group.

    Args:
        control_visitors: Number of visitors in the control group.
        control_conversions: Number of conversions in the control group.
        treatment_visitors: Number of visitors in the treatment group.
        treatment_conversions: Number of conversions in the treatment group.
        confidence_level: Confidence level for the test (90, 95, or 99).

    Returns:
        One of the following strings:
            "Experiment Group is Better": If the treatment group has a statistically significant higher conversion rate.
            "Control Group is Better": If the control group has a statistically significant higher conversion rate.
            "Indeterminate": If there is no statistically significant difference between the two groups.
    """

    # Calculate the conversion rates for each group.
    control_rate = control_conversions / control_visitors
    treatment_rate = treatment_conversions / treatment_visitors

    # Calculate the difference in conversion rates.
    rate_difference = treatment_rate - control_rate

    # Calculate the standard error of the difference.
    se_difference = np.sqrt(
        (control_rate * (1 - control_rate) / control_visitors)
        + (treatment_rate * (1 - treatment_rate) / treatment_visitors)
    )

    # Calculate the z-score.
    z_score = rate_difference / se_difference

    # Determine the critical value based on the chosen confidence level.
    if confidence_level == 90:
        critical_value = 1.645
    elif confidence_level == 95:
        critical_value = 1.96
    elif confidence_level == 99:
        critical_value = 2.576
    else:
        raise ValueError("Invalid confidence level.")

    # Compare the z-score to the critical value.
    if z_score > critical_value:
        return "Experiment Group is Better"
    elif z_score < -critical_value:
        return "Control Group is Better"
    else:
        return "Indeterminate"

def main():
    st.title("A/B Test Hypothesis Testing App")
    st.markdown(
        """
        This app performs hypothesis testing for A/B tests using the provided parameters.
        Enter the required information in the sidebar and click on 'Run Test' to see the result.
        """
    )

    st.sidebar.title("Input Parameters")

    control_visitors = st.sidebar.number_input("Control Group Visitors", min_value=1, step=1)
    control_conversions = st.sidebar.number_input("Control Group Conversions", min_value=0, step=1)
    treatment_visitors = st.sidebar.number_input("Treatment Group Visitors", min_value=1, step=1)
    treatment_conversions = st.sidebar.number_input("Treatment Group Conversions", min_value=0, step=1)
    confidence_level = st.sidebar.selectbox("Confidence Level", [90, 95, 99])

    if st.sidebar.button("Run Test"):
        result = test_hypothesis(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level)
        st.write("## Result:")
        if result == "Experiment Group is Better":
            st.success(result)
        elif result == "Control Group is Better":
            st.error(result)
        else:
            st.warning(result)

if __name__ == "__main__":
    main()

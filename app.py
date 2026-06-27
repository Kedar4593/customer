import streamlit as st

# --- Backend function (your code) ---
def classify_intent(user_query):
    query = user_query.lower()
    
    if "where" in query and "order" in query:
        return "Intent: Track Order", "You can track your package by clicking the link in your confirmation email."
        
    elif "payment" in query or "pay" in query or "options" in query:
        return "Intent: Payment Options", "We accept Visa, Mastercard, PayPal, and Apple Pay."
        
    elif "return" in query or "refund" in query:
        return "Intent: Return Request", "To return an item, please visit our Returns Portal and enter your order ID."
        +
    else:
        return "Intent: Unknown", "I'm sorry, I didn't quite catch that. Could you rephrase your question?"

# --- Streamlit Frontend ---
def main():
    st.title("🛍️ Shopping Assistant Chatbot")
    st.write("Ask me about your order, payment options, or returns!")

    # User input box
    user_input = st.text_input("You:", "")

    if user_input:
        intent, response = classify_intent(user_input)
        st.subheader(f"[{intent}]")
        st.success(response)

if __name__ == "__main__":
    main()

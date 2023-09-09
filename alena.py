import streamlit as st
from sympy import *
import matplotlib.pyplot as plt
import numpy as np
import json
import datetime
import sympy as sp
import os

st.set_page_config(page_title='Elena - DevTunisian',
                   page_icon=':f8db:',
                   layout='centered',
                   )
hide = """<style>
#MainMenu {visibility: hidden;}
"""

st.markdown(hide, unsafe_allow_html=True)
def make_file(number):
    fileName = f"users/{str(number)}.json"
    try:
        pass
    except FileNotFoundError:
        user = []
        with open(fileName, 'w') as f:
            json.dump(user, f)
    
def chatWithServer(number, chat):
    # Create a dictionary representing the chat message
    chat_message = {
        "msg": chat,
        'number': number
    }

    # Define the path to the chat file for the given phone number
    chat_file_path = f"chats/users-msg.json"

    # Load existing chat messages or create an empty list if the file doesn't exist yet
    try:
        with open(chat_file_path, 'r') as f:
            chat_data = json.load(f)
    except FileNotFoundError:
        chat_data = []

    # Append the new chat message to the list
    chat_data.append(chat_message)

    # Save the updated chat data back to the file
    with open(chat_file_path, 'w') as f:
        json.dump(chat_data, f)

    # Notify the user that the message has been sent successfully
    st.success('Message sent successfully')

def LoadAllMessages():
    fileName = 'chats/users-msg.json'
    with open(fileName, 'r') as AllMsg:
        data = json.load(AllMsg)
    return data
def save_calculation_result(result, number):
    try:
        # Define the path to the JSON file for the given phone number
        result_file_path = f"users/{number}.json"

        # Load existing results or create an empty list if the file doesn't exist yet
        try:
            with open(result_file_path, 'r') as f:
                results_data = json.load(f)
        except FileNotFoundError:
            results_data = []

        # Add the current calculation result along with a timestamp
        result_entry = {
            "result": result,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        results_data.append(result_entry)

        # Save the updated results data back to the file
        with open(result_file_path, 'w') as f:
            json.dump(results_data, f)

    except Exception as e:
        st.error(f"Error saving calculation result: {e}")

# Define a function to load recent calculations from the JSON file
def load_recent_calculations(number):
    recent_file_path = f"users/{number}.json"
    try:
        with open(recent_file_path, 'r') as f:
            recent_data = json.load(f)
        return recent_data
    except FileNotFoundError:
        return []
def read_json_files_in_folder(folder_path):
    json_file_names = []  # Store only file names
    
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return json_file_names
    
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Iterate over the files and get the file names
    for filename in files:
        if filename.endswith(".json"):
            json_file_names.append(filename)
    
    return json_file_names


how_use_web = """
# **Tools For Use This web**
1- **enter a phone number**
-
- enter a phone number for make your account in this website.
- length of the phone number is 8 characters .

2- **operator**
-
- for puissance use the operator ' ** '
- when  write cos(2x) or 2x or etc , replace 2x to 2 * x or cos(2 * x) or 2*x .
- when use '/' in equation use '()' exa:  (2*x+5)/(x*4-1) etc.

3 - **exponentielle (e)**
-
- for use e in equation write ('exp(x)') .

4 - **Resouder**
-
- for use resouder in equation write n*x = 0 , n * x = b etc.

5- **Racine Carré**
-
- for use racine Carré in equation write **('sqrt(x)')** .
"""
num = st.sidebar.text_input("Phone Number ")

if st.sidebar.markdown("[Login](#login)") and  num and len(num)<= 8 and num != '12345678':
    make_file(num)
    tabs = ['Calculer Limits','Equation','# Graphique','# derivabilité', '# All', '# recents','# chat with DevTunisian']
    chose = st.tabs(tabs)
    with (chose[0]):
        st.write(f'# **{tabs[0]}**')

        expression = st.text_input("Enter an expression (e.g., 'x**2 + 3*x - 1'):")
        limit_value = st.number_input("Enter the limit value:")
        if expression and st.button("Limit"):
            try:
                x = symbols('x')
                limit_result = limit(sympify(expression), x, limit_value)
                st.write("**Limit =**")
                st.latex((limit_result))
                calculation = {
                        "expr": expression,
                        "res": f"limit :{latex(limit_result)}",
                        
                    }
                save_calculation_result(calculation,num)
            except Exception as e:
                st.error(f"Error: {e}")
    with (chose[1]):
        st.write(f'# **{tabs[1]}**')
        equation = st.text_input("Enter an equation (e.g., 'x**2 + 1 = 0'):")
    
        if equation and st.button("solution"):
        # Separate the equation into LHS and RHS
            equation_parts = equation.split('=')
        
            if len(equation_parts) == 2:
                lhs = equation_parts[0].strip()
                rhs = equation_parts[1].strip()
            
                try:
                    x = symbols('x')
                    lhs_expr = sympify(lhs)
                    rhs_expr = sympify(rhs)
                
                    equation_to_solve = Eq(lhs_expr, rhs_expr)
                
                    solutions = solve(equation_to_solve, x)
                
                    if solutions:
                        st.write("Solutions:")
                        for sol in solutions:
                            st.latex(sol)
                            calculation = {
                        "expr": equation,
                        "res": f"solution :{latex(sol)}",
                        
                    }
                            save_calculation_result(calculation,num)
                    else:
                        st.write("No solutions found.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Invalid equation format. Please use 'LHS = RHS' format.")
    with (chose[2]):
        st.write(tabs[2])
        expression = st.text_input("Enter an expression `(e.g., 'x**2 + 3*x - 1' or exp(x) or cos(x) etc)` for the graph:")
        x_interval = st.text_input("Enter the x interval as a tuple (e.g., (-10, 10)):")
        y_interval = st.text_input("Enter the y interval as a tuple (e.g., (-20, 20)):")

        if expression and x_interval and y_interval  and st.button("Show"):
            try:
                x = symbols('x')
                expr = sympify(expression)
                f = lambdify(x, expr, 'numpy')

                # Parse the user-input intervals
                x_interval = eval(x_interval)
                y_interval = eval(y_interval)

                x_vals = np.linspace(x_interval[0], x_interval[1], 400)
                y_vals = f(x_vals)

                plt.figure(figsize=(8, 6))
                plt.plot(x_vals, y_vals)
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title(f'Graph of the Expression {expression}')
                plt.xlim(x_interval)
                plt.ylim(y_interval)
                st.pyplot(plt)
                
            except Exception as e:
                st.error(f"Error: {e}") 
    with (chose[3]):
            st.write(tabs[3])
            expression = st.text_input("Enter an expression (e.g., 'sin(x) - 2*cos(2*x)') to calculate its derivative:")

            if expression  and st.button("Derivé"):
                try:
                    x = symbols('x')
                    expr = sympify(expression)
                    derivative = diff(expr, x)

                    st.write("Original Expression:")
                    st.latex(expr)

                    st.write("Derivative:")
                    st.latex(derivative)
                    calculation = {
                        "expr": expression,
                        "res": f"derivative :{latex(derivative)}",
                        
                    }
                    save_calculation_result(calculation,num)
                except Exception as e:
                    st.error(f"Error: {e}") 
    with (chose[4]):
        st.write(tabs[4])
    
    # Input fields for equation, limit, and graph
        equation = st.text_input("Enter an equation (e.g., 'x**2 + 3*x - 1'):")
        limit_value = st.number_input("Enter the limit value (optional):")
        x_interval = ("-10,10")
        y_interval = ("-100,100")
    
        if equation  and st.button("calculate"):
            try:
                x = symbols('x')
                expr = sympify(equation)
            
                # Calculate and display the derivative
                derivative = diff(expr, x)
                st.write("Derivative:")
                st.latex(derivative)
            
            # Solve the equation if limit_value is provided
                if limit_value is not None:
                    equation_to_solve = Eq(expr, limit_value)
                    solutions = solve(equation_to_solve, x)
                    st.write("Solutions:")
                    for sol in solutions:
                        st.write(sol)
            
            # Generate and display the graph if x_interval is provided
                st.write("**Graph:**")
                if x_interval:
                    try:
                        x_interval = eval(x_interval)
                        y_interval = eval(y_interval)
                        f = lambdify(x, expr, 'numpy')
                        x_vals = np.linspace(x_interval[0], x_interval[1], 400)
                        y_vals = f(x_vals)

                        plt.figure(figsize=(8, 10))
                        plt.plot(x_vals, y_vals)
                        plt.xlabel('x')
                        plt.ylabel('y ')
                        plt.title('Graph of the Expression')
                        plt.xlim(x_interval)
                        plt.ylim(y_interval)
                        st.pyplot(plt)

                        
                        
                    except Exception as e:
                        st.error(f"Error generating the graph: {e}")
            
            except Exception as e:
                st.error(f"Error: {e}")

    with (chose[5]):
        st.write(tabs[5])

    # Load recent calculations from the JSON file
        recent_data = load_recent_calculations(num)

        if recent_data:
            st.write("Recent Calculations:")
            for idx, calculation in enumerate(recent_data, start=1):
                st.write(f"{idx}. {calculation['timestamp']}")
                
                st.latex(calculation['result']['expr'])
                st.latex(calculation['result']['res'])
        else:
            st.write("No recent calculations available.")

    
    with (chose[6]):
        st.write(tabs[6])
        chat = st.text_input('Send a Message to the server')
        send = st.button('Send Message')
        if send:
            if chat:
                chatWithServer(num, chat)
            else:
                st.error('Failed to send Message to server')
        if num == '27692361':
            data = LoadAllMessages()
            
            for message in data:
                with st.chat_message("user"):
                    st.write(f"{message['number']} : {message['msg']}")
else :
    st.header('< **open Sidebar for signing .**')
    st.write("# Welcome to **Elena** web Tools , This web has created for solve your math problem. \n # made by **DevTunisian** ")
if num == "27692361":
    folder_path = "users"
    user_data = read_json_files_in_folder(folder_path)
    st.sidebar.write("---")
    st.sidebar.write(how_use_web)
    st.sidebar.write("---")
    st.sidebar.write("# users")
    for data in user_data:
        file = data.replace('.json', '')
        st.sidebar.write(file)
    pass

else:

    st.sidebar.write("---")
    st.sidebar.write(how_use_web)
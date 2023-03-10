import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import numpy as np
import pandas as pd
import re

st.set_page_config(page_title="TOPSIS", page_icon=":tada:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m4wmgweb.json")
lottie_coding1 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_qxmkn9ou.json")
lottie_coding2 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_mn0yeqfs.json")
lottie_coding3 = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
    

selected = option_menu(None, ["Home", "How to use", "Analyze", 'Contact Us'], 
    icons=['house', 'question-circle', "twitter", 'envelope'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected == "Home":
    st.title("TOPSIS")
    st.subheader("Hey there!!! :wave: Welcome to our service")
    
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Wondering what we do?")
            st.markdown("We **_analyze_** the situation help you make a better decisions")
            st.write("Go to the Analyze tab to see the magic:sparkles::sparkles:")
        with right_column:
            st_lottie(lottie_coding3, height=400, key="coding")
     
    with st.container():
        st.subheader("How?!")
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown('<div style="text-align: justify;">We use a multi-criteria decision analysis (MCDA) and TOPSIS is one of the way to implement it.</div>', unsafe_allow_html=True)
            st.write("\n")
            st.markdown('<div style="text-align: justify;">It is a method of compensatory aggregation that compares a set of alternatives, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion. The weights of the criteria in TOPSIS method can be calculated using Ordinal Priority Approach, Analytic hierarchy process, etc. An assumption of TOPSIS is that the criteria are monotonically increasing or decreasing. Normalisation is usually required as the parameters or criteria are often of incongruous dimensions in multi-criteria problems. Compensatory methods such as TOPSIS allow trade-offs between criteria, where a poor result in one criterion can be negated by a good result in another criterion. This provides a more realistic form of modelling than non-compensatory methods, which include or exclude alternative solutions based on hard cut-offs. An example of application on nuclear power plants is provided in.</div>', unsafe_allow_html=True)
            st.write("\n")
            st.write("\n")
            st.write("\n")
           
    with st.container():
        st.subheader("Implementation")
#         left_column, right_column = st.columns(2)
#         with left_column:
#             st.markdown('<div style="text-align: justify;">We attempted to do some basic NLP techniques using TextBlob library. The tweets are being extracted using the twitter API named tweepy. After the extracting the dataset we do some pre-processing like stemming, tokenizing, etc. After that we use the inbuilt Naive Bayes model to classify the tweets and display the our analysis to you guys through data visualization.</div>', unsafe_allow_html=True)
#             st.write("\n")
#             st.write("Here is an instance to show you guys the accuracy of our model")
        image = Image.open('img/image.png')
        st.image(image)
        
        image1 = Image.open('img/image1.png')
        st.image(image1)
            
if selected == "How to use":
    with st.container():
        left_col, middle_col, right_col = st.columns(3)
        with middle_col:
            st_lottie(lottie_coding2, height=300, key="coding")
    
    with st.container():
        st.title("Didn't know how to use?!")
        st.subheader("No need to worry, it's very simple")
        st.write("Just follow the steps listed below:-")
        st.write("1. Firstly, go to the 'Analyze' tab.")
        image2 = Image.open('img/image2.png')
        st.image(image2)
        st.write("\n")
        st.write("2. There is a option to upload your dataset. Please upload a .csv format only")
        image3 = Image.open('img/image3.png')
        st.image(image3)
        st.write("\n")
        st.write(" Then you will get a glimpse of your dataset")
        image4 = Image.open('img/image4.png')
        st.image(image4)
        st.write("\n")
        st.write("3. Now enter the weights and impacts")
        image5 = Image.open('img/image5.png')
        st.image(image5)
        st.write("4. After filling in the information click on analyze and you will get the ranking as shown")
        image6 = Image.open('img/image6.png')
        st.image(image6)

if selected == "Analyze":
    st.title("Let's get started")
    st.write("Please upload your dataset (in .csv format only)")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write('Here is the sample of the data you provided')
        st.write(data)
        
        collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]
        numbers = st.text_input("Enter the weights (Please input the numbers separated with a single comma)")
        string = st.text_input("Enter the impacts (Please input + or - separeated with a single comma)")
        impact = string.split(",")
        weights = collect_numbers(numbers)
        
        go = st.button('Analyze')
        if go:
            df = data.drop(data.columns[[0]], axis=1)
            
            sos = []
            for i in range(df.shape[1]):
                sum = 0
                for j in range(df.shape[0]):
                    sum = sum + df.iloc[j,i]**2
                sos.append(sum)
            
            rosos = np.sqrt(sos)
            
            for i in range(df.shape[1]):
                for j in range(df.shape[0]):
                    df.iloc[j,i] = df.iloc[j,i] / rosos[i]
            
            for i in range(df.shape[1]):
                for j in range(df.shape[0]):
                    df.iloc[j,i] = df.iloc[j,i] * weights[i]
            
            idbest = []
            idworst = []
            
            for i in range(df.shape[1]):
                if impact[i] == '+':
                    idbest.append(df.iloc[:,1].max(axis=0))
                    idworst.append(df.iloc[:,1].min(axis=0))
                
                elif impact[i] == '-':
                    idbest.append(df.iloc[:,1].min(axis=0))
                    idworst.append(df.iloc[:,1].max(axis=0))
            
            sp = []
            sn = []
            for i in range(df.shape[0]):
                sump = 0
                sumn = 0
                for j in range(df.shape[1]):
                    sump = sump + (df.iloc[i,j] - idbest[j])**2
                    sumn = sumn + (df.iloc[i,j] - idworst[j])**2
                
                sp.append(sump)
                sn.append(sumn)
             
            sp = np.sqrt(sp)
            sn = np.sqrt(sn)
            
            p = []
            for i in range(df.shape[0]):
                p.append(sn[i] / (sp[i]+sn[i]))
            
            data['P'] = p
            data['Rank'] = data['P'].rank()
            st.write(data)
#     with st.container():
#         left_column, right_column = st.columns(2)
#         with left_column:
#             genre = st.radio("What do you want to do",
#                              ('I want to analyze the tweets from a twitter account', 'I want to analyze a topic', 'I want to analyze my dataset'))

#             if genre == "I want to analyze the tweets from a twitter account":
#                 st.write("You will be redirected to another website. Please [Click Here >](https://project-se-ts-1.streamlit.app/)")

#             if genre == "I want to analyze a topic":
#                 st.write("You will be redirected to another website. Please [Click Here >](https://project-se-ts-3.streamlit.app/)")

#             if genre == "I want to analyze my dataset":
#                 st.write("You will be redirected to another website. Please [Click Here >](https://project-se-ts-2.streamlit.app/)")
            
#         with right_column:
#             st_lottie(lottie_coding, height=250, key="coding")
        
#     with st.container():
#         st.subheader("Before going further please read the following instruction :-")
#         st.write("1. Maximum 10 tweets will be displayed due to the data and privacy protection bill")
#         st.write("2. Tweets extraction phase may take some time if number of tweets is large")
#         st.write("3. The analysis is done purely on the basis of some mathematical computation and we aren't responsible for the results")
#         st.write("4. Although it is a result of mathematical coputations but we assure that the results are accurate")
#         st.write("5. We are not intended to target any particular group of people, relegion, culture etc. and not intended to hurt anybody's feelings")

if selected == "Contact Us":
#     Use local CSS
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style.css")
    with st.container():
        left_column, right_column = st.columns(2)
        with right_column:
            st_lottie(lottie_coding1, height=550, key="coding")
        with left_column:
            st.write("---")
            st.header("Get In Touch With Us!")
            st.subheader("Feel free to ask anything")

            # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
            contact_form = """
            <form action="https://formsubmit.co/kbansal_be20@thapar.edu" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """
#             left_column, right_column = st.columns(2)
#             with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
#             with right_column:
            st.empty()

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ??? by <a style='display: block; text-align: center;'>Kushagar Bansal</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

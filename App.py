import streamlit as st
import pandas as pd
import base64,random
import time,datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import pafy
import plotly.express as px
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
# # user-Authentcation
# names=["Peter Parker","Rebecca miller"]
# usernames=["pparker","rmiller"]
#
# # load hashed Passwords
#
# file_path = Path(__file__).parent/"hashed_pw.pkl"
#
# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(hashed_passwords,file)
#
#
# authenticator= stauth.Authenticate(names,usernames,hashed_passwords,"sales_dashboard","abcdef",cookie_expiry_days=30)
#
#
# name,authentication_status,username=authenticator.login("Login","main")
#
#
# if authentication_status == False:
#     st.error("Username/Password is Incorrect.")
# if authentication_status == None:
#     st.warning("Please enter your username and password.")
# if authentication_status:

import pandas as pd


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data





def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title


def get_table_download_link(df, filename, text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


connection = pymysql.connect(host='localhost', user='root', password='', db='sra')
cursor = connection.cursor()


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills,
                courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (
        name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills,
        courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()


st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon='./Logo/SRA_Logo.ico',
)
def main():
    act = ["Choose Option", "SignUp", "Login"]
    choice = st.sidebar.selectbox("Choose among the given options:", act)
    if choice == "SignUp":
        img = Image.open('download.jpg')
        img = img.resize((250, 250))
        st.image(img)
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
    elif choice == "Choose Option":
        img = Image.open('images.jpg')
        img = img.resize((500, 500))
        st.image(img)
    else:
        run()

def deep():
    st.success('Welcome to Job Seeker Side')
    # st.sidebar.subheader('**ID / Password Required!**')

    ad_user = st.text_input("Username")
    ad_password = st.text_input("Password", type='password')
    if st.button('Login'):
        if ad_user == 'admin' and ad_password == '12345':
            st.success("Welcome ")
            st.success("Please Enter PDF File...")
            if st.button("For Uploading PDF"):
                run()
    if st.sidebar.button("Logout"):
        st.experimental_rerun()
    return
            # st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Upload your resume, and get smart recommendation based on it."</h4>''',
            #             unsafe_allow_html=True)
            #pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
            #pdf_file=12
            #if pdf_file is None:
                # with st.spinner('Uploading your Resume....'):
                #     time.sleep(4)
               # save_image_path = './Uploaded_Resumes/' + pdf_file.name

def run():

    st.title("Smart Resume Analyser")
    #st.sidebar.markdown("# Choose User")
    activities = ["Choose Option","Admin","Job Provider","Job Seeker"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    # link = '[©Developed by Spidy20](http://github.com/spidy20)'
    # st.sidebar.markdown(link, unsafe_allow_html=True)


    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    if choice == "Choose Option":
        img = Image.open('images (1).jpg')
        img = img.resize((500, 500))
        st.image(img)

    elif choice == 'Job Seeker':
        img = Image.open('./Logo/SRA_Logo.jpg')
        img = img.resize((250, 250))
        st.image(img)

        # st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Upload your resume, and get smart recommendation based on it."</h4>''',
        #             unsafe_allow_html=True)
        deep()
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")

        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            # with st.spinner('Uploading your Resume....'):
            #     time.sleep(4)
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello " + resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                                unsafe_allow_html=True)

                st.subheader("**Skills Recommendation💡**")
                ## Skill shows
                keywords = st_tags(label='### Skills that you have',
                                   text='See our skills recommendation',
                                   value=resume_data['skills'], key='1')

                ##  recommendation
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                              'streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                'user research', 'user experience']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                ## Courses recommendation
                for i in resume_data['skills']:
                    ## Data science recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                              'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                              'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                              'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                              'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='2')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)
                        st.header("**Job Recommendations For Data Science💼**")
                        st.write(
                            "Data Science [link](https://pk.linkedin.com/jobs/data-scientist-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Data Science Intern [link](https://www.rozee.pk/job/jsearch/q/Machine%20Learning/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Machine Learning [link](https://www.rozee.pk/job/jsearch/q/Machine%20Learning/fc/1185/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Deep Learning [link](https://pk.linkedin.com/jobs/machine-learning-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Artificial Intelligence [link](https://pk.linkedin.com/jobs/artificial-intelligence-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Computer Vision [link](https://www.linkedin.com/jobs/search/?geoId=102306254&keywords=computer%20vision&location=Punjab%2C%20Pakistan/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        rec_course = course_recommender(ds_course)
                        break

                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                              'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='3')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)
                        st.header("**Job Recommendations For Web Development💼**")
                        st.write(
                            "Python Developer [link](https://www.rozee.pk/job/jsearch/q/Web%20Developer/fc/1185/fe/713/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Web Developer Intern [link](https://pk.linkedin.com/jobs/web-developer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Python Developer Dgango [link](https://www.linkedin.com/jobs/search/?geoId=101022442&keywords=python%20developer%20django&location=Pakistan/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Web Development Remote [link](https://www.rozee.pk/job/jsearch/q/all/fca/95/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "React Developer [link](https://www.rozee.pk/job/jsearch/q/Web%20Developer/streamlit_app.py)")
                        rec_course = course_recommender(web_course)
                        break

                    ## Android App Development
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                              'Kivy', 'GIT', 'SDK', 'SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='4')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)
                        st.header("**Job Recommendations For Android App Development💼**")
                        st.write(
                            "Android Developer [link](https://www.rozee.pk/job/jsearch/q/Android/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Android App Developer [link](https://pk.linkedin.com/jobs/android-developer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "App Development [link](https://pk.linkedin.com/jobs/mobile-application-developer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Android Developer Intern [link](https://www.rozee.pk/job/jsearch/q/Android%20App%20Developer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "App Developer [link](https://www.rozee.pk/job/jsearch/q/Android/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        rec_course = course_recommender(android_course)
                        break

                    ## IOS App Development
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                              'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                              'Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='5')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)
                        st.header("**Job Recommendations For IOS App Development💼**")
                        st.write(
                            "IOS App Development [link](https://www.rozee.pk/job/jsearch/q/IOS%20Developer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "IOS Developer [link](https://pk.linkedin.com/jobs/ios-developer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "IOS Developement [link](https://pk.linkedin.com/jobs/ios-app-developer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "App Developer [link](https://pk.linkedin.com/jobs/ios-developer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "IOS App Developer [link](https://www.google.com/search?q=IOS+App+Development+Jobs+in+pakistan&ei=akXpYrS6AvWI9u8P8_mBwA8&uact=5&oq=IOS+App+Development+Jobs+in+pakistan&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGABKBAhGGABQAFgAYPYFaABwAXgAgAHUAogB1AKSAQMzLTGYAQCgAQKgAQHAAQE&sclient=gws-wiz&ibp=htl;jobs&sa=X&ved=2ahUKEwin6syzv6j5AhU-_bsIHfiFAWQQkd0GegQIChAB#fpstate=tldetail&htivrt=jobs&htiq=IOS+App+Development+Jobs+in+pakistan&htidocid=6p6TcpZF3d0AAAAAAAAAAA%3D%3D/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        rec_course = course_recommender(ios_course)
                        break

                    ## Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                              'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                              'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                              'Solid', 'Grasp', 'User Research']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='6')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)
                        st.header("**Job Recommendations For Ui-UX Recommendation💼**")
                        st.write(
                            "Graphic Developement [link](https://www.rozee.pk/job/jsearch/q/UI%20-%20UX%20Designer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Ui-UX Developement [link](https://pk.linkedin.com/jobs/ui-design-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Graphic Developer [link](https://www.rozee.pk/job/jsearch/q/UI%20&%20UX%20Developer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Ui-UX Developer [link](https://pk.linkedin.com/jobs/user-experience-designer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Adobe Developer [link](https://www.rozee.pk/job/jsearch/q/UI%20-%20UX%20Designer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        st.write(
                            "Adobe Ui-UX Developer [link](https://pk.linkedin.com/jobs/user-experience-designer-jobs?position=1&pageNum=0/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                        rec_course = course_recommender(uiux_course)
                        break

                #
                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                ### Resume writing recommendation
                st.subheader("**Resume Tips & Ideas💡**")
                resume_score = 0
                if 'Objective' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',
                        unsafe_allow_html=True)

                if 'Declaration' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration✍/h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',
                        unsafe_allow_html=True)

                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies⚽</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',
                        unsafe_allow_html=True)

                if 'Achievements' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',
                        unsafe_allow_html=True)

                if 'Projects' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',
                        unsafe_allow_html=True)

                st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score) + '**')
                st.warning(
                    "** Note: This score is calculated based on the content that you have added in your Resume. **")
                st.balloons()

                insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                            str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
                            str(recommended_skills), str(rec_course))

                ## Resume writing video
                st.header("**Bonus Video for Resume Writing Tips💡**")
                resume_vid = random.choice(resume_videos)
                res_vid_title = fetch_yt_video(resume_vid)
                st.subheader("✅ **" + res_vid_title + "**")
                st.video(resume_vid)

                ## Interview Preparation Video
                st.header("**Bonus Video for Interview👨‍💼 Tips💡**")
                interview_vid = random.choice(interview_videos)
                int_vid_title = fetch_yt_video(interview_vid)
                st.subheader("✅ **" + int_vid_title + "**")
                st.video(interview_vid)

                connection.commit()
            else:
                st.error('Something went wrong..')



    elif choice == 'Admin':
        img = Image.open('download (1).jpg')
        img = img.resize((400, 400))
        st.image(img)
        ## Admin Side
        st.success('Welcome to Admin Side')
        # st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.sidebar.button("Logout"):

            st.balloons()
            st.experimental_rerun()


        if st.button('Login'):
            if ad_user == 'admin' and ad_password == '12345':
                st.success("Welcome ")
                # Display Data
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills',
                                                 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

                ## Pie chart for predicted field recommendations
                labels = plot_data.Predicted_Field.unique()
                print(labels)
                values = plot_data.Predicted_Field.value_counts()
                print(values)
                st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                ### Pie chart for User's👨‍💻 Experienced Level
                labels = plot_data.User_level.unique()
                values = plot_data.User_level.value_counts()
                st.subheader("📈 ** Pie-Chart for User's👨‍💻 Experienced Level**")
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)


            else:
                st.error("Wrong ID & Password Provided")

    else:
        img = Image.open('images.png')
        img = img.resize((400, 400))
        st.image(img)

        st.success('Welcome to Job provider Side')
        # st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.sidebar.button("Logout"):
            st.experimental_rerun()
        if st.button('Login'):
            if ad_user == 'admin' and ad_password == '12345':
                st.success("Welcome ")
                st.header("**Post Job For Data Science💼**")
                st.write(
                    "Data Science [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Data Science Intern [link](https://www.rozee.pk/job/jsearch/q/Machine%20Learning/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Machine Learning [link](https://hiring.rozee.pk//streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Deep Learning [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Artificial Intelligence [link](https://hiring.rozee.pk//streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Computer Vision [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")






                st.header("**Post Job For Web Development💼**")
                st.write(
                    "Python Developer [link](https://www.rozee.pk/job/jsearch/q/Web%20Developer/fc/1185/fe/713/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Web Developer Intern [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Python Developer Dgango [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Web Development Remote [link](https://www.rozee.pk/job/jsearch/q/all/fca/95/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "React Developer [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")




                st.header("**Post Job For Android App Development💼**")
                st.write(
                    "Android Developer [link](https://www.rozee.pk/job/jsearch/q/Android/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Android App Developer [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "App Development [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Android Developer Intern [link](https://www.rozee.pk/job/jsearch/q/Android%20App%20Developer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write("App Developer [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")



                st.header("**Post Job For IOS App Development💼**")
                st.write(
                    "IOS App Development [link](https://www.rozee.pk/job/jsearch/q/IOS%20Developer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "IOS Developer [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "IOS Developement [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write("App Developer [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "IOS App Developer [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")


                st.header("**Post Job For Ui-UX Recommendation💼**")
                st.write(
                    "Graphic Developement [link](https://www.rozee.pk/job/jsearch/q/UI%20-%20UX%20Designer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Ui-UX Developement [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Graphic Developer [link](https://www.rozee.pk/job/jsearch/q/UI%20&%20UX%20Developer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Ui-UX Developer [link](https://hiring.rozee.pk/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Adobe Developer [link](https://www.rozee.pk/job/jsearch/q/UI%20-%20UX%20Designer/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                st.write(
                    "Adobe Ui-UX Developer [link](https://www.linkedin.com/help/linkedin/answer/a517545/post-a-job-on-linkedin?lang=en/streamlit_webapps/main/MC_pi/streamlit_app.py)")




                st.header("**Jobs Data 💼**")
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills',
                                                 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

                ## Pie chart for predicted field recommendations
                labels = plot_data.Predicted_Field.unique()
                print(labels)
                values = plot_data.Predicted_Field.value_counts()
                print(values)
                st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                ### Pie chart for User's👨‍💻 Experienced Level
                labels = plot_data.User_level.unique()
                values = plot_data.User_level.value_counts()
                st.subheader("📈 ** Pie-Chart for User's👨‍💻 Experienced Level**")
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)

            else:
                st.error("Wrong ID & Password Provided")





# def main():
# 	"""Simple Login App"""
#
# 	st.title("Simple Login App")
#
# 	menu = ["Home","Login","SignUp"]
# 	choice = st.sidebar.selectbox("Menu",menu)
#
# 	if choice == "Home":
# 		st.subheader("Home")
#
# 	elif choice == "Login":
# 		st.subheader("Login Section")
#
# 		username = st.sidebar.text_input("User Name")
# 		password = st.sidebar.text_input("Password",type='password')
# 		if st.sidebar.checkbox("Login"):
# 			# if password == '12345':
# 			create_usertable()
# 			hashed_pswd = make_hashes(password)
#
# 			result = login_user(username,check_hashes(password,hashed_pswd))
# 			if result:
#
# 				st.success("Logged In as {}".format(username))
#
# 				task = st.selectbox("Task",["Jobs","Profiles"])
# 				if task == "Jobs":
# 					run()
# 				else:
# 					st.subheader("User Profiles")
# 					user_result = view_all_users()
# 					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
# 					st.dataframe(clean_db)
# 			else:
# 				st.warning("Incorrect Username/Password")




# if __name__ == '__main__':
# 	main()

main()


























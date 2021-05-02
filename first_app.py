import streamlit as st
import numpy as np
import pandas as pd
import time
from PIL import Image
import matplotlib.pyplot as plt


import SessionState

#import segment_leaf
#from segment_leaf import detect

import tensorflow as tf


interpreter = tf.lite.Interpreter(model_path="plain2model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#model = tf.keras.models.load_model('200_epoch_96_87.h5')
model = tf.keras.models.load_model('200_epoch_97_87_soft.h5')
class_names = ['interveinal', 'margin', 'normal', 'spotty', 'tip']
rice_nitro_names = ['swap1','swap2','swap3','swap4']

session_state = SessionState.get(symptoms="", diagnoise_button=False)


def main():



    page = st.sidebar.selectbox("App Selections", ["Homepage", "fertilizer schedule", "Nitrogen deficiency in rice","leaf analysis", "leaf analysis result"])
    if page == "fertilizer schedule":
        st.title("Fertilizer schedule")
        schedule()
    elif page == "Homepage":
        homepage()
    elif page == "leaf diagnosis":
        st.title("Identify nutrient deficiency")
        health()
    elif page == "leaf analysis":
        st.title("Analyse leaf image")
        health_v2()
    elif page == "leaf analysis result":
        st.title("Results upon analysing leaf")
        result()
    elif page == "Nitrogen deficiency in rice":
        st.title("Identify nitrogen deficiency in rice")
        nitro_rice()

def homepage():
    st.title('Fertilizer Advicer')
    st.write('Welcome to the home page, visit differtent pages from navigation column.')
    st.write(':blossom: _fertilizer schedule_ - This page gives an overview of the fertilizers to use for different nutrient deficiencies')
    st.write(':blossom: _Nitrogen deficiency in rice_ - helps identify degree of nitrogen deficiency (use when rices leaves start becomming lighter)')
    st.write(":sunflower: _leaf analysis_ - helps in diagnosis of nutrient deficiencies like 'Potassium', 'Magnesium', 'Zinc', 'Iron', 'Manganese', 'Copper', 'Boron' and 'Sulphur' for rice/paddy, maize and wheat crops")
    st.write(":sunflower: _leaf analysis result_ - Visit after 'leaf analysis' page to view result of diagnosis. Also visit 'fertilizer schedule' to get customised fertilizer recommendation")
    session_state.analysis = ''
    session_state.rice_nitro_analysis = ''
    session_state.deficiency = []
    #fertilizer_df = pd.read_excel(r'd:\Documents\BE\PBL\8_sem\fertilizer.xlsx', sheet_name='fertilizer',  engine="openpyxl")
    #print(fertilizer_df.columns)
    #st.dataframe(fertilizer_df)


def schedule():
    land_value = st.number_input('Enter land size in acres')
    growth_value = st.radio('Stage of growth', ['sapling','new leaves/established','flowering'])
    crop_value = st.selectbox('Select crop', ['rice','maize','wheat'])

    schedule_button = st.button('Get schedule', key='schedule')
    if(schedule_button):
        if(session_state.deficiency):
            for defi in session_state.deficiency:
                show_table(land_value,growth_value,crop_value,defi)

        else:
            show_table(land_value,growth_value,crop_value,0)
            st.write('To get customized recommendations go to "leaf analysis" and "leaf analysis result" page')


def show_table(land_value,growth_value,crop_value, defi=0):
    # TODO: fetch rows from datafram matching criteria/calculate for particular case
    fertilizer_df = pd.read_excel(r'd:\Documents\BE\PBL\8_sem\fertilizer.xlsx', sheet_name='fertilizer',  engine="openpyxl")
    if(defi==0):
        st.write('List of Fertilizers for different nutrient deficiencies: ')
        st.write(fertilizer_df)

    else:
        st.write(f'You have selected: {land_value} acres, {crop_value} which is in {growth_value} stage.')
        st.write("Recommended fertilizer for: ", session_state.deficiency)
        all_nutrients = list(fertilizer_df['nutrient'])
        for nutri in session_state.deficiency:
            st.write(fertilizer_df.loc[fertilizer_df['nutrient']==nutri])

def load_image(image_file):
	img = Image.open(image_file)
	return img


def health_v2():

    #session_state = SessionState.get(symptoms="", diagnoise_button=False)
    #session_state.symptoms = ''

    leaf_age = st.radio('leaf age', ['mature/old','new/young','middle'])
    session_state.leaf_age  = leaf_age
    crop_value = st.selectbox('Select crop', ['rice','maize','wheat'])

    st.write('Upload image of affected leaf with white background')
    leaf_img = st.file_uploader('Upload leaf image', type=['png','jpeg','jpg'])

    diagnoise_button = st.button('Get diagnosis', key='diagnosis')
    if(diagnoise_button):
        session_state.diagnoise_button = True

        if leaf_img is not None:
            file_details = {"FileName":leaf_img.name,"FileType":leaf_img.type,"FileSize":leaf_img.size}
            st.write(file_details)

            img = load_image(leaf_img)
            st.image(img,width=120)
            #print('Img: ',(np.array(img)))

            st.write(f'You have uploaded a {leaf_age} leaf image for {crop_value} plant')
            st.write(f'Analysing image: ')

            input_arr = tf.keras.preprocessing.image.img_to_array(img)
            input_arr = tf.keras.preprocessing.image.smart_resize(input_arr,(120,120))
            input_arr = np.array([input_arr])  # Convert single image to a batch.
            predictions = model.predict(input_arr)
            print(predictions)
            pred_class = class_names[np.argmax(predictions)]
            print(np.argmax(predictions))
            print(np.max(predictions))
            print(np.sum(predictions))
            session_state.analysis = pred_class
            session_state.analysis_perc = round(np.max(predictions)*100,2)
            st.write('Analysis completed, go to results page')

        else:
            st.write("Please upload leaf image to analyse")


def result():
    if(session_state.rice_nitro_analysis != ''):
        st.write(f"Nitrogen deficiency level for rice leaf: **{session_state.rice_nitro_analysis}**")
        st.write("Confidence: ",session_state.rice_nitro_analysis_perc)
    if(session_state.analysis != ''):
        col1, col2 = st.beta_columns(2)
        symptoms = []

        session_state.stunted = col1.checkbox('stunted growth?')
        session_state.dead_spot = col1.checkbox('Red/Dead spots?')

        session_state.twisted = col2.checkbox('Twisted/Brittle leaves?')
        session_state.yellow = col2.checkbox('General yellowing of new leaves?')

        if session_state.stunted:
            symptoms.append('stunted')
        if session_state.dead_spot:
            symptoms.append('dead_spot')
        if session_state.yellow:
            symptoms.append('yellow')
        if session_state.twisted:
            symptoms.append('twisted')

        session_state.symptoms = symptoms
        st.write("Symptoms recognised: ")
        st.write("Leaf symptoms manual: ",session_state.symptoms)
        st.write("Leaf age state: ",session_state.leaf_age)
        st.write("Leaf symptom based on analysis: ",session_state.analysis)
        st.write("Confidence: ",session_state.analysis_perc)

        deficiencies = []
        #'interveinal', 'margin', 'normal', 'spotty', 'tip'
        #'mature/old','new/young','middle'


        if(session_state.leaf_age == 'mature/old'):
            if(session_state.analysis == 'margin'):
                deficiencies.append('Potassium')
            if(session_state.analysis == 'interveinal'):
                if('dead_spot' in session_state.symptoms):
                    deficiencies.append('Magnesium')

        if(session_state.leaf_age == 'middle'):
            if(session_state.analysis == 'interveinal'):
                if('stunted' in session_state.symptoms):
                    deficiencies.append('Zinc')

        if(session_state.leaf_age == 'new/young'):
            if(session_state.analysis == 'interveinal'):
                deficiencies.append('Iron')
            if(session_state.analysis == 'spotty' or session_state.analysis == 'margin'):
                deficiencies.append('Manganese')
            if(session_state.analysis == 'tip'):
                deficiencies.append('Copper') #CHLOROSIS!!!!
            if('twisted' in session_state.symptoms):
                deficiencies.append('Boron')
            if('yellow' in session_state.symptoms and session_state.analysis != 'interveinal'):
                deficiencies.append('Sulphur')

        session_state.deficiency = deficiencies

        if(session_state.analysis == 'normal'):
            st.write('Leaf image looks healthy :smiley:')
        if(len(deficiencies)>0):
            st.write(f'Nutrient deficiency identified: **{deficiencies}**')
            st.write('Go to fertilizer schedule to get recommendations')


    else:
        st.write("Please submit leaf sample via leaf analysis page to analyse for nutrient deficiencies")


def nitro_rice():
    st.write('Upload image of rice leaf with white background')
    leaf_img = st.file_uploader('Upload leaf image', type=['png','jpeg','jpg'])

    diagnoise_button = st.button('Get diagnosis', key='diagnosis')
    if(diagnoise_button):
        session_state.diagnoise_button = True

        if leaf_img is not None:
            file_details = {"FileName":leaf_img.name,"FileType":leaf_img.type,"FileSize":leaf_img.size}
            st.write(file_details)

            img = load_image(leaf_img)
            st.image(img,width=120)
            #print('Img: ',(np.array(img)))

            st.write(f'Analysing image: ')

            input_arr = tf.keras.preprocessing.image.img_to_array(img)
            input_arr = tf.keras.preprocessing.image.smart_resize(input_arr,(100,100))
            input_arr = np.array([input_arr])  # Convert single image to a batch.

            interpreter.set_tensor(input_details[0]['index'], input_arr)

            interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            output_data = interpreter.get_tensor(output_details[0]['index'])
            print(output_data)
            print(np.argmax(output_data[0]))
            print(np.max(output_data[0]))
            pred_perc = np.max(output_data[0])

            pred = rice_nitro_names[np.argmax(output_data[0])]
            print(pred)
            session_state.rice_nitro_analysis = pred
            session_state.rice_nitro_analysis_perc = round(pred_perc*100,2)


            #predictions = model.predict_proba(input_arr)
            #print(predictions)
            #pred_class = class_names[np.argmax(predictions)]
            #print(np.argmax(predictions))
            #session_state.analysis = pred_class
            st.write('Analysis completed, go to results page')

        else:
            st.write("Please upload leaf image to analyse")

if __name__ == '__main__':
    main()

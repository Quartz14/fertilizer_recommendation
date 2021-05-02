# fertilizer_recommendation
Help gardeners and farmers better care for their plants nutritional needs

## Deployed application: 
    https://share.streamlit.io/quartz14/fertilizer_recommendation/main/first_app.py

CROPS FOCUSSED:
* Rice
* Wheat
* Maize

NUTRIENTS FOCUSSED:
* Potassium
* Magnesium
* Zinc
* Iron
* Manganese
* Copper
* Boron
* Sulphur
* Nitrogen deficiency levels - only for rice

FILES:
* fertilizer.xls - Excel file containing the data on fertilizers. It has 2 pages which needs to be updated with the info collected
* first_app.py - The web application that is view by users
* 200_epoch_97_87_soft.h5 - neural network model for classifying leaf image into 1 of 5 classes ['interveinal', 'margin', 'normal', 'spotty', 'tip']
* plain2model.tflite - neural network model for classifying rice leaf image into 1 of 4 classes based on LCC
* nn_model_basic.ipynb - Jupyter notebook containing code used to train nn model
* SessionState.py - library to allow use of session in application

TO DO:
* Collect info on fertilizers based on stage of crop(Ex: seedling, established, flowering, mature), type of crop (Ex: rice,wheat, maize), per acre for nutrients: 'Potassium', 'Magnesium', 'Zinc', 'Iron', 'Manganese', 'Copper', 'Boron' and 'Sulphur'
* Add images to manual symptoms in results page to make it easier for user
* Further updates upon discussion

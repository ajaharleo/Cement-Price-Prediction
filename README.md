# Compressive strngth prediction of Cement

## Table of Content
  * [Demo](#demo)
  * [Overview](#overview)
  * [Problem Statement](#problem-statement)
  * [Data Description](#data-description)
  * [Technical Aspect](#technical-aspect)

## Demo
Deployment link: [https://concrete-strength-prediction1.herokuapp.com/](https://concrete-strength-prediction1.herokuapp.com/)


<img src="images\project.png" alt="Project UI/UX" />


## Overview
This is End to End machine learning Regression project which takes information related to components in concrete mixture as input and predict the compressive strength of the mixture. The dataset used for model training is from kaggle.Dataset contains 1030 entries of data of various items , 8 independent features of item and 1 sales as output feature.

## Problem Statement:
The quality of concrete is determined by its compressive strength, which is measured 
using a conventional crushing test on a concrete cylinder. The strength of the concrete 
is also a vital aspect in achieving the requisite longevity. It will take 28 days to test 
strength, which is a long period. So, what will we do now? We can save a lot of time and 
effort by using Data Science to estimate how much quantity of which raw material we 
need for acceptable compressive strength.

## Data Description
Cement (component 1) -- quantitative -- kg in a m3 mixture -- Input Variable
Blast Furnace Slag (component 2) -- quantitative -- kg in a m3 mixture -- Input Variable
Fly Ash (component 3) -- quantitative -- kg in a m3 mixture -- Input Variable
Water (component 4) -- quantitative -- kg in a m3 mixture -- Input Variable
Superplasticizer (component 5) -- quantitative -- kg in a m3 mixture -- Input Variable
Coarse Aggregate (component 6) -- quantitative -- kg in a m3 mixture -- Input Variable
Fine Aggregate (component 7) -- quantitative -- kg in a m3 mixture -- Input Variable
Age -- quantitative -- Day (1~365) -- Input Variable
Concrete compressive strength -- quantitative -- MPa -- Output Variable

## Technical Aspect
Every end to end Machine Learning project life cycle has these steps to get the desired output.

1. Data Collections
    - Downloaded [dataset](https://www.kaggle.com/datasets/elikplim/concrete-compressive-strength-data-set) from kaggle.

2. Exploratory Data Analysis
    - Analayse data using Visual and statistical aspects.
        - Our data doesn't have significant amount of outliers.
            <img src="images\outliers.png" alt="FAT_CONTENT" />

        - None of the fearures have highly positive or negative correlations.
            <img src="images\correlation.png" alt="FAT_CONTENT" />

3. Feature Engineering 
    - Data Cleaning 
        - KNN imputer is used to handle missing values 
        - Lable Encoding is used to convert categorical values into numerical values 
        - Outliers checking done by BoxPlot Method
    - Feature Scaling 
        - Standard Scaling operations are applied to scale the data 
4. Feature Selection 
    - Correlation method is used to check internal correlated features.
    - Used RandomForest Feature Importance to select important features  
5. Model Building
    - Trained data using various Machine Learning algorithams.
    - Model Hyperparameter tuning done with GridSearchCV.
    - Models Evaluated with R2 Score and RMSE score.
6. Pipeline 
    Sequence of data preprocessing components is called data pipeline. 
    1. Data Ingestion 
        - Download the data from source, extract it, split into train and test dataset and store in the destination
    2. Data Validation 
        - Validate data so noise data will not come in the piepline 
    3. Data Transformation 
        - Apply Feature Engineering , Feature Selction processes on data and store transformed data into required format/scale. 
    4. Model Trainer 
        - Training the Best model with tuned parameters.
    5. Model Evaluation 
        - Evaluation done by comparing model's accuracy with base accuracy and recent model. 
    6. Model Pusher 
        - If accuracy of trained model is higher than previous deployed model then push model into working.


## Technologies Used
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="Python" width="200"/>
<img src="https://static.tildacdn.com/tild3536-6337-4235-a664-373965303839/evidently_ai_logo_fi.png" alt="evidently" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1200px-Scikit_learn_logo_small.svg.png" alt="sklearn" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/2560px-Pandas_logo.svg.png" alt="pandas" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/NumPy_logo_2020.svg/2560px-NumPy_logo_2020.svg.png" alt="Numpy" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Heroku_logo.svg/2560px-Heroku_logo.svg.png" alt="Heroku" width="350"/>
<img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" alt="docker" width="350"/>
<img src="https://www.parasoft.com/wp-content/uploads/2021/04/CICD_CICD.png" alt="CICD" width="350"/>

=======
# Item_sales_predictions
Full Stack End to End Machine Learning Project with CI/CD Piepline
Working Link : https://concrete-strength-prediction1.herokuapp.com/ 
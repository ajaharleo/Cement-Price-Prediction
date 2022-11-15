# Compressive strngth prediction of Cement

## Table of Content
Demo
Overview
Problem Statement
Data Description
Technical Aspect

## Demo

image.png

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
    . Downloaded data from kaggle.

2. Exploratory Data Analysis
    . Analayse data using Visual and statistical aspects.
        . Our data doesn't have significant amount of outliers.
        image.png

        . None of the fearures have highly positive or negative correlations.
        image.png

        
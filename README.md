# Career Path Analyzer

*Final Undergrad Research - the following is a short version of my final paper*


## Final App
We built the final software artifact using streamlit, a data visualization tool that gave us a lot of
flexibility in showcasing our results.

The first screen has an input field where students can enter their "future job" (this is where our Linear
SVC predicts the text input).
<img width="1052" alt="Screen Shot 2022-05-30 at 6 18 43 PM" src="https://user-images.githubusercontent.com/35783824/171064084-a71d85fd-0e68-4d82-b461-a6f9f0caf867.png">

Once you’ve clicked enter the following results will show up with the member count, average time
in the industry and % with a bachelor. Additionally we have two other sections the Education Stats
and Industry Stats.

<img width="1051" alt="Screen Shot 2022-05-30 at 6 18 59 PM" src="https://user-images.githubusercontent.com/35783824/171064096-4d8472d4-8f94-4da6-a4a3-c111a634cb5b.png">

The education section we showcase the Higher Education level Chart (which is the highest education
level members have in our dataset)

<img width="1054" alt="Screen Shot 2022-05-30 at 6 19 12 PM" src="https://user-images.githubusercontent.com/35783824/171064109-e0e73b9f-9a54-45a0-923c-6913594a36f7.png">

We also see the Popular field of studies amongst professionals.

<img width="1050" alt="Screen Shot 2022-05-30 at 6 19 27 PM" src="https://user-images.githubusercontent.com/35783824/171064128-736b918b-159f-4198-956a-2ad5a80be055.png">

In our Industry Section we can view the popular companies and the skills one must have to be in that
specific industry.

<img width="1052" alt="Screen Shot 2022-05-30 at 6 19 40 PM" src="https://user-images.githubusercontent.com/35783824/171064142-99a7f5f2-bcbb-43fa-ac2a-8cc6a6c91808.png">


## Introduction

This work aims to predict a professional's industry based on a subset of publicly available profiles
from LinkedIn. We utilize certain features from each profile in our data set, for example, the Headline
column, and assess several machine learning models for our prediction task. Furthermore, we explore
pre-built models commonly used for text classification, Bag Of Words, Doc2Vec, and predict the
accuracy of these models by using classic machine learning algorithms such as K-Nearest Neighbor,
Naive base classifier, Linear Support Vector Classification, and Decision Tree. This research aims
to provide a soon-to-be graduate with a breakdown analysis of how professionals went about their
career path after graduation and which skills they've acquired to lead a successful career.


## Data Preparation
The dataset used for this paper is not publicly available online and requires a member to log in.
Today, there is no publicly available dataset containing user profiles from different industries on
LinkedIn. Therefore we built our scraping tool using python to collect more than 100+ profiles from
various sectors. For reference, you can find the scraper app in career-path-analyzer/linkedin-scraper. 
Each python file has a specific purpose in our data processing. Our entry -level file
[main.py](<http://main.py>) is a single function that uses chrome driver (a tool used for simulated
testing).

The program begins by requesting the following questions a user's login information, the industry
containing the profiles, and the city. We simulate the next process. We first log in, and the page
directs us to DuckDuck to begin our search. We then visit each profile based on their industry and
city and call upon the create_sheet function. The following process does three things, transforms the
text values in each LinkedIn profile, merges each item as one, and dumps the data in our google excel
worksheet (our database. See picture on the below).

## Preprocessing

Before getting the data ready to be used for training our machine learning algorithm, we must preprocess our raw dataset. In the 3.0 Background section, we use our text classification models to target
columns such as Headline and Job-Title. Another critical column is "Industry," containing our labels.
Despite the fact we've included the industry as a parameter in our data collection, they are specific
nuances between the employed dates and the headline they've added. Such distinctions are significant
to address before using our dataset. For example, in the Dates-Employed-1 column, we depict that a
profile may be working at a specific location if the timeline is formatted like Aug-2019-Present. If
not, we can use the Headline Column as the professional's current job. We can locate the function
that processes this condition in career-path-analyzer/text-classification/helper.py ->
*def*transform_profession(data_top, data):, which returns a list of the most recent job the
professional has held based on the Dates-Employed-1 == 'Present' then we return the Job-Title-1
column. We then add the newly created list in a DataFrame named profession. 

Before training, our last step is to remove any stop words and punctuations from our recently completed profession table.
In the same file, career-path-analyzer/text-classification/helper.py, we call upon the preprocess_text,
which has four different steps: We remove any punctuations, lowercase all of our words, and split the text with a space.
Next, we download the stop-words from nltk.corpus (a natural language toolkit with useful libraries
for pre-processing) and remove any stop words inside our corpus.
We then call the following method nltk.stem.wordnet.WordNetLemmatizer() removes certain words
in our list, and for example, dogs turn into singular dogs.

Finally, we join the list back into one singular text see image below and create a new column called:
clean_text_professional


## Machine Learning Baseline

In this section, we analyze the various machine learning algorithms baselines that we use to test the
accuracy of our text classification algorithms. We implement the following ML algorithms, Naive
Base Classifier, K-Nearest-Neighbor (KNN), Linear Support Vector Classification (LSVC), and
Decision Tree. Once we process our dataset, we split it into four pieces, X_training, X_testing,
y_training, and y_testing. We use the training and testing set for each ML model. For example, in
our bag-of-words Jupyter notebook, we call upon the sklearn.svm(Linear Support Vector
Classification) method, we then fit (train) the model encapsulating our X_training and y_training as
parameters. Once fit, we predict the model using our X_test variable, which contains a segment of
the pre-process dataset. We then validate the model's prediction by calculating its f1_score, the Fmeasure. 

It is a single-core metric for analyzing the valid optimistic projections in a class.

Another metric we use is the accuracy score, which computes subset accuracy in
which sets of labels must identically correspond to y_true (prediction the model has made). Finally,
we wrap up with the classification report, giving us an overall breakdown analysis of each label's
precision, recall, and f-1 score.

## Discussions and Results

This section will discuss the best-performing text classifier model and its results. We evaluated and
trained each model with 30%-100% of the dataset and found that Bag Of Words overall had the best
accuracy rate. Overall, the Linear Support Vector Classifier performed the best, consistently
averaging 80%. Let's explore why this ML model worked so well; unlike Support Vector Classifier,
LinearSVC uses a linear kernel for the basis function (meaning it is restrictive and much less tunable
as we want a linear interpolation).


<img width="477" alt="Screen Shot 2022-05-30 at 6 12 33 PM" src="https://user-images.githubusercontent.com/35783824/171063702-e9a6e087-7db3-4915-bf27-5630749ea263.png">

Linear Support Vector Classification was the best performing algorithm as it just above averaged
between 70%-80% prediction.



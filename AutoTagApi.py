from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tagPredictor import preprocess, inverseTransform

app = FastAPI()

class TagItems(BaseModel):
    Question: str


model = joblib.load('tagPredictor.pkl')


# df1 = pd.read_csv('output.csv')
# tfidf = TfidfVectorizer(analyzer='word', max_features=40, ngram_range=(1, 3), stop_words='english')
# X = tfidf.fit_transform(df1['title'])
# multilabel = MultiLabelBinarizer()
# y = multilabel.fit_transform(df1['tags'])

@app.post('/recommeded_tags')
async def predict_tags(item: TagItems):
    tags = []
    question_tfidf = preprocess([item.Question])
    yhat = model.predict(question_tfidf)
    predicted_tags = inverseTransform(yhat)
    for tags_tuple in predicted_tags:
        for tag in tags_tuple:
            tags.append(tag)
    return {"Predicted Tags": str(tags)}

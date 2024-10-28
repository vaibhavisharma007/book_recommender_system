from flask import Flask,render_template,request
import pickle
import numpy as np


# Load datasets using 'with' to manage file context
with open("popular.pkl", "rb") as f:
    popular_df = pickle.load(f)

with open("pt.pkl", "rb") as f:
    pt = pickle.load(f)

with open("books.pkl", "rb") as f:
    books = pickle.load(f)

with open("similarity_scores.pkl", "rb") as f:
    similarity_score = pickle.load(f)


app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',book_name=list(popular_df["Book-Title"].values),
                           author=list(popular_df["Book-Author"].values),
                           image=list(popular_df["Image-URL-M"].values),
                           votes=list(popular_df["number_of_ratings"].values),
                           rating=list(popular_df["avg_rating"].values))
@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")
@app.route('/recommend_books',methods=['Post'])
def recommend():
    input = request.form.get('input')  # Get book title from form
    idx=np.where(pt.index == input)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[idx])),key=lambda x:x[1],reverse=True)[0:9]
    data=[]
    for i in similar_items:
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template("recommend.html",data=data)

    

if __name__  ==  "__main__":
    app.run(debug=True)
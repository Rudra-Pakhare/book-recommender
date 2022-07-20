from flask import Flask,render_template,request
import numpy as np
import pickle

popularDf = pickle.load(open('popular.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           bookName = list(popularDf['Book-Title'].values),
                           author=list(popularDf['Book-Author'].values),
                           image=list(popularDf['Image-URL-M'].values),
                           votes=list(popularDf['num_ratings'].values),
                           rating=list(popularDf['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/recommend_books',methods=['post'])
def recommendBook():
    bookName = request.values.get('bookName')
    index = np.where(pt.index == bookName)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        items = []
        temp = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(items)

    return render_template('recommend.html', data = data)


if __name__ == '__main__':
    app.run(debug=True)
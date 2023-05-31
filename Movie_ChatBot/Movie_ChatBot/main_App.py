import re
from bs4 import BeautifulSoup
from lxml import etree
import requests
import tkinter as tk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.stem import WordNetLemmatizer


def scrapeURL(URL):
    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, "html.parser")
    return soup


def get_URL(movieName):
    movieName = re.sub('[^a-zA-Z0-9]', '_', movieName)  # replacing special char with _
    movieName = movieName.replace("__", "_")  # replacing any double _ with a single _
    movieName = movieName.rstrip("_")  # remove the _ at the end of the string if there is one
    movieURL = "https://www.rottentomatoes.com/m/" + movieName
    return movieURL


def getMovieInfo(scraper):
    with open('movie_Info.txt', 'w') as f:
        pass
    #
    dom = etree.HTML(str(scraper))  # construct a tree using the html obtained from the scraper to make searching of
    # certain elements easier
    desc = dom.xpath('//*[@id="movie-info"]/div/div/drawer-more/p/text()')
    print("Saved all movie info to file")
    with open('Desc.txt', 'w') as f:
        pass
    with open('Desc.txt', 'w') as f:
        f.write(desc[0])
    Description = ""
    with open("Desc.txt", "r+") as file:
        for line in file:
            if not line.isspace():
                Description += line.lstrip()
        file.truncate(0)
        file.seek(0)
        file.write(Description)

    list1 = scraper.find("ul", id="info").get_text()
    with open("movie_Info.txt", "a") as file:
        file.write(list1)
    result = ""
    with open("movie_Info.txt", "r+") as file:
        for line in file:
            if not line.isspace():
                result += line.lstrip()
        file.truncate(0)
        file.seek(0)
        file.write(result)

    file_to_Write = ""
    result = ""
    text_files = ["Director.txt", "Distributor.txt", 'Genre.txt', 'gross.txt', 'Original.txt', 'Producer.txt',
                  'rating.txt', 'runtime.txt', 'streaming.txt', 'theater.txt', 'Writer.txt', 'sound.txt']
    for file in text_files:
        with open(file, 'w') as f:
            pass
    print("Distributing information to their relevant file")
    with open("movie_Info.txt", "r+") as file:
        for line in file:
            if line == "Rating:\n":
                result = ""
                file_to_Write = "rating.txt"

            elif line == "Genre:\n":
                try:
                    with open(file_to_Write, "a") as f:
                        f.write(result)
                # Code to write to file goes here
                except FileNotFoundError:
                    continue
                result = ""
                file_to_Write = "Genre.txt"
            elif line == "Original Language:\n":
                try:
                    with open(file_to_Write, "a") as f:
                        f.write(result)
                # Code to write to file goes here
                except FileNotFoundError:
                    continue
                result = ""
                file_to_Write = "Original.txt"
            elif line == "Director:\n":
                try:
                    with open(file_to_Write, "a") as f:
                        f.write(result)
                # Code to write to file goes here
                except FileNotFoundError:
                    continue
                result = ""
                file_to_Write = "Director.txt"
            elif line == "Producer:\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "Producer.txt"
            elif line == "Writer:\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "Writer.txt"
            elif line == "Release Date (Theaters):\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "theater.txt"
            elif line == "Release Date (Streaming):\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "streaming.txt"
            elif line == "Box Office (Gross USA):\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "gross.txt"
            elif line == "Runtime:\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "runtime.txt"
            elif line == "Distributor:\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "distributor.txt"
            elif line == "Production Co:\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "production.txt"
            elif line == "Sound Mix:\n":
                with open(file_to_Write, "a") as f:
                    f.write(result)
                result = ""
                file_to_Write = "sound.txt"
            else:
                result += line

        with open(file_to_Write, "a") as f:
            f.write(result)


# Define the function to be executed when the user clicks the submit button
def submit():
    question = question_entry.get("1.0", "end-1c")

    if question == "/bye":
        exit()
    # Get the values of the user's inputs
    movie_name = movie_entry.get()
    url = get_URL(movie_name)
    print("movie url is " + url)
    htmlScraper = scrapeURL(url)
    print("Website scraped")
    getMovieInfo(htmlScraper)

    # Step 1: Read questions from the file
    with open('movie_Questions.txt', 'r') as file:
        questions = file.readlines()

    # Step 2: Lemmatize the questions
    lemmatizer = WordNetLemmatizer()
    questions = [lemmatizer.lemmatize(question.strip()) for question in questions]
    print("lemmatized the questions")
    # Step 3: Create count vectors for each question in the questions list
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(questions)
    print("Vectorized each question")
    # Step 4: Process user input
    user_input = lemmatizer.lemmatize(question.strip())
    user_input_vector = vectorizer.transform([user_input])
    print("Vectorized and lemmitized the user question")

    if question == "/help":
        answer = "Here are some sample questions:\n- What's the description of " + movie_name + "?\n- Who directed " + movie_name + "?"
        output.delete("1.0", tk.END)
        output.config(width=question_entry["width"], height=question_entry["height"])
        output.insert("1.0", answer)
    elif np.all(user_input_vector.toarray() == 0):
        answer = "Sorry, I don't get that! Try again"
        output.delete("1.0", tk.END)
        output.config(width=question_entry["width"], height=question_entry["height"])
        output.insert("1.0", answer)
    else:
        # Step 6: Calculate cosine similarity with all questions
        similarities = cosine_similarity(user_input_vector, X)
        closest = np.argmax(similarities)
        ans = ""

        if closest == 0 or closest == 1 or closest == 2 or closest == 3:
            with open("Desc.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 4 or closest == 5 or closest == 6 or closest == 7 or closest == 8 or closest == 9:
            with open("rating.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 10 or closest == 11 or closest == 12 or closest == 13:
            with open("Genre.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 14 or closest == 15 or closest == 16 or closest == 17:
            with open("Original.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 18 or closest == 19 or closest == 20 or closest == 21:
            with open("Director.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 22 or closest == 23 or closest == 24:
            with open("Producer.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 25 or closest == 26 or closest == 27 or closest == 28:
            with open("Writer.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 29 or closest == 30 or closest == 31 or closest == 32:
            with open("theater.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 33 or closest == 34 or closest == 35 or closest == 36:
            with open("streaming.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 37 or closest == 38 or closest == 39 or closest == 40:
            with open("gross.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 41 or closest == 42 or closest == 43 or closest == 44:
            with open("runtime.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 45 or closest == 46 or closest == 47 or closest == 48:
            with open("distributor.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 49 or closest == 50 or closest == 51 or closest == 52:
            with open("production.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        elif closest == 53 or closest == 54 or closest == 55 or closest == 56:
            with open("sound.txt", "r+") as f:
                this_List = f.readlines()
                ans = ""
                for line in this_List:
                    ans += line
        output.delete("1.0", tk.END)
        output.config(width=question_entry["width"], height=question_entry["height"])
        output.insert("1.0", ans)


# Create a new Tkinter window
window = tk.Tk()

# Set the initial size of the window
window.geometry("500x400")

# Create a label for the movie name input field
movie_label = tk.Label(window, text="Movie name:")
movie_label.pack()

# Create a text entry field for the movie name input
movie_entry = tk.Entry(window)
movie_entry.pack()

# Create a label for the question input field
question_label = tk.Label(window, text="Question:\nEnter /help for questions\nEnter /bye to exit")
question_label.pack()

# Create a text entry field for the question input
question_entry = tk.Text(window, width=50, height=3)
question_entry.pack()

# Create a label for the output area
output_label = tk.Label(window, text="Answer:")
output_label.pack()

# Create a text output area for the answer
output = tk.Text(window, width=50, height=3)
output.pack()

# Create a button to submit the user input and trigger the processing function
submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.pack()

# Start the main event loop
window.mainloop()

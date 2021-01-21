# Design #

Key facts:
* The requirements for bookmarkable turns, sharing, and no attached storage necessitate that the application store all the required data to play the game in the URL.
* The requirement for security necessitates that this data be encoded.
* The requirement for undo necessitates that the required information be stored sequentially, so it is easy to move backward through the game. 

The following data must all be present or able to be derived from the URL:
* The current word, as well as previous words from this session
* Letters (or a word) guessed, and the number of guesses remaining (derived based on the current word and letters guessed)

The URL structure will be as follows:
* List of previous words played in this session. Each word is represented by its index in the word list (see below). 
* Current word, also represented by the index in the word list. 
* List of letters or a word guessed. Each guess will be separated by a comma to differentiate letter guesses from word guesses. 

Word Lookup Table:
```
["FINESSE", "WHITMAN", "TACONY", "VECCHIO", "PALMYRA", "GOLDEN", "BRIDGE", "NARROWS", "BIFROST"]
```

In order to prevent users from seeing anything about the game from the URL, this data is encoded using a simple scheme that transforms each character of the URL using the numerical value of the corresponding character in a secret key environment variable stored on the server. This basic scheme is obviously not perfectly secure, however I felt that this scheme was adequate given the limited development time for the application and that the data protected is not sensitive. 
<br><br>
The example below shows the decoded and (example) encoded URL strings corresponding to the third word in a session with the letter guesses E, T, A, O, I and a word guess of BRIDGE:
<br><br>
25-7-E,T,A,O,BRIDGE,I
<br><br>
2PCMD0,23T3WTHJV5OYP1
<br><br>
This data is stored in the URL (after the /session/) and meets all the requirements outlined above. 

# Meeting Requirements #

1. All rules are captured in the application logic.
2. The new game button makes a POST request to the /session/{session_data}/games endpoint, triggering the application to select a new word. 
3. All game data is stored in the URL. Bookmarking a particular URL will save a snapshot of that turn.
4. As above, all game data is stored in the URL. Sending someone the URL will allow them to pick up the game at that point (without affecting another ongoing game). 
5. The undo button makes a POST request to the /session/{session_data}/undo endpoint, which removes a previous guess or goes back to the previous word if there are no guesses. 
6. The game will run in any web browser. 
7. The data in the URL is encoded (see "Design" above) for security. 
8. The application can be run using the included Dockerfile (see "Running The Application").
9. The application uses only Flask and pytest. 

# Running The Application #

To run the backend application, you must have Docker installed. Below are sample instructions for Ubuntu to create a new image from the Dockerfile and run the application.
<br><br>
Launch a terminal window in the same directory as this README file and create a new Docker image from the Dockerfile (here I named named it "hangman" - feel free to use whatever you want):

```
docker build -t hangman .
```

Then launch the docker image using the name provided above:

```
docker container run -ti hangman /bin/sh
```

Once the image loads, you will need to provide a secret key for the application to use. The below command will generate a random 100 character key:

```
export HANGMAN_KEY=$(tr -dc A-Z0-9,- </dev/urandom | head -c 100)
```

Then, you can start Flask's development server with the below command: 

```
flask run
```

Navigate to http://127.0.0.1:5000 to demo the application.
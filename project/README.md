# mines

## Setup Instructions

Note that I used Python 3.7.0 for this project.

From the root directory:
Install python requirements (preferably in an isolated environment)
`pip install -r project/requirements.py`

Install all front-end requirements
`npm install`

For web-sockets to work, I used Redis on port 6379.
For this, I used Docker.
`docker run -p 6379:6379 -d redis:2.8`

Run DB migrations:
`python project/manage.py migrate`

For dev purposes, I set up webpack to run in watch mode.
`npm run dev`
Run Django's dev server as well
`python project/manage.py runserver`

Navigate to `localhost:8000` and enjoy!


## Some notes, and a retrospective

I haven't had the chance to play with React in a very long time, so this came as a welcomed opportunity to do so. From the get-go, I knew that I also wanted to get this working with web sockets, so that the game could be loosely played in multiplayer.

I spent a few days researching various technologies that I've never worked with before, or in a very long time. My research lead me to a number of articles on async Python/Django, Channels, React, Redux and WebSockets. It was quite enlightening, though overwhelming at times.

I designed the back-end first. I spent an evening considering how I would approach building the board, storing it, and tracking changes. I slept on it one night, and decided to simply represent it as a 2D array, stored as JSON on the model.

This ended up working well. With a few properties for easily accessing it, I was happy with how robust the solution turned out to be. I was also happy with my decision to separate Room and Game as two models. In retrospect, I certainly would not have named any model properties "state", had I worked with React recently, especially since I also had game state. Things got a bit confusing at the end, but it still worked out OK.

I'm quite happy with the finished product. It plays well, and relatively smoothly. There's slight delay when playing with larger grids. Perhaps with time, better algorithms could be made to flip tiles. One thing that I thought of at the end, was that I should've stored the locations of the bombs after setting them. This would've allowed me to know exactly where they were based on their coordinates, without having to do as much traversal of the grid. A good lesson for next time, keep track of your important facts!

With some additional time, I would've liked to use Redux as the state manager for my React app. I really wanted to use this, but I decided to drop it due to time, and in favour of doing it the manual way, and learning my lessons.

I also would've liked to add some safeguards for the multiplayer game. For larger puzzles, it is possible to have a race condition where a player attempts to flip a tile, while tile-flipping is already happening.

Next, I would've rebuilt the room list with sockets, to keep it fully in-sync, as the game is. It certainly did the trick as is, but it would've been nice.

Lastly, I would've built some tests for both the front, and back ends. I still intend to do this to get a chance to see it through, but I simply ran out of time to do it before submission.

## Resources Used:
Channels Tutorial: https://channels.readthedocs.io/en/latest/tutorial/part_1.html
Django and React: https://www.valentinog.com/blog/tutorial-api-django-rest-react/
React Tutorial: https://reactjs.org/tutorial/tutorial.html

Even though I didn't end up using Redux, the docs still gave me a lot of insight.
Redux tutorial docs: https://redux.js.org/introduction and https://redux.js.org/advanced

Many StackOverflow threads for various roadblocks encountered, et al.

This article on colours used for Minesweeper numbers: https://www.sporcle.com/games/patrickstar92/minesweeper_colors/results

Cheers!
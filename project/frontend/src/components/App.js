import React from 'react';
import ReactDOM from 'react-dom';
import RoomList from './RoomList';
import GameRoom from './game/GameRoom';
import {
    BrowserRouter as Router,
    Route,
} from 'react-router-dom'

const App = () => (
    <Router>
        <div className='col-md-12'>
            <h1>Minesweeper</h1>
            <Route exact path='/' component={RoomList}/>
            <Route exact path='/game/:id' component={GameRoom}/>
        </div>
    </Router>
);

const wrapper = document.getElementById('app');
wrapper ? ReactDOM.render(<App />, wrapper) : null;
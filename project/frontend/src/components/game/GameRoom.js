import React, { Component } from 'react';
import Game from './Game';
import fetch from 'cross-fetch';
import {Link} from 'react-router-dom'


class GameRoom extends Component {
    constructor(props) {
        super(props);

        this.squareClicked = this.squareClicked.bind(this);
        this.updateGameState = this.updateGameState.bind(this);
    }

    state = {
        socket: null,
        data: null,
        loaded: false,
        placeholder: 'Loading...',
    }

    componentDidMount() {
        const game_id = this.props.match.params.id;
        const endpoint = ['/api/mines/game/', game_id, '/'].join('');

        fetch(endpoint)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({ placeholder: 'Something went wrong' });
                }
                return response.json();
            }).then(data => {
                const socket_endpoint = ['ws://', window.location.host, '/ws/game/', game_id, '/'].join('');
                const socket = new WebSocket(socket_endpoint)

                socket.onmessage = this.updateGameState;

                this.setState({socket, data, loaded: true})
            })
    }

    componentWillUnmount() {
        const socket = this.state.socket;
        socket.close();
    }

    squareClicked(x, y) {
        const socket = this.state.socket;
        socket.send(JSON.stringify({game_id: this.props.match.params.id, x, y}))
    }

    updateGameState(response) {
        const current_state = this.state.data;
        const data = JSON.parse(response.data);
        const {obscured_game_state, state} = data;

        this.setState({data: Object.assign({}, current_state, {
            obscured_game_state, state
        })});
    }

    render() {
        if (!this.state.loaded) {
            return (
                <p>{this.state.placeholder}</p>
            )
        }

        return (
            <React.Fragment>
                <div className='col-md-12 go-back'>
                    <Link to='/'>Back to Room List</Link>
                </div>
                <div className='col-md-12 room-name text-center'>
                    <h3>{this.state.data.room_name}</h3>
                </div>
                <Game gameId={this.props.match.params.id}
                    gameState={JSON.parse(this.state.data.obscured_game_state)}
                    state={this.state.data.state}
                    onClick={this.squareClicked}
                />
            </React.Fragment>
        )
    }
}

export default GameRoom;
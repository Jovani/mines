import React, { Component } from 'react';

class GameAwareComponent extends Component {
    constructor(props) {
        super(props);

        this.gameIsOpen = this.gameIsOpen.bind(this);
        this.gameIsWon = this.gameIsWon.bind(this);
        this.gameIsLost = this.gameIsLost.bind(this);
    }

    gameIsOpen() {
        return this.props.state === 'open';
    }

    gameIsWon() {
        return this.props.state === 'won';
    }

    gameIsLost() {
        return this.props.state === 'lost';
    }
}

export default GameAwareComponent;
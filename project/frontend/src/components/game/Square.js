import React, { Component } from 'react';
import PropTypes from 'prop-types';
import GameAwareComponent from './GameAwareComponent';
import Game from './Game';

const Bomb = () => <i className='fas fa-bomb'></i>
const Peace = () => <i className='fas fa-hand-peace'></i>

class Square extends GameAwareComponent {
    constructor(props) {
        super(props);

        this.getValue = this.getValue.bind(this);
        this.canFlip = this.canFlip.bind(this);   
    }

    getValue() {
        const value = this.props.data.value;
        const flipped = this.props.data.flipped;

        // The buttons were displaying weirdly when empty. Giving them an arbitrary value helped.
        if (!flipped) return <React.Fragment>&nbsp;</React.Fragment>;

        // Give the player a little indicator if they've won.
        if (value === -1) {
            if (this.gameIsWon()) return <Peace />;
                
            return <Bomb />;
        }

        const className = `square-value value-${value}`
        return <span className={className}>{value}</span>
    }

    canFlip() {
        return (
            this.gameIsOpen() &&
            !this.props.data.flipped
        )
    }

    render() {
        return <button className='square'
                       onClick={
                           () => this.canFlip()
                               ? this.props.onClick(this.props.x, this.props.y)
                               : null
                       }
        >
            {this.getValue()}
        </button>
    }
}

Square.propTypes = {
    data: PropTypes.object.isRequired,
    x: PropTypes.number.isRequired,
    y: PropTypes.number.isRequired,
    state: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired
}

export default Square;
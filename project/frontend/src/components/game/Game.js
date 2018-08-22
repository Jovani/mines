import React from 'react';
import Square from './Square';
import GameAwareComponent from './GameAwareComponent';
import PropTypes from 'prop-types';


class Game extends GameAwareComponent {
    pickRandomMessage() {
        const messages = [
            'You can do it!',
            "Don't give up!",
            'The cake is a lie',
            'The tension is killing me!',
            'So a mine walks into a bar, and...',
            '"Mine!" - the Seagulls, Finding Nemo',
            'How many mines could a minesweeper find, if a minesweeper could find mines?',
        ]

        return messages[Math.floor(Math.random() * messages.length)];
    }

    pickRandomLossMessage() {
        const messages = [
            "Oh no, don't pick that one!",
            'Aiiiiiii!',
            'Kaboom!!!',
            'Dang. Better luck next time.',
            'No! Your other left!!',
            ':(',
            'No soup for you!',
        ]

        return messages[Math.floor(Math.random() * messages.length)];
    }

    pickRandomWinMessage() {
        const messages = [
            "Wooooooooo!",
            'Success!',
            'You did it!',
            'Congradulations!',
            'Phew, that was stressful!',
            ':D',
        ]

        return messages[Math.floor(Math.random() * messages.length)];
    }

    render() {
        const {gameState, onClick, state} = this.props;

        return (
            <React.Fragment>
                <div className='col-md-12'>
                    {(() => {
                        if (this.gameIsOpen()) return (
                            <div className='alert alert-info text-center'>
                                {this.pickRandomMessage()}
                            </div>
                        )

                        if (this.gameIsLost()) return (
                            <div className='alert alert-danger text-center'>
                                Loss - {this.pickRandomLossMessage()}
                            </div>
                        )

                        if (this.gameIsWon()) return (
                            <div className='alert alert-success text-center'>
                                Win - {this.pickRandomWinMessage()}
                            </div>
                        )
                    })()}
                </div>
                <div className='col-md-12 game-board'>
                    {gameState.map(
                        (row, x) => <div key={x} className='square-row'>
                            {row.map(
                                (square_data, y) => <Square key={y} data={square_data} x={x} y={y} state={state} onClick={onClick} />
                            )}
                        </div>
                    )}
                </div>
            </React.Fragment>
        )
    }
}

export default Game;
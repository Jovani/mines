import React, { Component } from 'react';
import PropTypes from 'prop-types';
import RoomTableContainer from './RoomTableContainer';
import CreateRoomForm from './CreateRoomForm'

class RoomList extends Component {
    constructor(props) {
        super(props);

        this.goToGame = this.goToGame.bind(this);
    }

    goToGame(game_id) {
        this.props.history.push('game/' + game_id);
    }

    render() {
        return (
            <React.Fragment>
                <div className='row'>
                    <div className='col-md-12'>
                        <RoomTableContainer endpoint={'api/mines/rooms/open/'}
                                            onClick={this.goToGame}
                        />
                    </div>
                </div>
                <div className='row'>
                    <CreateRoomForm onCreate={this.goToGame}/>
                </div>
            </React.Fragment>
        )
    }
}

RoomList.propTypes = {
    history: PropTypes.object.isRequired
}

export default RoomList;
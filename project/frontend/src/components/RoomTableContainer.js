import React, { Component } from 'react';
import PropTypes from 'prop-types';
import fetch from 'cross-fetch';

import RoomTable from './RoomTable';


class RoomTableContainer extends Component {
    state = {
        data: [],
        loaded: false,
        placeholder: 'Loading...'
    };

    componentDidMount() {
        fetch(this.props.endpoint)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({ placeholder: 'Something went wrong' });
                }
                return response.json();
            })
            .then(data => this.setState({ data: data, loaded: true }));
    }

    render() {
        const { data, loaded, placeholder } = this.state;

        return loaded
            ? <RoomTable data={data} onClick={this.props.onClick} />
            : <p>{placeholder}</p>;
    }
}

RoomTableContainer.propTypes = {
    endpoint: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired
}

export default RoomTableContainer;
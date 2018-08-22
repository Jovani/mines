import React, {Component} from 'react';
import fetch from 'cross-fetch';
import PropTypes from 'prop-types';


class CreateRoomForm extends Component {
    constructor(props) {
        super(props);

        const SIZE_MIN = 1;
        const SIZE_MAX = 30;

        const DIFFICULTY_CHOICES = {
            'easy': 'Easy',
            'medium': 'Medium',
            'hard': 'Hard',
        };

        const ENDPOINT = 'api/mines/rooms/';

        this.constants = {
            grid_size: {min: SIZE_MIN, max: SIZE_MAX},
            difficulty: DIFFICULTY_CHOICES,
            endpoint: ENDPOINT,
        }

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleInputValidation = this.handleInputValidation.bind(this);
        this.validateInput = this.validateInput.bind(this);
    }

    // A default state. Ideally we'd fetch this and restrictions from the server.
    // For the sake of simplicity, this will do.
    state = {
        name: '',
        state: 'open',
        grid_size: 10,
        difficulty: 'medium',
        error: '',
        name_error: false,
    }

    handleSubmit(event) {
        event.preventDefault();
        const {name, grid_size, difficulty} = this.state;

        fetch(this.constants.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;',
            },
            body: JSON.stringify({
                name, grid_size, difficulty
            }),
        }).then(response => {
            if (response.status !== 200) {
                return this.setState({ error: "Something went wrong, please try again. Ensure that you've given the new room a name."});
            }

            return response.json();
        }).then(data => {
            if (!data) return;

            const parsed_data = JSON.parse(data);
            this.props.onCreate(parsed_data.id);
        })
        
    }

    handleInputChange(event) {
        const {name, value} = event.target;
    
        this.setState({
            [name]: value
        });
    }

    handleInputValidation(event) {
        const {name, value} = event.target;

        const validated_value = this.validateInput(name, value)

        this.setState({
            [name]: validated_value
        });
    }

    validateInput(name, value) {
        switch (name) {
            case 'grid_size':
                if (value > 30) return 30;
                if (value < 1) return 1;
                return value;

            case 'name':
                this.setState({name_error: value.length === 0})
            default:
                return value;
        }
    }

    render() {
        return (
            <React.Fragment>
                {
                    this.state.error.length
                        ? <div className='col-md-12'>
                              <div className='alert alert-danger text-center'>
                                  {this.state.error}
                              </div>
                          </div>
                        : null
                }
                
                <div className='col-md-12'>
                    <h3>Start a new game:</h3>
                    <form onSubmit={this.handleSubmit}>
                        <div className='row'> 
                            <div className='col-md-4'>
                                <label htmlFor='room-name'>Room Name:</label>
                                <input type='text'
                                    name='name'
                                    id='room-name'
                                    className='form-control'
                                    value={this.state.name}
                                    onChange={this.handleInputChange}
                                    onBlur={this.handleInputValidation}
                                />
                                {this.state.name_error
                                    ? <small id='name-error' className='form-text text-danger'>
                                        You need to give your game room a name.
                                    </small>
                                    : null
                                }
                                
                            </div>

                            <div className='col-md-4'>
                                <label htmlFor='grid-size'>Grid Size:</label>
                                <input type='number'
                                    name='grid_size'
                                    id='grid-size'
                                    className='form-control'
                                    value={this.state.grid_size}
                                    min={this.constants.grid_size.min}
                                    max={this.constants.grid_size.max}
                                    onChange={this.handleInputChange}
                                    onBlur={this.handleInputValidation}
                                />
                                <small id='grid-size-help' className='form-text text-muted'>
                                    Enter a number from 1 to 30, inclusive. This will be the length and width of the game grid.
                                </small>
                            </div>

                            <div className='col-md-4'>
                                <label htmlFor='difficulty'>Difficulty:</label>
                                <select name='difficulty'
                                        id='difficulty'
                                        className='form-control'
                                        value={this.state.difficulty}
                                        onChange={this.handleInputChange}
                                        onBlur={this.handleInputValidation}
                                >
                                    {Object.entries(this.constants.difficulty).map(
                                        ([key, verbose]) => (
                                            <option key={key} value={key}>{verbose}</option>
                                        )
                                    )}
                                </select>
                            </div>

                            <div className='col-md-12'>
                                <input type='submit' value='Start Game' className='btn btn-success float-right' />
                            </div>
                        </div>
                    </form>
                </div>
            </React.Fragment>
        )
    }
}

CreateRoomForm.propTypes = {
    onCreate: PropTypes.func.isRequired
};

export default CreateRoomForm;

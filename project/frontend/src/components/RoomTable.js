import React from 'react';
import PropTypes from 'prop-types';


const RoomTable = ({ data, onClick }) => {
    return (
        <div className='room-table'>
            <h3>
                {data.length} Open Games
            </h3>
            <table className='table table-hover'>
                <thead className='thead-dark'>
                    <tr>
                        <th>Room</th>
                        <th>Grid Size</th>
                        <th>Difficulty</th>
                    </tr>
                </thead>
                {
                    data.length
                        ? (
                            <tbody>
                                {data.map(item => (
                                    <tr key={item.id} onClick={() => onClick(item.game_id)}>
                                        <td>{item.name}</td>
                                        <td>{item.grid_size} x {item.grid_size}</td>
                                        <td>{item.difficulty}</td>
                                    </tr>
                                ))}
                            </tbody>
                          )
                        : null
                }
            </table>
            {
                !data.length
                    ? (
                        <div className='col-md-12 text-center'>
                            <p>There are currently no open rooms. Start a new game, below. Good luck!</p>
                        </div>
                      )
                    : null
            }
        </div>
    )
}

RoomTable.propTypes = {
    data: PropTypes.array.isRequired,
    onClick: PropTypes.func.isRequired
};

export default RoomTable;
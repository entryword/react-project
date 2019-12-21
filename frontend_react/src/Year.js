import React from 'react';

function Year(props) {
    return (
        <select
            className="form-control search-year"
            id="year"
            value={props.value}
            onChange={props.onChange}
            onBlur={props.onBlur}>
            <option key="2015" value="2015">
                2015
            </option>
            <option key="2016" value="2016">
                2016
            </option>
            <option key="2017" value="2017">
                2017
            </option>
            <option key="2018" value="2018">
                2018
            </option>
            <option key="2019" value="2019">
                2019
            </option>
            <option key="2020" value="2020">
                2020
            </option>
        </select>
    );
}

export default Year;

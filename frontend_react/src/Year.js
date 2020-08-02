import React from 'react';

const thisYear = new Date().getFullYear();
let yearArr = [];
for (var i = 2015; i <= thisYear; i++) {
    yearArr.push(i);
}

function Year(props) {
    return (
        <select
            className="form-control search-year"
            id="year"
            value={props.value}
            onChange={props.onChange}
            onBlur={props.onBlur}
            disabled={props.disabledTime}>
            >
            {yearArr.map(year => (
                <option key={year} value={year}>
                    {year}
                </option>
            ))}
        </select>
    );
}

export default Year;

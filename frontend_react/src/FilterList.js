import React, { Component } from 'react';

class FilterList extends Component {
    render() {
        const { filters, definitions, handleFilterReset } = this.props;
        return (
            <div className="filter-view">
                <i className="fa fa-filter" />
                {Object.keys(filters).map((key, index) => (
                    <span key={`${key}${index}`}>
                        {filters[key].length > 0 && (
                            <span key={`${key}${index}`}>
                                {key.toUpperCase()}:
                                {filters[key].map((f, index) =>
                                    key !== 'place'
                                        ? `${definitions[key][f]}${
                                              index !== filters[key].length - 1
                                                  ? '+'
                                                  : ''
                                          }`
                                        : f
                                )}
                                ::
                            </span>
                        )}
                    </span>
                ))}
                <i className="fa fa-times" onClick={handleFilterReset} />
            </div>
        );
    }
}

export default FilterList;

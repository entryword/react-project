import React, { Component } from 'react';

class FilterList extends Component {
    isFilterEmptry = filters => {
        const checkedFilters = Object.keys(filters).filter(key => {
            return filters[key].length > 0;
        });
        return checkedFilters.length > 0;
    };
    render() {
        const { filters, definitions, handleFilterReset } = this.props;
        return (
            <React.Fragment>
                {this.isFilterEmptry(filters)}
                {this.isFilterEmptry(filters) && (
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
                                                      index !==
                                                      filters[key].length - 1
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
                        <i
                            className="fa fa-times"
                            onClick={handleFilterReset}
                        />
                    </div>
                )}
            </React.Fragment>
        );
    }
}

export default FilterList;

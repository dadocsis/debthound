import React from "react";
import MultiSelect from "@khanacademy/react-multi-select";

const COLORS = {
    RED: 'red',
    GREY: 'grey',
    GREEN: 'green',
    BLUE: 'blue',
    YELLOW: 'yellow',
    TEAL: 'teal',
    WHITE: 'white',
    BLACK: 'black'
};

const colorMap = {
    'blue': 'badge-primary',
    'grey': 'badge-secondary',
    'green': 'badge-success',
    'red': 'badge-danger',
    'yellow': 'badge-warning',
    'teal': 'badge-info',
    'white': 'badge-light',
    'black': 'badge-dark'
};

const getColorClass = (color) => colorMap[color];

const Label = props => {
    const {options} = props;
    let deleteButtonStyle = "btn btn-secondary btn-sm float-right";
    let deleteButtonText = 'delete'
    let style = 'd-flex justify-content-between';

    if (options && options.deleteStyle === 'compact'){
        deleteButtonStyle = "btn btn-sm t-back p-0";
        deleteButtonText = (<i className="far fa-times-circle"></i>)
        style = 'd-flex'
    }

    function deleteHandler(e) {
        if (props.deleteLabel){
            props.deleteLabel(props.label.toJS())
        }
    }
    if (options && options.deleteStyle === 'compact'){
        return (<div className={style}>
        <span className={"badge badge-pill " + getColorClass(props.label.get('description'))}>{props.label.get('name')}
            <button type="button" className={deleteButtonStyle} onClick={deleteHandler}>{deleteButtonText}</button>
        </span>

    </div>);
    }

    return (<div className={style}>
        <span className={"badge badge-pill " + getColorClass(props.label.get('description'))}>{props.label.get('name')}
        </span>
        <button type="button" className={deleteButtonStyle} onClick={deleteHandler}>{deleteButtonText}</button>

    </div>);
};

class MyMultiSelect extends React.Component {

    constructor(props) {
        super(props);
        if (this.props.selected){
            this.state = {selected: this.props.selected}
        }
        else {
            this.state = {selected: [],}
        };
    }

    handleSelectedChanged(selected) {
        this.setState({selected});
        if (this.props.myChangeHandler){
            this.props.myChangeHandler(selected)
        }

    }

    handleApplyMultiSelect(){
        if (this.props.myApplyHandler){
            this.props.myApplyHandler(this.state.selected)
        }
    }

    // componentDidMount() {
    //     this.setState({selected: this.props.selected || []})
    // }

    render() {
        const {
            ItemRenderer,
            options,
            selectAllLabel,
            valueRenderer,
            isLoading,
            disabled,
            disableSearch,
            filterOptions,
            overrideStrings,
            overrideOptions
        } = this.props;
        const {selected} = this.state;

        return <div>
            <MultiSelect
                options={options}
                onSelectedChanged={this.handleSelectedChanged.bind(this)}
                selected={selected}
                valueRenderer={valueRenderer}
                ItemRenderer={ItemRenderer}
                selectAllLabel={selectAllLabel}
                isLoading={isLoading}
                disabled={disabled}
                disableSearch={disableSearch}
                filterOptions={filterOptions}
                overrideStrings={overrideStrings}
            />
            { overrideOptions && overrideOptions.showSubmitChangeButton &&
            <button type="button" className="btn btn-primary float-right"
                    onClick={this.handleApplyMultiSelect.bind(this)}>Filter</button>}
        </div>

    }
}

const ordinal_suffix_of = (i) => {
    let j = i % 10,
        k = i % 100;
    if (j == 1 && k != 11) {
        return i + "st";
    }
    if (j == 2 && k != 12) {
        return i + "nd";
    }
    if (j == 3 && k != 13) {
        return i + "rd";
    }
    return i + "th";
};


const WEEKDAYS = ['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun']

const getDayOfWeek = (dayint) => WEEKDAYS[dayint];

export {
    COLORS,
    getColorClass,
    MyMultiSelect,
    Label,
    ordinal_suffix_of,
    WEEKDAYS,
    getDayOfWeek
}
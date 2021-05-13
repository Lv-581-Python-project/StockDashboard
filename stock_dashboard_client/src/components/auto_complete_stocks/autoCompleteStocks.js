import React, {Component} from 'react';
import axios from 'axios';
import Checkbox from '@material-ui/core/Checkbox';
import TextField from '@material-ui/core/TextField';
import Autocomplete, {createFilterOptions} from '@material-ui/lab/Autocomplete';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small"/>;
const checkedIcon = <CheckBoxIcon fontSize="small"/>;

export default class CheckboxesTags extends Component {
    state = {stock_options: [], activeOptions: [], showOptions: false,inputOption: {name:"",company_name: ""}}
    handleOnChange = (event, value) => {
        this.props.setStocks(value);
    }

    filterOptions = createFilterOptions({
        matchFrom: 'start',
        stringify: option => option,
    });

    handleOnInputChange = (event, value, reason) => {
        console.log(value);
        // console.log(reason);
        this.setState({inputOption:{name:value,company_name:value}})
        this.setState({
            activeOptions: this.state.stock_options.filter(option => {
                // console.log(option);
                return (option.name.toLowerCase().startsWith(value.toLowerCase()) ||
                    option.company_name.toLowerCase().startsWith(value.toLowerCase()))
            })
        })
        this.setState({showOptions: value.length >= 1})

    }

    componentWillMount() {
        axios({
            method: 'get',
            url: 'http://localhost:5000/api/stocks/',
            config: {headers: {'Content-Type': 'application/json'}}
        }).then(response => this.setState({stock_options: response.data}))
            .catch(errors => console.log(errors))
    }

    render() {
        const options=this.state.showOptions ? this.state.activeOptions.slice(0, 100): this.state.stock_options.slice(0, 50)
        this.state.inputOption.name.length>1 && options.unshift(this.state.inputOption)
        console.log(options)
        return (
            <Autocomplete
                multiple
                id="checkboxes-tags-demo"
                options={options}
                disableCloseOnSelect
                disableListWrap
                getOptionLabel={(option) => option.name}
                // filterOptions={this.filterOptions}
                onChange={this.handleOnChange}
                onInputChange={this.handleOnInputChange}
                style={{width: "40vw"}}
                renderOption={(option, {selected}) => (
                    <React.Fragment>
                        <Checkbox
                            icon={icon}
                            checkedIcon={checkedIcon}
                            style={{marginRight: 8,}}
                            checked={selected}

                        />
                        {option.name + " " + option.company_name}
                    </React.Fragment>
                )}

                renderInput={(params) => {
                    return (
                        <TextField {...params} variant="outlined" label="Stocks" placeholder="Favorites"/>
                    )
                }}
            />
        );
    }
}

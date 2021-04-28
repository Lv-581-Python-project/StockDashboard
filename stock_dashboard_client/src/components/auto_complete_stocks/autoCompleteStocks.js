import React, {Component} from 'react';
import axios from 'axios';
import Checkbox from '@material-ui/core/Checkbox';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small"/>;
const checkedIcon = <CheckBoxIcon fontSize="small"/>;

export default class CheckboxesTags extends Component {
    state = {stock_options:[]}
    handleOnChange = (event, value) => {
        this.props.setStocks(value);
    }
    componentWillMount(){
        axios({
            method: 'get',
            url: 'http://localhost:5000//api/stocks/',
            config: { headers: { 'Content-Type': 'application/json' } }
        }).then(response => this.setState({stock_options:response.data}))
            .catch(errors => console.log(errors))
    }
    render() {
        return (
            <Autocomplete
                multiple
                id="checkboxes-tags-demo"
                options={this.state.stock_options}
                disableCloseOnSelect
                disableListWrap
                getOptionLabel={(option) => option.name }
                onChange={this.handleOnChange}
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

// Top 100 films as rated by IMDb users. http://www.imdb.com/chart/top
const top100Films = [
    {stock_id: 1, name: 'IBM', companyName: 'IBM'},
    {stock_id: 2, name: 'AAPL', companyName: 'Apple'},
    {stock_id: 3, name: 'GOOGL', companyName: 'Google'},
    {stock_id: 4, name: 'B', companyName: 'Barnes Group Inc.'},
    {stock_id: 5, name: 'BA', companyName: 'The Boeing Company'},
    {stock_id: 6, name: 'BMRA', companyName: 'Biomerica, Inc.'},
    {stock_id: 7, name: 'BNL', companyName: 'Broadstone Net Lease, Inc.'},
    {stock_id: 8, name: 'BLUWU', companyName: 'Blue Water Acquisition Corp.'},
    {stock_id: 9, name: 'BPTS', companyName: 'Biophytis SA'},
    {stock_id: 10, name: 'BTNB', companyName: 'Bridgetown 2 Holdings Limited'},
    {stock_id: 11, name: 'BQ', companyName: 'Boqii Holding Limited'},
    {stock_id: 12, name: 'BENEW', companyName: 'Benessere Capital Acquisition Corp.'},
    {stock_id: 13, name: 'BOACU', companyName: 'Bluescape Opportunities Acquisition Corp.'},
    {stock_id: 14, name: 'C', companyName: 'Citigroup Inc.'},
    {stock_id: 15, name: 'CBAHU', companyName: 'CBRE Acquisition Holdings, Inc.'},
    {stock_id: 16, name: 'CAP-UN', companyName: 'Capitol Investment Corp. V'},
    {stock_id: 17, name: 'CPTKU', companyName: 'Crown PropTech Acquisitions'},
    {stock_id: 18, name: 'CLAAU', companyName: 'Colonnade Acquisition Corp. II'},
    {stock_id: 19, name: 'CCVIU', companyName: 'Churchill Capital Corp VI'},
    {stock_id: 20, name: 'COUR', companyName: 'Coursera, Inc.'}
];
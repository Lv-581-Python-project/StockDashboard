import React from 'react';
import Checkbox from '@material-ui/core/Checkbox';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;

export default function CheckboxesTags() {
  return (
    <Autocomplete
      multiple
      id="checkboxes-tags-demo"
      options={top100Films}
      disableCloseOnSelect
      getOptionLabel={(option) => option.name + " " + option.companyName}
      renderOption={(option, { selected }) => (
        <React.Fragment>
          <Checkbox
            icon={icon}
            checkedIcon={checkedIcon}
            style={{ marginRight: 8 }}
            checked={selected}
          />
          {option.name + " " + option.companyName}
        </React.Fragment>
      )}
      style={{ width: 500 }}
      renderInput={(params) => (
        <TextField {...params} variant="outlined" label="Checkboxes" placeholder="Favorites" />
      )}
    />
  );
}

// Top 100 films as rated by IMDb users. http://www.imdb.com/chart/top
const top100Films = [
  {name:'IBM',companyName: 'IBM'},
    {name:'AAPL',companyName: 'Apple'},
    {name:'GOOGL',companyName: 'Google'},
    {name:'B',companyName: 'Barnes Group Inc.'},
    {name:'BA',companyName: 'The Boeing Company'},
    {name:'BMRA',companyName: 'Biomerica, Inc.'},
    {name:'BNL',companyName: 'Broadstone Net Lease, Inc.'},
    {name:'BLUWU',companyName: 'Blue Water Acquisition Corp.'},
    {name:'BPTS',companyName: 'Biophytis SA'},
    {name:'BTNB',companyName: 'Bridgetown 2 Holdings Limited'},
    {name:'BQ',companyName: 'Boqii Holding Limited'},
    {name:'BENEW',companyName: 'Benessere Capital Acquisition Corp.'},
    {name:'BOACU',companyName: 'Bluescape Opportunities Acquisition Corp.'},
    {name:'C',companyName: 'Citigroup Inc.'},
    {name:'CBAHU',companyName: 'CBRE Acquisition Holdings, Inc.'},
    {name:'CAP-UN',companyName: 'Capitol Investment Corp. V'},
    {name:'CPTKU',companyName: 'Crown PropTech Acquisitions'},
    {name:'CLAAU',companyName: 'Colonnade Acquisition Corp. II'},
    {name:'CCVIU',companyName: 'Churchill Capital Corp VI'},
    {name:'COUR',companyName: 'Coursera, Inc.'}
];
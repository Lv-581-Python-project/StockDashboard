import {Component} from 'react';
import Paper from '@material-ui/core/Paper';
import Grid from "@material-ui/core/Grid";
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import {
    ArgumentAxis,
    ValueAxis,
    Chart,
    LineSeries,
} from '@devexpress/dx-react-chart-material-ui';
import TimelineIcon from "@material-ui/icons/Timeline";

const data = [
    {argument: 1, value: 10},
    {argument: 2, value: 20},
    {argument: 3, value: 30},
    {argument: 4, value: 5},
    {argument: 5, value: 1},
    {argument: 6, value: 32},
    {argument: 7, value: 15},
    {argument: 8, value: 4},
    {argument: 9, value: 92},
];

class ChartItem extends Component {
    state = {stock_data: [],fromValue:"",toValue:""}
    setMessage = (message) => {
        this.setState({message: message})
    }

    handleFromInput = (event)=>{
        // let fromDate = event.target.value
        // fromDate = fromDate.replace("T"," ")+":00"
        this.setState({fromValue: event.target.value})
        console.log(this.state.fromValue)
    }

    handleToInput = (event)=>{
        this.setState({fromValue: event.target.value})
        console.log(this.state.toValue)
    }
    handleDrawChart = ()=>{

    }

    render() {
        return (
            <Grid style={{marginLeft: "2vw",marginBottom:20}} container>
                <Grid item style={{margin: 40, textAlign: "center"}} xs={7} >
                    <Paper elevation={0} style={{marginBottom: 10, fontSize: "1.4em"}}>{this.props.stock.company_name}</Paper>
                </Grid>
                <Grid container>
                    <Grid item xs={7} >
                        <Paper>
                            <Chart
                                data={data}
                            >
                                <ArgumentAxis/>
                                <ValueAxis/>

                                <LineSeries valueField="value" argumentField="argument"/>
                            </Chart>
                        </Paper>
                    </Grid>
                    <Grid item xs={3} >
                        <Grid style={{marginLeft: "2vw"}} >
                            <Paper elevation={0}>
                                <div style={{marginBottom: "1vh", marginTop: "1vh"}}>
                                    <label>From<input value={this.state.fromValue} onChange={this.handleFromInput} style={{width: "99%", height: "4vh"}}
                                                      type="datetime-local"/></label>
                                </div>
                                <div>
                                    <label>To<input value={this.state.toValue} onChange={this.handleToInput} style={{width: "99%", height: "4vh"}}
                                                    type="datetime-local"/></label>
                                </div>

                            </Paper>
                        </Grid>
                        <Grid style={{marginLeft: "2vw"}} >
                            <Paper elevation={0} style={{justifyContent:"center",alignItems:"center", display:"flex"}}>
                            <Button
                            variant="contained"
                            color="primary"
                            endIcon={<TimelineIcon>Draw Chart</TimelineIcon>}
                            onClick={this.handleDrawChart}
                            style={{marginTop: 30, padding: 17, borderRadius: 15,}}
                        >
                            Draw Chart
                        </Button>
                                </Paper>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default ChartItem;

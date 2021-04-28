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
    state = {stocks: []}
    setMessage = (message) => {
        this.setState({message: message})
    }

    render() {
        return (
            // <Paper>
            //     {this.props.stock.name}
            //     <input type="datetime-local"/>
            //     <input type="datetime-local"/>
            // </Paper>

            <Grid style={{marginLeft: "2vw"}} container>
                <Grid item style={{margin: 40, textAlign: "center"}} xs={6} justify="center" alignItems="center">
                    <Paper elevation={0} style={{marginBottom: 10, fontSize: "1.4em"}}>Stock Name</Paper>
                </Grid>
                <Grid container>
                    <Grid xs={6} justify="center" alignItems="center">
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
                    <Grid  xs={3}  direction="column" justify="center" alignItems="center" >
                        <Grid style={{marginLeft: "2vw"}} justify="center" alignItems="center">
                            <Paper>
                                <div style={{marginBottom: "1vh", marginTop: "1vh"}}>
                                    <label>From<input style={{width: "99%", height: "4vh"}}
                                                      type="datetime-local"/></label>
                                </div>
                                <div>
                                    <label>To<input style={{width: "99%", height: "4vh"}}
                                                    type="datetime-local"/></label>
                                </div>

                            </Paper>
                        </Grid>
                        <Grid style={{marginLeft: "2vw"}} justify="center" alignItems="center">
                            <Paper style={{justifyContent:"center",alignItems:"center"}}>
                            <Button
                            variant="contained"
                            color="primary"
                            endIcon={<TimelineIcon>Draw Chart</TimelineIcon>}
                            onClick={this.goToDashboard}
                            style={{marginTop: 30, padding: 17, borderRadius: 15}}
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

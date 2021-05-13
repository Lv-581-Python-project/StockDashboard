import {Component} from 'react';
import Chart from "react-apexcharts";
import Paper from '@material-ui/core/Paper';
import Grid from "@material-ui/core/Grid";
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
// import {
//     ArgumentAxis,
//     ValueAxis,
//     Chart,
//     LineSeries,
//
// } from '@devexpress/dx-react-chart-material-ui';
// import { ArgumentScale, ValueScale, Animation } from '@devexpress/dx-react-chart';
import TimelineIcon from "@material-ui/icons/Timeline";
import axios from "axios";

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
const format = () => tick => tick;
const options = {
            xaxis: {
                categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999],
                labels: {
                    // format: 'dd/MM',
                    datetimeFormatter: {
                        year: 'yyyy',
                        month: 'MM',
                        day: 'dd',
                        hour: 'HH:mm'
                    },
                    rotate: -45,
                            maxHeight: 150,
                    formatter: function(value, timestamp, opts) {
            return opts.dateFormatter(new Date(timestamp)).format("dd MMM")
          }

                }

            },

            yaxis: {
                labels: {
                    formatter: (value) => {
                        return value.toPrecision(7)
                    },
                }
            },
            tooltip: {
                shared: false,
                y: {
                    formatter: function (val) {
                        return val
                    }
                }
            },
            chart: {
                type: 'area',
                stacked: false,


                zoom: {
                    type: 'x',
                    enabled: true,
                    autoScaleYaxis: true
                },
                toolbar: {
                    autoSelected: 'zoom'
                }
            },


        }
class ChartItem extends Component {

    state = {
        stock_data: [],
        fromValue: "2021-03-12T11:02",
        toValue: "2021-04-12T11:05",
        chart_data: [],
        categories:[],
        series: [
            {
                name: this.props.stock.name,
                data: [30, 40, 45, 50, 49, 60, 70, 91]
            }
        ],
        stroke: {
            curve: 'straight',
        }
    }

    handleFromInput = (event) => {
        // let fromDate = event.target.value
        // fromDate = fromDate.replace("T"," ")+":00"
        this.setState({fromValue: event.target.value})
        console.log(this.state.fromValue)
    }

    handleToInput = (event) => {
        // let toDate = event.target.value
        // toDate = toDate.replace("T"," ")+":00"
        this.setState({toValue: event.target.value})
        console.log(this.state.toValue)
    }
    handleDrawChart = () => {
        let toDate = this.state.toValue
        toDate = toDate.replace("T", " ") + ":00"
        let fromDate = this.state.fromValue
        fromDate = fromDate.replace("T", " ") + ":00"
        axios({
            method: 'get',
            url: `http://localhost:5000/api/stocks/${this.props.stock.id}?from=${fromDate}&to=${toDate}`,
            config: {headers: {'Content-Type': 'application/json'}}
        }).then(response => {
            // this.setState({stock_data: response.data})
            // let data_for_chart = []
            let categories1 = []
            let data = []
            response.data.forEach((stock) => {
                // data_for_chart.push({argument: stock.created_at, value: stock.price})
                categories1.push(stock.created_at)
                data.push(stock.price)
            })
            this.setState({
                // options: options1,
                categories:categories1,
                series: [
                    {
                        data: data
                    }
                ],

            })
        })
            .catch(errors => console.log(errors))
    }

    render() {


        const options1 = JSON.parse(JSON.stringify(options));
        options1.xaxis.categories = this.state.categories
        console.log(this.state.categories)
        console.log(options1)
        console.log(JSON.stringify(options1))
        const options2 = JSON.parse(JSON.stringify(options1));

        console.log(options2)
        return (
            <Grid style={{marginLeft: "2vw", marginBottom: 20}} container>
                <Grid item style={{margin: 40, textAlign: "center"}} xs={7}>
                    <Paper elevation={0}
                           style={{marginBottom: 10, fontSize: "1.4em"}}>{this.props.stock.company_name}</Paper>
                </Grid>
                <Grid container>
                    <Grid item xs={7}>
                        <Paper>
                            <Chart
                                options={options2}
                                series={this.state.series}
                                type="line"

                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={3}>
                        <Grid style={{marginLeft: "2vw"}}>
                            <Paper elevation={0}>
                                <div style={{marginBottom: "1vh", marginTop: "1vh"}}>
                                    <label>From<input value={this.state.fromValue} onChange={this.handleFromInput}
                                                      style={{width: "99%", height: "4vh"}}
                                                      type="datetime-local"/></label>
                                </div>
                                <div>
                                    <label>To<input value={this.state.toValue} onChange={this.handleToInput}
                                                    style={{width: "99%", height: "4vh"}}
                                                    type="datetime-local"/></label>
                                </div>

                            </Paper>
                        </Grid>
                        <Grid style={{marginLeft: "2vw"}}>
                            <Paper elevation={0}
                                   style={{justifyContent: "center", alignItems: "center", display: "flex"}}>
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

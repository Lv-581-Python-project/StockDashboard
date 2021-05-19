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

// const data = [
//     {argument: 1, value: 10},
//     {argument: 2, value: 20},
//     {argument: 3, value: 30},
//     {argument: 4, value: 5},
//     {argument: 5, value: 1},
//     {argument: 6, value: 32},
//     {argument: 7, value: 15},
//     {argument: 8, value: 4},
//     {argument: 9, value: 92},
// ];
const format = () => tick => tick;
const convert_date = (d) => {
    let month = (d.getMonth() + 1).toString();
    if (month.length < 2) {
        month = "0" + month
    }
    let date = d.getDate().toString()
    if (date.length < 2) {
        date = "0" + date
    }
    let hours = d.getHours().toString()
    if (hours.length < 2) {
        hours = "0" + hours
    }
    let minutes = d.getMinutes().toString()
    console.log(minutes.length)
    if (minutes.length < 2) {
        minutes = "0" + minutes
    }
    let seconds = d.getSeconds().toString()
    if (seconds.length < 2) {
        seconds = "0" + seconds
    }
    let res_date = d.getFullYear() + "-" + month + "-" + date + " " + hours + ":" + minutes+":"+ seconds
    return res_date
}

const getChartData = (fromDate, toDate , stock_id) => {

    return axios({
        method: 'get',
        url: `http://localhost:5000/api/stocks/${stock_id}?from=${fromDate}&to=${toDate}`,
        config: {headers: {'Content-Type': 'application/json'}}
    })
}

class ChartItem extends Component {


    state = {
        stock_data: [],
        time: 2,
        fromValue: "",
        toValue: "",
        chart_data: [],
        categories: [],
        data_is_default: true,
        options: {
            xaxis: {
                categories: [],
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
                    formatter: function (value, timestamp, opts) {
                        return new Date(value)
                    }

                }

            },

            yaxis: {
                labels: {
                    formatter: (value, index) => {
                        return value.toFixed(1)
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


        },
        series: [
            {
                name: this.props.stock.name,
                data: []
            }
        ],
        stroke: {
            curve: 'straight',
        }
    }

    // update plot with default date every 15 minutes
    componentDidMount() {

        if (this.state.data_is_default===true) {

            let d = new Date(Date.now());
            let d2 = new Date(Date.now());
            d2.setDate(d.getDate() - 30)
            d2.setMonth(d.getMonth() +1)
            let date_now = convert_date(d);
            let date_difference = convert_date(d2)
            console.log(date_difference)
            this.interval = setInterval(() => {
                getChartData(date_difference, date_now, this.props.stock.id)
                    .then(response => {
                        this.handleResponse(response);
                    })
                    .catch(errors => console.log(errors));

            }, 1000 * 30)

        }


    }

    componentWillUnmount() {
        clearInterval(this.interval);
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
    handleResponse = (response) => {
        let categories1 = []
        let data = []
        response.data.forEach((stock) => {
            categories1.push(stock.created_at)
            data.push(stock.price)
        })
        const options1 = JSON.parse(JSON.stringify(this.state.options));
        options1.xaxis.categories = this.state.categories
        options1.xaxis.labels.formatter = (value, timestamp, opts) => {
            return new Date(value)
        }
        options1.yaxis.labels.formatter = (value, index) => {
            return value.toFixed(1)
        }
        this.setState({
            options: options1,
            categories: categories1,
            series: [
                {
                    data: data
                }
            ],

        })
    }
    handleDrawChart = () => {
        let toDate = this.state.toValue
        toDate = toDate.replace("T", " ") + ":00"
        let fromDate = this.state.fromValue
        fromDate = fromDate.replace("T", " ") + ":00"
        getChartData(fromDate, toDate, this.props.stock.id).then(response => {

            this.handleResponse(response);
            this.setState({data_is_default: false})
        })
            .catch(errors => console.log(errors))
    }

    render() {
        console.log(this.state.series.data)
        console.log(this.state.toValue)
        console.log(this.state.fromValue)
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
                                options={this.state.options}
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

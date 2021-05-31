import axios from 'axios';
import {Component} from 'react';
import AutoComplete from "../auto_complete_stocks/autoCompleteStocks";
import Button from '@material-ui/core/Button';
import Alert from '@material-ui/lab/Alert';
import TimelineIcon from '@material-ui/icons/Timeline';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import {withRouter} from 'react-router-dom';
import "../../css/home.css";


class Home extends Component {
    state = {stocks: [], showAlert: false}
    setStocks = (stocks) => {
        this.setState({stocks: stocks})
    }
    goToDashboard = () => {
        let missing_names = this.state.stocks.filter((stock) => {
            if (!Object.keys(stock).includes("id")) {

                return stock.name
            }
        })
        axios({
            method: 'post',
            url: 'http://localhost:5000/api/dashboard/',
            data: {
                all_stocks: this.state.stocks,
                missing_names: missing_names
            },
            config: {headers: {'Content-Type': 'application/json'}}
        }).then(response => {

            this.props.history.push(`/dashboard/${response.data.dashboard_hash}`)

        })
            .catch(errors => {
                console.log(errors)
                this.setState({showAlert: true})
            })

    }


    render() {
        // console.log(this.state.stocks)
        return (
            <Grid
                container
                xs={12}
                spacing={3}
                direction="column"
                alignItems="center"
                justify="center"
                style={{marginTop: "2%"}}
            >
                <Grid item xs={8}>
                    <Paper style={{textAlign: "justify"}} className="textStyle" elevation={0}>Stock (also capital stock)
                        is all of the shares into
                        which ownership of a corporation is divided. In American English, the shares are collectively
                        known as "stock". A single share of the stock represents fractional ownership of the
                        corporation in proportion to the total number of shares. This typically entitles the stockholder
                        to that fraction of the company's earnings, proceeds from liquidation of assets (after discharge
                        of all senior claims such as secured and unsecured debt), or voting power, often dividing
                        these up in proportion to the amount of money each stockholder has invested. Not all stock is
                        necessarily equal, as certain classes of stock may be issued for example without voting rights,
                        with enhanced voting rights, or with a certain priority to receive profits or liquidation
                        proceeds before or after other classes of shareholders.
                    </Paper>
                </Grid>
                <Grid item xs={8}>
                    <Paper style={{textAlign: "justify"}} className="textStyle" elevation={0}>Stock can be bought and
                        sold privately or on stock
                        exchanges, and such transactions are typically heavily regulated by governments to prevent
                        fraud, protect investors, and benefit the larger economy. The stocks are deposited with the
                        depositories in the electronic format also known as Demat account. As new shares are issued by a
                        company, the ownership and rights of existing shareholders are diluted in return for cash to
                        sustain or grow the business.
                    </Paper>
                </Grid>
                <Grid item xs={8}>
                    <Paper style={{textAlign: "justify"}} className="textStyle" elevation={0}>Companies can also buy
                        back stock, which often lets investors
                        recoup the initial investment plus capital gains from subsequent rises in stock price. Stock
                        options, issued by many companies as part of employee compensation, do not represent ownership,
                        but represent the right to buy ownership at a future time at a specified price. This would
                        represent a windfall to the employees if the option is exercised when the market price is higher
                        than the promised price, since if they immediately sold the stock they would keep the difference
                        (minus taxes).
                    </Paper>
                </Grid>
                <Grid xs={6} container className="autoComplete" direction="column" alignItems='center' justify='center'>
                    <AutoComplete setStocks={this.setStocks}/>
                    {this.state.showAlert ?
                        <Alert style={{marginTop: 10, width: "38vw"}} severity="error">Error. Non-existent stock
                            inputed. Please check your list of inputed stocks and try again.</Alert> : null}
                    <Button
                        variant="contained"
                        color="primary"
                        endIcon={<TimelineIcon>Show Charts</TimelineIcon>}
                        onClick={this.goToDashboard}
                        style={{marginTop: 30, padding: 17, borderRadius: 15}}
                    >
                        Show Charts
                    </Button>
                </Grid>


            </Grid>
        );
    }
}

export default withRouter(Home);

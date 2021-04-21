import {Component} from 'react';
import AutoComplete from "../auto_complete_stocks/autoCompleteStocks";
import Button from '@material-ui/core/Button';
import TimelineIcon from '@material-ui/icons/Timeline';
import {withRouter} from 'react-router-dom';

class Home extends Component {
    state = {stocks: []}
    setStocks = (stocks) => {
        this.setState({stocks: stocks})
    }
    goToDashboard= () => {
        let stocks = this.state.stocks.map((stock)=>stock.id)
        this.props.history.push(`/dashboard?stocks=[${stocks.toString()}]`)
    }
    render() {
        console.log(this.state.stocks)
        return (
            <div>
                <AutoComplete setStocks={this.setStocks}/>
                <Button
                    variant="contained"
                    color="primary"
                    endIcon={<TimelineIcon>Show Charts</TimelineIcon>}
                    onClick={this.goToDashboard}
                >
                    Show Charts
                </Button>
            </div>
        );
    }
}

export default withRouter(Home);

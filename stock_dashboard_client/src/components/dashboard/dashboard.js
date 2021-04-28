import {Component} from 'react';
import ChartItem from './chart';
import AutoComplete from "../auto_complete_stocks/autoCompleteStocks";
import {withRouter} from 'react-router-dom';

class Dashboard extends Component {
    state = {stocks: [1,2]}
    setStocks = (stocks)=>{
        this.setState({stocks: stocks})
    }
    setMessage = (message) => {
        this.setState({message: message})
    }

    render() {
        console.log(this.state.stocks)
        return (
            <div>

                {/*{this.state.stocks.map((stock)=>{ console.log(stock);return(<ChartItem stock={stock} />)})}*/}
                <ChartItem/>
                <ChartItem/>
            </div>
        );
    }
}

export default withRouter(Dashboard);

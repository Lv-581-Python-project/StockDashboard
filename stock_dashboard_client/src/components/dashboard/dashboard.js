import {Component} from 'react';
import Chart from './chart';
import AutoComplete from "../auto_complete_stocks/autoCompleteStocks";
import {withRouter} from 'react-router-dom';

class Dashboard extends Component {
    state = {stocks: []}
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

                {this.state.stocks.map((stock)=>{ console.log(stock);return(<Chart stock={stock} />)})}
                {/*<Chart/>*/}
                {/*<Chart/>*/}
            </div>
        );
    }
}

export default withRouter(Dashboard);

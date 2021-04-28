import {Component} from 'react';
import ChartItem from './chart';
import Grid from "@material-ui/core/Grid";
import {withRouter} from 'react-router-dom';

class Dashboard extends Component {
    state = {stocks: []}
    setStocks = (stocks)=>{
        this.setState({stocks: stocks})
    }

    render() {
        console.log(this.state.stocks)
        return (
            <Grid container xs={12}>

                {this.state.stocks.map((stock)=>{ console.log(stock);return(<ChartItem stock={stock} />)})}
                {/*<ChartItem/>*/}
                {/*<ChartItem/>*/}
            </Grid>
        );
    }
}

export default withRouter(Dashboard);

import {Component} from 'react';
import ChartItem from './chart';
import Grid from "@material-ui/core/Grid";
import {withRouter} from 'react-router-dom';
import axios from "axios";
import Button from "@material-ui/core/Button";
import ShareIcon from '@material-ui/icons/Share';
class Dashboard extends Component {
    state = {stocks: []}
    setStocks = (stocks)=>{
        this.setState({stocks: stocks})
    }
    handleShare(){
        const currentURL = document.createElement('textarea');
        currentURL.value = window.location.href;
        document.body.appendChild(currentURL);
        currentURL.select();
        document.execCommand('copy');
        document.body.removeChild(currentURL);
    }
    componentWillMount(){
        let currentURL = window.location.href.split("/")
        axios({
            method: 'get',
            url: `http://localhost:5000/api/dashboard/${currentURL[currentURL.length -1]}`,
            config: { headers: { 'Content-Type': 'application/json' } }
        }).then(response => this.setStocks(response.data.stocks))
            .catch(errors => console.log(errors))
    }

    render() {
        return (

            <Grid container style={{marginTop:40}}>
                <Grid item xs={10}>
                {this.state.stocks.map((stock)=>{ console.log(stock);return(<ChartItem key={stock.id} stock={stock} />)})}
                    </Grid>
                <Grid xs={2}>
                    <Button
                        variant="contained"
                        color="primary"
                        endIcon={<ShareIcon>Share</ShareIcon>}
                        onClick={this.handleShare}
                        style={{ width:"8vw",padding:15,borderRadius: 15,position:"fixed",bottom:30,right:19}}

                    >
                        Share
                    </Button>
                </Grid>
            </Grid>
        );
    }
}

export default withRouter(Dashboard);

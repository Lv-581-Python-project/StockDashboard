import {Component} from 'react';
import AutoComplete from "../auto_complete_stocks/autoCompleteStocks";
import Button from '@material-ui/core/Button';
import TimelineIcon from '@material-ui/icons/Timeline';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import {withRouter} from 'react-router-dom';
import "../../css/home.css";
class Home extends Component {
    state = {stocks: []}
    setStocks = (stocks) => {
        this.setState({stocks: stocks})
    }
    goToDashboard = () => {
        let stocks = this.state.stocks.map((stock) => stock.id)
        this.props.history.push(`/dashboard?stocks=[${stocks.toString()}]`)
    }

    render() {
        console.log(this.state.stocks)
        return (
            <Grid
                container
                xs = {12}
                spacing={3}
                direction="column"
                alignItems="center"
                justify="center"
                style={{marginTop: "2%"}}
            >
                <Grid item xs={8}>
                    <Paper className="textStyle" elevation={0}>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non eros
                        vehicula, lobortis
                        dui a, efficitur sapien. Proin vel pretium dolor, a maximus quam. Praesent ut nisl posuere,
                        aliquet felis sed, varius tortor. Donec finibus tellus a sapien facilisis, a hendrerit lacus
                        bibendum. Donec pretium tellus sed dui rutrum luctus id a sapien. In pellentesque odio sed ipsum
                        vestibulum blandit. Donec orci mauris, facilisis in elit placerat, venenatis faucibus nibh. In
                        placerat enim vel tortor mollis ullamcorper efficitur aliquet ipsum. Fusce in tincidunt quam. In
                        urna mauris, eleifend at suscipit vel, vestibulum non sem. Sed eget augue ut nibh blandit
                        feugiat.
                    </Paper>
                </Grid>
                <Grid item xs={8}>
                    <Paper className="textStyle" elevation={0}>Donec vel est eget libero tempor convallis. Proin sed urna ut nibh blandit
                        sodales. Nunc sollicitudin ipsum quis felis laoreet placerat. Nam quis ligula nec eros lobortis
                        consequat non ac erat. Duis cursus hendrerit erat ac vehicula. Proin in pellentesque ex. Integer
                        nec urna auctor, sagittis arcu tempus, sollicitudin elit.
                    </Paper>
                </Grid>
                <Grid item xs={8}>
                    <Paper className="textStyle" elevation={0}>Donec maximus lacus orci, id efficitur lorem rhoncus ac. Quisque dictum, turpis
                        pretium aliquet rutrum, velit sapien vestibulum nisl, et interdum sapien lacus in tortor. Nam a
                        arcu eget lacus sodales tempor. Phasellus sit amet sapien mi. Aenean vel diam magna. Nam rhoncus
                        tincidunt magna sit amet eleifend. Ut nulla risus, hendrerit sed aliquam id, faucibus at mauris.
                        Nulla molestie, magna vitae vulputate luctus, sapien nibh ornare leo, nec pulvinar ipsum nunc
                        vitae magna. Cras tempus purus facilisis dui sodales mattis. Integer nec ante egestas, maximus
                        nisl vel, euismod ligula. Donec felis mi, tristique in commodo vel, aliquam at erat. Mauris
                        sollicitudin porttitor enim, nec accumsan purus. Quisque quis libero sagittis, maximus ante id,
                        aliquet massa. In maximus sem at lacus congue, quis dapibus ex pharetra.
                    </Paper>
                </Grid>
                <Grid xs={6} container className="autoComplete" direction="row"  alignItems='center' justify='center'>
                <AutoComplete setStocks={this.setStocks}/>
                <Button
                    variant="contained"
                    color="primary"
                    endIcon={<TimelineIcon>Show Charts</TimelineIcon>}
                    onClick={this.goToDashboard}
                    style={{marginTop:30,padding:17,borderRadius:15}}
                >
                    Show Charts
                </Button>
                    </Grid>
            </Grid>
        );
    }
}

export default withRouter(Home);

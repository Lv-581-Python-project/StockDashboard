import {Component} from 'react';
import Paper from '@material-ui/core/Paper';

class Chart extends Component {
    state = {stocks: []}
    setMessage = (message) => {
        this.setState({message: message})
    }

    render() {
        return (
            <Paper>
                {this.props.stock.name}
                <input type="datetime-local"/>
                <input type="datetime-local"/>
            </Paper>
        );
    }
}

export default Chart;

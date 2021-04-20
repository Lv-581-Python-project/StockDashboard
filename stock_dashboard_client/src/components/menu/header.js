import { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Typography from '@material-ui/core/Typography';
export default class Header extends Component {

    state = {message: this.props.name ? this.props.name : "Message"}
    handleClick=(event)=>{
        let value = event.target.value;
        this.setState({message: value});
        this.props.setMessage && this.props.setMessage(value)
    }
    render() {
        return (
        <div>
            <AppBar position="static" >
            <Typography>text</Typography>
            </AppBar>
            { this.state.message }
            <input onChange={this.handleClick}/>
        </div>
        );
    }
}

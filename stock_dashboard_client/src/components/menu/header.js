import {Component} from 'react';
import AppBar from '@material-ui/core/AppBar';
import Typography from '@material-ui/core/Typography';
import {Link} from "react-router-dom";

export default class Header extends Component {

    // handleHomeClick = ()=>{
    //     this.props.history.push(`/`)
    // }

    render() {
        return (
            <div>
                <AppBar position="static">
                    <Link to='/' style={{textDecoration: 'none',color:"#fff"}}>
                        <Typography style={{margin:10}} variant="h3">Stock Dashboard</Typography>
                    </Link>
                </AppBar>

            </div>
        );
    }
}

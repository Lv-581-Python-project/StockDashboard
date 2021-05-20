import {Component} from 'react';
import AppBar from '@material-ui/core/AppBar';
import Typography from '@material-ui/core/Typography';
import {Link} from "react-router-dom";

export default class Header extends Component {

    render() {
        return (
            <div>
                <AppBar position="static">

                    <Typography style={{margin: 10}} variant="h3">
                        <Link to='/' style={{textDecoration: 'none', color: "#fff"}}>
                            Stock Dashboard
                        </Link>
                    </Typography>

                </AppBar>

            </div>
        );
    }
}

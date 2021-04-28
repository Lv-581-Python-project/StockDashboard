import {Component} from 'react';
import './css/App.css';
import Header from './components/menu/header';
import Dashboard from "./components/dashboard/dashboard";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import Home from "./components/home/home";

class App extends Component {
    render() {

        return (
            <div>

                <Router>
                    <Header/>
                    <Switch>
                        <Route path="/dashboard/:param1" component={Dashboard}/>
                        <Route path="/" component={Home}/>
                        <Redirect path='*' to='/'/>
                    </Switch>
                </Router>
            </div>
        );
    }
}

export default App;

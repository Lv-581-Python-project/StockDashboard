import {Component} from 'react';
import './css/App.css';
import Header from './components/menu/header';
import AutoComplete from './components/auto_complete_stocks/autoCompleteStocks'
class App extends Component {
    state = {message: "Message"}
    setMessage = (message)=>{
        this.setState({message: message})
    }
    render() {
        return (
            <div className="App">
                <Header name="wfawfa" setMessage = {this.setMessage}/>
                <Header/>
                <Header/>
                <Header/>
                <Header/>
                {this.state.message}
                <AutoComplete/>
            </div>
  );
  }
}

export default App;

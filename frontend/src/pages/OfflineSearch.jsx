import React, { Component } from 'react';
import console from "react-console";
import Select from 'react-select'
import ToggleButton from 'react-toggle-button'
import languages from 'countries-list';
import { w3cwebsocket as W3CWebSocket } from "websocket";

import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import Paper from '@material-ui/core/Paper';
import Avatar from '@material-ui/core/Avatar';
import Slider from '@material-ui/core/Slider';

import { withStyles } from "@material-ui/core/styles";

import AuthContext from '../context/AuthContext'

import TinderCard from 'react-tinder-card'

const useStyles = theme => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  root: {
    boxShadow: 'none',
  }
});

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

class OfflineSearch extends Component {
    static contextType = AuthContext
  state = {
    chatView: false,
    messages: [],
    room: null,
    fieldsArray: ['hey'],
    tinderCards: ['hey'],
    value:'',
    matchList:[],
    currentIndex: null,
  }

  swipe = async(e) => {
    if (this.state.currentIndex < this.state.fieldsArray.length) {
      this.setState({currentIndex: this.state.currentIndex+1})
    }
    else {
      this.setState({currentIndex: null})
    }
  }

  createRoom = async(e) => {
    const {user} =this.context;
                        fetch('http://localhost:8000/chat/send_friend_request/', {
                          method: 'POST', // или 'PUT'
                          body: JSON.stringify({user1: user.custom_user_id, user2: e.friend_id}), // данные могут быть 'строкой' или {объектом}!
                          headers: {
                            'Content-Type': 'application/json'
                          }
                        })
                            .then(response => response.json().then((text) => {
                                alert(text.result);
                                this.swipe();
                            }));
  }

  ignoreUser = async(e) => {
    const {user} =this.context;
                        fetch('http://localhost:8000/chat/ignore_user/', {
                          method: 'POST', // или 'PUT'
                          body: JSON.stringify({user1: user.custom_user_id, user2: e.friend_id}), // данные могут быть 'строкой' или {объектом}!
                          headers: {
                            'Content-Type': 'application/json'
                          }
                        })
                            .then(response => response.json().then((text) => {
                                alert(text.result);
                                this.swipe();
                            }));
  }

  swiped = (direction, id) => {
    this.setState({currentIndex: this.state.currentIndex-1})
    alert(direction==='right')
    if (direction==='right'){
      this.createRoom({ friend_id: id});
    }
    else {
      this.ignoreUser({ friend_id: id});
    }
  }

  outOfFrame = (name) => {
    console.log(name + ' left the screen!')
  }

  componentDidMount() {

    const {user} =this.context;
    fetch('http://localhost:8000/chat/get_most_like_minded/', {
      method: 'POST', // или 'PUT'
      body: JSON.stringify({user_id: user.user_id}), // данные могут быть 'строкой' или {объектом}!
      headers: {
        'Content-Type': 'application/json'
      }
    })
        .then(response => response.json().then((text) => {
            let newFieldsArray = [];
            let newTinderCards = [];
            let newMatchList = [];
            for (const f_user of text.result){
                newMatchList.push({like_mindness: f_user.name})
                let url = 'url(media/photos/tree.jpg)'
                if (f_user.photo !== 'None'){
                  url = 'url('+f_user.photo+')'
                }
                let distance = 'unknown'
                if (f_user.distance !== 'None'){
                  distance = f_user.distance + ' km'
                }
                newFieldsArray.push(
                  <div>
                     <div style={{ backgroundImage: url }} className='card'>
                      <h3>{f_user.name}</h3>
                    </div>
                  <Button
                    onClick={e => {
                      this.createRoom({ friend_id: f_user.id});
                    }}
                  > Accept </Button>
                  <Button
                    onClick={e => {
                      this.ignoreUser({ friend_id: f_user.id});
                    }}
                  >  Ignore
                  </Button>
                  You match on {f_user.like_mindness} percent.
                  Distance is {distance}
                  Description: {f_user.description}
                  Age is {f_user.age}
                  </div>
            );
            }
            this.setState({ fieldsArray: newFieldsArray });
            this.setState({ currentIndex: 0})
        }));
    }
  
  componentWillUpdate(nextProps, nextState) {
    localStorage.setItem('user', JSON.stringify(nextState));
  }

  render() {
    // window.navigator.geolocation.getCurrentPosition(this.success, this.success);
    const { classes } = this.props;
    return (
      <Container component="main" maxWidth="xs">
                  <div>
            <CssBaseline />
            <div className={classes.paper}>
            <div className='cardContainer'>
            {this.state.currentIndex != null ? this.state.fieldsArray[this.state.currentIndex] : 'No potential users :('}
            </div>
            </div>
          </div>
      </Container>
    )

  }
}
export default withStyles(useStyles)(OfflineSearch);

// export {Chatsearch}
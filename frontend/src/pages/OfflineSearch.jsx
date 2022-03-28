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
    value:'',
  }

  createRoom = async(e) => {
    const {user} =this.context;
                        fetch('http://localhost:8000/chat/create_chat_room/', {
                          method: 'POST', // или 'PUT'
                          body: JSON.stringify({user1: user.custom_user_id, user2: e.friend_id}), // данные могут быть 'строкой' или {объектом}!
                          headers: {
                            'Content-Type': 'application/json'
                          }
                        })
                            .then(response => response.json().then((text) => {
                                alert("created");
                            }));
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
            for (const f_user of text.result){
                newFieldsArray.push(
                  <Button
                    onClick={e => {
                      this.createRoom({ friend_id: f_user.id});
                    }}
                  > {f_user.id} - {f_user.like_mindness} </Button>
            );
            }
            this.setState({ fieldsArray: newFieldsArray });
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
                {this.state.fieldsArray}
            </div>
          </div>
      </Container>
    )

  }
}
export default withStyles(useStyles)(OfflineSearch);

// export {Chatsearch}
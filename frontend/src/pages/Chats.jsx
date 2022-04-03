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

class Chatsearch extends Component {
    static contextType = AuthContext
  state = {
    chatView: false,
    messages: [],
    room: null,
    fieldsArray: ['hey'],
    value:'',
    chatRestored: false,
    talkingWith: 0,
  }

  // client = new W3CWebSocket('ws://localhost:8000/ws/chat/' + this.state.room + '/');

  onButtonClicked = (e) => {
    const {user} =this.context;
    this.client.send(JSON.stringify({
      type: "message",
      message: this.state.value,
      name: user.custom_user_id
    }));
    this.state.value = ''
    e.preventDefault();
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
                            }));
  }

  enterRoom = async(e) => {
    this.setState({ room: e.room})
    this.setState({ chatView: true})
    this.state.chatView = true;
          let client = new W3CWebSocket('ws://localhost:8000/ws/friend_chat/' + e.room + '/');
          this.client = client;
          client.onopen = function(e) {
            client.send(JSON.stringify({
              type: "open_chat",
              message: 'Start searching',
              name: "name"
            }));
          };
              client.onmessage = (message) => {
                const dataFromServer = JSON.parse(message.data);
                console.log('got reply! ', dataFromServer.type);
                if (dataFromServer) {
                   if (dataFromServer.type === 'chat_restored') {
                    this.setState({ chatRestored: true });

                  } 
                  else if (dataFromServer.type === 'restore_chat' && this.state.chatRestored === false) {
                    this.setState((state) =>
                      ({
                        messages: [...state.messages,
                        {
                          msg: dataFromServer.message,
                          name: dataFromServer.name
                        }]
                      })
                    );
                  }
                  else if (dataFromServer.type === 'restore_chat' && this.state.chatRestored === true) {
                    
                  }
                  else {
                    this.setState((state) =>
                      ({
                        messages: [...state.messages,
                        {
                          msg: dataFromServer.message,
                          name: dataFromServer.name
                        }]
                      })
                    );
                  }
                  
                }
              };
  }

  componentDidMount() {

    const {user} =this.context;
    fetch('http://localhost:8000/chat/get_user_chats/', {
      method: 'POST', // или 'PUT'
      body: JSON.stringify({user_id: user.custom_user_id}), // данные могут быть 'строкой' или {объектом}!
      headers: {
        'Content-Type': 'application/json'
      }
    })
        .then(response => response.json().then((text) => {
            let newFieldsArray = [];
            for (const chat of text.chat_ids){
                newFieldsArray.push(
                  <Button
                    onClick={e => {
                      this.setState({ chatView: true });
                      this.enterRoom({ room: chat.chat_id});
                      this.setState({ talkingWith: chat.user_id})
                    }}
                  > {chat.chat_id} - {chat.user_id} </Button>
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
        {this.state.chatView ?
          <div style={{ marginTop: 50, }}>
            Room Name: {this.state.room}
            <Paper style={{ height: 500, maxHeight: 500, overflow: 'auto', boxShadow: 'none', }}>
              {this.state.messages.map(message => <>
                <Card className={classes.root}>
                  <CardHeader
                    avatar={
                      <Avatar className={classes.avatar}>
                        R
                      </Avatar>
                    }
                    title={message.name}
                    subheader={message.msg}
                  />
                </Card>
              </>)}
            </Paper>

            <form className={classes.form} noValidate onSubmit={this.onButtonClicked}>
              <TextField
                id="outlined-helperText"
                label="Make a comment"
                defaultValue="Default Value"
                variant="outlined"
                value={this.state.value}
                fullWidth
                onChange={e => {
                  this.setState({ value: e.target.value });
                  this.value = this.state.value;
                }}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
              >
                Start Chatting
                </Button>
                                  <Button
                    onClick={e => {
                      this.ignoreUser({ friend_id: this.state.talkingWith});
                    }}
                  >  Ignore
                  </Button>
            </form>
          </div>

          :

          <div>
            <CssBaseline />
            <div className={classes.paper}>
                {this.state.fieldsArray}
            </div>
          </div>}
      </Container>
    )

  }
}
export default withStyles(useStyles)(Chatsearch);

// export {Chatsearch}
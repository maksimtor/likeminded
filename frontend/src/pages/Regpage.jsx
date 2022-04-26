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

class Regpage extends Component {

    state = {
        isLoggedIn: false,
        username: '',
        email: '',
        password: '',
        fields: {},
        errors: {},
    }

    handleValidation = async(e) =>  {
        let formIsValid = true;
        let copyErrors = {}
        this.setState({ errors: {}});

        //Name
        if (!this.state.username) {
          formIsValid = false;
          copyErrors.username = "Cannot be empty";
        }
        if (typeof this.state.email !== "undefined") {
          let lastAtPos = this.state.email.lastIndexOf("@");
          let lastDotPos = this.state.email.lastIndexOf(".");

          if (
            !(
              lastAtPos < lastDotPos &&
              lastAtPos > 0 &&
              this.state.email.indexOf("@@") == -1 &&
              lastDotPos > 2 &&
              this.state.email.length - lastDotPos > 2
            )
          ) {
            formIsValid = false;
            copyErrors.email = "Email is not valid";
          }
        }
        if (!this.state.email) {
          formIsValid = false;
          copyErrors.email = "Cannot be empty";
        }

        //Name
        if (!this.state.password) {
          formIsValid = false;
          copyErrors.password = "Cannot be empty";
        }
        this.setState({ errors: copyErrors});

        fetch('http://localhost:8000/chat/validate_user/', {
          method: 'POST', // или 'PUT'
          body: JSON.stringify({username: this.state.username, email: this.state.email}), // данные могут быть 'строкой' или {объектом}!
          headers: {
            'Content-Type': 'application/json'
          }
        })
            .then(response => response.json().then((text) => {
                let copyErrors = { ...this.state.errors};
                if (text.problems==='both'){
                    copyErrors["username"] = "User with this name already exists."
                    copyErrors["email"] = "User with this email already exists."
                }
                else if (text.problems==='email'){
                    copyErrors["email"] = "User with this email already exists."
                }
                else if (text.problems==='username'){
                    copyErrors["username"] = "User with this name already exists."
                }
                this.setState({ errors: copyErrors});

                if (Object.keys(this.state.errors).length === 0) {
                    fetch('http://localhost:8000/chat/create_real_user/', {
                      method: 'POST', // или 'PUT'
                      body: JSON.stringify({username: this.state.username, email: this.state.email, password: this.state.password}), // данные могут быть 'строкой' или {объектом}!
                      headers: {
                        'Content-Type': 'application/json'
                      }
                    })
                        .then(response => response.json().then((text) => {
                            alert("User was created)")
                        }));
                }
                e.preventDefault();
            }));


        // //Email
        // if (!fields["email"]) {
        //   formIsValid = false;
        //   errors["email"] = "Cannot be empty";
        // }

        // if (typeof fields["email"] !== "undefined") {
        //   let lastAtPos = fields["email"].lastIndexOf("@");
        //   let lastDotPos = fields["email"].lastIndexOf(".");

        //   if (
        //     !(
        //       lastAtPos < lastDotPos &&
        //       lastAtPos > 0 &&
        //       fields["email"].indexOf("@@") == -1 &&
        //       lastDotPos > 2 &&
        //       fields["email"].length - lastDotPos > 2
        //     )
        //   ) {
        //     formIsValid = false;
        //     errors["email"] = "Email is not valid";
        //   }
        // }
    }

  register = (e) => {
    // TODO: validation
    // TODO: creating new user
    // TODO: if success, log in and send user to profile page
    // if (this.handleValidation()) {
    //   alert("Form submitted");
    // } else {
    //   alert(this.handleValidation())
    //   alert("Form has errors.");
    // }

    // e.preventDefault();
  }


  componentDidMount() {
  }
  
  componentWillUpdate(nextProps, nextState) {
  }

  render() {
    const { classes } = this.props;
    return (
      <Container component="main" maxWidth="xs">
          <div>
            <div className={classes.paper}>
              <Typography component="h1" variant="h5">
                ChattyRooms
                </Typography>
              <form className={classes.form} noValidate>
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  name="Username"
                  label="Username"
                  type="Username"
                  id="Username"
                  value={this.state.username}
                  onChange={e => {
                    this.setState({ username: e.target.value });
                    this.value = this.state.username;
                  }}
                />
                <span style={{ color: "red" }}>{this.state.errors["username"]}</span>
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  name="email"
                  label="Email"
                  type="email"
                  id="email"
                  value={this.state.email}
                  onChange={e => {
                    this.setState({ email: e.target.value });
                    this.value = this.state.email;
                  }}
                />
                <span style={{ color: "red" }}>{this.state.errors["email"]}</span>
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  value={this.state.password}
                  onChange={e => {
                    this.setState({ password: e.target.value });
                    this.value = this.state.password;
                  }}
                />
                <span style={{ color: "red" }}>{this.state.errors["password"]}</span>
                <Button
                  onClick={this.handleValidation}
                  type="button"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  Register
                  </Button>
                <Grid container>
                  <Grid item xs>
                    <Link href="#" variant="body2">
                      Forgot password?
                      </Link>
                  </Grid>
                </Grid>
              </form>
            </div>
          </div>
      </Container>
    )

  }
}
export default withStyles(useStyles)(Regpage);
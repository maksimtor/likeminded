import React, { Component } from 'react';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';

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

class Regpage extends Component {
  static contextType = AuthContext
  state = {
    isLoggedIn: false,
    username: '',
    email: '',
    password: '',
    fields: {},
    errors: {},
  }

  handleValidation = async () => {
    let copyErrors = {}
    this.setState({ errors: {} });

    //Name
    if (!this.state.username) {
      copyErrors.username = "Cannot be empty";
    }
    if (typeof this.state.email !== "undefined") {
      let lastAtPos = this.state.email.lastIndexOf("@");
      let lastDotPos = this.state.email.lastIndexOf(".");

      if (
        !(
          lastAtPos < lastDotPos &&
          lastAtPos > 0 &&
          this.state.email.indexOf("@@") === -1 &&
          lastDotPos > 2 &&
          this.state.email.length - lastDotPos > 2
        )
      ) {
        copyErrors.email = "Email is not valid";
      }
    }
    if (!this.state.email) {
      copyErrors.email = "Cannot be empty";
    }

    //Name
    if (!this.state.password) {
      copyErrors.password = "Cannot be empty";
    }
    this.setState({ errors: copyErrors });
    const { csrfTokens } = this.context;
    alert(csrfTokens['X-CSRFToken'])
    fetch('http://localhost:8000/chat/api/users/', {
      method: 'POST', // или 'PUT'
      body: JSON.stringify({ registration: true, user: { username: this.state.username, email: this.state.email, password: this.state.password } }), // данные могут быть 'строкой' или {объектом}!
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': csrfTokens['X-CSRFToken']
      },
      credentials: "include"
    })
      .then(response => response.json().then((text) => {
        if (text['id']) {
          alert("Good job")
        }
        else if (text['user']) {
          alert(JSON.stringify(text['user']['non_field_errors']))
        }
      }));
  }

  componentDidMount() {
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
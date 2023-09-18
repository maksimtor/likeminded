import React, { Component } from 'react'
import AuthContext from '../context/AuthContext'
import { withStyles } from "@material-ui/core/styles";import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';


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

class Loginpage extends Component {
    static contextType = AuthContext
    state = {
        username: '',
        password: '',
    }
    render(){
        const { classes } = this.props;
        const {loginUser} = this.context
        return (
            <Container component="main" maxWidth="xs">
                <div>
                    <div className={classes.paper}>
                        <Typography component="h1" variant="h5">
                            Регистрация
                        </Typography>
                        <form onSubmit={loginUser}>
                            <TextField
                                variant="outlined"
                                margin="normal"
                                required
                                fullWidth
                                name="username"
                                label="Username"
                                type="text"
                                id="username"
                                value={this.state.username}
                                onChange={e => {
                                    this.setState({ username: e.target.value });
                                    this.value = this.state.username;
                                }}
                                />
                            <TextField
                                variant="outlined"
                                margin="normal"
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="text"
                                id="password"
                                value={this.state.password}
                                onChange={e => {
                                    this.setState({ password: e.target.value });
                                    this.value = this.state.password;
                                }}
                                />
                                <Button
                                    type="submit"
                                    fullWidth
                                    variant="contained"
                                    color="primary"
                                    className={classes.submit}
                                    >
                                    Log In
                                </Button>
                        </form>
                    </div>
                </div>
            </Container>
        )        
    }

}

export default withStyles(useStyles)(Loginpage);
// import React, { Component, useContext } from 'react';
// import AuthContext from '../context/AuthContext'
// import console from "react-console";
// import Select from 'react-select'
// import ToggleButton from 'react-toggle-button'
// import languages from 'countries-list';
// import { w3cwebsocket as W3CWebSocket } from "websocket";

// import Button from '@material-ui/core/Button';
// import CssBaseline from '@material-ui/core/CssBaseline';
// import TextField from '@material-ui/core/TextField';
// import Link from '@material-ui/core/Link';
// import Grid from '@material-ui/core/Grid';
// import Typography from '@material-ui/core/Typography';
// import Container from '@material-ui/core/Container';
// import Card from '@material-ui/core/Card';
// import CardHeader from '@material-ui/core/CardHeader';
// import Paper from '@material-ui/core/Paper';
// import Avatar from '@material-ui/core/Avatar';
// import Slider from '@material-ui/core/Slider';

// import { withStyles } from "@material-ui/core/styles";

// const useStyles = theme => ({
//   paper: {
//     marginTop: theme.spacing(8),
//     display: 'flex',
//     flexDirection: 'column',
//     alignItems: 'center',
//   },
//   avatar: {
//     margin: theme.spacing(1),
//     backgroundColor: theme.palette.secondary.main,
//   },
//   form: {
//     width: '100%', // Fix IE 11 issue.
//     marginTop: theme.spacing(1),
//   },
//   submit: {
//     margin: theme.spacing(3, 0, 2),
//   },
//   root: {
//     boxShadow: 'none',
//   }
// });


// const sleep = (milliseconds) => {
//   return new Promise(resolve => setTimeout(resolve, milliseconds))
// }

// class Loginpage extends Component {

//     state = {
//         isLoggedIn: false,
//         username: '',
//         email: '',
//         password: '',
//         fields: {},
//         error: '',
//     }

//     loginUser = useContext(AuthContext)

//     handleValidation = async(e) =>  {
//         fetch('http://localhost:8000/chat/validate_login/', {
//           method: 'POST', // или 'PUT'
//           body: JSON.stringify({email: this.state.email, password: this.state.password}), // данные могут быть 'строкой' или {объектом}!
//           headers: {
//             'Content-Type': 'application/json'
//           }
//         })
//             .then(response => response.json().then((text) => {
//                 if (text.exists==='yes'){
//                     // log in
//                     alert("yeeei")
//                 }
//                 else {
//                     alert("noo :(")
//                 }
//                 e.preventDefault();
//             }));
//     }

//   componentDidMount() {
//   }
  
//   componentWillUpdate(nextProps, nextState) {
//   }

//   render() {
//     const { classes } = this.props;
//     let {loginUser} = useContext(AuthContext)
//     return (
//       <Container component="main" maxWidth="xs">
//           <div>
//             <CssBaseline />
//             <div className={classes.paper}>
//               <Typography component="h1" variant="h5">
//                 ChattyRooms
//                 </Typography>
//               <form className={classes.form} noValidate>
//                 <TextField
//                   variant="outlined"
//                   margin="normal"
//                   required
//                   fullWidth
//                   name="email"
//                   label="Email"
//                   type="email"
//                   id="email"
//                   value={this.state.email}
//                   onChange={e => {
//                     this.setState({ email: e.target.value });
//                     this.value = this.state.email;
//                   }}
//                 />
//                 <TextField
//                   variant="outlined"
//                   margin="normal"
//                   required
//                   fullWidth
//                   name="password"
//                   label="Password"
//                   type="password"
//                   id="password"
//                   value={this.state.password}
//                   onChange={e => {
//                     this.setState({ password: e.target.value });
//                     this.value = this.state.password;
//                   }}
//                 />
//                 <span style={{ color: "red" }}>{this.state.error}</span>
//                 <Button
//                   onClick={this.handleValidation}
//                   type="button"
//                   fullWidth
//                   variant="contained"
//                   color="primary"
//                   className={classes.submit}
//                 >
//                   Login
//                   </Button>
//                 <Grid container>
//                   <Grid item xs>
//                     <Link href="#" variant="body2">
//                       Forgot password?
//                       </Link>
//                   </Grid>
//                 </Grid>
//               </form>
//             </div>
//           </div>
//       </Container>
//     )

//   }
// }
// export default withStyles(useStyles)(Loginpage);


import React, {useContext} from 'react'
import AuthContext from '../context/AuthContext'

const Loginpage = () => {
    let {loginUser} = useContext(AuthContext)
    return (
        <div>
            <form onSubmit={loginUser}>
                <input type="text" name="username" placeholder="Enter Username" />
                <input type="password" name="password" placeholder="Enter Password" />
                <input type="submit"/>
            </form>
        </div>
    )
}

export default Loginpage
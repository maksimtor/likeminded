import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import console from "react-console";
import Select from 'react-select'
import ToggleButton from 'react-toggle-button'
import languages from 'countries-list';
import { w3cwebsocket as W3CWebSocket } from "websocket";

import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
// import Link from '@material-ui/core/Link';
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
import { FreeButton as CustomButton } from '../components/FreeButton';
import { CustomLink } from '../components/CustomLink';

const useStyles = theme => ({
  // paper: {
  //   marginTop: theme.spacing(8),
  //   display: 'flex',
  //   flexDirection: 'column',
  //   alignItems: 'center',
  // },
  // avatar: {
  //   margin: theme.spacing(1),
  //   backgroundColor: theme.palette.secondary.main,
  // },
  // form: {
  //   width: '100%', // Fix IE 11 issue.
  //   marginTop: theme.spacing(1),
  // },
  // submit: {
  //   margin: theme.spacing(3, 0, 2),
  // },
  // root: {
  //   boxShadow: 'none',
  // },
  paper: {
    padding: '150px 0',
    textAlign: 'center',
  },
  chatEnd: {
    textAlign: 'center',
  }
});

const genders = [
  { value: 'M', label: 'Male' },
  { value: 'F', label: 'Female' },
  { value: 'A', label: 'Other/Anything' }
]

const goals = [
  { value: 'FR', label: 'Friendship' },
  { value: 'RO', label: 'Romantic' },
  { value: 'AN', label: 'Anything' }
]

const interests = [
  ".net",
  "3d",
  "3d-modeling",
  "3d-printing",
  "a.i.",
  "accounting",
  "action-movies",
  "actionscript",
  "advertising",
  "agile",
  "air-sports",
  "algorithms",
  "alternative-energy",
  "alternative-health",
  "alternative-music",
  "ambient-music",
  "american-football",
  "analytics",
  "anatomy",
  "android",
  "angular",
  "animals",
  "animation",
  "anime",
  "archaeology",
  "architecture",
  "art",
  "art-history",
  "assembly-language",
  "astronomy",
  "autocad",
  "autodesk",
  "back-end",
  "beauty",
  "biology",
  "biomechanics",
  "bloging",
  "blues-music",
  "board-games",
  "books",
  "bootstrap",
  "botany",
  "branding",
  "business",
  "c++",
  "c-sharp",
  "cars",
  "chemistry",
  "classical-music",
  "climbing",
  "clojure",
  "cloud-computing",
  "cobol",
  "cocos2d",
  "coffeescript",
  "computer-science",
  "confectionery",
  "cooking",
  "cordova",
  "cosmology",
  "country-music",
  "crime-stories",
  "cryptography",
  "css",
  "culture",
  "cycling",
  "d3",
  "dance",
  "dance-music",
  "dart",
  "data-structures",
  "design",
  "design-patterns",
  "digital-art",
  "diving",
  "django",
  "drawing",
  "ecology",
  "ecommerce",
  "electronic-music",
  "electronics",
  "elixir",
  "elm",
  "ember.js",
  "engineering",
  "express",
  "fashion",
  "film",
  "flex",
  "flux",
  "folk-music",
  "football",
  "foreign-languages",
  "fortran",
  "front-end",
  "functional-programming",
  "game-design",
  "gaming",
  "gardening",
  "geology",
  "geometry",
  "ghost-hunting",
  "git",
  "github",
  "go",
  "google",
  "graphic-design",
  "grunt",
  "gulp",
  "hip-hop-music",
  "history",
  "html",
  "identity",
  "illustration",
  "illustrator",
  "indie-pop",
  "industrial-design",
  "inspirational-music",
  "interactive-design",
  "ionic",
  "ios",
  "java",
  "javascript",
  "jazz-music",
  "jogging",
  "jquery",
  "jsf",
  "kitesurfing",
  "lapis",
  "laravel",
  "latin-music",
  "learning",
  "lego",
  "less",
  "life",
  "linux",
  "lisp",
  "literature",
  "logic",
  "lua",
  "magento",
  "magic",
  "marketing",
  "math",
  "mathematics",
  "matlab",
  "mean.js",
  "mechanics",
  "medicine",
  "meteor",
  "meteorology",
  "moai-sdk",
  "mobile",
  "mongodb",
  "motor-sports",
  "multimedia",
  "music",
  "mvc",
  "mysql",
  "nature",
  "news",
  "node.js",
  "nodebots",
  "objective-c",
  "oceanography",
  "oocss",
  "oop",
  "open-source",
  "opera",
  "origami",
  "osx",
  "perl",
  "philosophy",
  "photography",
  "photoshop",
  "php",
  "pixi.js",
  "pop-music",
  "programming",
  "psychology",
  "python",
  "r&b-music",
  "raspberry-pi",
  "react",
  "reggae",
  "robotics",
  "rock-music",
  "ruby",
  "ruby-on-rails",
  "rust",
  "rxjs",
  "sailing",
  "sailor",
  "sails.js",
  "sass",
  "scala",
  "science",
  "science-fiction",
  "scratch",
  "scrum",
  "shopping",
  "socket.io",
  "software",
  "soul",
  "space",
  "spark",
  "sport",
  "spring-mvc",
  "sql",
  "stage3d",
  "startups",
  "statistics",
  "swift",
  "symphony",
  "systems-theory",
  "tdd",
  "technology",
  "turbogears",
  "typescript",
  "typography",
  "ufo",
  "ui-design",
  "universe",
  "ux-design",
  "vaadin",
  "video-gaming",
  "vim",
  "water-sports",
  "web",
  "web-design",
  "web2py",
  "webgl",
  "webkit",
  "webpack",
  "windows",
  "wordpress",
  "writing",
  "yoga",
  "zend",
  "zoology"
];


let languages_select = [];
let interests_select = [];
let countries_select = [];
let areas_select = [];

for (const [key, value] of Object.entries(languages.languages)) {
  // languages_select.push({value: l.key, label: l.name})
  languages_select.push({value: key, label:value.name})
  console.log("hi")
}

for (const [key, value] of Object.entries(languages.continents)) {
  // languages_select.push({value: l.key, label: l.name})
  areas_select.push({value: key, label:value})
  console.log("hi")
}

for (const [key, value] of Object.entries(languages.countries)) {
  // languages_select.push({value: l.key, label: l.name})
  countries_select.push({value: key, label:value.name})
  areas_select.push({value: key, label:value.name})
  console.log("hi")
}

for (const i in interests) {
  // languages_select.push({value: l.key, label: l.name})
  interests_select.push({value: interests[i], label:interests[i]})
  console.log("hi")
}

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

class InChatSearch extends Component {
     static contextType = AuthContext

  state = {
    isLoggedIn: false,
    messages: [],
    value: '',
    name: 'hey',
    age: '',
    gender: 'M',
    languages: [],
    interests: [],
    country: '',
    room: '',
    locToggle: false,
    geoLat: '',
    geoLon: '',
    polEco: 5,
    polGov: 5,
    personalityExtraversion: 5,
    personalityAgreeableness: 5,
    personalityOpenness: 5,
    personalityConscientiousness: 5,
    personalityNeuroticism: 5,
    politPref: false,
    intPref: false,
    locPref: false,
    areaPref: [],
    persPref: false,
    goals:'',
    genderPref: '',
    ageRange:[1,100],
    ageOptimal: 25,
    canUnblind: false,              // get data from api if partner is registered
    unblindRequestSent: false,      
    unblindRequestReceived: false,
    unblinded: false,
    status: 'prepare',
  }

  // client = new W3CWebSocket('ws://localhost:8000/ws/chat/' + this.state.room + '/');

  onButtonClicked = (e) => {
    const {user} =this.context;
    this.client.send(JSON.stringify({
      type: "chat_message",
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

  sendUnblindRequest = (e) => {
    const {user} =this.context;
    this.client.send(JSON.stringify({
      type: "unblind_request",
      message: user.custom_user_id,
      name: 'name'
    }));
    this.state.unblindRequestSent = true;
    e.preventDefault();
  }

  approveUnblindRequest = (e) => {
    const {user} =this.context;
    this.client.send(JSON.stringify({
      type: "approve_request",
      message: user.custom_user_id,
      name: 'name'
    }));
    this.state.unblinded = true;
    e.preventDefault();
  }

  success = (pos) => {
    this.setState({ geoLat: pos.coords.latitude });
    this.setState({ geoLon: pos.coords.longitude });
  }

  endChat = (e) => {
    this.client.close();
    this.setState({ status: 'ended' });
  }

  stopSearch = (e) => {
    this.setState( {status: 'prepare'});
    this.searchClient.close();
    e.preventDefault();
  }


  enterRoom = async(e) => {
          this.setState({status: 'searching'});
          const {user} = this.context;
          let client = new W3CWebSocket('ws://localhost:8000/ws/chat_search/' + user.custom_user_id + '/');
          this.searchClient = client;
          client.onopen = function(e) {
            client.send(JSON.stringify({
              type: "message",
              message: 'Start searching',
              name: "name"
            }));
          };
          client.onmessage = (message) => {
            const dataFromServer = JSON.parse(message.data);
            console.log('got reply! ', dataFromServer.type);
            if (dataFromServer) {
              let room = dataFromServer.message;
              this.setState({ room: room });
              this.client = new W3CWebSocket('ws://localhost:8000/ws/chat/' + this.state.room + '/');
              this.client.onopen = () => {
                // this.client.send(JSON.stringify({
                //   type: "possible_unblind",
                //   message: user.custom_user_id,
                //   name: "name"
                // }));
              this.setState({ status: 'chatting' })
              };
              this.client.onmessage = (message) => {
                const dataFromServer = JSON.parse(message.data);
                if (dataFromServer) {
                  if (dataFromServer.type === 'exit_message') {
                    this.setState({ status: 'ended' });

                  }
                  else if (dataFromServer.type === 'possible_unblind'){
                    if (dataFromServer.message.toString() !== user.custom_user_id.toString()){
                      this.setState({ canUnblind: true })
                      this.setState({ talkingWith: dataFromServer.message})
                        fetch('http://localhost:8000/chat/create_historical_chat/', {
                          method: 'POST', // или 'PUT'
                          body: JSON.stringify({user1: user.custom_user_id, user2: dataFromServer.message}), // данные могут быть 'строкой' или {объектом}!
                          headers: {
                            'Content-Type': 'application/json'
                          }
                        })
                            .then(response => response.json().then((text) => {
                                
                            }));
                    }
                  }
                  else if (dataFromServer.type === 'unblind_request'){
                    this.setState({ canUnblind: false })
                    if (dataFromServer.message.toString() !== user.custom_user_id.toString()) {
                      this.setState({ unblindRequestReceived: true });
                    }
                  }
                  else if (dataFromServer.type === 'approve_request'){
                    this.setState({ canUnblind: false })
                    this.setState({unblindRequestReceived: false})
                    if (dataFromServer.message.toString() !== user.custom_user_id.toString()){
                        fetch('http://localhost:8000/chat/create_chat_room/', {
                          method: 'POST', // или 'PUT'
                          body: JSON.stringify({user1: user.custom_user_id, user2: dataFromServer.message}), // данные могут быть 'строкой' или {объектом}!
                          headers: {
                            'Content-Type': 'application/json'
                          }
                        })
                            .then(response => response.json().then((text) => {
                                this.setState({ unblinded: true })
                            }));
                    }
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
              this.setState({ isLoggedIn: true });
            }
          };
  }

  componentDidMount() {
    this.userData = JSON.parse(localStorage.getItem('user'));
    if (localStorage.getItem('user')) {
        this.setState({
          name: this.userData.name,
          age: this.userData.age,
          gender: this.userData.gender,
          languages: this.userData.languages,
          interests: this.userData.interests,
          country: this.userData.country,
          locToggle: this.userData.locToggle,
          geoLat: this.userData.geoLat,
          geoLon: this.userData.geoLon,
          polEco: this.userData.polEco,
          polGov: this.userData.polGov,
          personalityExtraversion: this.userData.personalityExtraversion,
          personalityAgreeableness: this.userData.personalityAgreeableness,
          personalityOpenness: this.userData.personalityOpenness,
          personalityConscientiousness: this.userData.personalityConscientiousness,
          personalityNeuroticism: this.userData.personalityNeuroticism,
          politPref: this.userData.politPref,
          intPref: this.userData.intPref,
          locPref: this.userData.locPref,
          areaPref: this.userData.areaPref,
          persPref: this.userData.persPref,
          goals: this.userData.goals,
          genderPref: this.userData.genderPref,
          ageRange: this.userData.ageRange,
          ageOptimal: this.userData.ageOptimal
        })
    }
      // this.client.onopen = () => {
      //   console.log('WebSocket Client Connected');
      // };
      // this.client.onmessage = (message) => {
      //   const dataFromServer = JSON.parse(message.data);
      //   console.log('got reply! ', dataFromServer.type);
      //   if (dataFromServer) {
      //     this.setState((state) =>
      //       ({
      //         messages: [...state.messages,
      //         {
      //           msg: dataFromServer.message,
      //           name: dataFromServer.name,
      //         }]
      //       })
      //     );
      //   }
      // };
    
  }
  
  componentWillUpdate(nextProps, nextState) {
    // localStorage.setItem('user', JSON.stringify(nextState));
  }



  render() {
    // window.navigator.geolocation.getCurrentPosition(this.success, this.success);
    const { classes } = this.props;
    return (
      <Container component="main" maxWidth="xs">
        {this.state.status === 'chatting' || this.state.status === 'ended' ?
          <div>
            You are talking to user
            <Paper style={{ height: 400, maxHeight: 500, overflow: 'auto', boxShadow: 'none', }}>
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

            { this.state.status === 'ended' ?

            <div>
            <div className={classes.chatEnd}>
            <div className='ended-div'>Chat ended!</div>
                <CustomButton
                  onClick={this.enterRoom}
                  type="button"
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                >
                  Start Chatting Again!
                  </CustomButton>
                  </div>
            </div>
            :
            <div>
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
              <CustomButton
                type="submit"
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
              >
                Search again
                </CustomButton>
              </form>
                <CustomButton
                  onClick={this.endChat}
                  type="button"
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                >
                  End chat!
                  </CustomButton>
              </div>}
              {this.state.canUnblind ?
                <div>
              <CustomButton
                  onClick={this.sendUnblindRequest}
                  type="button"
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                >
                  Unblind
                  </CustomButton>
                  <CustomButton
                                    buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                    onClick={e => {
                      this.ignoreUser({ friend_id: this.state.talkingWith});
                    }}
                  >  Ignore
                  </CustomButton>
                  </div>
                :
                <div></div>
                }

              {this.state.unblindRequestReceived ?
              <CustomButton
                  onClick={this.approveUnblindRequest}
                  type="button"
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                >
                  Approve
                  </CustomButton>
                :
                <div></div>
                }
              {this.state.unblinded ? <div>Unblinded!</div> : <div></div>}
          </div>

          : this.state.status === 'prepare' ?

          <div>
            <div className={classes.paper}>
              <form noValidate>
                <CustomButton
                  onClick={this.enterRoom}
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                  fullWidth
                >
                  Naiti sobesednika
                  </CustomButton>
                <div className='or'>or</div>
                <Link className="mainLink" to="/profile">Izmenit predpochteniya</Link>
              </form>
            </div>
          </div>

          : this.state.status === 'searching' ?

          <div className={classes.paper}><div class="loader"></div>
                          <CustomButton
                  onClick={this.stopSearch}
                  type="button"
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                >
                  Stop search
                  </CustomButton></div>
          : <div></div>}
      </Container>
    )

  }
}
export default withStyles(useStyles)(InChatSearch);

// export {Chatsearch}
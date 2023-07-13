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

class Chatsearch extends Component {

  state = {
    isLoggedIn: false,
    messages: [],
    value: '',
    name: 'hey',
    age: '',
    gender: { value: 'A', label: 'Other/Anything' },
    interests: [],
    room: '',
    locToggle: false,
    geoLat: 0,
    geoLon: 0,
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
    areaRestrictToggle: false,
    areaPref: 10,
    persPref: false,
    goals:{ value: 'AN', label: 'Anything' },
    genderPref: { value: 'A', label: 'Other/Anything' },
    ageRange:[1,100],
    ageOptimal: 25,
    status: 'prepare',
  }

  // client = new W3CWebSocket('ws://localhost:8000/ws/chat/' + this.state.room + '/');

  onButtonClicked = (e) => {
    this.client.send(JSON.stringify({
      type: "chat_message",
      message: this.state.value,
      name: this.state.name
    }));
    this.state.value = ''
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
    var json_data = {'name': this.state.name};
    var state = this.state
    state['registration'] = false
    fetch('http://localhost:8000/chat/create_user/', {
      method: 'POST', // или 'PUT'
      body: JSON.stringify(this.state), // данные могут быть 'строкой' или {объектом}!
      headers: {
        'Content-Type': 'application/json'
      }
    })
        .then(response => response.json().then((text) => {
          let client = new W3CWebSocket('ws://localhost:8000/ws/chat_search/' + text.user_id + '/');
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
                console.log('WebSocket Client Connected');
              };
              this.setState({ status: 'chatting' })
              this.client.onmessage = (message) => {
                const dataFromServer = JSON.parse(message.data);
                console.log('got reply! ', dataFromServer.type);
                if (dataFromServer) {
                  if (dataFromServer.type === 'exit_message') {
                    this.setState({ isLoggedIn: false });
                    this.setState({ status: 'ended' });
                  } else {
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
        }));
  }

  componentDidMount() {
    this.userData = JSON.parse(localStorage.getItem('user'));
    if (localStorage.getItem('user')) {
        this.setState({
          name: this.userData.name,
          age: this.userData.age,
          gender: this.userData.gender,
          interests: this.userData.interests,
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
          areaRestrictToggle: this.userData.areaRestrictToggle,
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
    localStorage.setItem('user', JSON.stringify(nextState));
  }

  render() {
    // window.navigator.geolocation.getCurrentPosition(this.success, this.success);
    const { classes } = this.props;
    return (
      <Container component="main" maxWidth="xs">
        {this.state.status === 'chatting' || this.state.status === 'ended' ?
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

            { this.state.status === 'ended' ?
            <div>
            <span>Chat ended!</span>
                <Button
                  onClick={this.enterRoom}
                  type="button"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  Start Chatting Again!
                  </Button>
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
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
              >
                Start Chatting
                </Button>
            </form>
                            <Button
                  onClick={this.endChat}
                  type="button"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  End chat!
                  </Button>
              </div>}
          </div>

          : this.state.status === 'prepare' ?

          <div>
            <div className={classes.paper}>
              <Typography component="h1" variant="h5">
                ChattyRooms
                </Typography>
              <h3>Tell us about yourself :)</h3>
              {this.state.geo}
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
                  value={this.state.name}
                  onChange={e => {
                    this.setState({ name: e.target.value });
                    this.value = this.state.name;
                  }}
                />
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  name="Age"
                  label="Age"
                  type="Age"
                  id="age"
                  value={this.state.age}
                  onChange={e => {
                    this.setState({ age: e.target.value });
                    this.value = this.state.age;
                  }}
                />
                <label for="gender">Gender: </label>
                <Select
                 value={this.state.gender}
                 onChange={(value) => {
                  this.setState({gender: value})
                 }}
                 name="gender"
                 id="gender"
                 options={genders}
                />
                <label for="inetests">Interests: </label>
                <Select
                 value={this.state.interests}
                 onChange={(value) => {
                  this.setState({interests: value})
                 }}
                 name="interests"
                 id="interests"
                 options={interests_select}
                 isMulti
                />
                <label>Get location: </label>
                <ToggleButton
                  value={ this.state.locToggle || false }
                  onToggle={(value) => {
                    this.setState({locToggle: !value,});
                    if (!this.state.locToggle) {window.navigator.geolocation.getCurrentPosition(this.success, this.success)};
                  }} />
                <div>
                {(() => {
                  if (this.state.locToggle) {
                    return (<>{this.state.geoLat}:{this.state.geoLon}</>)
                  }
                })()}
                </div>
                <p> Political coordinates </p>
                <p>Are you leaning towards left or right? </p>
                <Slider 
                  value={this.state.polEco}
                  step={1}
                  marks
                  min={-10}
                  max={10}
                  onChange={(event: any, newValue: any) => {
                    this.setState({polEco: newValue})
                  }} 
                  />
                <p>Are you leaning towards liberalism or auth? </p>
                <Slider 
                  value={this.state.polGov}
                  step={1}
                  marks
                  min={-10}
                  max={10}
                  onChange={(event: any, newValue: any) => {
                    this.setState({polGov: newValue})
                  }} 
                  />
                <p> Personality </p>
                <p> Extraversion </p>
                <Slider 
                  value={this.state.personalityExtraversion}
                  step={1}
                  marks
                  min={0}
                  max={10}
                  onChange={(event: any, newValue: any) => {
                    this.setState({personalityExtraversion: newValue})
                  }} 
                  />
                <p> Agreeableness </p>
                <Slider 
                  value={this.state.personalityAgreeableness}
                  step={1}
                  marks
                  min={0}
                  max={10}
                  onChange={(event: any, newValue: any) => {
                    this.setState({personalityAgreeableness: newValue})
                  }} 
                  />
                <p> Openness </p>
                <Slider 
                  value={this.state.personalityOpenness}
                  step={1}
                  marks
                  min={0}
                  max={10}
                  onChange={(event: any, newValue: any) => {
                    this.setState({personalityOpenness: newValue})
                  }} 
                  />
                <p> Conscientiousness </p>
                <Slider 
                  value={this.state.personalityConscientiousness}
                  step={1}
                  marks
                  min={0}
                  max={10}
                  onChange={(event: any, newValue: any) => {
                    this.setState({personalityConscientiousness: newValue})
                  }} 
                  />
                <p> Neuroticism </p>
                <Slider 
                  value={this.state.personalityNeuroticism}
                  step={1}
                  marks
                  min={0}
                  max={10}
                  onChange={(event: any, newValue: any) => {
                    this.setState({personalityNeuroticism: newValue})
                  }} 
                  />
                <p> Preferences </p>
                <p> Do you want to find a person with similar political beliefs? </p>
                <ToggleButton
                  value={ this.state.politPref || false }
                  onToggle={(value) => {
                    this.setState({politPref: !value,});
                  }} />
                <p> Do you care about person location? </p>
                <ToggleButton
                  value={ this.state.locPref || false }
                  onToggle={(value) => {
                    this.setState({locPref: !value,});
                  }} />
                <p> Do you want to restrict location area? </p>
                <ToggleButton
                  value={ this.state.areaRestrictToggle || false }
                  onToggle={(value) => {
                    this.setState({areaRestrictToggle: !value,});
                  }} />
                {this.state.areaRestrictToggle ?
                <div>
                <label for="areaPref">Restrict area: </label>
                <Slider
                  valueLabelDisplay="on"
                  value={this.state.areaPref}
                  step={1}
                  min={0}
                  max={100}
                  onChange={(event: any, newValue: any) => {
                    this.setState({areaPref: newValue})
                  }} 
                  />
                </div>
                :
                <div></div>
                }
                <p> Do you want to find a person with similar interests? </p>
                <ToggleButton
                  value={ this.state.intPref || false }
                  onToggle={(value) => {
                    this.setState({intPref: !value,});
                  }} />
                <p> Do you want to find a person with similar personality? </p>
                <ToggleButton
                  value={ this.state.persPref || false }
                  onToggle={(value) => {
                    this.setState({persPref: !value,});
                  }} />
                <label for="goals">What are your goals? </label>
                <Select
                 value={this.state.goals}
                 onChange={(value) => {
                  this.setState({goals: value})
                 }}
                 name="goals"
                 id="goals"
                 options={goals}
                />
                <label for="goals">Do you care about gender of the person? </label>
                <Select
                 value={this.state.genderPref}
                 onChange={(value) => {
                  this.setState({genderPref: value})
                 }}
                 name="gender"
                 id="gender"
                 options={genders}
                />
                <p> Age pref: </p>
                <Slider
                  getAriaLabel={() => 'Temperature range'}
                  value={this.state.ageRange}
                  valueLabelDisplay="on"
                  step={1}
                  min={0}
                  max={100}
                  onChange={(event: any, newValue: any) => {
                    this.setState({ageRange: newValue})
                  }} 
                  />
                <p> Optimal age: </p>
                <Slider
                  valueLabelDisplay="on"
                  value={this.state.ageOptimal}
                  step={1}
                  min={0}
                  max={100}
                  onChange={(event: any, newValue: any) => {
                    this.setState({ageOptimal: newValue})
                  }} 
                  />

                <Button
                  onClick={this.enterRoom}
                  type="button"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  Start Chatting
                  </Button>
                <Grid container>
                  <Grid item xs>
                    <Link href="#" variant="body2">
                      Forgot password?
                      </Link>
                  </Grid>
                  <Grid item>
                    <Link href="#" variant="body2">
                      {"Don't have an account? Sign Up"}
                    </Link>
                  </Grid>
                </Grid>
              </form>
            </div>
          </div>
        : this.state.status === 'searching' ?
                  <div>Searching
                          <Button
                  onClick={this.stopSearch}
                  type="button"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  Stop search
                  </Button></div>
          : <div></div>
        }
      </Container>
    )

  }
}
export default withStyles(useStyles)(Chatsearch);

// export {Chatsearch}
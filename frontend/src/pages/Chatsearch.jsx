import React, { Component } from 'react';
import console from "react-console";
import Select from 'react-select'
import ToggleButton from 'react-toggle-button'
import languages from 'countries-list';
import { w3cwebsocket as W3CWebSocket } from "websocket";

import Button from '@material-ui/core/Button';
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
import { FreeButton as CustomButton } from '../components/FreeButton';


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
  languages_select.push({ value: key, label: value.name });
  console.log("hi");
}

for (const [key, value] of Object.entries(languages.continents)) {
  // languages_select.push({value: l.key, label: l.name})
  areas_select.push({ value: key, label: value });
  console.log("hi");
}

for (const [key, value] of Object.entries(languages.countries)) {
  // languages_select.push({value: l.key, label: l.name})
  countries_select.push({ value: key, label: value.name });
  areas_select.push({ value: key, label: value.name });
  console.log("hi");
}

for (const i in interests) {
  // languages_select.push({value: l.key, label: l.name})
  interests_select.push({ value: interests[i], label: interests[i] });
  console.log("hi");
}

class Chatsearch extends Component {
  static contextType = AuthContext

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
    polToggle: false,
    polEco: 5,
    polGov: 5,
    persToggle: false,
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
    goals: { value: 'AN', label: 'Anything' },
    genderPref: { value: 'A', label: 'Other/Anything' },
    ageRange: [1, 100],
    ageOptimal: 25,
    status: 'prepare',
    user_info: {
      description: "Nothing",
      country: null,
      languages: null,
      interests: [],
      polit_coordinates: null,
      age: 25,
      location: null,
      gender: { value: 'A', label: 'Other/Anything' },
      personality: null,
    },
    user_prefs: {
      age: { min_age: 18, max_age: 100, optimal_age: 25 },
      polit: true,
      interests: true,
      location: true,
      personality: true,
      area_restrict: true,
      loc_area: 10,
      goals: { value: 'AN', label: 'Anything' },
      gender: { value: 'A', label: 'Other/Anything' },
    }
  }

  onButtonClicked = (e) => {
    this.client.send(JSON.stringify({
      type: "chat_message",
      message: this.state.value,
      name: this.state.name
    }));
    this.setState({ value: '' })
    e.preventDefault();
  }

  success = (pos) => {
    let copyInfo = { ...this.state.user_info };
    copyInfo.location = {}
    copyInfo.location.lon = pos.coords.longitude;
    copyInfo.location.lat = pos.coords.latitude;
    this.setState({ user_info: copyInfo });
    // this.setState({ geoLat:  });
    // this.setState({ geoLon:  });
  }
  endChat = () => {
    this.client.close();
    this.setState({ status: 'ended' });
  }

  stopSearch = (e) => {
    this.setState({ status: 'prepare' });
    this.searchClient.close();
    e.preventDefault();
  }

  enterRoom = async () => {
    this.setState({ status: 'searching' });
    var state = JSON.parse(JSON.stringify(this.state));
    state['registration'] = false;
    state['user_info']['gender'] = this.state.user_info.gender.value;
    state['user_prefs']['goals'] = this.state.user_prefs.goals.value;
    state['user_prefs']['gender'] = this.state.user_prefs.gender.value;
    var int_values = [];
    for (var key in state.user_info.interests) {
      int_values.push(state.user_info.interests[key].value);
      alert(state.user_info.interests[key].value);
    }
    state['user_info']['interests'] = int_values;
    fetch('http://localhost:8000/chat/api/users/', {
      method: 'POST', // или 'PUT'
      body: JSON.stringify(state), // данные могут быть 'строкой' или {объектом}!
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(response => response.json().then((text) => {
        let client = new W3CWebSocket('ws://localhost:8000/ws/chat_search/' + text.id + '/');
        this.searchClient = client;
        client.onopen = function () {
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
            this.client = new W3CWebSocket('ws://localhost:8000/ws/chat/' + this.state.room + '/' + text.id + '/');
            this.client.onopen = () => {
              console.log('WebSocket Client Connected');
            };
            this.setState({ status: 'chatting' })
            this.client.onmessage = (message) => {
              const dataFromServer = JSON.parse(message.data);
              console.log('got reply! ', dataFromServer.type);
              if (dataFromServer) {
                if (dataFromServer.type === 'exit_message') {
                  this.client.close();
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
      let gender = this.userData.user_info.gender;
      var gender_reformed;
      var i;
      for (i in genders) {
        if (genders[i].value === gender) {
          gender_reformed = genders[i];
          this.userData.user_info.gender = gender_reformed;
          break;
        }
      }

      let goals_db = this.userData.user_prefs.goals;
      var goals_reformed;
      for (i in goals) {
        if (goals[i].value === goals_db) {
          goals_reformed = goals[i];
          this.userData.user_prefs.goals = goals_reformed;
          break;
        }
      }

      let gender_pref = this.userData.user_prefs.gender;
      var gender_pref_reformed;
      for (i in genders) {
        if (genders[i].value === gender_pref) {
          gender_pref_reformed = genders[i];
          this.userData.user_prefs.gender = gender_pref_reformed;
          break;
        }
      }
      this.setState({
        name: this.userData.name,
        age: this.userData.age,
        user_info: this.userData.user_info,
        user_prefs: this.userData.user_prefs,
      })
    }

  }

  UNSAFE_componentWillUpdate(nextProps, nextState) {
    localStorage.setItem('user', JSON.stringify(nextState));
  }

  render() {
    const { classes } = this.props;
    return (
      <Container component="main" maxWidth="xs">
        {this.state.status === 'chatting' || this.state.status === 'ended' ?
          <div>
            Room Name: {this.state.room}
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

            {this.state.status === 'ended' ?
              <div>
                <span>Chat ended!</span>
                <CustomButton
                  onClick={this.enterRoom}
                  type="button"
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  Start Chatting Again!
                </CustomButton>
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
                    fullWidth
                    variant="contained"
                    color="primary"
                    className={classes.submit}
                  >
                    Start Chatting
                  </CustomButton>
                </form>
                <CustomButton
                  onClick={this.endChat}
                  buttonStyle='btn--nrm'
                  buttonSize='btn--large'
                  type="button"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  End chat!
                </CustomButton>
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
                    value={this.state.user_info.age}
                    onChange={e => {
                      let copyInfo = { ...this.state.user_info };
                      copyInfo.age = e.target.value;
                      this.setState({ user_info: copyInfo });
                      this.value = this.state.user_info.age;
                    }}
                  />
                  <label htmlFor="gender">Gender: </label>
                  <Select
                    value={this.state.user_info.gender}
                    onChange={(value) => {
                      let copyInfo = { ...this.state.user_info };
                      copyInfo.gender = value;
                      this.setState({ user_info: copyInfo });
                    }}
                    name="gender"
                    id="gender"
                    options={genders}
                  />
                  <label htmlFor="interests">Interests: </label>
                  <Select
                    value={this.state.user_info.interests}
                    onChange={(value) => {
                      let copyInfo = { ...this.state.user_info };
                      copyInfo.interests = value;
                      this.setState({ user_info: copyInfo });
                    }}
                    name="interests"
                    id="interests"
                    options={interests_select}
                    isMulti
                  />
                  <label>Get location: </label>
                  <ToggleButton
                    value={this.state.user_info.location}
                    onToggle={(value) => {
                      let copyInfo = { ...this.state.user_info };
                      copyInfo.location = value ? null : { lon: 0, lat: 0 };
                      this.setState({ user_info: copyInfo });
                      // this.setState({locToggle: !value,});
                      if (!this.state.user_info.location) {
                        window.navigator.geolocation.getCurrentPosition(this.success, this.success)
                      }
                    }} />
                  <div>
                    {(() => {
                      if (this.state.user_info.location) {
                        return (<>{this.state.user_info.location.lat}:{this.state.user_info.location.lon}</>)
                      }
                    })()}
                  </div>
                  <p> Political coordinates </p>
                  <ToggleButton
                    value={this.state.user_info.polit_coordinates}
                    onToggle={(value) => {
                      let copyInfo = { ...this.state.user_info };
                      copyInfo.polit_coordinates = value ? null : { eco: 0, cult: 0 };
                      this.setState({ user_info: copyInfo });
                    }} />
                  {(() => {
                    if (this.state.user_info.polit_coordinates) {
                      return (<div><p>Are you leaning towards left or right? </p>
                        <Slider
                          value={this.state.user_info.polit_coordinates.eco}
                          step={1}
                          marks
                          min={-10}
                          max={10}
                          onChange={(event, newValue) => {
                            let copyInfo = { ...this.state.user_info };
                            copyInfo.polit_coordinates.eco = newValue;
                            this.setState({ user_info: copyInfo });
                          }}
                        />
                        <p>Are you leaning towards liberalism or auth? </p>
                        <Slider
                          value={this.state.user_info.polit_coordinates.cult}
                          step={1}
                          marks
                          min={-10}
                          max={10}
                          onChange={(event, newValue) => {
                            let copyInfo = { ...this.state.user_info };
                            copyInfo.polit_coordinates.cult = newValue;
                            this.setState({ user_info: copyInfo });
                          }}
                        /></div>)
                    }
                  })()}

                  <p> Personality </p>
                  <ToggleButton
                    value={this.state.user_info.personality}
                    onToggle={(value) => {
                      let copyInfo = { ...this.state.user_info };
                      copyInfo.personality = value ? null : { extraversion: 0, agreeableness: 0, openness: 0, conscientiousness: 0, neuroticism: 0 };
                      this.setState({ user_info: copyInfo });
                    }} />
                  {(() => {
                    if (this.state.user_info.personality) {
                      return (<div><p> Extraversion </p>
                        <Slider
                          value={this.state.user_info.extraversion}
                          step={1}
                          marks
                          min={0}
                          max={10}
                          onChange={(event, newValue) => {
                            let copyInfo = { ...this.state.user_info };
                            copyInfo.personality.extraversion = newValue;
                            this.setState({ user_info: copyInfo });
                          }}
                        />
                        <p> Agreeableness </p>
                        <Slider
                          value={this.state.user_info.agreeableness}
                          step={1}
                          marks
                          min={0}
                          max={10}
                          onChange={(event, newValue) => {
                            let copyInfo = { ...this.state.user_info };
                            copyInfo.personality.agreeableness = newValue;
                            this.setState({ user_info: copyInfo });
                          }}
                        />
                        <p> Openness </p>
                        <Slider
                          value={this.state.user_info.openness}
                          step={1}
                          marks
                          min={0}
                          max={10}
                          onChange={(event, newValue) => {
                            let copyInfo = { ...this.state.user_info };
                            copyInfo.personality.openness = newValue;
                            this.setState({ user_info: copyInfo });
                          }}
                        />
                        <p> Conscientiousness </p>
                        <Slider
                          value={this.state.user_info.conscientiousness}
                          step={1}
                          marks
                          min={0}
                          max={10}
                          onChange={(event, newValue) => {
                            let copyInfo = { ...this.state.user_info };
                            copyInfo.personality.conscientiousness = newValue;
                            this.setState({ user_info: copyInfo });
                          }}
                        />
                        <p> Neuroticism </p>
                        <Slider
                          value={this.state.user_info.neuroticism}
                          step={1}
                          marks
                          min={0}
                          max={10}
                          onChange={(event, newValue) => {
                            let copyInfo = { ...this.state.user_info };
                            copyInfo.personality.neuroticism = newValue;
                            this.setState({ user_info: copyInfo });
                          }}
                        /></div>)
                    }
                  })()}

                  <p> Preferences </p>
                  <p> Do you want to find a person with similar political beliefs? </p>
                  <ToggleButton
                    value={this.state.user_prefs.polit || false}
                    onToggle={(value) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.polit = !value;
                      this.setState({ user_prefs: copyPrefs });
                    }} />
                  <p> Do you care about person location? </p>
                  <ToggleButton
                    value={this.state.user_prefs.location || false}
                    onToggle={(value) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.location = !value;
                      this.setState({ user_prefs: copyPrefs });
                    }} />
                  <p> Do you want to restrict location area? </p>
                  <ToggleButton
                    value={this.state.user_prefs.area_restrict || false}
                    onToggle={(value) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.area_restrict = !value;
                      this.setState({ user_prefs: copyPrefs });
                    }} />
                  {this.state.user_prefs.area_restrict ?
                    <div>
                      <label htmlFor="areaPref">Restrict area: </label>
                      <Slider
                        valueLabelDisplay="on"
                        value={this.state.user_prefs.loc_area}
                        step={1}
                        min={0}
                        max={100}
                        onChange={(event, newValue) => {
                          let copyPrefs = { ...this.state.user_prefs };
                          copyPrefs.loc_area = newValue;
                          this.setState({ user_prefs: copyPrefs });
                        }}
                      />
                    </div>
                    :
                    <div></div>
                  }
                  <p> Do you want to find a person with similar interests? </p>
                  <ToggleButton
                    value={this.state.user_prefs.interests}
                    onToggle={(value) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.interests = !value;
                      this.setState({ user_prefs: copyPrefs });
                    }} />
                  <p> Do you want to find a person with similar personality? </p>
                  <ToggleButton
                    value={this.state.user_prefs.personality}
                    onToggle={(value) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.personality = !value;
                      this.setState({ user_prefs: copyPrefs });
                    }} />
                  <label htmlFor="goals">What are your goals? </label>
                  <Select
                    value={this.state.user_prefs.goals}
                    onChange={(value) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.goals = value;
                      this.setState({ user_prefs: copyPrefs });
                    }}
                    name="goals"
                    id="goals"
                    options={goals}
                  />
                  <label htmlFor="goals">Do you care about gender of the person? </label>
                  <Select
                    value={this.state.user_prefs.gender}
                    onChange={(value) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.gender = value;
                      this.setState({ user_prefs: copyPrefs });
                    }}
                    name="gender"
                    id="gender"
                    options={genders}
                  />
                  <p> Age pref: </p>
                  <Slider
                    getAriaLabel={() => 'Temperature range'}
                    value={[this.state.user_prefs.age.min_age, this.state.user_prefs.age.max_age]}
                    valueLabelDisplay="on"
                    step={1}
                    min={0}
                    max={100}
                    onChange={(event, newValue) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.age.min_age = newValue[0];
                      copyPrefs.age.max_age = newValue[1];
                      this.setState({ user_prefs: copyPrefs });
                    }}
                  />
                  <p> Optimal age: </p>
                  <Slider
                    valueLabelDisplay="on"
                    value={this.state.user_prefs.age.optimal_age}
                    step={1}
                    min={0}
                    max={100}
                    onChange={(event, newValue) => {
                      let copyPrefs = { ...this.state.user_prefs };
                      copyPrefs.age.optimal_age = newValue;
                      this.setState({ user_prefs: copyPrefs });
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
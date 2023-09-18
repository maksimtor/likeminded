import React, { Component } from 'react';
import console from "react-console";
import Select from 'react-select'
import ToggleButton from 'react-toggle-button'
import languages from 'countries-list';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
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

class Profile extends Component {

  static contextType = AuthContext

  state = {
    isLoggedIn: false,
    messages: [],
    value: '',
    name: '',
    age: '',
    gender: genders.M,
    interests: [],
    room: '',
    locToggle: false,
    geoLat: '',
    geoLon: '',
    polToggle: false,
    polEco: 5,
    polGov: 5,
    persToggle: false,
    personalityExtraversion: 0,
    personalityAgreeableness: 0,
    personalityOpenness: 5,
    personalityConscientiousness: 5,
    personalityNeuroticism: 5,
    politPref: false,
    intPref: false,
    locPref: false,
    areaRestrictToggle: false,
    areaPref: 10,
    persPref: false,
    goals:'',
    genderPref: '',
    ageRange:[1,100],
    ageOptimal: 25,
    description: '',
    photo: '',
    image: '',
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
      age: {min_age: 18, max_age: 100, optimal_age: 25},
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

  // client = new W3CWebSocket('ws://localhost:8000/ws/chat/' + this.state.room + '/');

  onButtonClicked = (e) => {
    this.client.send(JSON.stringify({
      type: "message",
      message: this.state.value,
      name: this.state.name
    }));
    this.setState({ value: '' });
    e.preventDefault();
  }

  success = (pos) => {
    let copyInfo = {...this.state.user_info};
    copyInfo.location = {}
    copyInfo.location.lon = pos.coords.longitude;
    copyInfo.location.lat = pos.coords.latitude;
    this.setState({ user_info: copyInfo });
    // this.setState({ geoLat:  });
    // this.setState({ geoLon:  });
  }


  enterRoom = async(e) => {
    const {user, authTokens, csrfTokens} =this.context;
    var state = this.state
    state['user_id'] = user.user_id
    state['user_info']['gender'] = this.state.user_info.gender.value;
    state['user_prefs']['goals'] = this.state.user_prefs.goals.value;
    state['user_prefs']['gender'] = this.state.user_prefs.gender.value;
    state['user_info']['description'] = 'Hi';
    var int_values = [];
    for (var key in state.user_info.interests){
      int_values.push(state.user_info.interests[key].value);
      alert(state.user_info.interests[key].value);
    }
    state['user_info']['interests'] = int_values;

    fetch('http://localhost:8000/chat/api/users/' + user.custom_user_id + '/', {
      method: 'PATCH', // или 'PUT'
      body: JSON.stringify(state), // данные могут быть 'строкой' или {объектом}!
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': csrfTokens['X-CSRFToken'],
        'Authorization': 'Bearer ' + authTokens['access'],
      },
      credentials: "include"
    })
        .then(response => response.json().then((text) => {

        }));
  }
    handleImageChange = (e) => {
      const {user} =this.context;
    this.setState({
      image: e.target.files[0]
    })
    console.log(this.state);
    let form_data = new FormData();
    form_data.append('image', e.target.files[0]);
    form_data.append('user_id', user.custom_user_id)
    let url = 'http://localhost:8000/chat/upload_profile_photo/';
    fetch(url, {
      method: 'POST',
      body: form_data,
    })
        .then(res => {
        })
  };

  componentDidMount() {
    const {user, authTokens} =this.context;
    fetch('http://localhost:8000/chat/api/users/' + user.custom_user_id + '/', {
      method: 'GET', // или 'PUT'
      // body: JSON.stringify({'user_id': user.user_id}), // данные могут быть 'строкой' или {объектом}!
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authTokens['access'],
      }
    })
        .then(response => response.json().then((text) => {
          let gender = text.user_info.gender;
          var gender_reformed;
          var i;
          for (i in genders){
            if (genders[i].value === gender){
              gender_reformed = genders[i];
              text.user_info.gender = gender_reformed;
              break;
            }
          }

          let interests_db = text.user_info.interests;
          var interests_reformed = [];
          for (i in interests_db){
            interests_reformed.push({value: interests_db[i], label:interests_db[i]})
          }
          text.user_info.interests = interests_reformed;
          let goals_db = text.user_prefs.goals;
          var goals_reformed;
          for (i in goals){
            if (goals[i].value === goals_db){
              goals_reformed = goals[i];
              text.user_prefs.goals = goals_reformed;
              break;
            }
          }

          let gender_pref = text.user_prefs.gender;
          var gender_pref_reformed;
          for (i in genders){
            if (genders[i].value === gender_pref){
              gender_pref_reformed = genders[i];
              text.user_prefs.gender = gender_pref_reformed;
              break;
            }
          }
          // alert(country)
          this.setState({
            name: text.name,
            age: text.user_info.age,
            gender: gender_reformed,
            interests: interests_reformed,
            locToggle: text.user_info.location,
            geoLat: text.user_info.location ? text.user_info.location.lat : 0,
            geoLon: text.user_info.location ? text.user_info.location.lon : 0,
            polToggle: text.user_info.polit_coordinates,
            polEco: text.user_info.polit_coordinates ? text.user_info.polit_coordinates.eco : 0,
            polGov: text.user_info.polit_coordinates ? text.user_info.polit_coordinates.cult : 0,
            persToggle: text.user_info.personality,
            personalityExtraversion: text.user_info.personality ? text.user_info.personality.extraversion*10 : 0,
            personalityAgreeableness: text.user_info.personality ? text.user_info.personality.agreeableness*10 : 0,
            personalityOpenness: text.user_info.personality ? text.user_info.personality.openness*10 : 0,
            personalityConscientiousness: text.user_info.personality ? text.user_info.personality.conscientiousness*10 : 0,
            personalityNeuroticism: text.user_info.personality ? text.user_info.personality.neuroticism*10 : 0,
            politPref: text.user_prefs.polit,
            intPref: text.user_prefs.interests,
            locPref: text.user_prefs.location,
            areaRestrictToggle: text.user_prefs.area_restrict,
            areaPref: text.user_prefs.loc_area,
            persPref: text.user_prefs.personality,
            goals: goals_reformed,
            genderPref: gender_pref_reformed,
            ageRange: [text.user_prefs.age.min_age, text.user_prefs.age.max_age],
            ageOptimal: text.user_prefs.age.optimal_age,
            description: text.user_info.description,
            photo: text.photo,
            user_info: text.user_info,
            user_prefs: text.user_prefs,
        })

    }));
    
  }
  
  componentWillUpdate(nextProps, nextState) {
    // localStorage.setItem('user', JSON.stringify(nextState));
  }

  render() {
    // window.navigator.geolocation.getCurrentPosition(this.success, this.success);
    const { classes } = this.props;
    return (
      <Container component="main" maxWidth="xs">
        {this.state.isLoggedIn ?
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
            </form>
          </div>

          :

          <div>
            <div>
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
                    let copyInfo = {...this.state.user_info};
                    copyInfo.age = e.target.value;
                    this.setState({ user_info: copyInfo });
                    this.value = this.state.user_info.age;
                  }}
                />
                <label for="gender">Gender: </label>
                <Select
                 value={this.state.user_info.gender}
                 onChange={(value) => {
                  let copyInfo = {...this.state.user_info};
                  copyInfo.gender = value;
                  this.setState({ user_info: copyInfo });
                 }}
                 name="gender"
                 id="gender"
                 options={genders}
                />
                <label for="inetests">Interests: </label>
                <Select
                 value={this.state.user_info.interests}
                 onChange={(value) => {
                  let copyInfo = {...this.state.user_info};
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
                  value={ this.state.user_info.location }
                  onToggle={(value) => {
                    let copyInfo = {...this.state.user_info};
                    copyInfo.location = value ? null : {lon: 0, lat: 0};
                    this.setState({ user_info: copyInfo });
                    // this.setState({locToggle: !value,});
                    if (!this.state.user_info.location) {
                      window.navigator.geolocation.getCurrentPosition(this.success, this.success)
                    };
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
                  value={ this.state.user_info.polit_coordinates }
                  onToggle={(value) => {
                    let copyInfo = {...this.state.user_info};
                    copyInfo.polit_coordinates = value ? null : {eco: 0, cult: 0};
                    this.setState({ user_info: copyInfo });
                    // this.setState({polToggle: !value,});
                    //alert(this.state.polToggle)
                    //if (!this.state.polToggle) {window.navigator.geolocation.getCurrentPosition(this.success, this.success)};
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
                        onChange={(event: any, newValue: any) => {
                          let copyInfo = {...this.state.user_info};
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
                        onChange={(event: any, newValue: any) => {
                          let copyInfo = {...this.state.user_info};
                          copyInfo.polit_coordinates.cult = newValue;
                          this.setState({ user_info: copyInfo });
                        }} 
                        /></div>)
                  }
                })()}

                <p> Personality </p>
                <ToggleButton
                  value={ this.state.user_info.personality }
                  onToggle={(value) => {
                    let copyInfo = {...this.state.user_info};
                    copyInfo.personality = value ? null : {extraversion: 0, agreeableness: 0, openness: 0, conscientiousness: 0, neuroticism: 0};
                    this.setState({ user_info: copyInfo });
                    //alert(this.state.polToggle)
                    //if (!this.state.polToggle) {window.navigator.geolocation.getCurrentPosition(this.success, this.success)};
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
                  onChange={(event: any, newValue: any) => {
                    let copyInfo = {...this.state.user_info};
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
                  onChange={(event: any, newValue: any) => {
                    let copyInfo = {...this.state.user_info};
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
                  onChange={(event: any, newValue: any) => {
                    let copyInfo = {...this.state.user_info};
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
                  onChange={(event: any, newValue: any) => {
                    let copyInfo = {...this.state.user_info};
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
                  onChange={(event: any, newValue: any) => {
                    let copyInfo = {...this.state.user_info};
                    copyInfo.personality.neuroticism = newValue;
                    this.setState({ user_info: copyInfo });
                  }} 
                  /></div>)
                  }
                })()}
                
                <p> Preferences </p>
                <p> Do you want to find a person with similar political beliefs? </p>
                <ToggleButton
                  value={ this.state.user_prefs.polit || false }
                  onToggle={(value) => {
                    let copyPrefs = {...this.state.user_prefs};
                    copyPrefs.polit = !value;
                    this.setState({ user_prefs: copyPrefs });
                  }} />
                <p> Do you care about person location? </p>
                <ToggleButton
                  value={ this.state.user_prefs.location || false }
                  onToggle={(value) => {
                    let copyPrefs = {...this.state.user_prefs};
                    copyPrefs.location = !value;
                    this.setState({ user_prefs: copyPrefs });
                  }} />
                <p> Do you want to restrict location area? </p>
                <ToggleButton
                  value={ this.state.user_prefs.area_restrict || false }
                  onToggle={(value) => {
                    let copyPrefs = {...this.state.user_prefs};
                    copyPrefs.area_restrict = !value;
                    this.setState({ user_prefs: copyPrefs });
                  }} />
                {this.state.user_prefs.area_restrict ?
                <div>
                <label for="areaPref">Restrict area: </label>
                <Slider
                  valueLabelDisplay="on"
                  value={this.state.user_prefs.loc_area}
                  step={1}
                  min={0}
                  max={100}
                  onChange={(event: any, newValue: any) => {
                    let copyPrefs = {...this.state.user_prefs};
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
                  value={ this.state.user_prefs.interests }
                  onToggle={(value) => {
                    let copyPrefs = {...this.state.user_prefs};
                    copyPrefs.interests = !value;
                    this.setState({ user_prefs: copyPrefs });
                  }} />
                <p> Do you want to find a person with similar personality? </p>
                <ToggleButton
                  value={ this.state.user_prefs.personality}
                  onToggle={(value) => {
                    let copyPrefs = {...this.state.user_prefs};
                    copyPrefs.personality = !value;
                    this.setState({ user_prefs: copyPrefs });
                  }} />
                <label for="goals">What are your goals? </label>
                <Select
                 value={this.state.user_prefs.goals}
                 onChange={(value) => {
                  let copyPrefs = {...this.state.user_prefs};
                    copyPrefs.goals = value;
                    this.setState({ user_prefs: copyPrefs });
                 }}
                 name="goals"
                 id="goals"
                 options={goals}
                />
                <label for="goals">Do you care about gender of the person? </label>
                <Select
                 value={this.state.user_prefs.gender}
                 onChange={(value) => {
                  let copyPrefs = {...this.state.user_prefs};
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
                  onChange={(event: any, newValue: any) => {
                    let copyPrefs = {...this.state.user_prefs};
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
                  onChange={(event: any, newValue: any) => {
                    let copyPrefs = {...this.state.user_prefs};
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
                  Save info
                  </Button>
              </form>
            </div>
          </div>}
      </Container>
    )

  }
}
export default withStyles(useStyles)(Profile);

// export {Chatsearch}
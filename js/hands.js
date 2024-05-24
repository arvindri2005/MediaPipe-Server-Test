const video3 = document.getElementsByClassName('input_video3')[0];
const out3 = document.getElementsByClassName('output3')[0];
const controlsElement3 = document.getElementsByClassName('control3')[0];
const canvasCtx3 = out3.getContext('2d');
const fpsControl = new FPS();
const instructions = document.getElementById('instructions');



const spinner = document.querySelector('.loading');
spinner.ontransitionend = () => {
  spinner.style.display = 'none';
};

function onResultsHands(results) {

  // Cordinates which are required for the gesture recognition are sent to the server
  if(results.multiHandLandmarks && results.multiHandedness){
    const rightlandmarks = results.multiHandLandmarks[0];
    const leftlandmarks = results.multiHandLandmarks[1];
    const rightHand = results.multiHandedness[0].label === 'Right';
    if(instructions.value === ""){
      instructions.value = "Initialize";
    }
    let data = {
      "instructions": instructions.value,
      "rightlandmarks": rightlandmarks,
      "leftlandmarks": leftlandmarks,
      "height": out3.height,
      "width": out3.width,
    }
    if(instructions.value === 'A'){
      if(typeof leftlandmarks === 'undefined'){
        var outputElement = document.getElementById('output');
        if (outputElement) {
          outputElement.textContent = "Both hands are not visible";
        }
        
      }else{
          socket.send(JSON.stringify(data));
      }
    }
    else{
      socket.send(JSON.stringify(data));
    }
    
  }

  document.body.classList.add('loaded');
  fpsControl.tick();

  canvasCtx3.save();
  canvasCtx3.clearRect(0, 0, out3.width, out3.height);
  canvasCtx3.drawImage(
      results.image, 0, 0, out3.width, out3.height);
  if (results.multiHandLandmarks && results.multiHandedness) {
    for (let index = 0; index < results.multiHandLandmarks.length; index++) {
      const classification = results.multiHandedness[index];
      const isRightHand = classification.label === 'Right';
      const landmarks = results.multiHandLandmarks[index];
      drawConnectors(
          canvasCtx3, landmarks, HAND_CONNECTIONS,
          {color: isRightHand ? '#00FF00' : '#FF0000'}),
      drawLandmarks(canvasCtx3, landmarks, {
        color: isRightHand ? '#00FF00' : '#FF0000',
        fillColor: isRightHand ? '#FF0000' : '#00FF00',
        radius: (x) => {
          return lerp(x.from.z, -0.15, .1, 10, 1);
        }
      });
    }
  }
  canvasCtx3.restore();
}

const hands = new Hands({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.1/${file}`;
}});
hands.onResults(onResultsHands);

const camera = new Camera(video3, {
  onFrame: async () => {
    await hands.send({image: video3});
  },
  width: 480,
  height: 480
});
camera.start();

new ControlPanel(controlsElement3, {
      selfieMode: true,
      maxNumHands: 2,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })
    .add([
      new StaticText({title: 'MediaPipe Hands'}),
      fpsControl,
      new Toggle({title: 'Selfie Mode', field: 'selfieMode'}),
      new Slider(
          {title: 'Max Number of Hands', field: 'maxNumHands', range: [1, 4], step: 1}),
      new Slider({
        title: 'Min Detection Confidence',
        field: 'minDetectionConfidence',
        range: [0, 1],
        step: 0.01
      }),
      new Slider({
        title: 'Min Tracking Confidence',
        field: 'minTrackingConfidence',
        range: [0, 1],
        step: 0.01
      }),
    ])
    .on(options => {
      video3.classList.toggle('selfie', options.selfieMode);
      hands.setOptions(options);
    });


//Handle the prediction result came from server
const socket = new WebSocket('ws://localhost:8000');
    socket.addEventListener('open', function (event) {
        socket.send('Connection Established');
    });

    socket.addEventListener('message', function (event) {
        var outputElement = document.getElementById('output');
        if (outputElement) {
          var data = JSON.parse(event.data);
          var gesture = data.gesture;
          var accuracy = data.accuracy;
          outputElement.textContent = `Gesture: ${gesture}, Accuracy: ${accuracy}`;
          //Todo
          // Show the color according to the arrray data.correct
          
        }
    });
    const contactServer = () => {
        socket.send("Initialize");
    }


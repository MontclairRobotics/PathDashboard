<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PATH GUI</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    header {
      background-color: #333;
      color: white;
      padding: 1em;
      text-align: center;
    }
    #app {
      display: flex;
      height: 100vh;
      overflow: hidden;
    }
    #canvas-container {
      flex: 3;
      position: relative;
      background: #f0f0f0;
    }
    canvas {
      display: block;
      border: 1px solid #ccc;
      margin: auto;
    }
    #controls {
      flex: 1;
      padding: 1em;
      background: #eaeaea;
      overflow-y: auto;
    }
    button {
      margin: 0.5em 0;
      padding: 0.5em 1em;
      cursor: pointer;
      background: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
    }
    button:hover {
      background: #0056b3;
    }
    #output {
      margin-top: 1em;
      font-family: monospace;
      white-space: pre-wrap;
      background: #fff;
      padding: 0.5em;
      border: 1px solid #ccc;
      border-radius: 4px;
      max-height: 100px;
      overflow-y: auto;
    }
    #waypoint-code {
      margin-top: 1em;
      font-family: monospace;
      white-space: pre-wrap;
      background: #fff;
      padding: 0.5em;
      border: 1px solid #ccc;
      border-radius: 4px;
      max-height: 200px;
      overflow-y: auto;
    }
  </style>
</head>
<body>
  <header>
    <h1>Montclair FRC Path GUI</h1>
  </header>
  <div id="app">
    <div id="canvas-container">
      <canvas id="plannerCanvas" width="1200" height="600"></canvas>
    </div>
    <div id="controls">
      <h2>Controls</h2>
      <button id="toggle-tweak">Enable Tweaking Mode</button>
      <button id="clear">Clear Selection</button>
      <button onclick=sendAutoString()>PUSH</button>
      <h3>Waypoint Sequence</h3>
      <div id="output"></div>
      <h3>Generated Code for Waypoints</h3>
      <button id="generate-code">Generate Waypoint Code</button>
      <div id="waypoint-code"></div>
    </div>
  </div>
  <script>
    function sendAutoString() {
        let autoString = selectedWaypoints.join(''); 
  
        fetch("http://localhost:8000", {  
            method: "POST",
            headers: { "Content-Type": "text/plain" },
            body: autoString
        })
        .then(response => response.text())
        .then(data => console.log("Response:", data))
        .catch(error => console.error("Error:", error));
    }
  </script>
  
  <script>
    const canvas = document.getElementById('plannerCanvas');
    const ctx = canvas.getContext('2d');
    const output = document.getElementById('output');
    const waypointCode = document.getElementById('waypoint-code');
    
    const predefinedWaypoints = [
      { id: "1", x: 121, y: 130.125 },
      { id: "2", x: 150, y: 113.125 },
      { id: "3", x: 181, y: 92.125 },
      { id: "4", x: 118, y: 468.125 },
      { id: "5", x: 145, y: 488.125 },
      { id: "6", x: 175, y: 507.125 },
      { id: "S1", x: 518, y: 107.125 },
      { id: "S2", x: 516, y: 245.125 },
      { id: "S3", x: 516, y: 298.125 },
      { id: "S4", x: 518, y: 352.125 },
      { id: "S5", x: 518, y: 497.125 },
      { id: "a", x: 301, y: 311.125 },
      { id: "A", x: 300, y: 287.125 },
      { id: "b", x: 320, y: 256.125 },
      { id: "B", x: 340, y: 247.125 },
      { id: "c", x: 375, y: 246.125 },
      { id: "C", x: 398, y: 258.125 },
      { id: "d", x: 418, y: 285.125 },
      { id: "D", x: 416, y: 313.125 },
      { id: "e", x: 402, y: 341.125 },
      { id: "E", x: 378, y: 354.125 },
      { id: "f", x: 342, y: 356.125 },
      { id: "F", x: 320, y: 344.125 },
    ];

    let selectedWaypoints = [];
    let renderWaypoints = [];
    let tweakingMode = false;
    let draggingWaypoint = null;
    const fieldImage = new Image();

    fieldImage.src = 'https://lh3.googleusercontent.com/pw/AP1GczNS3jp1GGMGcutugRuk_jJedvIXzUh-UtLmJmfoOnhEgrTC6iVNxFFsqYrgR6Oj-hFmqTxG4fMMHV5PVP9dfTklGLayMINvMEM4bFH7WHLBEHw_ZwPw=w600-h315-p-k';
    fieldImage.onload = () => redrawCanvas();

    function drawCircle(x, y, color = 'blue', label = '') {
      ctx.beginPath();
      ctx.arc(x, y, 10, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.closePath();
      if (label) {
        ctx.font = '12px Arial';
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, x, y);
      }
    }

    function drawLine(x1, y1, x2, y2) {
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = 'green';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.closePath();
    }

    function redrawCanvas() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(fieldImage, 0, 0, canvas.width, canvas.height);

      for (let i = 0; i < renderWaypoints.length - 1; i++) {
        const wp1 = predefinedWaypoints.find(wp => wp.id === renderWaypoints[i]);
        const wp2 = predefinedWaypoints.find(wp => wp.id === renderWaypoints[i + 1]);
        if (wp1 && wp2) drawLine(wp1.x, wp1.y, wp2.x, wp2.y);
      }

      predefinedWaypoints.forEach(wp => {
        const color = renderWaypoints.includes(wp.id) ? 'green' : 'blue';
        drawCircle(wp.x, wp.y, color, wp.id);
      });
    }

    function getClickedWaypoint(x, y) {
      return predefinedWaypoints.find(wp => Math.hypot(wp.x - x, wp.y - y) <= 10);
    }

    function updateOutput() {
      output.textContent = selectedWaypoints.join('');
    }

    function generateWaypointCode() {
      const code = `const predefinedWaypoints = ${JSON.stringify(predefinedWaypoints, null, 2)};`;
      waypointCode.textContent = code;
    }

    canvas.addEventListener('mousedown', e => {
      if (!tweakingMode) return;
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      draggingWaypoint = getClickedWaypoint(x, y);
    });

    canvas.addEventListener('mousemove', e => {
      if (draggingWaypoint) {
        const rect = canvas.getBoundingClientRect();
        draggingWaypoint.x = e.clientX - rect.left;
        draggingWaypoint.y = e.clientY - rect.top;
        redrawCanvas();
      }
    });

    canvas.addEventListener('mouseup', () => (draggingWaypoint = null));

    canvas.addEventListener('click', e => {
      if (tweakingMode) return;
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const clickedWaypoint = getClickedWaypoint(x, y);
      if (clickedWaypoint) {
        if (['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F'].includes(clickedWaypoint.id)) {
          let level = prompt(`Enter a level for ${clickedWaypoint.id} (1-4):`);
          level = parseInt(level, 10);
          if (level >= 1 && level <= 4) {
            selectedWaypoints.push(`${clickedWaypoint.id}${level}`);
            renderWaypoints.push(clickedWaypoint.id);
          } else {
            alert('Invalid level! Please enter a number between 1 and 4.');
            return;
          }
        } else {
          selectedWaypoints.push(clickedWaypoint.id);
          renderWaypoints.push(clickedWaypoint.id);
        }
        redrawCanvas();
        updateOutput();
      }
    });

    document.getElementById('clear').addEventListener('click', () => {
      selectedWaypoints = [];
      renderWaypoints = [];
      redrawCanvas();
      updateOutput();
    });

    document.getElementById('copy').addEventListener('click', () => {
      navigator.clipboard
        .writeText(selectedWaypoints.join(''))
        .catch(() => alert('Failed to copy!'));
    });

    document.getElementById('toggle-tweak').addEventListener('click', () => {
      tweakingMode = !tweakingMode;
      alert(tweakingMode ? 'Tweaking mode enabled.' : 'Tweaking mode disabled.');
    });

    document.getElementById('generate-code').addEventListener('click', generateWaypointCode);
  </script>
</body>
</html>

import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
//import { computeBoundsTree, disposeBoundsTree, acceleratedRaycast } from 'three-mesh-bvh';

// Constants definitions
const NO_DIMS = 3;
const HALF_GRID_SIZE = 1; // because we are normalizing in the range ± 1;
const SPACING = 10;
// Color Scheme
const COLORS = {
    BKG: '#000240',
    LABEL: '#FFE000',
    SPIKES: '#FFFFFF'
}

// Patch THREE's raycast method
//THREE.Mesh.prototype.raycast = acceleratedRaycast;

// Create a scene a camera and a renderer
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
var renderer = new THREE.WebGLRenderer();
renderer.setClearColor(COLORS.BKG)
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);


// Function to create a reference open cube made of 3 grids
function createPseudoCube() {
    var grids = [];
    for (var i = 0; i < NO_DIMS; i++) {
        grids[i] = new THREE.GridHelper((HALF_GRID_SIZE*2), SPACING);
        scene.add(grids[i]);
    }
    grids[0].rotation.x = -Math.PI * 0.5; // Back 
    grids[0].position.z = -HALF_GRID_SIZE;

    grids[1].rotation.z = -Math.PI * 0.5; // Left
    grids[1].position.x = -HALF_GRID_SIZE;

    grids[2].position.y = -HALF_GRID_SIZE; // Bottom
}

// Function to assign labels to the 3 axes
function createAxisLabel(text, position, color) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    context.font = '12px Futura';
    context.fillStyle = color;
    context.fillText(text, canvas.width * 0.5, canvas.height * 0.5);

    var texture = new THREE.CanvasTexture(canvas);

    var spriteMaterial = new THREE.SpriteMaterial({map: texture});
    var sprite = new THREE.Sprite(spriteMaterial);
    sprite.position.copy(position);
    scene.add(sprite);
}

// Function to create interactions on mouse over: scale change + tooltip show/hide
function setupMouseInteraction() {
    // Visual feedback on mouse hover on the points
    var mouse = new THREE.Vector2();
    var raycaster = new THREE.Raycaster();
    var INTERSECTED;
    var light = new THREE.DirectionalLight(0xffffff, 1, 100);
    light.position.set(0, 1, 0);
    scene.add(light)
    
    // Create lines for the spikes
    var lineMaterial = new THREE.LineBasicMaterial({color: COLORS.SPIKES});
    var lines = [];
    for (var i = 0; i < NO_DIMS; i++) {
        var geometry = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
        var line = new THREE.Line(geometry, lineMaterial);
        line.visible = false;
        scene.add(line);
        lines.push(line);
    }
    // Set tooltips
    var tooltip = document.createElement('div');
    tooltip.style.position = 'absolute';
    tooltip.style.visibility = 'hidden';
    tooltip.style.background = '#fff';
    tooltip.style.border = '1px solid #000';
    tooltip.style.font = '14px Futura';
    tooltip.style.padding = '10px';
    document.body.appendChild(tooltip);

    window.addEventListener('mousemove', function(event) {
        // mouse's normalized coordinates
        mouse.x = (event.clientX / this.window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / this.window.innerHeight) * 2 + 1;
        // update raycaster with mouse position
        raycaster.setFromCamera(mouse, camera);
        // update light to follow mouse
        light.position.set(mouse.x, mouse.y, 0);
        // if an object was previously intersected set it back to default scale
        if (INTERSECTED) {
            INTERSECTED.scale.set(1, 1, 1);
            INTERSECTED = null;
            tooltip.style.visibility = 'hidden';
            lines.forEach(line => line.visible = false);
        }
        // get intersecting objects
        var spheres = scene.children.filter(object => object.geometry && object.geometry.type === 'SphereGeometry');
        //spheres.forEach(object => object.geometry.computeBoundsTree())
        var intersects = raycaster.intersectObjects(spheres);
        if (intersects.length > 0) {
            var object = intersects[0].object;
            // if intersected object is a sphere magnify it
            object.scale.set(1.5, 1.5, 1.5);
            INTERSECTED = object; // memorize last intersected objects
            // Show tooltip
            var id = object.userData.id[0];
            var coordinates = object.userData.id.slice(1).join('\n'); // TODO: use normalizedData
            tooltip.textContent = 'ID: ' + id + '\n' + coordinates;
            tooltip.style.left = (event.clientX + 10) + 'px';
            tooltip.style.top = (event.clientY + 10) + 'px';
            tooltip.style.visibility = 'visible';
            // Show spikes
            lines.forEach((line, i) => {
                var positions = line.geometry.attributes.position.array;
                positions[0] = object.position.x;
                positions[1] = object.position.y;
                positions[2] = object.position.z;
                // Define lines' endpoints
                if (i == 0) { // x axes
                    positions[3] = -1;
                    positions[4] = object.position.y;
                    positions[5] = object.position.z;
                } else if (i ==1) { // y axes
                    positions[3] = object.position.x;
                    positions[4] = -1;
                    positions[5] = object.position.z;
                } else if (i==2) { // z axes
                    positions[3] = object.position.x;
                    positions[4] = object.position.y;
                    positions[5] = -1;
                }
                line.geometry.attributes.position.needsUpdate = true;
                line.visible = true; 
            });  
        }
    }, false);
}


fetch('/data')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // Min Max data calculation for grid normalization and color coding
        var minX = Math.min(...data.map(d => d[0]));
        var maxX = Math.max(...data.map(d => d[0]));
        var minY = Math.min(...data.map(d => d[1]));
        var maxY = Math.max(...data.map(d => d[1]));
        var minZ = Math.min(...data.map(d => d[2]));
        var maxZ = Math.max(...data.map(d => d[2]));

        // Normalize in ±1 range
        var normalizedData = data.map(d => [
            2 * (d[0] - minX) / (maxX - minX) - 1,
            2 * (d[1] - minY) / (maxY - minY) - 1,
            2 * (d[2] - minZ) / (maxZ - minZ) - 1
        ]);
        console.log(normalizedData)

        for (var i = 0; i < normalizedData.length; i++) {
            var geometry = new THREE.SphereBufferGeometry(0.03, 32 ,32);
            var id = data.shift(); // Remove the id as the first element of the array
            // Points position
            var x = normalizedData[i][0];
            var y = normalizedData[i][1];
            var z = normalizedData[i][2];

            // Points color coding
            var r = (normalizedData[i][0] + 1) / 2;
            var g = (normalizedData[i][1] + 1) / 2;
            var b = (normalizedData[i][2] + 1) / 2;

            var material = new THREE.MeshLambertMaterial({color: new THREE.Color(r, g, b), emissive: new THREE.Color(r, g, b)});
            var sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(x, y, z);
            sphere.userData.id = id;
            scene.add(sphere);
        }
        createPseudoCube();
        for (var i = -1; i <= 1; i += 0.1) {
            var position = new THREE.Vector3(i, 0, -HALF_GRID_SIZE); // x axes
            position.y = HALF_GRID_SIZE;
            createAxisLabel(i.toFixed(1), position, COLORS.LABEL);
            position = new THREE.Vector3(-HALF_GRID_SIZE, i, 0); // y axes
            position.z = HALF_GRID_SIZE;
            createAxisLabel(i.toFixed(1), position, COLORS.LABEL);
            position = new THREE.Vector3(0, -HALF_GRID_SIZE, i); // z axes
            position.x = HALF_GRID_SIZE;
            createAxisLabel(i.toFixed(1), position, COLORS.LABEL);
        }
    });


// Create a cursor
var cursorGeometry = new THREE.ConeGeometry(0.03, 0.1, 32);
var cursorMaterial = new THREE.MeshBasicMaterial({color: COLORS.LABEL});
var cursor = new THREE.Mesh(cursorGeometry, cursorMaterial);
cursor.rotation.x = -Math.PI * 0.5;
scene.add(cursor);

// Add mouse or trackpad grab
var controls = new OrbitControls(camera, renderer.domElement);

// Position the camera
camera.position.z = 3;
camera.lookAt(scene.position);

// Call setupMouseIjnteraction to enable mouse events
setupMouseInteraction()

// Rendering function
var animate = function () {
    requestAnimationFrame(animate);
    //console.log(camera.position);  // Print camera position
    //console.log(scene.children.length);
    renderer.render(scene, camera);
    controls.update();
};
animate();
    
// Connect to SocketIO and listen to 'cursor_update' event
var socket = io.connect('http://localhost:5000');
socket.on('update_cursor', function(msg) {
    // Update cursor's position
    cursor.position.set(msg.x, msg.y, msg.z);
});
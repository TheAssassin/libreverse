// thanks to https://tonybox.net/posts/simple-stl-viewer/ for the inspiration

/**
 * Set up a three.js based STL model preview.
 * @param url URL to the STL file
 * @param element JavaScript element (e.g., queried through document.getElementById)
 * @param parentElement element whose size to use for initial display (if null, element will be used)
 */
function setup_stl_viewer(url, element, parentElement) {
    var height = element.clientHeight;
    var width = element.clientWidth;

    if (parentElement != null) {
        height = parentElement.clientHeight;
        width = parentElement.clientWidth;
    }

    // we can use the client's calculated width/height
    // 1 and 1000 define some sort of "clipping" in some obscure unit
    var camera = new THREE.PerspectiveCamera(70, width / height, 2, 1000);

    // the WebGL renderer works pretty well
    // alpha here means we use the page background
    var renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
    renderer.setSize(width, height);
    // add the actual canvas to the element we passed
    element.appendChild(renderer.domElement);

    // whenever the page is resized, the canvas size should be adjusted
    window.addEventListener("resize", function() {
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    }, false);

    // these control settings work fine in my opinion, not to slow and not too fast
    var controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.rotateSpeed = 0.35;
    controls.dampingFactor = 0.2;
    controls.enableZoom = true;

    // we need to define the scene by adding lights where appropriate
    var scene = new THREE.Scene();

    // we want one global hemisphere light that illuminates the entire model from above
    var hemisphereLight = new THREE.HemisphereLight(0xffffff, 1);
    scene.add(hemisphereLight);

    // we also want to keep a point light from the camera angle
    // note: if we include blue in the light color, it'll create a blue reflection on the surface
    // this is apparently due to the orange color of the model, which only includes red and green
    var pointLight = new THREE.PointLight(0x505000);
    camera.add(pointLight);


    // make sure to add camera to scene, otherwise the point light won't work
    scene.add(camera);

    // finally, we can load the STL model
    var loader = new THREE.STLLoader();
    loader.load(url, function (geometry) {
        // color might have to be adjusted
        var material = new THREE.MeshPhongMaterial({
            color: 0xff8000,
            specular: 100,
            shininess: 100
        });

        // add mesh to scene
        var mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // this nifty little snippet allows us to automatically center the model in the view, no matter how it's generated
        // this is great, because slicers also just orient the mesh on the build plate, no matter how it's rotated
        var middle = new THREE.Vector3();
        geometry.computeBoundingBox();
        geometry.boundingBox.getCenter(middle);
        mesh.geometry.applyMatrix4(new THREE.Matrix4().makeTranslation(-middle.x, -middle.y, -middle.z));

        // rotate mesh so the model doesn't lie on the side
        mesh.rotation.x = Math.PI / -2;

        // trying to orient the model similar to the screenshots OpenSCAD renders
        // we (still) use a perspective camera, so there will always be a small difference, though
        var largestDimension = Math.max(
            geometry.boundingBox.max.x,
            geometry.boundingBox.max.y,
            geometry.boundingBox.max.z
        );
        camera.position.x = 0.8 * largestDimension * 1.33;
        camera.position.y = 0.8 * largestDimension * 1.67;
        camera.position.z = 0.8 * largestDimension * 2;
        // this callback is responsible for updating the controls; it will be called automatically by three.jjs
        var animate = function () {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };
        animate();
    });
}

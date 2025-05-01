<script lang="ts">
    import * as THREE from "three";
    import { onMount } from "svelte";
    import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
    import { ThreeMFLoader } from "three/examples/jsm/Addons.js";
  
    let container: HTMLDivElement;
    let scene = new THREE.Scene();
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let controls: OrbitControls;
  
    onMount(() => {
      init();
      window.addEventListener("resize", onResize);
      return () => window.removeEventListener("resize", onResize);
    });
  
    function init() {
      const width = container.clientWidth;
      const height = container.clientHeight;
  
      // camera
      camera = new THREE.PerspectiveCamera(45, width / height, 0.2, 2000);
      camera.position.set(0, 0, 25);
      camera.lookAt(0, 0, 0);
  
      // renderer
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(width, height);
      renderer.setPixelRatio(window.devicePixelRatio);
      container.appendChild(renderer.domElement);
  
      // orbit controls
      controls = new OrbitControls(camera, renderer.domElement);
      controls.target.set(0, 0, 0);
      controls.enableDamping = true;
      controls.dampingFactor = 0.1;
      controls.minDistance = 10;
      controls.maxDistance = 100;
  
      // cube
      const geometry = new THREE.BoxGeometry(10, 10, 10);
    //   const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const material = new THREE.MeshStandardMaterial({ 
        // map:new THREE.TextureLoader().load("./image/minecraftbox.jpg"),
        color: 0x000000 });
      const cube = new THREE.Mesh(geometry, material);

      const light = new THREE.DirectionalLight(0xffffff, 10);
      light.position.set(100, 150, -100);
      scene.add(light);
      scene.add(cube);
  
      const animate = () => {
        controls.update();
        cube.rotation.x += 0.005;
        cube.rotation.y += 0.01;
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
      };
      animate();
    }
  
    function onResize() {
      const width = container.clientWidth;
      const height = container.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    }
  </script>
  
  <div
    bind:this={container}
    id="black-box"
  ></div>
  
  <style>
    #black-box {
      width: 300px;   
      height: 300px;   
      margin: 0 auto; 
      /* border: 1px solid red; */
      overflow: hidden;
    }
  
  </style>
  